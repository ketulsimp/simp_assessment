from pymongo import AsyncMongoClient
from app.conf.settings import settings

class DBManager:
    _client: AsyncMongoClient = None
    _db = None
    
db_manager = DBManager()

async def connect_to_mongo():
    db_manager._client = AsyncMongoClient(settings.mongo_uri)
    db_manager._db = db_manager._client["user"]
    try:
        await db_manager._client.admin.command('ping')
        print('Connection to Mongo Successfull')
    except Exception:
        print('Connection Error')
        

def get_db():
    return db_manager._db