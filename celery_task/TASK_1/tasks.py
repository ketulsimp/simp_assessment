from celery_worker import celery_app
import time

@celery_app.task
def daily_task():
    print("Daily task started")
    time.sleep(5)  
    print("Daily task completed")

@celery_app.task(bind=True,max_retries=3,base_delay=10,soft_time_limit=20,time_limit=30):
def generate_daily_report(self,report_type,user_id):
    try:
        print(f"Generating {report_type} report for user {user_id}")
        time.sleep(10)  
        print(f"{report_type} report for user {user_id} generated successfully")
    except Exception as e:
        print(f"Error generating report: {e}")
        self.retry(exc=e)
    
@celery_app.task
def notify_user(user_id,message):
    print(f"Notifying user {user_id} with message: {message}")
    time.sleep(2)  
    print(f"User {user_id} notified successfully")