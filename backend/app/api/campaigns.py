from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from ..core.database import get_db
from ..schemas import (
    CampaignCreate, CampaignUpdate, CampaignResponse, CampaignListResponse,
    CampaignMetrics, CampaignInteractionResponse
)
from ..services.campaign_service import CampaignService

router = APIRouter()

@router.get("/", response_model=CampaignListResponse)
async def get_campaigns(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    campaign_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of campaigns"""
    service = CampaignService(db)
    return await service.get_campaigns(
        page=page,
        page_size=page_size,
        search=search,
        status=status,
        campaign_type=campaign_type
    )

@router.get("/metrics", response_model=CampaignMetrics)
async def get_campaign_metrics(db: AsyncSession = Depends(get_db)):
    """Get campaign metrics for dashboard"""
    service = CampaignService(db)
    return await service.get_campaign_metrics()

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get campaign by ID"""
    service = CampaignService(db)
    campaign = await service.get_campaign_by_id(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.post("/", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignCreate, db: AsyncSession = Depends(get_db)):
    """Create new campaign"""
    service = CampaignService(db)
    return await service.create_campaign(campaign)

@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: uuid.UUID,
    campaign_update: CampaignUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update campaign"""
    service = CampaignService(db)
    campaign = await service.update_campaign(campaign_id, campaign_update)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete campaign"""
    service = CampaignService(db)
    success = await service.delete_campaign(campaign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"}

@router.post("/{campaign_id}/launch")
async def launch_campaign(
    campaign_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Launch campaign"""
    service = CampaignService(db)
    success = await service.launch_campaign(campaign_id, background_tasks)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found or cannot be launched")
    return {"message": "Campaign launched successfully", "campaign_id": campaign_id}

@router.post("/{campaign_id}/pause")
async def pause_campaign(campaign_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Pause campaign"""
    service = CampaignService(db)
    success = await service.pause_campaign(campaign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found or cannot be paused")
    return {"message": "Campaign paused successfully", "campaign_id": campaign_id}

@router.post("/{campaign_id}/resume")
async def resume_campaign(campaign_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Resume campaign"""
    service = CampaignService(db)
    success = await service.resume_campaign(campaign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found or cannot be resumed")
    return {"message": "Campaign resumed successfully", "campaign_id": campaign_id}

@router.get("/{campaign_id}/interactions")
async def get_campaign_interactions(
    campaign_id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    interaction_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get campaign interactions"""
    service = CampaignService(db)
    interactions = await service.get_campaign_interactions(
        campaign_id, page, page_size, interaction_type
    )
    return interactions

@router.get("/{campaign_id}/performance")
async def get_campaign_performance(campaign_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get detailed campaign performance analytics"""
    service = CampaignService(db)
    performance = await service.get_campaign_performance(campaign_id)
    if not performance:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return performance

@router.post("/{campaign_id}/test")
async def test_campaign(
    campaign_id: uuid.UUID,
    test_phone_numbers: list[str],
    db: AsyncSession = Depends(get_db)
):
    """Send test campaign to specific phone numbers"""
    service = CampaignService(db)
    result = await service.test_campaign(campaign_id, test_phone_numbers)
    if not result:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": f"Test sent to {len(test_phone_numbers)} numbers", "results": result}