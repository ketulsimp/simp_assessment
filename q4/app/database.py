from motor.motor_asyncio import AsyncIOMotorClient

client=AsyncIOMotorClient("mongodb://localhost:27017/")
db=client["q4"]
user_collection=db["users"]
task_collection=db["tasks"]
