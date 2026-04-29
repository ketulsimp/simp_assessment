from app.config.db import get_db
from bson import ObjectId

async def fetch_tasks(username, priority):
    db = get_db()
    tasks = []
    if priority:
        async for task in db.tasks.find({'username': username, 'priority': priority}, {'_id': 0}):
            tasks.append(task)
    else:
        async for task in db.tasks.find({'username': username}, {'_id': 0}):
            tasks.append(task)
    return tasks

async def store_task(task, user):
    db = get_db()
    doc = {
        'username': user,
        'title': task.title,
        'priority': task.priority.value,
        'status': task.status.value
    }
    await db.tasks.insert_one(doc)
    
async def put_task(id, user, status):
    db = get_db()
    await db.tasks.update_one({'_id': ObjectId(id), 'username': user}, {"$set": {'status': status}})