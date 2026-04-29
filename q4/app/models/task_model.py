from pydantic import BaseModel, Field
from enum import Enum


class Priority(Enum):
    low = "LOW"
    high = "HIGH"
    medium = "MEDIUM"
    
class Status(Enum):
    pending: str = "PENDING"
    completed: str = "COMPLETED"

class Task(BaseModel):
    title: str = Field(...)
    priority: Priority = Field(default=Priority.low)
    status: Status = Field(default=Status.pending)
    