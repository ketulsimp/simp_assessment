from pydantic import BaseModel,Field
from typing import Optional

class UserCreate(BaseModel):
    username:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class CreateTask(BaseModel):
    name:str
    title:str
    priority=Field(default="low/medium/high")

class UpdateTask(BaseModel):
    name:Optional[str]=None
    title:Optional[str]=None