from sqlalchemy import create_engine,Column,Table,INTEGER,DECIMAL,VARCHAR,MetaData,DATETIME

engine=create_engine("mysql+pymysql://root:Ashish%40123@localhost/assessment")
meta=MetaData

products=Table('products',meta,
    Column('product_id',INTEGER,primary_key=True,autoincrement=True),
    Column('name',VARCHAR(30)), 
    Column('price',DECIMAL),
    Column('stock',DECIMAL),
    Column('created_at',DATETIME)
)

meta.create_all(engine)
connection=engine.connect()