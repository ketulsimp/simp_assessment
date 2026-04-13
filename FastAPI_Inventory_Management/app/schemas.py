
from pydantic import BaseModel,Field
from typing import Optional

class UserRegister(BaseModel):
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class CreateProduct(BaseModel):
    id:str
    name: str
    category: str
    price: float
    stock: int

class UpdateProduct(BaseModel):
    name: Optional[str]
    category: Optional[str]
    price: Optional[float]
    stock: Optional[int]

    