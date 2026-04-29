
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str
    priority: str

class TaskUpdate(BaseModel):
    status: str