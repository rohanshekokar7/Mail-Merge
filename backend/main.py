from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy import text
from core.config import settings
from db.session import get_db, engine
from workers.celery_app import celery_app
from workers.tasks import health_check_task
import redis
from sqlalchemy.orm import Session
from api.routers import auth, users

app = FastAPI(title="Mail Merge Platform API")

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    status = {
        "api": "ok",
        "database": "unknown",
        "redis": "unknown"
    }
    
    # Check DB
    try:
        db.execute(text("SELECT 1"))
        status["database"] = "ok"
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        
    # Check Redis
    try:
        r = redis.Redis.from_url(settings.REDIS_URL)
        r.ping()
        status["redis"] = "ok"
    except Exception as e:
        status["redis"] = f"error: {str(e)}"
        
    return status

@app.post("/test-celery")
def test_celery():
    task = health_check_task.delay()
    return {"message": "Task queued", "task_id": task.id}
