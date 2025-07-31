from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, text
from sqlalchemy.orm import selectinload
from typing import Optional, List, Dict, Any
import uuid
import math
from datetime import datetime, timedelta

from ..models import Customer, Event, Offer
from ..schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse, CustomerSummary,
    CustomerListResponse, CustomerMetrics
)
from .ml_service import MLService

class CustomerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ml_service = MLService()

    async def get_customers(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        customer_type: Optional[str] = None,
        status: Optional[str] = None,
        risk_level: Optional[str] = None
    ) -> CustomerListResponse:
        """Get paginated list of customers with filtering"""
        
        # Build query
        query = select(Customer)
        
        # Apply filters
        conditions = []
        
        if search:
            search_term = f"%{search}%"
            conditions.append(
                or_(
                    Customer.phone_number.ilike(search_term),
                    Customer.first_name.ilike(search_term),
                    Customer.last_name.ilike(search_term),
                    Customer.email.ilike(search_term)
                )
            )
        
        if customer_type:
            conditions.append(Customer.customer_type == customer_type)
        
        if status:
            conditions.append(Customer.status == status)
        
        if risk_level:
            if risk_level == "high":
                conditions.append(Customer.churn_score > 0.8)
            elif risk_level == "medium":
                conditions.append(and_(Customer.churn_score > 0.5, Customer.churn_score <= 0.8))
            elif risk_level == "low":
                conditions.append(Customer.churn_score <= 0.5)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Get total count
        count_query = select(func.count()).select_from(Customer)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(desc(Customer.created_at))
        
        # Execute query
        result = await self.db.execute(query)
        customers = result.scalars().all()
        
        # Convert to summary format
        customer_summaries = []
        for customer in customers:
            summary = CustomerSummary(
                id=customer.id,
                phone_number=customer.phone_number,
                full_name=customer.full_name,
                customer_type=customer.customer_type,
                status=customer.status,
                arpu_30d=customer.arpu_30d,
                churn_score=customer.churn_score,
                days_since_last_activity=customer.days_since_last_activity,
                risk_level=customer.risk_level,
                created_at=customer.created_at,
                last_activity_at=customer.last_activity_at
            )
            customer_summaries.append(summary)
        
        total_pages = math.ceil(total / page_size)
        
        return CustomerListResponse(
            customers=customer_summaries,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    async def get_customer_by_id(self, customer_id: uuid.UUID) -> Optional[CustomerResponse]:
        """Get customer by ID"""
        query = select(Customer).where(Customer.id == customer_id)
        result = await self.db.execute(query)
        customer = result.scalar_one_or_none()
        
        if not customer:
            return None
        
        return CustomerResponse.model_validate(customer)

    async def create_customer(self, customer_data: CustomerCreate) -> CustomerResponse:
        """Create new customer"""
        customer = Customer(**customer_data.model_dump())
        
        # Set initial values
        customer.activation_date = datetime.utcnow()
        customer.last_activity_at = datetime.utcnow()
        
        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)
        
        return CustomerResponse.model_validate(customer)

    async def update_customer(
        self, 
        customer_id: uuid.UUID, 
        customer_update: CustomerUpdate
    ) -> Optional[CustomerResponse]:
        """Update customer"""
        query = select(Customer).where(Customer.id == customer_id)
        result = await self.db.execute(query)
        customer = result.scalar_one_or_none()
        
        if not customer:
            return None
        
        # Update fields
        update_data = customer_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        customer.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(customer)
        
        return CustomerResponse.model_validate(customer)

    async def delete_customer(self, customer_id: uuid.UUID) -> bool:
        """Delete customer"""
        query = select(Customer).where(Customer.id == customer_id)
        result = await self.db.execute(query)
        customer = result.scalar_one_or_none()
        
        if not customer:
            return False
        
        await self.db.delete(customer)
        await self.db.commit()
        
        return True

    async def get_customer_metrics(self) -> CustomerMetrics:
        """Get customer metrics for dashboard"""
        
        # Total customers
        total_query = select(func.count()).select_from(Customer)
        total_result = await self.db.execute(total_query)
        total_customers = total_result.scalar()
        
        # Active customers
        active_query = select(func.count()).select_from(Customer).where(Customer.status == 'active')
        active_result = await self.db.execute(active_query)
        active_customers = active_result.scalar()
        
        # Churned customers
        churned_query = select(func.count()).select_from(Customer).where(Customer.status == 'churned')
        churned_result = await self.db.execute(churned_query)
        churned_customers = churned_result.scalar()
        
        # High value customers (ARPU > 1000)
        high_value_query = select(func.count()).select_from(Customer).where(Customer.arpu_30d > 1000)
        high_value_result = await self.db.execute(high_value_query)
        high_value_customers = high_value_result.scalar()
        
        # At risk customers (churn score > 0.7)
        at_risk_query = select(func.count()).select_from(Customer).where(Customer.churn_score > 0.7)
        at_risk_result = await self.db.execute(at_risk_query)
        at_risk_customers = at_risk_result.scalar()
        
        # Average ARPU
        avg_arpu_query = select(func.avg(Customer.arpu_30d)).select_from(Customer).where(Customer.status == 'active')
        avg_arpu_result = await self.db.execute(avg_arpu_query)
        avg_arpu = avg_arpu_result.scalar() or 0
        
        # Average churn score
        avg_churn_query = select(func.avg(Customer.churn_score)).select_from(Customer).where(Customer.status == 'active')
        avg_churn_result = await self.db.execute(avg_churn_query)
        avg_churn_score = avg_churn_result.scalar() or 0
        
        # Customer type breakdown
        prepaid_query = select(func.count()).select_from(Customer).where(Customer.customer_type == 'prepaid')
        prepaid_result = await self.db.execute(prepaid_query)
        prepaid_customers = prepaid_result.scalar()
        
        postpaid_customers = total_customers - prepaid_customers
        
        return CustomerMetrics(
            total_customers=total_customers,
            active_customers=active_customers,
            churned_customers=churned_customers,
            high_value_customers=high_value_customers,
            at_risk_customers=at_risk_customers,
            avg_arpu=avg_arpu,
            avg_churn_score=avg_churn_score,
            prepaid_customers=prepaid_customers,
            postpaid_customers=postpaid_customers
        )

    async def get_customer_events(self, customer_id: uuid.UUID, limit: int = 50) -> List[Dict[str, Any]]:
        """Get customer events/activities"""
        query = (
            select(Event)
            .where(Event.customer_id == customer_id)
            .order_by(desc(Event.occurred_at))
            .limit(limit)
        )
        
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        return [
            {
                "id": str(event.id),
                "event_type": event.event_type,
                "event_name": event.event_name,
                "amount": float(event.amount) if event.amount else None,
                "duration": event.duration,
                "data_volume_mb": event.data_volume_mb,
                "channel": event.channel,
                "occurred_at": event.occurred_at.isoformat(),
                "properties": event.properties
            }
            for event in events
        ]

    async def predict_churn(self, customer_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Predict churn for specific customer"""
        customer = await self.get_customer_by_id(customer_id)
        if not customer:
            return None
        
        # Use ML service to predict churn
        churn_probability = await self.ml_service.predict_churn(customer)
        
        # Update customer record with new churn score
        update_query = (
            select(Customer)
            .where(Customer.id == customer_id)
        )
        result = await self.db.execute(update_query)
        db_customer = result.scalar_one_or_none()
        
        if db_customer:
            db_customer.churn_score = churn_probability
            await self.db.commit()
        
        return {
            "customer_id": str(customer_id),
            "churn_probability": churn_probability,
            "risk_level": "high" if churn_probability > 0.8 else "medium" if churn_probability > 0.5 else "low",
            "factors": await self.ml_service.get_churn_factors(customer),
            "recommendations": await self.ml_service.get_retention_recommendations(customer)
        }

    async def get_next_best_offer(self, customer_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Get next best offer for customer"""
        customer = await self.get_customer_by_id(customer_id)
        if not customer:
            return None
        
        # Use ML service to get next best offer
        offer_id = await self.ml_service.predict_next_best_offer(customer)
        
        if not offer_id:
            return None
        
        # Get offer details
        offer_query = select(Offer).where(Offer.id == offer_id)
        result = await self.db.execute(offer_query)
        offer = result.scalar_one_or_none()
        
        if not offer:
            return None
        
        return {
            "customer_id": str(customer_id),
            "offer": {
                "id": str(offer.id),
                "name": offer.name,
                "description": offer.description,
                "offer_type": offer.offer_type,
                "price": float(offer.price),
                "data_mb": offer.data_mb,
                "voice_minutes": offer.voice_minutes,
                "sms_count": offer.sms_count,
                "validity_days": offer.validity_days
            },
            "confidence_score": await self.ml_service.get_offer_confidence(customer, offer),
            "reasoning": await self.ml_service.get_offer_reasoning(customer, offer)
        }