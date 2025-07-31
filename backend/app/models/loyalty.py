from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from ..core.database import Base

class LoyaltyPoint(Base):
    __tablename__ = "loyalty_points"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    
    # Points
    points_earned = Column(Integer, nullable=False)
    points_spent = Column(Integer, default=0)
    current_balance = Column(Integer, nullable=False)
    
    # Transaction details
    transaction_type = Column(String(50), nullable=False)  # earned, spent, expired
    description = Column(Text)
    reference_id = Column(UUID(as_uuid=True))  # Reference to campaign, offer, etc.
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<LoyaltyPoint(customer_id={self.customer_id}, type={self.transaction_type}, points={self.points_earned})>"