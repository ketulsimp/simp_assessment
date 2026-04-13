
from celery import Celery
import logging

logging.basicConfig(level=logging.INFO)

celery_app = Celery(
    'email_tasks', 
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['tasks'])

celery_app.conf.update(
    task_routes={
        'tasks.send_email': {'queue': 'emails'},
        'tasks.send_bulk_emails': {'queue': 'emails'},
    },

