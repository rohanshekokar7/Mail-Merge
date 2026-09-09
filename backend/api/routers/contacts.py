import csv
import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Any

from db.session import get_db
from api.deps import get_current_active_user
from models.user import User
from models.contact import Contact as ContactModel, CampaignRecipient as CampaignRecipientModel
from models.campaign import Campaign as CampaignModel
from schemas.contact import Contact, CampaignRecipient

router = APIRouter()

@router.post("/campaigns/{campaign_id}/upload")
async def upload_contacts_csv(
    campaign_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload a CSV file of contacts for a campaign.
    """
    campaign = db.query(CampaignModel).filter(CampaignModel.id == campaign_id, CampaignModel.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    content = await file.read()
    decoded = content.decode("utf-8")
    
    # Parse CSV
    reader = csv.DictReader(io.StringIO(decoded))
    if not reader.fieldnames or 'email' not in [f.lower().strip() for f in reader.fieldnames]:
        raise HTTPException(status_code=400, detail="CSV must contain an 'email' column")

    contacts_created = 0
    
    for row in reader:
        # Extract email and dynamic data
        email = None
        dynamic_data = {}
        for key, value in row.items():
            clean_key = key.lower().strip()
            if clean_key == 'email':
                email = value.strip()
            else:
                dynamic_data[clean_key] = value.strip()
                
        if not email:
            continue
            
        # Find or create contact
        contact = db.query(ContactModel).filter(ContactModel.email == email, ContactModel.user_id == current_user.id).first()
        if not contact:
            contact = ContactModel(email=email, user_id=current_user.id, dynamic_data=dynamic_data)
            db.add(contact)
            db.flush()
        else:
            # Update dynamic data
            contact.dynamic_data = {**contact.dynamic_data, **dynamic_data}
            
        # Link to campaign if not already linked
        existing_recipient = db.query(CampaignRecipientModel).filter(
            CampaignRecipientModel.campaign_id == campaign_id,
            CampaignRecipientModel.contact_id == contact.id
        ).first()
        
        if not existing_recipient:
            recipient = CampaignRecipientModel(
                campaign_id=campaign_id,
                contact_id=contact.id,
                email=email
            )
            db.add(recipient)
            contacts_created += 1

    db.commit()
    return {"message": f"Successfully uploaded and linked {contacts_created} contacts"}

@router.get("/campaigns/{campaign_id}/recipients", response_model=List[CampaignRecipient])
def get_campaign_recipients(
    campaign_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get recipients for a campaign.
    """
    campaign = db.query(CampaignModel).filter(CampaignModel.id == campaign_id, CampaignModel.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    recipients = db.query(CampaignRecipientModel).filter(CampaignRecipientModel.campaign_id == campaign_id).offset(skip).limit(limit).all()
    return recipients
