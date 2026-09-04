from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.base_class import Base

class Followup(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    sequence_number = Column(Integer, nullable=False)
    delay_days = Column(Integer, nullable=False)
    subject_template = Column(Text, nullable=True)
    body_template = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    campaign = relationship("Campaign", back_populates="followups")

class FollowupJob(Base):
    __tablename__ = "followup_jobs"

    id = Column(Integer, primary_key=True, index=True)
    campaign_recipient_id = Column(Integer, ForeignKey("campaign_recipients.id", ondelete="CASCADE"), nullable=False, index=True)
    followup_id = Column(Integer, ForeignKey("followups.id", ondelete="CASCADE"), nullable=False, index=True)
    
    scheduled_at = Column(DateTime(timezone=True), nullable=False, index=True)
    executed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, nullable=False, default="SCHEDULED", index=True) # SCHEDULED, EXECUTED, CANCELLED, FAILED
    attempts = Column(Integer, default=0, nullable=False)
    last_error = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    recipient = relationship("CampaignRecipient")
    followup = relationship("Followup")
