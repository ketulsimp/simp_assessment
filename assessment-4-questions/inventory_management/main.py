from fastapi import FastAPI
from app.routes.auth import auth
from app.routes.inventory import products

app=FastAPI(__name__)
app.add_api_route(auth)
app.add_api_route(products)



