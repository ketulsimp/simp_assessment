from jose import JWTError,jwt
from datetime import datetime,timedelta

SECRET_KEY="ADMIN@123"
ALGORITHM="HS256"

def create_token(data:dict):
    to_encode=data.copy()
    to_encode["expire"]=datetime.utcnow()+timedelta(minutes=30)
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

    
def decode_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload["user_id"]
    except JWTError:
        return None
    

