from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from app.config.settings import settings
import jwt
from typing import Annotated

oauth2 = OAuth2PasswordBearer(tokenUrl='/login')


async def authorize(token: Annotated[OAuth2PasswordBearer,Depends(oauth2)] ):
    try:
        user = jwt.decode(token,settings.secret_key,algorithms=["HS256"])
        return user.get('sub')
    except Exception:
        raise HTTPException(
            status_code=403,
            detail='Invalid Jwt TOken'
        )