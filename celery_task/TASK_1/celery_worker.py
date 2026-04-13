from celery import Celery
from celery.schedules import crontab


celery_app = Celery('tasks', 
                    broker='redis://localhost:6379/0', 
                    backend='redis://localhost:6379/0',
                    include=["tasks"])

celery_app.conf.beat_schedule = {
    'run-task-daily': {
        'task': 'tasks.daily_task',
        'schedule': crontab(hour=2, minute=0),  
    },
    "generate-daily-report": {
        'task': 'tasks.generate_daily_report',
        'schedule': crontab(hour=3, minute=0),
    },
    "notify-users": {
        'task': 'tasks.notify_user',
        'schedule': crontab(hour=5, minute=0),
    },
}

celery_app.conf.timezone = 'UTC'


