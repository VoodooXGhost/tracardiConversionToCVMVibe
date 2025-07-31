from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from ..core.database import get_db
from ..schemas import (
    SegmentCreate, SegmentUpdate, SegmentResponse, SegmentListResponse,
    SegmentCustomerCount
)
from ..services.segment_service import SegmentService

router = APIRouter()

@router.get("/", response_model=SegmentListResponse)
async def get_segments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of segments"""
    service = SegmentService(db)
    return await service.get_segments(
        page=page,
        page_size=page_size,
        search=search,
        is_active=is_active
    )

@router.get("/{segment_id}", response_model=SegmentResponse)
async def get_segment(segment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get segment by ID"""
    service = SegmentService(db)
    segment = await service.get_segment_by_id(segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    return segment

@router.post("/", response_model=SegmentResponse)
async def create_segment(segment: SegmentCreate, db: AsyncSession = Depends(get_db)):
    """Create new segment"""
    service = SegmentService(db)
    return await service.create_segment(segment)

@router.put("/{segment_id}", response_model=SegmentResponse)
async def update_segment(
    segment_id: uuid.UUID,
    segment_update: SegmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update segment"""
    service = SegmentService(db)
    segment = await service.update_segment(segment_id, segment_update)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    return segment

@router.delete("/{segment_id}")
async def delete_segment(segment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete segment"""
    service = SegmentService(db)
    success = await service.delete_segment(segment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Segment not found")
    return {"message": "Segment deleted successfully"}

@router.post("/{segment_id}/refresh")
async def refresh_segment(segment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Refresh segment customer count"""
    service = SegmentService(db)
    count = await service.refresh_segment_count(segment_id)
    if count is None:
        raise HTTPException(status_code=404, detail="Segment not found")
    return {"segment_id": segment_id, "customer_count": count}

@router.get("/{segment_id}/customers")
async def get_segment_customers(
    segment_id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get customers in segment"""
    service = SegmentService(db)
    customers = await service.get_segment_customers(segment_id, page, page_size)
    if customers is None:
        raise HTTPException(status_code=404, detail="Segment not found")
    return customers

@router.post("/preview")
async def preview_segment(conditions: dict, db: AsyncSession = Depends(get_db)):
    """Preview segment customer count without saving"""
    service = SegmentService(db)
    count = await service.preview_segment_count(conditions)
    return {"customer_count": count, "conditions": conditions}

@router.get("/{segment_id}/analytics")
async def get_segment_analytics(segment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get segment analytics"""
    service = SegmentService(db)
    analytics = await service.get_segment_analytics(segment_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Segment not found")
    return analytics