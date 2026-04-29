from fastapi import APIRouter,HTTPException
from app.auth import hash_password,verify_password,create_token
from app.database import user_collection
from app.schemas import UserCreate,UserLogin


auth_route=APIRouter(prefix="/auth_route")

@auth_route.post("/register")
async def register(user:UserCreate):
    existing_user=await user_collection.find_one({"user":user.username})
    if existing_user:
        raise HTTPException(status_code=401,detail="User Already Exists")
    
    user.password=hash_password(user.password)
    user=await user_collection.insert_one(user)
    return {"message":"User Created Successfully"}

@auth_route.login("/login")
async def login(user:UserLogin):
    db_user=await user_collection.find_one({"user":user.username})

    if not db_user and not verify_password(user.password,db_user["password"]):
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    
    token=create_token({"sub":user.username})
    return{"access_token":token,"token_type":"Bearer"}

