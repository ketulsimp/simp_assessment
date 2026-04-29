from fastapi import FastAPI
from app.config.db import connect, disconnect
from contextlib import asynccontextmanager
from app.routes import auth_rt, task_rt

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield
    await disconnect()
    
app = FastAPI(lifespan=lifespan)
app.include_router(auth_rt)
app.include_router(task_rt)