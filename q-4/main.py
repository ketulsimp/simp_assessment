from fastapi import FastAPI

from routes.routes import task_router


app = FastAPI()

app.include_router(task_router)