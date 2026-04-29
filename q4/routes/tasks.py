from fastapi import Depends,HTTPException,APIRouter
from model.db_model import tasks
from schemas.schema import Task
from utils.jwt import verify_user
import uuid

task=APIRouter(__name__,prefix='/task')

@task.post('/create')
async def create_task(task:Task,user:dict=Depends(verify_user)):
    task_id=str(int(uuid.uuid4())[4])
    added_by=user['name']
    await tasks.insert_one({
        'task_id':task_id,
        'title':task['title'],
        'description':task['description'],
        'added_by':added_by
    })

    return {"message":'Task created successfully','Task-id':task_id}

@task.get('/show')
async def show_tasks(user:dict=Depends(verify_user)):
    all_tasks=await tasks.find({'added_by':user['name']})
    task_list=[]
    for t in all_tasks:
        t['_id']=str(t['_id'])
        task_list.append(t)
    return task_list

@task.put('/update')
async def update_task(task_id:int,task:Task,user:dict=Depends(verify_user)):
    query=await tasks.find_one({'task_id':task_id})
    if not query:
        raise HTTPException(404,detail='task not found')
    await tasks.update_one({'task_id':task_id},{'$set':{
        'title':task['title'],
        'descriiption':task['description']
    }})

    return {"message":"Task updated successfully"}

@task.delete('/delete/{task_id}')
async def delete_task(task_id:int,user:dict=Depends(verify_user)):
    query=await tasks.find_one({'task_id':task_id})
    if not query:
        raise HTTPException(404,detail='Task not found')
    await tasks.delete_one({'task_id':task_id})

    return {'message':'Task deleted successfully'}