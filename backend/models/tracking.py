from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from db.base_class import Base

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    campaign_recipient_id = Column(Integer, ForeignKey("campaign_recipients.id", ondelete="CASCADE"), nullable=False, index=True)
    
    provider = Column(String, nullable=False) # e.g. SMTP, SES, Mailpit
    provider_message_id = Column(String, nullable=True, index=True)
    event_type = Column(String, nullable=False, index=True) # QUEUED, SENDING, SENT, FAILED
    status = Column(String, nullable=False)
    error = Column(Text, nullable=True)
    metadata_ = Column("metadata", JSONB, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id = Column(Integer, primary_key=True, index=True)
    campaign_recipient_id = Column(Integer, ForeignKey("campaign_recipients.id", ondelete="CASCADE"), nullable=False, index=True)
    
    event_type = Column(String, nullable=False, index=True) # OPEN, CLICK, DELIVERED, BOUNCED, COMPLAINT, UNSUBSCRIBE, REPLY
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    metadata_ = Column("metadata", JSONB, nullable=True)
