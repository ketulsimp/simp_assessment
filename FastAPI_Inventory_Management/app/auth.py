from fastapi import APIRouter,HTTPException
from passlib.context import CryptContext
from utils import create_token
from Flask_Product_Management.app.database import user_collection
from schemas import UserRegister,UserLogin
f


router=APIRouter()
pwd_context=CryptContext(schemes=["bcrypt"])

@router.post("/register")
async def register_user(user:UserRegister):
    existing_user=await user_collection.find_one({"username":user.username})
    if existing_user:
        raise HTTPException(status_code=400,detail="Username already exists")
    
    hashed_password=pwd_context.hash(user.password)
    users={
        "username":user.username,
        "password":hashed_password,
        "role":user.role
    }
    await user_collection.insert_one(users)
    return {"message":"User registered successfully"}

@router.post("/login")
async def login_user(user:UserLogin):
    user_db=await user_collection.find_one({"username":user.username})

    if not user_db or not pwd_context.verify(user.password,user_db["password"]):
        raise HTTPException(status_code=400,detail="Invalid username or password")
    
    token=create_token(user_db)
    return {
            "access_token":token
            }

