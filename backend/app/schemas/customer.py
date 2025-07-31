from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
import uuid

class CustomerBase(BaseModel):
    phone_number: str = Field(..., description="Customer phone number")
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    customer_type: str = Field(default="prepaid", description="prepaid or postpaid")
    province: Optional[str] = None
    city: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    status: Optional[str] = None

class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    status: str
    activation_date: datetime
    current_balance: Decimal
    arpu_30d: Decimal
    arpu_90d: Decimal
    total_revenue: Decimal
    total_voice_minutes: int
    total_sms_sent: int
    total_data_mb: int
    days_since_last_activity: int
    total_recharges: int
    avg_recharge_amount: Decimal
    primary_device_brand: Optional[str]
    primary_device_model: Optional[str]
    device_type: Optional[str]
    churn_score: Decimal
    lifetime_value: Decimal
    next_best_offer_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
    last_activity_at: datetime
    
    # Computed properties
    full_name: Optional[str] = None
    is_high_value: bool = False
    is_at_risk: bool = False
    risk_level: str = "unknown"

class CustomerSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    phone_number: str
    full_name: Optional[str]
    customer_type: str
    status: str
    arpu_30d: Decimal
    churn_score: Decimal
    days_since_last_activity: int
    risk_level: str
    created_at: datetime
    last_activity_at: datetime

class CustomerListResponse(BaseModel):
    customers: List[CustomerSummary]
    total: int
    page: int
    page_size: int
    total_pages: int

class CustomerMetrics(BaseModel):
    total_customers: int
    active_customers: int
    churned_customers: int
    high_value_customers: int
    at_risk_customers: int
    avg_arpu: Decimal
    avg_churn_score: Decimal
    prepaid_customers: int
    postpaid_customers: int