from jose import jwt
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends
from model.db_model import users

security=HTTPBearer()

SECRET_KEY='@Ashish123'
ALGORITHM='HS256'

def create_access_token(data:dict):
    to_encode=data.copy()
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

async def verify_user(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token=credentials.credentials
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get('sub')
        if not email:
            return "Invalid Token"
        user=await users.find_one({'email':email})
        return user
    except Exception as e:
        raise e