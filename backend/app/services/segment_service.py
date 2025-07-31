from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, text
from typing import Optional, List, Dict, Any
import uuid
import math
from datetime import datetime

from ..models import Segment, Customer, CustomerSegment
from ..schemas import (
    SegmentCreate, SegmentUpdate, SegmentResponse, SegmentListResponse,
    SegmentCustomerCount, CustomerSummary, CustomerListResponse
)

class SegmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_segments(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> SegmentListResponse:
        """Get paginated list of segments"""
        
        query = select(Segment)
        
        # Apply filters
        conditions = []
        
        if search:
            search_term = f"%{search}%"
            conditions.append(
                or_(
                    Segment.name.ilike(search_term),
                    Segment.description.ilike(search_term)
                )
            )
        
        if is_active is not None:
            conditions.append(Segment.is_active == is_active)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Get total count
        count_query = select(func.count()).select_from(Segment)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(desc(Segment.created_at))
        
        # Execute query
        result = await self.db.execute(query)
        segments = result.scalars().all()
        
        # Convert to response format
        segment_responses = [SegmentResponse.model_validate(segment) for segment in segments]
        
        total_pages = math.ceil(total / page_size)
        
        return SegmentListResponse(
            segments=segment_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    async def get_segment_by_id(self, segment_id: uuid.UUID) -> Optional[SegmentResponse]:
        """Get segment by ID"""
        query = select(Segment).where(Segment.id == segment_id)
        result = await self.db.execute(query)
        segment = result.scalar_one_or_none()
        
        if not segment:
            return None
        
        return SegmentResponse.model_validate(segment)

    async def create_segment(self, segment_data: SegmentCreate) -> SegmentResponse:
        """Create new segment"""
        segment = Segment(**segment_data.model_dump())
        
        # Calculate initial customer count
        segment.customer_count = await self._calculate_segment_count(segment.conditions)
        
        self.db.add(segment)
        await self.db.commit()
        await self.db.refresh(segment)
        
        # Update customer-segment relationships
        await self._update_segment_memberships(segment)
        
        return SegmentResponse.model_validate(segment)

    async def update_segment(
        self, 
        segment_id: uuid.UUID, 
        segment_update: SegmentUpdate
    ) -> Optional[SegmentResponse]:
        """Update segment"""
        query = select(Segment).where(Segment.id == segment_id)
        result = await self.db.execute(query)
        segment = result.scalar_one_or_none()
        
        if not segment:
            return None
        
        # Update fields
        update_data = segment_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(segment, field, value)
        
        segment.updated_at = datetime.utcnow()
        
        # Recalculate customer count if conditions changed
        if 'conditions' in update_data:
            segment.customer_count = await self._calculate_segment_count(segment.conditions)
            await self._update_segment_memberships(segment)
        
        await self.db.commit()
        await self.db.refresh(segment)
        
        return SegmentResponse.model_validate(segment)

    async def delete_segment(self, segment_id: uuid.UUID) -> bool:
        """Delete segment"""
        query = select(Segment).where(Segment.id == segment_id)
        result = await self.db.execute(query)
        segment = result.scalar_one_or_none()
        
        if not segment:
            return False
        
        await self.db.delete(segment)
        await self.db.commit()
        
        return True

    async def refresh_segment_count(self, segment_id: uuid.UUID) -> Optional[int]:
        """Refresh segment customer count"""
        query = select(Segment).where(Segment.id == segment_id)
        result = await self.db.execute(query)
        segment = result.scalar_one_or_none()
        
        if not segment:
            return None
        
        # Recalculate count
        new_count = await self._calculate_segment_count(segment.conditions)
        segment.customer_count = new_count
        segment.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self._update_segment_memberships(segment)
        
        return new_count

    async def get_segment_customers(
        self, 
        segment_id: uuid.UUID, 
        page: int = 1, 
        page_size: int = 20
    ) -> Optional[CustomerListResponse]:
        """Get customers in segment"""
        # First check if segment exists
        segment_query = select(Segment).where(Segment.id == segment_id)
        segment_result = await self.db.execute(segment_query)
        segment = segment_result.scalar_one_or_none()
        
        if not segment:
            return None
        
        # Get customers matching segment conditions
        customers_query = await self._build_customer_query_from_conditions(segment.conditions)
        
        # Get total count
        count_query = select(func.count()).select_from(customers_query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        customers_query = customers_query.offset(offset).limit(page_size)
        
        # Execute query
        result = await self.db.execute(customers_query)
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

    async def preview_segment_count(self, conditions: Dict[str, Any]) -> int:
        """Preview segment customer count without saving"""
        return await self._calculate_segment_count(conditions)

    async def get_segment_analytics(self, segment_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Get segment analytics"""
        segment_query = select(Segment).where(Segment.id == segment_id)
        segment_result = await self.db.execute(segment_query)
        segment = segment_result.scalar_one_or_none()
        
        if not segment:
            return None
        
        # Get customers in segment for analytics
        customers_query = await self._build_customer_query_from_conditions(segment.conditions)
        result = await self.db.execute(customers_query)
        customers = result.scalars().all()
        
        if not customers:
            return {
                "segment_id": str(segment_id),
                "segment_name": segment.name,
                "customer_count": 0,
                "avg_arpu": 0,
                "avg_churn_score": 0,
                "customer_type_distribution": {},
                "risk_distribution": {},
                "province_distribution": {}
            }
        
        # Calculate analytics
        total_arpu = sum(float(c.arpu_30d) for c in customers)
        avg_arpu = total_arpu / len(customers) if customers else 0
        
        total_churn = sum(float(c.churn_score) for c in customers)
        avg_churn_score = total_churn / len(customers) if customers else 0
        
        # Distribution calculations
        customer_type_dist = {}
        risk_dist = {"low": 0, "medium": 0, "high": 0}
        province_dist = {}
        
        for customer in customers:
            # Customer type distribution
            ctype = customer.customer_type
            customer_type_dist[ctype] = customer_type_dist.get(ctype, 0) + 1
            
            # Risk distribution
            if customer.churn_score > 0.8:
                risk_dist["high"] += 1
            elif customer.churn_score > 0.5:
                risk_dist["medium"] += 1
            else:
                risk_dist["low"] += 1
            
            # Province distribution
            province = customer.province or "Unknown"
            province_dist[province] = province_dist.get(province, 0) + 1
        
        return {
            "segment_id": str(segment_id),
            "segment_name": segment.name,
            "customer_count": len(customers),
            "avg_arpu": round(avg_arpu, 2),
            "avg_churn_score": round(avg_churn_score, 3),
            "customer_type_distribution": customer_type_dist,
            "risk_distribution": risk_dist,
            "province_distribution": province_dist
        }

    async def _calculate_segment_count(self, conditions: Dict[str, Any]) -> int:
        """Calculate number of customers matching segment conditions"""
        try:
            query = await self._build_customer_query_from_conditions(conditions)
            count_query = select(func.count()).select_from(query.subquery())
            result = await self.db.execute(count_query)
            return result.scalar()
        except Exception:
            # If conditions are invalid, return 0
            return 0

    async def _build_customer_query_from_conditions(self, conditions: Dict[str, Any]):
        """Build SQLAlchemy query from segment conditions"""
        query = select(Customer)
        
        query_conditions = []
        
        for field, condition in conditions.items():
            if not isinstance(condition, dict) or 'operator' not in condition or 'value' not in condition:
                continue
            
            operator = condition['operator']
            value = condition['value']
            
            # Map field names to Customer attributes
            if hasattr(Customer, field):
                column = getattr(Customer, field)
                
                if operator == '=':
                    query_conditions.append(column == value)
                elif operator == '>':
                    query_conditions.append(column > value)
                elif operator == '<':
                    query_conditions.append(column < value)
                elif operator == '>=':
                    query_conditions.append(column >= value)
                elif operator == '<=':
                    query_conditions.append(column <= value)
                elif operator == '!=':
                    query_conditions.append(column != value)
                elif operator == 'in':
                    if isinstance(value, list):
                        query_conditions.append(column.in_(value))
                elif operator == 'not_in':
                    if isinstance(value, list):
                        query_conditions.append(~column.in_(value))
                elif operator == 'like':
                    query_conditions.append(column.ilike(f"%{value}%"))
        
        if query_conditions:
            query = query.where(and_(*query_conditions))
        
        return query

    async def _update_segment_memberships(self, segment: Segment):
        """Update customer-segment membership table"""
        # Delete existing memberships for this segment
        delete_query = text("DELETE FROM customer_segments WHERE segment_id = :segment_id")
        await self.db.execute(delete_query, {"segment_id": segment.id})
        
        # Get customers matching segment conditions
        customers_query = await self._build_customer_query_from_conditions(segment.conditions)
        result = await self.db.execute(customers_query)
        customers = result.scalars().all()
        
        # Insert new memberships
        for customer in customers:
            membership = CustomerSegment(
                customer_id=customer.id,
                segment_id=segment.id
            )
            self.db.add(membership)
        
        await self.db.commit()