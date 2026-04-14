from flask import url_for,render_template,redirect,Blueprint,request
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from app.database.db import connection,products
from datetime import datetime,timezone

product=Blueprint(__name__)

class Product(FlaskForm):
    product_id:IntegerField
    product_name:StringField
    price:IntegerField
    stock:IntegerField

@product.route('/add-product',methods=['POST','GET'])
def add_product():
    form=Product()
    if product.validate_on_submit():
        product_id=form.product_id.data
        name=form.product_name.data
        price=form.price.data
        stock=form.stock.data
        created_at=datetime.now(timezone.utc)
        connection.execute(products.insert().values(product_id=product_id,name=name,price=price,stock=stock,created_at=created_at))
        return {"message":'Product added'}
    return render_template('products')

