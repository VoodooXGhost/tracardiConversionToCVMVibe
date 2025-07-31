from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base

class Segment(Base):
    __tablename__ = "segments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    conditions = Column(JSONB, nullable=False)  # Segment rules in JSON format
    is_active = Column(Boolean, default=True)
    customer_count = Column(Integer, default=0)
    created_by = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    customer_segments = relationship("CustomerSegment", back_populates="segment")

    def __repr__(self):
        return f"<Segment(id={self.id}, name={self.name}, count={self.customer_count})>"

class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), primary_key=True)
    segment_id = Column(UUID(as_uuid=True), ForeignKey("segments.id", ondelete="CASCADE"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    segment = relationship("Segment", back_populates="customer_segments")

    def __repr__(self):
        return f"<CustomerSegment(customer_id={self.customer_id}, segment_id={self.segment_id})>"