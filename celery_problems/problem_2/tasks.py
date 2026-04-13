from celery_problems.problem_2.celery_ import celery
from celery.exceptions import MaxRetriesExceededError
import logging

@celery.task(name='tasks.send_email', max_retries=3, bind=True, retry_delay=10, retry_jitter=True)
def send_email(self,email):
    try:
        print('sending_email')
    except MaxRetriesExceededError:
        logging.warning(f"{email} failed to sent")
    except Exception:
        self.retry(countdown=5)
                

