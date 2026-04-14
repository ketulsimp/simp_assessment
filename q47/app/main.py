from fastapi import FastAPI
from app.routes import auth_rt,product_rt

app = FastAPI()

app.include_router(product_rt)
app.include_router(auth_rt)

@app.get('/')
async def hello():
    return "Greeting to the front page.."