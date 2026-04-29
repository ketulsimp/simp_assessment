from fastapi import Depends,APIRouter,HTTPException
from schemas.schema import RegisterUser,LoginUser
from model.db_model import users
import bcrypt
from utils.jwt import create_access_token

auth=APIRouter(__name__)

@auth.post('/register')
async def register(user:RegisterUser):
    query=await users.find_one({'email':user['email']})
    if query:
        raise HTTPException(401,detail='User already exist')
    hashed=bcrypt.hashpw(user['password'],salt=bcrypt.gensalt())
    await users.insert_one({
        'name':user['name'],
        'email':user['email'],
        'password':hashed
    })
    return {"message":'User added successfully'}

@auth.post('/login')
async def login(user:LoginUser):
    query=await users.find_one({'email':user['email']})
    if not query:
        raise HTTPException(404,detail='user not found')
    
    check=bcrypt.checkpw(user['password'],query['password'])
    if not check:
        raise HTTPException(401,detail='Invalid password')
    
    token=create_access_token({'sub':user['email']})

    return {"Token":token}