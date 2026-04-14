from fastapi import Depends
from app.routes.auth_rt import oauth_scheme
from fastapi import HTTPException
import jwt


def authenticate(token = Depends(oauth_scheme)):
    try:
        user_data = jwt.decode(token,"This_is_my_highly_secret_key","HS256")
        return user_data
    except Exception:
        raise HTTPException(401, 'Invalid Token')