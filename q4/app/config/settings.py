from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    mongo_uri: str = os.environ.get('MONGO_URI',"mongodb://localhost:27017/")
    secret_key: str = os.environ.get('SECRET_KEY',"rANDOMR_SECRET_KEY")
    
settings = Settings()