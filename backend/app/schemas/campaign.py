from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
import uuid

class CampaignBase(BaseModel):
    name: str = Field(..., description="Campaign name")
    description: Optional[str] = None
    campaign_type: str = Field(default="sms", description="Campaign type (sms, email, push)")
    message_template: str = Field(..., description="Message template")
    target_segment_id: Optional[uuid.UUID] = None
    budget: Optional[Decimal] = None
    cost_per_message: Optional[Decimal] = None

class CampaignCreate(CampaignBase):
    scheduled_at: Optional[datetime] = None
    created_by: Optional[str] = None

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    message_template: Optional[str] = None
    target_segment_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    budget: Optional[Decimal] = None
    cost_per_message: Optional[Decimal] = None

class CampaignResponse(CampaignBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    status: str
    scheduled_at: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    # Performance metrics
    target_count: int
    sent_count: int
    delivered_count: int
    opened_count: int
    clicked_count: int
    converted_count: int
    
    # Financial
    total_cost: Decimal
    revenue_generated: Decimal
    
    # Computed rates
    delivery_rate: float
    open_rate: float
    click_rate: float
    conversion_rate: float
    roi_percentage: float
    
    # Metadata
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime

class CampaignListResponse(BaseModel):
    campaigns: List[CampaignResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class CampaignMetrics(BaseModel):
    total_campaigns: int
    active_campaigns: int
    completed_campaigns: int
    total_sent: int
    total_delivered: int
    total_opened: int
    total_clicked: int
    total_converted: int
    avg_delivery_rate: float
    avg_open_rate: float
    avg_click_rate: float
    avg_conversion_rate: float
    total_cost: Decimal
    total_revenue: Decimal
    avg_roi: float

class CampaignInteractionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    campaign_id: uuid.UUID
    customer_id: uuid.UUID
    interaction_type: str
    occurred_at: datetime
    properties: Optional[Dict[str, Any]] = None