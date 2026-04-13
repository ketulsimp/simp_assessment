from motor.motor_asyncio import AsyncIOMotorClient

client=AsyncIOMotorClient('mongodb://localhost:27017/assessment')
db=client['inventory']
users=db['users']
products=db['products']