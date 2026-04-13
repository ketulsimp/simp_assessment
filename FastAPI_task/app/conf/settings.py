import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    mongo_uri = os.environ.get('MONGO_URI')
    
settings = Settings()