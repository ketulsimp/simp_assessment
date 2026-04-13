from fastapi import APIRouter, Body, Depends, HTTPException, BackgroundTasks
from typing import Annotated
from app.models.product_model import Product
from app.conf.security import authenticate
from app.conf.db import get_db
from pymongo.database import Database
from app.logging import send_restock_logs, send_upstock_logs

product_rt = APIRouter(prefix='/products')

@product_rt.post('/')
async def create(product: Annotated[Product,Body()], user_info = Depends(authenticate), db = Depends(get_db)):
    if user_info.get('role') != 'admin':
        raise HTTPException(403,'Forbidden')
    await db['products'].insert_one(product.model_dump())
    
@product_rt.put('/{product_id}')
async def update(product_id: str, product: Annotated[Product,Body()], user_info = Depends(authenticate), db: Database = Depends(get_db)):
    if user_info.get('role') != 'admin':
        raise HTTPException(403,'Forbidden')
    await db['products'].find_one_and_replace({'_id':product_id},product.model_dump())
    
@product_rt.put('/{product_id}')
async def delete(product_id: str, product: Annotated[Product,Body()], user_info = Depends(authenticate), db: Database = Depends(get_db)):
    if user_info.get('role') != 'admin':
        raise HTTPException(403,'Forbidden')
    await db['products'].find_one_and_delete({'_id':product_id})
    
@product_rt.get('/')
async def get(user_info = Depends(authenticate), db: Database = Depends(get_db)):
    cursor = await db['products'].find({})
    products = []
    async for product in cursor:
        products.append(product)
    return products

@product_rt.put('/restock/{product_id}')
async def restock(background_tasks: BackgroundTasks, product_id: str, increase_by: int, user_info = Depends(authenticate), db: Database = Depends(get_db)):
    if user_info.get('role') != 'admin':
        raise HTTPException(403,'Forbidden')
    await db['products'].find_one_and_update({'_id':product_id}, {"$set" : {'stock': {"$inc":increase_by}}})
    background_tasks.add_task(send_restock_logs,product_id,increase_by)
    

@product_rt.put('/sell/{product_id}')
async def sell(background_tasks: BackgroundTasks, product_id: str, decrease_by: int, user_info = Depends(authenticate), db: Database = Depends(get_db)):
    if user_info.get('role') != 'admin':
        raise HTTPException(403,'Forbidden')
    await db['products'].find_one_and_update({'_id':product_id}, {"$set" : {'stock': {"$inc": -decrease_by}}})
    background_tasks.add_task(send_upstock_logs,product_id,decrease_by)
       
@product_rt.get('/low-stock/{threshold}')
async def get_low_stock(threshold:int,user_info = Depends(authenticate), db: Database = Depends(get_db)):
    cursor = await db['products'].aggregate([{"$sort": "$stock"},{"$limit":threshold}])
    products = []
    async for product in cursor:
        products.append(product)
    return products


@product_rt.get('/get-inventory-value')
async def get_inventory_value(user_info = Depends(authenticate), db: Database = Depends(get_db)):
    cursor = await db['products'].aggregate([{"$group": {'_id':'$category','totalSum': {'$sum': {'$multiply': ['$price','$stock']}}}}])
    products = []
    async for product in cursor:
        products.append(product)
    return products

@product_rt.get('/search')
async def search(name: str, category: str, page: int, user_info = Depends(authenticate), db: Database = Depends(get_db)):
    per_page = 5
    cursor = await db['products'].aggregate([{'$match': {'name':name, 'category':category}}, {'$sort': 'price'},{'$skip':page*per_page},{'$limit':per_page}])
    products = []
    async for product in products:
        products.append(product)
    return products