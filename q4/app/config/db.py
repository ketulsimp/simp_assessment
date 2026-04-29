from pymongo import AsyncMongoClient
from pymongo.database import Database
from app.config.settings import settings
import logging

class DbManager:
    client: AsyncMongoClient = None
    db = None
    
    
manager = DbManager()

async def connect():
    try:
        manager.client = AsyncMongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
        manager.db = manager.client["fastapi_final_assessment"]
        await manager.client.admin.command('ping')
        print("Connecion Successfull")
    except Exception:
        logging.exception("Connection Failed")
        
async def disconnect():
    await manager.client.aclose()
    
def get_db():
    return manager.db