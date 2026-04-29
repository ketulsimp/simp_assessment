from celery import Celery
from model.db_model import orders

celery=Celery(backend='redis://localhost:6379/0',broker='redis://localhost:6379/0')

@celery.task(bind=True,max_retries=2)
def process_order(self,order_id:str,items:list):
    skipped_items=[]
    processed_items=[]
    try:
        query=orders.find_one({'order_id':order_id})
        if not query:
            orders.insert_one({
                'order_id':order_id
            })
            for i in range(len(items)):
                query=orders.find_one({'items.item_id':items[i]['item_id']})
                if not query:
                    orders.update_one({'order_id':order_id},{'$set':{'items':{'items.addtoset':items[i]}}},upsert=True)
                    processed_items.append(items[i])
                else:
                    skipped_items.append(items[i])
        return {'order_id':order_id,'processed_items':processed_items,'skipped_items':skipped_items}
                
    except Exception as e:
        if self.retries>self.max_retries:
            return {"Max retry limit reached"}
        
