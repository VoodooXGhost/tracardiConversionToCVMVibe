from sqlalchemy import Column, String, Integer, Decimal, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    campaign_type = Column(String(50), nullable=False, default='sms')
    
    # Campaign configuration
    message_template = Column(Text, nullable=False)
    target_segment_id = Column(UUID(as_uuid=True), ForeignKey("segments.id"))
    
    # Scheduling
    status = Column(String(20), default='draft', index=True)
    scheduled_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Performance metrics
    target_count = Column(Integer, default=0)
    sent_count = Column(Integer, default=0)
    delivered_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    clicked_count = Column(Integer, default=0)
    converted_count = Column(Integer, default=0)
    
    # Financial
    budget = Column(Decimal(10, 2))
    cost_per_message = Column(Decimal(5, 4))
    total_cost = Column(Decimal(10, 2), default=0.00)
    revenue_generated = Column(Decimal(12, 2), default=0.00)
    
    # Metadata
    created_by = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    interactions = relationship("CampaignInteraction", back_populates="campaign")

    def __repr__(self):
        return f"<Campaign(id={self.id}, name={self.name}, status={self.status})>"

    @property
    def delivery_rate(self):
        if self.sent_count > 0:
            return round((self.delivered_count / self.sent_count) * 100, 2)
        return 0.0

    @property
    def open_rate(self):
        if self.delivered_count > 0:
            return round((self.opened_count / self.delivered_count) * 100, 2)
        return 0.0

    @property
    def click_rate(self):
        if self.opened_count > 0:
            return round((self.clicked_count / self.opened_count) * 100, 2)
        return 0.0

    @property
    def conversion_rate(self):
        if self.clicked_count > 0:
            return round((self.converted_count / self.clicked_count) * 100, 2)
        return 0.0

    @property
    def roi_percentage(self):
        if self.total_cost and self.total_cost > 0:
            return round(((self.revenue_generated - self.total_cost) / self.total_cost) * 100, 2)
        return 0.0

class CampaignInteraction(Base):
    __tablename__ = "campaign_interactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    
    # Interaction details
    interaction_type = Column(String(50), nullable=False)  # sent, delivered, opened, clicked, converted
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Additional data
    properties = Column(JSONB)

    # Relationships
    campaign = relationship("Campaign", back_populates="interactions")

    def __repr__(self):
        return f"<CampaignInteraction(campaign_id={self.campaign_id}, type={self.interaction_type})>"