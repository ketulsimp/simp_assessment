from jose import jwt
from fastapi import Depends
from datetime import datetime,timedelta,timezone
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from app.database.db import users

ALGORITHM="HS256"
SECRET_KEY="secret@123"
security=HTTPBearer()

def create_token(data:dict):
    to_encode=data.copy()
    expiry=datetime.now(timezone.utc)+timedelta(minutes=10)
    to_encode.update({'expire':expiry})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

async def verify_token(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token=credentials.credentials
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        name=payload.get('sub')
        user=await users.find_one({'name':name})
        return user
    except Exception as e:
        raise Exception(e)