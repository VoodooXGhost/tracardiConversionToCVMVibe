from sqlalchemy import Column, String, Integer, Decimal, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from ..core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False, index=True)
    event_name = Column(String(100), nullable=False)
    
    # Event data
    properties = Column(JSONB)  # Flexible event properties
    amount = Column(Decimal(10, 2))  # For financial events
    duration = Column(Integer)  # For call events (seconds)
    data_volume_mb = Column(Integer)  # For data events
    
    # Context
    channel = Column(String(50))  # ussd, app, web, retail
    location_province = Column(String(50))
    location_city = Column(String(50))
    
    # Metadata
    occurred_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Event(id={self.id}, type={self.event_type}, customer_id={self.customer_id})>"