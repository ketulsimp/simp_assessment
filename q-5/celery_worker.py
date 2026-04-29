from celery import Celery
from task import shared_task


cerlery_app = Celery("assingment-5", broker="redis://localhost:6379/0",backend="redis:localhost:6379/0", tasks=shared_task)
