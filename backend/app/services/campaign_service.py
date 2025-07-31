from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from typing import Optional, List, Dict, Any
import uuid
import math
from datetime import datetime
from fastapi import BackgroundTasks

from ..models import Campaign, CampaignInteraction, Segment, Customer
from ..schemas import (
    CampaignCreate, CampaignUpdate, CampaignResponse, CampaignListResponse,
    CampaignMetrics, CampaignInteractionResponse
)

class CampaignService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_campaigns(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        campaign_type: Optional[str] = None
    ) -> CampaignListResponse:
        """Get paginated list of campaigns"""
        
        query = select(Campaign)
        
        # Apply filters
        conditions = []
        
        if search:
            search_term = f"%{search}%"
            conditions.append(
                or_(
                    Campaign.name.ilike(search_term),
                    Campaign.description.ilike(search_term)
                )
            )
        
        if status:
            conditions.append(Campaign.status == status)
        
        if campaign_type:
            conditions.append(Campaign.campaign_type == campaign_type)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Get total count
        count_query = select(func.count()).select_from(Campaign)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(desc(Campaign.created_at))
        
        # Execute query
        result = await self.db.execute(query)
        campaigns = result.scalars().all()
        
        # Convert to response format
        campaign_responses = [CampaignResponse.model_validate(campaign) for campaign in campaigns]
        
        total_pages = math.ceil(total / page_size)
        
        return CampaignListResponse(
            campaigns=campaign_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    async def get_campaign_by_id(self, campaign_id: uuid.UUID) -> Optional[CampaignResponse]:
        """Get campaign by ID"""
        query = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.db.execute(query)
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            return None
        
        return CampaignResponse.model_validate(campaign)

    async def create_campaign(self, campaign_data: CampaignCreate) -> CampaignResponse:
        """Create new campaign"""
        campaign = Campaign(**campaign_data.model_dump())
        
        # Set initial target count based on segment
        if campaign.target_segment_id:
            segment_query = select(Segment).where(Segment.id == campaign.target_segment_id)
            segment_result = await self.db.execute(segment_query)
            segment = segment_result.scalar_one_or_none()
            if segment:
                campaign.target_count = segment.customer_count
        
        self.db.add(campaign)
        await self.db.commit()
        await self.db.refresh(campaign)
        
        return CampaignResponse.model_validate(campaign)

    async def update_campaign(
        self, 
        campaign_id: uuid.UUID, 
        campaign_update: CampaignUpdate
    ) -> Optional[CampaignResponse]:
        """Update campaign"""
        query = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.db.execute(query)
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            return None
        
        # Update fields
        update_data = campaign_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(campaign, field, value)
        
        campaign.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(campaign)
        
        return CampaignResponse.model_validate(campaign)

    async def delete_campaign(self, campaign_id: uuid.UUID) -> bool:
        """Delete campaign"""
        query = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.db.execute(query)
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            return False
        
        # Only allow deletion of draft campaigns
        if campaign.status != 'draft':
            return False
        
        await self.db.delete(campaign)
        await self.db.commit()
        
        return True

    async def launch_campaign(self, campaign_id: uuid.UUID, background_tasks: BackgroundTasks) -> bool:
        """Launch campaign"""
        query = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.db.execute(query)
        campaign = result.scalar_one_or_none()
        
        if not campaign or campaign.status not in ['draft', 'scheduled']:
            return False
        
        # Update campaign status
        campaign.status = 'running'
        campaign.started_at = datetime.utcnow()
        
        await self.db.commit()
        
        # Add background task to process campaign
        background_tasks.add_task(self._process_campaign, campaign_id)
        
        return True

    async def pause_campaign(self, campaign_id: uuid.UUID) -> bool:
        """Pause campaign"""
        query = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.db.execute(query)
        campaign = result.scalar_one_or_none()
        
        if not campaign or campaign.status != 'running':
            return False
        
        campaign.status = 'paused'
        await self.db.commit()
        
        return True

    async def resume_campaign(self, campaign_id: uuid.UUID) -> bool:
        """Resume campaign"""
        query = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.db.execute(query)
        campaign = result.scalar_one_or_none()
        
        if not campaign or campaign.status != 'paused':
            return False
        
        campaign.status = 'running'
        await self.db.commit()
        
        return True

    async def get_campaign_metrics(self) -> CampaignMetrics:
        """Get campaign metrics for dashboard"""
        
        # Total campaigns
        total_query = select(func.count()).select_from(Campaign)
        total_result = await self.db.execute(total_query)
        total_campaigns = total_result.scalar()
        
        # Active campaigns
        active_query = select(func.count()).select_from(Campaign).where(Campaign.status == 'running')
        active_result = await self.db.execute(active_query)
        active_campaigns = active_result.scalar()
        
        # Completed campaigns
        completed_query = select(func.count()).select_from(Campaign).where(Campaign.status == 'completed')
        completed_result = await self.db.execute(completed_query)
        completed_campaigns = completed_result.scalar()
        
        # Aggregate metrics
        metrics_query = select(
            func.sum(Campaign.sent_count),
            func.sum(Campaign.delivered_count),
            func.sum(Campaign.opened_count),
            func.sum(Campaign.clicked_count),
            func.sum(Campaign.converted_count),
            func.sum(Campaign.total_cost),
            func.sum(Campaign.revenue_generated)
        ).select_from(Campaign)
        
        metrics_result = await self.db.execute(metrics_query)
        metrics = metrics_result.first()
        
        total_sent = metrics[0] or 0
        total_delivered = metrics[1] or 0
        total_opened = metrics[2] or 0
        total_clicked = metrics[3] or 0
        total_converted = metrics[4] or 0
        total_cost = metrics[5] or 0
        total_revenue = metrics[6] or 0
        
        # Calculate averages
        avg_delivery_rate = (total_delivered / total_sent) if total_sent > 0 else 0
        avg_open_rate = (total_opened / total_delivered) if total_delivered > 0 else 0
        avg_click_rate = (total_clicked / total_opened) if total_opened > 0 else 0
        avg_conversion_rate = (total_converted / total_clicked) if total_clicked > 0 else 0
        avg_roi = ((total_revenue - total_cost) / total_cost) if total_cost > 0 else 0
        
        return CampaignMetrics(
            total_campaigns=total_campaigns,
            active_campaigns=active_campaigns,
            completed_campaigns=completed_campaigns,
            total_sent=total_sent,
            total_delivered=total_delivered,
            total_opened=total_opened,
            total_clicked=total_clicked,
            total_converted=total_converted,
            avg_delivery_rate=avg_delivery_rate,
            avg_open_rate=avg_open_rate,
            avg_click_rate=avg_click_rate,
            avg_conversion_rate=avg_conversion_rate,
            total_cost=total_cost,
            total_revenue=total_revenue,
            avg_roi=avg_roi
        )

    async def get_campaign_interactions(
        self, 
        campaign_id: uuid.UUID, 
        page: int = 1, 
        page_size: int = 50,
        interaction_type: Optional[str] = None
    ):
        """Get campaign interactions"""
        query = select(CampaignInteraction).where(CampaignInteraction.campaign_id == campaign_id)
        
        if interaction_type:
            query = query.where(CampaignInteraction.interaction_type == interaction_type)
        
        # Get total count
        count_query = select(func.count()).select_from(CampaignInteraction).where(
            CampaignInteraction.campaign_id == campaign_id
        )
        if interaction_type:
            count_query = count_query.where(CampaignInteraction.interaction_type == interaction_type)
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(desc(CampaignInteraction.occurred_at))
        
        result = await self.db.execute(query)
        interactions = result.scalars().all()
        
        interaction_responses = [
            CampaignInteractionResponse.model_validate(interaction) 
            for interaction in interactions
        ]
        
        total_pages = math.ceil(total / page_size)
        
        return {
            "interactions": interaction_responses,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    async def get_campaign_performance(self, campaign_id: uuid.UUID):
        """Get detailed campaign performance"""
        campaign = await self.get_campaign_by_id(campaign_id)
        if not campaign:
            return None
        
        # Get interaction breakdown
        interaction_query = select(
            CampaignInteraction.interaction_type,
            func.count(CampaignInteraction.id)
        ).where(
            CampaignInteraction.campaign_id == campaign_id
        ).group_by(CampaignInteraction.interaction_type)
        
        interaction_result = await self.db.execute(interaction_query)
        interactions = dict(interaction_result.fetchall())
        
        return {
            "campaign": campaign,
            "interaction_breakdown": interactions,
            "performance_metrics": {
                "delivery_rate": campaign.delivery_rate,
                "open_rate": campaign.open_rate,
                "click_rate": campaign.click_rate,
                "conversion_rate": campaign.conversion_rate,
                "roi_percentage": campaign.roi_percentage
            }
        }

    async def test_campaign(self, campaign_id: uuid.UUID, phone_numbers: List[str]):
        """Send test campaign"""
        campaign = await self.get_campaign_by_id(campaign_id)
        if not campaign:
            return None
        
        # Mock test sending (in production, integrate with SMS gateway)
        results = []
        for phone in phone_numbers:
            results.append({
                "phone_number": phone,
                "status": "sent",
                "message": f"Test message sent successfully to {phone}"
            })
        
        return results

    async def _process_campaign(self, campaign_id: uuid.UUID):
        """Background task to process campaign execution"""
        # This is a mock implementation
        # In production, this would:
        # 1. Get target customers from segment
        # 2. Send messages via SMS gateway
        # 3. Track delivery status
        # 4. Update campaign metrics
        
        import asyncio
        import random
        
        # Simulate campaign processing
        await asyncio.sleep(5)  # Simulate processing time
        
        query = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.db.execute(query)
        campaign = result.scalar_one_or_none()
        
        if campaign and campaign.status == 'running':
            # Mock performance metrics
            target_count = campaign.target_count
            sent_count = int(target_count * random.uniform(0.95, 1.0))
            delivered_count = int(sent_count * random.uniform(0.92, 0.98))
            opened_count = int(delivered_count * random.uniform(0.85, 0.95))
            clicked_count = int(opened_count * random.uniform(0.08, 0.15))
            converted_count = int(clicked_count * random.uniform(0.20, 0.40))
            
            campaign.sent_count = sent_count
            campaign.delivered_count = delivered_count
            campaign.opened_count = opened_count
            campaign.clicked_count = clicked_count
            campaign.converted_count = converted_count
            campaign.total_cost = sent_count * float(campaign.cost_per_message or 2.5)
            campaign.revenue_generated = converted_count * random.uniform(200, 800)
            campaign.status = 'completed'
            campaign.completed_at = datetime.utcnow()
            
            await self.db.commit()