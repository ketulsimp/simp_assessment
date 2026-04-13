from celery import Celery
import random
import time
import logging

logger=logging.getLogger('myapp')
logger.setLevel(logging.INFO)

file_handler=logging.FileHandler("notifications.log")
formatter=logging.Formatter("%{asctime}s %{levelname}s %{message}s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

celery=Celery(__name__,broker="redis://127.0.0.1:6379",backend="redis://127.0.0.1:6379")

@celery.task(bind=True,max_retries=3)
def send_email(self,email):
    try:
        time.sleep(5)
        print(f'Sending email to {email}')
        if random.choice([True,False]):
            raise Exception("Random Failure")
        return {'message':'SUCCESS'}
    except Exception as e:
        print(f'ERROR : {e}')
        if self.request.retries>=self.max_retries:
            raise Exception(f"Retry Limit Reached Final Failure: {str(e)}")
        raise self.retry(exc=e, countdown=5)
    

@celery.task(bind=True,max_retries=3)
def send_bulk_email(self,l):
    try:
        for i in l:
            print(f'Sending email to {i['email']}')
            if random.choice([True,False]):
                logger.error(f"Failed to send email to {i['email']}")
                raise Exception("Random Failure")
        return {"message":'SUCCESS'}
    except Exception as e:
        print(f"ERROR : {e}")
        if self.request.retries>self.max_retries:
            print("Maximum limit reached")
            raise Exception(f"Failed")
        raise self.retry(exc=e,countdown=3)
    
emails=[{"email": "a@test.com"}, {"email": "b@test.com"}]
send_bulk_email.apply_async(args=[emails])