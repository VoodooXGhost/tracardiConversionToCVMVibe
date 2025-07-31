from sqlalchemy import Column, String, Integer, Decimal, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from ..core.database import Base

class Offer(Base):
    __tablename__ = "offers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    offer_type = Column(String(50), nullable=False)  # data_bundle, voice_bundle, discount, upgrade
    
    # Offer details
    price = Column(Decimal(10, 2), nullable=False)
    value = Column(Decimal(10, 2))  # Original value for discounts
    validity_days = Column(Integer)
    
    # Offer configuration
    data_mb = Column(Integer)  # For data bundles
    voice_minutes = Column(Integer)  # For voice bundles
    sms_count = Column(Integer)  # For SMS bundles
    discount_percentage = Column(Decimal(5, 2))  # For discount offers
    
    # Availability
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime(timezone=True), server_default=func.now())
    valid_until = Column(DateTime(timezone=True))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Offer(id={self.id}, name={self.name}, type={self.offer_type})>"

    @property
    def is_valid(self):
        from datetime import datetime
        now = datetime.utcnow()
        return (
            self.is_active and
            (not self.valid_until or self.valid_until > now)
        )