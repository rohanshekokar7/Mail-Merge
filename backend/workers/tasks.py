import time
import smtplib
from email.message import EmailMessage
from jinja2 import Template
from sqlalchemy.orm import Session
from datetime import datetime

from workers.celery_app import celery_app
from core.config import settings
from db.session import SessionLocal
from models.campaign import Campaign, CampaignStatus
from models.contact import CampaignRecipient, RecipientStatus

@celery_app.task
def health_check_task():
    # Simulate some work
    time.sleep(1)
    return {"status": "ok", "message": "Celery worker is healthy!"}

@celery_app.task(bind=True)
def process_campaign(self, campaign_id: int):
    """
    Process a campaign by sending emails to all pending recipients.
    """
    db: Session = SessionLocal()
    try:
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign or campaign.status != CampaignStatus.RUNNING:
            return {"status": "aborted", "reason": "Campaign not found or not in RUNNING state"}
            
        recipients = db.query(CampaignRecipient).filter(
            CampaignRecipient.campaign_id == campaign_id,
            CampaignRecipient.status == RecipientStatus.PENDING
        ).all()
        
        if not recipients:
            campaign.status = CampaignStatus.COMPLETED
            campaign.completed_at = datetime.utcnow()
            db.commit()
            return {"status": "completed", "sent": 0}
            
        sent_count = 0
        subject_template = Template(campaign.subject_template or "")
        body_template = Template(campaign.body_template or "")
        
        # Connect to SMTP
        try:
            server = smtplib.SMTP(settings.SMTP_HOST or "localhost", settings.SMTP_PORT)
            if settings.SMTP_USE_TLS:
                server.starttls()
            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        except Exception as e:
            return {"status": "error", "reason": f"SMTP connection failed: {str(e)}"}
            
        for recipient in recipients:
            contact = recipient.contact
            data = contact.dynamic_data
            
            # Render templates
            try:
                subject = subject_template.render(**data)
                body = body_template.render(**data)
                
                # Send email
                msg = EmailMessage()
                msg.set_content(body)
                msg['Subject'] = subject
                msg['From'] = settings.SMTP_FROM_EMAIL
                msg['To'] = recipient.email
                
                server.send_message(msg)
                
                # Update DB
                recipient.status = RecipientStatus.SENT
                recipient.rendered_subject = subject
                recipient.rendered_body = body
                recipient.sent_at = datetime.utcnow()
                sent_count += 1
                
            except Exception as e:
                recipient.status = RecipientStatus.FAILED
                recipient.failure_reason = str(e)
                
            # Throttle slightly
            time.sleep(0.1)
            
        server.quit()
        
        # Check if all done
        pending_count = db.query(CampaignRecipient).filter(
            CampaignRecipient.campaign_id == campaign_id,
            CampaignRecipient.status == RecipientStatus.PENDING
        ).count()
        
        if pending_count == 0:
            campaign.status = CampaignStatus.COMPLETED
            campaign.completed_at = datetime.utcnow()
            
        db.commit()
        return {"status": "success", "sent": sent_count}
        
    finally:
        db.close()
