from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.base_class import Base
import enum

class RecipientStatus(str, enum.Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    SENDING = "SENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    OPENED = "OPENED"
    REPLIED = "REPLIED"
    BOUNCED = "BOUNCED"
    FAILED = "FAILED"
    UNSUBSCRIBED = "UNSUBSCRIBED"
    SUPPRESSED = "SUPPRESSED"
    SKIPPED = "SKIPPED"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    dynamic_data = Column(JSONB, nullable=False, default=dict)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class CampaignRecipient(Base):
    __tablename__ = "campaign_recipients"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    email = Column(String, nullable=False, index=True)
    rendered_subject = Column(Text, nullable=True)
    rendered_body = Column(Text, nullable=True)
    status = Column(Enum(RecipientStatus), default=RecipientStatus.PENDING, nullable=False, index=True)
    
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    replied_at = Column(DateTime(timezone=True), nullable=True)
    first_opened_at = Column(DateTime(timezone=True), nullable=True)
    last_opened_at = Column(DateTime(timezone=True), nullable=True)
    
    followup_eligible = Column(Boolean, default=True, nullable=False)
    unsubscribed = Column(Boolean, default=False, nullable=False)
    suppressed = Column(Boolean, default=False, nullable=False)
    failure_reason = Column(Text, nullable=True)
    
    provider_message_id = Column(String, nullable=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('campaign_id', 'contact_id', name='uq_campaign_contact'),
    )

    campaign = relationship("Campaign", back_populates="recipients")
    contact = relationship("Contact")
