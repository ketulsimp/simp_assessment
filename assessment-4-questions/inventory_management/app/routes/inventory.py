from app.database.db import products,users
from app.schemas.schema import Product
from app.utils.jwt import verify_token
from fastapi import HTTPException,Depends,APIRouter
import json

products=APIRouter()

@products.post('/add-product')
async def add_product(product:Product,user:dict=Depends(verify_token)):
    query=await users.find_one({'name':user.name})
    if query['role']!='admin':
        raise HTTPException(status_code=400,detail='Not allowed. Only admin can ad products')
    await products.insert_one({
        'product_id':product.id,
        'product_name':product.product_name,
        'category':product.category,
        'price':product.price,
        'stock':product.stock
    })
    return {"message":'Product Added Successfully',"Product":"f{product.name}"}

@products.get('read-products',response_model=list[Product])
async def read_product(user=Depends(verify_token)):
    query=products.find()
    product_list=[]
    async for product in query:
        product['_id']=str(product["_id"])
        product_list.append(product)
    return product_list

@products.put('/update-product/{id}')
async def update_product(id:int,updated:Product,user=Depends(verify_token)):
    query=await products.find_one({"product_id":id})
    if not query:
        raise HTTPException(status_code=404,detail='Product not found')
    query2=await users.find_one({'name':user.name})
    if query2['role']!='admin':
        raise HTTPException(status_code=401,detail='Only admin can update products')
    result=await products.update_one({'product_id':id},updated.model_dump())
    if result.modified_count==0:
        raise HTTPException(status_code=404,detail='product not found')
    return ({"Message":"Product updated"})

@products.delete('/delete-product/{id}')
async def delete_product(id:int,updated:Product,user=Depends(verify_token)):
    query=await products.find_one({"product_id":id})
    if not query:
        raise HTTPException(status_code=404,detail='Product not found')
    query2=await users.find_one({'name':user.name})
    if query2['role']!='admin':
        raise HTTPException(status_code=401,detail='Only admin can update products')
    result=await products.delete_one({'product_id':id})
    if result.deleted_count==0:
        raise HTTPException(status_code=404,detail='product not found')
    return ({"Message":"Product deleted"})


# stock management
@products.post('/restock-products/{id}/{restock_amount}')
async def restock(id:int,restock_amount:int,user=Depends(verify_token)):
    query2=await users.find_one({'name':user.name})
    if query2['role']!='admin':
        raise HTTPException(status_code=401,detail='Only admin can restock products')
    query=await products.find_one({'product_id':id})
    if not query:
        raise HTTPException(status_code=404,detail='Product not found')
    
    result=await products.update_one({'product_id':id},{"$set":{'stock':{"$add":["$stock",restock_amount]}}})
    if result.modified_count==0:
        raise HTTPException(status_code=404,detail='product not found')
    with open ('movements.txt','w') as f:
        w=f.write(f"Product restocked {query['product_name']}:{query['stock']}")
        json.dump(w,f)
    return ({"Message":"Product restocked"})


@products.post('/sell-products/{id}/{sold_products}')
async def sell(id:int,sold_products:int,user=Depends(verify_token)):
    query2=await users.find_one({'name':user.name})
    if query2['role']!='admin':
        raise HTTPException(status_code=401,detail='Only admin can restock products')
    query=await products.find_one({'product_id':id})
    if not query:
        raise HTTPException(status_code=404,detail='Product not found')
    
    result=await products.update_one({'product_id':id},{"$set":{'stock':{"$subtract":["$stock",sold_products]}}})
    if result.modified_count==0:
        raise HTTPException(status_code=404,detail='product not found')
    return ({"Message":"Product sold"})


@products.post('/low-stock-products/{id}/')
async def low_stock(id:int,user=Depends(verify_token)):
    query2=await users.find_one({'name':user.name})
    if query2['role']!='admin':
        raise HTTPException(status_code=401,detail='Only admin can restock products')
    query=await products.find_one({'product_id':id})
    if not query:
        raise HTTPException(status_code=404,detail='Product not found')
    if query['stock']<=10:
        return ({"Message":"Product has low stock"})
    return {"message":'Plenty of stock  '}

#reports
@products.get('/inventory-value')
async def value(user=Depends(verify_token)):
    query=products.find()
    products_value={}
    async for p in query:
        products_value.update({p['category']:p['stock']*p['price']})
    
    return {"Products_value":f"{products_value}"}

@products.get('/stock-movements')
async def movements(user=Depends(verify_token)):
    with open ('movements.txt','r') as f:
        content=f.read()
        r=json.loads(content)
    return r