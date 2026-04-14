from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.conf.db import get_db
from app.models.auth_model import Register, Login
from typing import Annotated
from app.utils.auth_utils import generate_access_token, hash_password, check_password
from datetime import timedelta

auth_rt = APIRouter(
    prefix='/auth',
    tags=['auth']
)

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

@auth_rt.post('/register')
async def register(user_data: Annotated[Register,Form()], db = Depends(get_db)):
    hashed_password = hash_password(user_data.password.get_secret_value())
    await db['users'].insert_one({'username':user_data.username, 'password': hashed_password, 'role': user_data.get('role')})
    
@auth_rt.post('/login')
async def login(user_credentials: Annotated[OAuth2PasswordRequestForm,Depends()], db = Depends(get_db)):
    user_info = await db['users'].find_one({'username': user_credentials.username})
    if user_info is not None and check_password(user_credentials.password,user_info.get('password')):
        print('Login Successfull.')
        access_token = generate_access_token({'sub': user_info.get('username'), 'exp': timedelta(minutes=5),'role': user_info.get('role')})
        return {'access_token': access_token, 'token_type': 'bearer'}
    
