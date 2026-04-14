from sqlalchemy import Integer, String, Column

class Product:
    id = Column('id', type_=Integer,primary_key=True)
    name = Column('name',type_=String)
    price = Column('id', type_=Integer,primary_key=True)