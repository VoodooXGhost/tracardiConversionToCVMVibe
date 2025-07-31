from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class SegmentCondition(BaseModel):
    field: str = Field(..., description="Field name to filter on")
    operator: str = Field(..., description="Comparison operator (=, >, <, >=, <=, !=, in, not_in)")
    value: Any = Field(..., description="Value to compare against")

class SegmentBase(BaseModel):
    name: str = Field(..., description="Segment name")
    description: Optional[str] = None
    conditions: Dict[str, Any] = Field(..., description="Segment conditions in JSON format")
    is_active: bool = True

class SegmentCreate(SegmentBase):
    created_by: Optional[str] = None

class SegmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class SegmentResponse(SegmentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    customer_count: int
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime

class SegmentListResponse(BaseModel):
    segments: List[SegmentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class SegmentCustomerCount(BaseModel):
    segment_id: uuid.UUID
    segment_name: str
    customer_count: int
    conditions: Dict[str, Any]