from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(...)
    category: str = Field(...)
    price: int = Field(...)
    stock: int = Field(...)
    