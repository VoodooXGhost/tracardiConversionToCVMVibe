from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from ..core.database import get_db
from ..schemas import (
    OfferCreate, OfferUpdate, OfferResponse, OfferListResponse
)
from ..services.offer_service import OfferService

router = APIRouter()

@router.get("/", response_model=OfferListResponse)
async def get_offers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    offer_type: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of offers"""
    service = OfferService(db)
    return await service.get_offers(
        page=page,
        page_size=page_size,
        search=search,
        offer_type=offer_type,
        is_active=is_active
    )

@router.get("/{offer_id}", response_model=OfferResponse)
async def get_offer(offer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get offer by ID"""
    service = OfferService(db)
    offer = await service.get_offer_by_id(offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.post("/", response_model=OfferResponse)
async def create_offer(offer: OfferCreate, db: AsyncSession = Depends(get_db)):
    """Create new offer"""
    service = OfferService(db)
    return await service.create_offer(offer)

@router.put("/{offer_id}", response_model=OfferResponse)
async def update_offer(
    offer_id: uuid.UUID,
    offer_update: OfferUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update offer"""
    service = OfferService(db)
    offer = await service.update_offer(offer_id, offer_update)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.delete("/{offer_id}")
async def delete_offer(offer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete offer"""
    service = OfferService(db)
    success = await service.delete_offer(offer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Offer not found")
    return {"message": "Offer deleted successfully"}

@router.get("/types/available")
async def get_offer_types():
    """Get available offer types"""
    return {
        "offer_types": [
            {"value": "data_bundle", "label": "Data Bundle"},
            {"value": "voice_bundle", "label": "Voice Bundle"},
            {"value": "sms_bundle", "label": "SMS Bundle"},
            {"value": "discount", "label": "Discount Offer"},
            {"value": "upgrade", "label": "Service Upgrade"}
        ]
    }

@router.get("/{offer_id}/performance")
async def get_offer_performance(
    offer_id: uuid.UUID,
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get offer performance analytics"""
    service = OfferService(db)
    performance = await service.get_offer_performance(offer_id, days)
    if not performance:
        raise HTTPException(status_code=404, detail="Offer not found")
    return performance