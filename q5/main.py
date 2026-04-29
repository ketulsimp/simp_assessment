from tasks import process_task


task = process_task.delay("3",[{'item_id':1}])