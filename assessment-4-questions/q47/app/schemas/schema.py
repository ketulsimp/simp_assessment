from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class RegisterUser(BaseModel):
    name:str=Field(...,example="Ashish")
    password:str=Field(...,min_length=5)
    role:str=Field(Optional(),default='viewer')

class LoginUser(BaseModel):
    name:str=Field(...,example="Ashish")
    password:str=Field(...,min_length=5)

class Product(BaseModel):
    product_id:int=Field(...,ge=1)
    product_name:str=Field(...,example='Mobile')
    category:str=Field(...,example='Electronics')
    price:int=Field(...,gt=1)
    stock:int=Field(...,ge=1)