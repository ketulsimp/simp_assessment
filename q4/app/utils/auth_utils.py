import jwt
from app.config.settings import settings
import datetime
from app.config.db import get_db
from fastapi import HTTPException
import bcrypt

def create_access_token(username):
    payload = {
        'sub': username,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=10)
    }
    return jwt.encode(payload,settings.secret_key,"HS256")

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())


async def store_user_in_mongo(username, password):
    # Expecting the username to be unique for each user
    db = get_db()
    user_exist = await db.users.find_one({'username':username})
    if user_exist:
        raise HTTPException(
            status_code=400,
            detail='User already Exist'
        )
    try:
        await db.users.insert_one({'username': username, 'password': hash_password(password)})
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Database Insertion Error'
        )
    
async def authenticate_user(form):
    db = get_db()
    user_exist = await db.users.find_one({'username': form.username})
    if user_exist and bcrypt.checkpw(form.password.encode('utf-8'),user_exist.get('password')):
        return True
    raise HTTPException(
        status_code=401,
        detail='Authentication Error'
    )
    