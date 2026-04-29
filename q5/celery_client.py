from celery import Celery

celery_client = Celery(
    "tasks",
    backend="redis://localhost:6379/1",
    broker="redis://localhost:6379/0"
)

