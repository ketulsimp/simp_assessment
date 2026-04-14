from pydantic import BaseModel, Field, SecretStr
from enum import Enum

class Role(Enum):
    admin = "ADMIN"
    viewer = "VIEWER"

class Register(BaseModel):
    username: str = Field(...)
    password: SecretStr =  Field(...)
    role: Role 
    
    
class Login(BaseModel):
    username: str = Field(...)
    password: SecretStr = Field(...)