from celery_client import celery_client
import json

def check_valid(item):
    if item.get("item_id",False) and item.get("price",False): 
        return True
    return False

def check_if_order_id_exist(order_id, data):
    for order in data:
        if order.get('order_id')==order_id:
            return order
    return None

@celery_client.task(bind=True,max_retries=5)
def process_task(self,order_id: str, items: list):
    with open("/home/raj/Desktop/Final_Assessment/q5/tmp/orders/.json","r") as file:
        data = json.load(file)
    order_id_presence = check_if_order_id_exist(order_id,data)
    if order_id_presence:
        items_present = order_id_presence.get('items')
        data.remove(order_id_presence)
        items_dictionary = {item['item_id']: True for item in items_present}
        valid_items = []
        for item in items:
            if check_valid(item) and not items_dictionary.get(item.get('item_id')):
                valid_items.append(item)
        block = {
            'order_id': order_id,
            'items': valid_items + items_present
        }
        data.append(block)
    else: 
        valid_items = []
        for item in items:
            if check_valid(item):
                valid_items.append(item)
        if len(valid_items)==0:
            self.retry(countdown=3)
        block = {
            'order_id': order_id,
            'items': valid_items
        }
        data.append(block)
    with open("/home/raj/Desktop/Final_Assessment/q5/tmp/orders/.json","w") as file:
        json.dump(data,file)
    