from sqlalchemy import Column, String, Integer, Decimal, DateTime, Boolean, Text, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(255))
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(Date)
    gender = Column(String(10))
    
    # Telco specific fields
    customer_type = Column(String(20), nullable=False, default='prepaid')
    activation_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), nullable=False, default='active', index=True)
    
    # Location data
    province = Column(String(50))
    city = Column(String(50))
    
    # Financial metrics
    current_balance = Column(Decimal(10, 2), default=0.00)
    arpu_30d = Column(Decimal(10, 2), default=0.00, index=True)
    arpu_90d = Column(Decimal(10, 2), default=0.00)
    total_revenue = Column(Decimal(12, 2), default=0.00)
    
    # Usage metrics
    total_voice_minutes = Column(Integer, default=0)
    total_sms_sent = Column(Integer, default=0)
    total_data_mb = Column(Integer, default=0)
    
    # Behavioral metrics
    days_since_last_activity = Column(Integer, default=0)
    total_recharges = Column(Integer, default=0)
    avg_recharge_amount = Column(Decimal(10, 2), default=0.00)
    
    # Device information
    primary_device_brand = Column(String(50))
    primary_device_model = Column(String(100))
    device_type = Column(String(20))
    
    # Predictive scores (ML generated)
    churn_score = Column(Decimal(3, 2), default=0.00, index=True)
    lifetime_value = Column(Decimal(12, 2), default=0.00)
    next_best_offer_id = Column(UUID(as_uuid=True))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<Customer(id={self.id}, phone={self.phone_number}, type={self.customer_type})>"

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or "Unknown"

    @property
    def is_high_value(self):
        return self.arpu_30d and self.arpu_30d > 1000

    @property
    def is_at_risk(self):
        return self.churn_score and self.churn_score > 0.7

    @property
    def risk_level(self):
        if not self.churn_score:
            return "unknown"
        if self.churn_score > 0.8:
            return "high"
        elif self.churn_score > 0.5:
            return "medium"
        else:
            return "low"