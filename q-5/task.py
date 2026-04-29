from celery import shared_task
import json
import os 

FILE_PATH = "/temp/orders.json"

def load_data():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return json.load(f)

def save_data():
    with open(FILE_PATH,"w") as f:
        return json.load(f,FILE_PATH)
    
@shared_task(bind=True,max_retries=2, default_retry_delay=3)
def process_order(self,order_id:str,items:list))
    data = load_data

    if order_id not in data:
        data[order_id] = []
    
    existing_ids = {items["item_id"] for items in data[order_id]}
    processed_items = []
    skipped_items = []
    
    for item in items:
        if "item_id" not in item or "price" not in item:
            skipped_items.append(item)
        
        if "item_id" in existing_ids:
            continue

        processed_items.append(item)
        data["order_id"].append(item)

    save_data(data)

    return {
        "order_id": order_id,
        "processed_items": processed_items,
        "skipped_items": skipped_items
    }
