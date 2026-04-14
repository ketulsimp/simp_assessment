from problem_2.celery_ import celery
from celery import Task
from celery.exceptions import SoftTimeLimitExceeded

@celery.task(name='tasks.generate_report', max_retries=3, bind=True, retry_delay=10, retry_jitter=True)
def generate_report(self,report_type, user_id, date_range):
    try:
        print('executing task')
    except SoftTimeLimitExceeded:
        print("softtimelimit exceeded")
        print('deleting partial files')
    except Exception:
        self.retry(countdown=10)
        
        
@celery.task(name='tasks.daily_task')
def daily_task():
    print('daily_task started')
