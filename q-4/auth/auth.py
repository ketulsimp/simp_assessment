from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from jose import jwt,JWTError

SECRET_KEY= "myname is smit"
ALGORITHM= "HS256"

security= HTTPBearer()

def create_token(username:str):
    return jwt.encode({"username": username}, SECRET_KEY,algorithm = ALGORITHM)

def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials,SECRET_KEY,
                             algorithms = [ALGORITHM])
        return payload["username"]
    except JWTError:
        raise HTTPException(status_code=401,detail = "INVALID TOKEN")
    