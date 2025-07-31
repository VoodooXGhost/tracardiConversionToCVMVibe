from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
import uuid

class OfferBase(BaseModel):
    name: str = Field(..., description="Offer name")
    description: Optional[str] = None
    offer_type: str = Field(..., description="Offer type (data_bundle, voice_bundle, discount, upgrade)")
    price: Decimal = Field(..., description="Offer price")
    value: Optional[Decimal] = None
    validity_days: Optional[int] = None
    data_mb: Optional[int] = None
    voice_minutes: Optional[int] = None
    sms_count: Optional[int] = None
    discount_percentage: Optional[Decimal] = None
    is_active: bool = True

class OfferCreate(OfferBase):
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

class OfferUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    value: Optional[Decimal] = None
    validity_days: Optional[int] = None
    data_mb: Optional[int] = None
    voice_minutes: Optional[int] = None
    sms_count: Optional[int] = None
    discount_percentage: Optional[Decimal] = None
    is_active: Optional[bool] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

class OfferResponse(OfferBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    valid_from: datetime
    valid_until: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    is_valid: bool

class OfferListResponse(BaseModel):
    offers: List[OfferResponse]
    total: int
    page: int
    page_size: int
    total_pages: int