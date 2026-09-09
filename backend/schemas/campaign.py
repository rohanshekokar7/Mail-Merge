from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from models.campaign import CampaignStatus

class CampaignBase(BaseModel):
    name: str
    subject_template: Optional[str] = None
    body_template: Optional[str] = None
    status: CampaignStatus = CampaignStatus.DRAFT
    scheduled_at: Optional[datetime] = None

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    subject_template: Optional[str] = None
    body_template: Optional[str] = None
    status: Optional[CampaignStatus] = None
    scheduled_at: Optional[datetime] = None

class CampaignInDBBase(CampaignBase):
    id: int
    user_id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    paused_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Campaign(CampaignInDBBase):
    pass
