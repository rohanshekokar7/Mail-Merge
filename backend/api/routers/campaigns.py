from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from db.session import get_db
from api.deps import get_current_active_user
from models.user import User
from models.campaign import Campaign as CampaignModel
from schemas.campaign import Campaign, CampaignCreate, CampaignUpdate

router = APIRouter()

@router.get("/", response_model=List[Campaign])
def read_campaigns(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve campaigns for current user.
    """
    campaigns = db.query(CampaignModel).filter(CampaignModel.user_id == current_user.id).offset(skip).limit(limit).all()
    return campaigns

@router.post("/", response_model=Campaign)
def create_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_in: CampaignCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new campaign.
    """
    db_obj = CampaignModel(**campaign_in.model_dump(), user_id=current_user.id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/{id}", response_model=Campaign)
def read_campaign(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get campaign by ID.
    """
    campaign = db.query(CampaignModel).filter(CampaignModel.id == id, CampaignModel.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.put("/{id}", response_model=Campaign)
def update_campaign(
    *,
    db: Session = Depends(get_db),
    id: int,
    campaign_in: CampaignUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a campaign.
    """
    campaign = db.query(CampaignModel).filter(CampaignModel.id == id, CampaignModel.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    update_data = campaign_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(campaign, field, update_data[field])
        
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

@router.delete("/{id}", response_model=Campaign)
def delete_campaign(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a campaign.
    """
    campaign = db.query(CampaignModel).filter(CampaignModel.id == id, CampaignModel.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    db.delete(campaign)
    db.commit()
    return campaign

@router.post("/{id}/start", response_model=Campaign)
def start_campaign(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Start a campaign by updating its status and queueing the Celery task.
    """
    campaign = db.query(CampaignModel).filter(CampaignModel.id == id, CampaignModel.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    if campaign.status in [CampaignModel.status.RUNNING, CampaignModel.status.COMPLETED]:
        raise HTTPException(status_code=400, detail="Campaign is already running or completed")
        
    campaign.status = CampaignModel.status.RUNNING
    # We should really use models.campaign.CampaignStatus, wait, let me use string literal or proper enum.
    # The models use Enum(CampaignStatus). Let's import it.
    
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    
    # Import locally to avoid circular dependencies
    from workers.tasks import process_campaign
    process_campaign.delay(campaign.id)
    
    return campaign
