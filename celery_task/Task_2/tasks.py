
from celery_worker import celery_app
import time
import logging

logging.basicConfig(level=logging.INFO)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def send_email(self,to, subject, body):
    try:
        # Simulate email sending
        logging.info(f"Sending email to {to} with subject '{subject}'")
        time.sleep(2)  # Simulate time taken to send an email
        logging.info(f"Email sent to {to}")
    except Exception as exc:
        logging.error(f"Failed to send email to {to}: {exc}")
        raise self.retry(exc=exc)
    
@celery_app.task
def send_bulk_emails(users):
    for user in users:
        send_email.delay(user['email'], "Hello!", "This is a bulk email.")  
