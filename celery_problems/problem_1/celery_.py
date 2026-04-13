from celery import Celery
from celery.beat import crontab

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

celery.conf.time_limit = 300
celery.conf.soft_time_limit = 200

celery.conf.task_routes = {
    'tasks.generate_report': {'queue': 'reports'},
    'tasks.*': {'queue': 'default'}
}

celery.conf.timezone = 'UTC'
celery.conf.beat_schedule = {
    'daily_task': {
        'task': 'tasks.daily_task',
        'schedule': crontab(hour=2)
    }
}