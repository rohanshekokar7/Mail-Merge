from workers.celery_app import celery_app
import time

@celery_app.task
def health_check_task():
    # Simulate some work
    time.sleep(1)
    return {"status": "ok", "message": "Celery worker is healthy!"}
