
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from auth.auth import create_token, get_current_user
from models import TaskCreate, LoginRequest, TaskUpdate
from database import task_collection

task_router = APIRouter()


@task_router.post("/login")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "admin123":
        token = create_token(data.username)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid Credentials")


@task_router.post("/tasks")
def create_task(task: TaskCreate, user: str = Depends(get_current_user)):
    new_task = {
        "title": task.title,
        "priority": task.priority,
        "status": "pending",
        "owner": user
    }
    result = task_collection.insert_one(new_task)
    return {"id": str(result.inserted_id)}


@task_router.get("/tasks")
def get_tasks(priority: str = None, user: str = Depends(get_current_user)):
    query = {"owner": user}
    if priority:
        query["priority"] = priority

    tasks = []
    for t in task_collection.find(query):
        t["_id"] = str(t["_id"])
        tasks.append(t)

    return tasks


@task_router.patch("/tasks/{task_id}")
def update_task(task_id: str, data: TaskUpdate, user: str = Depends(get_current_user)):
    task = task_collection.find_one({"_id": ObjectId(task_id)})

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["owner"] != user:
        raise HTTPException(status_code=403, detail="Not allowed")

    task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": data.status}}
    )

    return {"message": "Updated"}