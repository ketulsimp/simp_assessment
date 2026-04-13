from fastapi import APIRouter,HTTPException,Depends
from utils import decode_token
from Flask_Product_Management.app.database import product_collection
from schemas import CreateProduct,UpdateProduct
from fastapi.security import OAuth2PasswordBearer

router1=APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id


@router1.post("/products")
async def create_product(product:CreateProduct, user_id= Depends(get_current_user)):
    product_dict = product.model_dump()
    product_dict["created_by"] = user_id
    result = await product_collection.insert_one(product_dict)
    return {"message": "Product created successfully", "product_id": str(result.inserted_id)}   



@router1.get("/products/{product_id}")
async def read_product(product_id: str, user_id=Depends(get_current_user)):
    product = await product_collection.find_one({"_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router1.get("/products")
async def read_products(page: int = 1,limit:int=5, user_id=Depends(get_current_user)):
    skip=(page-1)*limit
    products = []
    async for product in product_collection.find().skip(skip).limit(limit):
        products.append(product)
    return products


@router1.put("/products/{product_id}")
async def update_product(product_id: str, product: UpdateProduct, user_id=Depends(get_current_user)):
    existing_product = await product_collection.find_one({"_id": product_id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found") 
    
    update_product= await product_collection.update_one({"_id": product_id},
                                                        {"$set": product.model_dump()}
                                                        )
    if update_product.modified_count == 0:
        raise HTTPException(status_code=400, detail="Product Updation Failed")
    
    return {"message": "Product updated successfully"}


@router1.delete("/products/{product_id}")
async def delete_product(product_id: str, user_id=Depends(get_current_user)):
    existing_product = await product_collection.find_one({"_id": product_id})

    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")    

    if delete_product.deleted_count == 0:
        raise HTTPException(status_code=400, detail="Product Deletion Failed")  
    return {"message": "Product deleted successfully"}


    

