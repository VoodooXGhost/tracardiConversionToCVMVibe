from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from typing import Optional, Dict, Any
import uuid
import math
from datetime import datetime

from ..models import Offer
from ..schemas import OfferCreate, OfferUpdate, OfferResponse, OfferListResponse

class OfferService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_offers(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        offer_type: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> OfferListResponse:
        """Get paginated list of offers"""
        
        query = select(Offer)
        
        # Apply filters
        conditions = []
        
        if search:
            search_term = f"%{search}%"
            conditions.append(
                or_(
                    Offer.name.ilike(search_term),
                    Offer.description.ilike(search_term)
                )
            )
        
        if offer_type:
            conditions.append(Offer.offer_type == offer_type)
        
        if is_active is not None:
            conditions.append(Offer.is_active == is_active)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Get total count
        count_query = select(func.count()).select_from(Offer)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(desc(Offer.created_at))
        
        # Execute query
        result = await self.db.execute(query)
        offers = result.scalars().all()
        
        # Convert to response format
        offer_responses = [OfferResponse.model_validate(offer) for offer in offers]
        
        total_pages = math.ceil(total / page_size)
        
        return OfferListResponse(
            offers=offer_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    async def get_offer_by_id(self, offer_id: uuid.UUID) -> Optional[OfferResponse]:
        """Get offer by ID"""
        query = select(Offer).where(Offer.id == offer_id)
        result = await self.db.execute(query)
        offer = result.scalar_one_or_none()
        
        if not offer:
            return None
        
        return OfferResponse.model_validate(offer)

    async def create_offer(self, offer_data: OfferCreate) -> OfferResponse:
        """Create new offer"""
        offer = Offer(**offer_data.model_dump())
        
        self.db.add(offer)
        await self.db.commit()
        await self.db.refresh(offer)
        
        return OfferResponse.model_validate(offer)

    async def update_offer(
        self, 
        offer_id: uuid.UUID, 
        offer_update: OfferUpdate
    ) -> Optional[OfferResponse]:
        """Update offer"""
        query = select(Offer).where(Offer.id == offer_id)
        result = await self.db.execute(query)
        offer = result.scalar_one_or_none()
        
        if not offer:
            return None
        
        # Update fields
        update_data = offer_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(offer, field, value)
        
        offer.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(offer)
        
        return OfferResponse.model_validate(offer)

    async def delete_offer(self, offer_id: uuid.UUID) -> bool:
        """Delete offer"""
        query = select(Offer).where(Offer.id == offer_id)
        result = await self.db.execute(query)
        offer = result.scalar_one_or_none()
        
        if not offer:
            return False
        
        await self.db.delete(offer)
        await self.db.commit()
        
        return True

    async def get_offer_performance(self, offer_id: uuid.UUID, days: int = 30) -> Optional[Dict[str, Any]]:
        """Get offer performance analytics"""
        offer = await self.get_offer_by_id(offer_id)
        if not offer:
            return None
        
        # Mock performance data for demonstration
        import random
        
        return {
            "offer_id": str(offer_id),
            "offer_name": offer.name,
            "total_purchases": random.randint(50, 500),
            "total_revenue": random.uniform(10000, 100000),
            "conversion_rate": random.uniform(0.02, 0.08),
            "customer_satisfaction": random.uniform(3.5, 5.0),
            "repeat_purchase_rate": random.uniform(0.15, 0.35),
            "performance_trend": [
                {"date": f"2024-01-{i:02d}", "purchases": random.randint(5, 25)}
                for i in range(1, 31)
            ]
        }