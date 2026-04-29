from celery_worker import celery_app
import time

@celery_app.task(bind=True,max_retries=2)
def process_order(self,order_id,items:list):
    try:
        print(f"Processing Order with {order_id}")
        time.sleep(3)

        for item in items:
            print(item)

    except Exception as e:
        self.retry(exc=e,max_retries=2)


