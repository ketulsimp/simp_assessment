from fastapi import APIRouter, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth_utils import *
from typing import Annotated

auth_rt = APIRouter()

@auth_rt.post('/login')
async def login(form: Annotated[OAuth2PasswordRequestForm,Depends()]):
    if await authenticate_user(form):
        token = create_access_token(form.username)
        return {'access_token': token, 'type': 'Bearer'}

@auth_rt.post('/register')
async def register(username = Form(...), password = Form(...)):
    await store_user_in_mongo(username,password)