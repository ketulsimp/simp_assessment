from fastapi import APIRouter,HTTPException,Depends
from app.database import task_collection
from app.dependencies import get_current_user
from bson import ObjectId
from app.schemas import CreateTask,UpdateTask


task_route=APIRouter(prefix="/task_route")

@task_route.get("/dashboard")
async def dashboard(user=Depends(get_current_user)):
    user_id=get_current_user()

    return{
        "message":"Welcome!!",
        "user_id":user_id
    }

async def verify_id(id:str):
    try:
        return ObjectId(id)
    except:
        raise HTTPException(status_code=403,detail="Invalid ObjectId")
    

@task_route.post("/tasks")
async def create_task(task:CreateTask=Depends(get_current_user)):

    task_dict=task.model_dump()

    result=await task_collection.insert_one(task_dict)

    return {
        "result": str(result.inserted_id),
        "message":"Task Created Sucessfully"
    }

@task_route.get("/tasks")
async def read_tasks(user_id:str=Depends(get_current_user),page:int=1,limit:int=5):
    obj_id=verify_id(user_id)
    skip=(page-1)*limit

    result=[]
    async for items in task_collection.find(),skip(skip).limit(limit):
        result.append(items)
    return {
        "user_id":items[obj_id],
        "name":items["name"],
        "description":items["description"],
        "amount":items["amount"]
    }

@task_route.put("tasks/{task_id}")
async def update_task(task_id:int ,task:UpdateTask,user_id:str=Depends(get_current_user)):
    obj_id=verify_id(user_id)

    task=await task_collection.find_one({"_id":obj_id})

    update_task={k:v for k,v in task.model_dump().items() if not None }

    result=await task_collection.update_one({"_id":obj_id},{"$set":update_task})

    if result.modified_count==0:
        raise HTTPException(status_code=403,detail="Task Not Updated")
    
@task_route.delete("/tasks/{task_id}")
async def delete_task(task_id):
    result=await task_collection.delete_one(task_id)

    if result.deleted_count==0:
        raise HTTPException(status_code=403,detail="Task Not Deleted")
    