from fastapi import APIRouter, Depends, Form
from app.config.security import authorize
from app.utils.task_utils import *
from app.models.task_model import Task, Priority, Status

task_rt = APIRouter(prefix="/tasks")

@task_rt.get("/")
async def get_tasks(priority: Priority | None = None , user = Depends(authorize)):
    return await fetch_tasks(user, priority.value if priority else None)

@task_rt.post("/")
async def post_task(task: Task = Form(), user = Depends(authorize)):
    await store_task(task,user)
    
@task_rt.put("/{id}")
async def update_task(id: str, status: Status, user = Depends(authorize)):
    await put_task(id,user,status.value)