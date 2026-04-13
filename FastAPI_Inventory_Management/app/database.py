from motor.motor_asyncio import AsyncIOMotorClient


client=AsyncIOMotorClient("mongodb://localhost:27017/")
db=client["inventory_db"]
user_collection=db["users"]
product_collection=db["products"]
stock_collection=db["stocks"]