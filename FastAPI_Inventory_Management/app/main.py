from fastapi import FastAPI
import uvicorn
from auth import router 
from products import router1

app=FastAPI(title="Inventory Management API")


app.include_router(router)
app.include_router(router1)

if __name__=="__main__":\

    uvicorn.run("main:app",reload=True)