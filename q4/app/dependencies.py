from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import user_collection
from jose import jwt 
from app.config import SECRET_KEY,ALGORITHM


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithm=[ALGORITHM])
        user_id=await user_collection.find_one(payload["sub"])
        return user_id
    except:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    
def admin_required(user=Depends(get_current_user)):
    if user["role"] != "admin" and user["password"] !="admmin123":
        raise HTTPException(status_code=403,detail="Admin Authentication Required")
    return user 

