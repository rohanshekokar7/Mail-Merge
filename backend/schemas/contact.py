from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional
from datetime import datetime
from models.contact import RecipientStatus

class ContactBase(BaseModel):
    email: str
    dynamic_data: Dict[str, Any] = {}

class ContactCreate(ContactBase):
    pass

class ContactInDBBase(ContactBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Contact(ContactInDBBase):
    pass

class CampaignRecipientBase(BaseModel):
    email: str
    status: RecipientStatus = RecipientStatus.PENDING

class CampaignRecipientCreate(CampaignRecipientBase):
    campaign_id: int
    contact_id: int

class CampaignRecipientInDBBase(CampaignRecipientBase):
    id: int
    campaign_id: int
    contact_id: int
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CampaignRecipient(CampaignRecipientInDBBase):
    pass
