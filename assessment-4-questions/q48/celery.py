from celery import Celery
from celery.result import AsyncResult
from celery.schedules import crontab
import logging
import time        
import random


logger=logging.getLogger("myapp")
logger.setLevel(logging.INFO)

file_handler=logging.FileHandler("notifications.log")
formatter=logging.Formatter("%{asctime}s - %{error}s - %{message}s")
file_handler.formatter(formatter)

logger.addHandler(file_handler)

celery_app=Celery(broker="redis://127.0.0.1:6479",backend="redis://127.0.0.1:6479")

celery_app.conf.beat_schedule={
    'daily-email':{
        'task':'daily_task',
        'schedule':crontab(hour=2,minute=0)
    },
    'daily-report':{
        'task':'generate_report'
    }
}

@celery_app.task(name='daily_task',bind=True,max_retries=3)
def daily_task(self):
    try:
        users=['ashish@gmail.com','bhavin@gmail.com']
        for user in users:
            logger.info(f'Sending email to {user}')
            time.sleep(2)
            if random.choice([True,False]):
                raise Exception(f"Failed to send email to {user}")
        logger.info('All emails sent successfully')
        return {'status':'SUCCESS'}
    except Exception as e:
        logger.info(f"ERROR : {e}")
        print(f"ERROR : {e}")
        if self.request.retries>=self.max_retries:
            logger.error("Max retries reached. Task failed permanently.")
            raise e
        logger.warning(f'Retrying Attempt : {self.request.retries+1}')
        raise self.retry(exc=e,countdown=5)        


@celery_app.task(bind=True,max_retries=3,queue='report_queue')
def generate_report(self,email):
    try:
        time.sleep(10)
        print(f'Sending report to {email}')
        if random.choice([True,False]):
            raise Exception("Random Failure")
        logger.info(f'Report sent to {email}')
        notify_user.delay(email)
        return {'message':'SUCCESS'}
    except Exception as e:
        print(f'ERROR : {e}')
        if self.request.retries>=self.max_retries:
            raise Exception(f"Retry Limit Reached Final Failure: {str(e)}")
        raise self.retry(exc=e, countdown=5)

@celery_app.task()
def notify_user(email):
    print(f'Notifying to {email}')
    if random.choice([True,False]):
        raise Exception("Random Failure")
    logger.info(f'Notified to {email}')
    notify_user.delay(email)
    return {'message':'SUCCESS'}