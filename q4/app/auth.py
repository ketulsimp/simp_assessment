from jose import jwt
from bcrypt import gensalt,checkpw,hashpw
from app.config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTE
from datetime import datetime,timedelta

def hash_password(password:str):
    return hashpw(password.encode(),salt=gensalt)

def verify_password(plain,hashed):
    return checkpw(plain.encode(),hashed)

def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)