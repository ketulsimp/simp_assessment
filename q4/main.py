from fastapi import FastAPI
from routes.auth import auth
from routes.tasks import task

app=FastAPI()
app.router(auth)
app.router(task)