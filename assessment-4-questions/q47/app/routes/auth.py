from app.schemas.schema import RegisterUser,LoginUser
from app.database.db import users
from fastapi import APIRouter,HTTPException
import bcrypt
from app.utils.jwt import create_token

auth=APIRouter()

@auth.post('/register')
async def register(user:RegisterUser):
    query=await users.find_one({'name':user.name})
    if query:
        raise HTTPException(status_code=401,detail='User already exist')
    
    hashed_pass=bcrypt.hashpw(user.password.encode(),salt=bcrypt.gensalt()).decode()
    await users.insert_one({
        'name':user.name,
        'password':hashed_pass,
        'role':user.role
    })
    return {"message":"User registered successfully"}

@auth.login('/login')
async def login(user:LoginUser):
    query=await users.find_one({'name':user.name})
    if not query:
        raise HTTPException(status_code=404,detail="User doesn't exist")
    token=create_token({'sub':user.name})
    return {"message":f"Welcome {query['name']}","token":token}
