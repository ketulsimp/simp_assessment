from flask import Blueprint, Request, jsonify
from flask_sqlalchemy import SQLAlchemy

product_rt = Blueprint('product',url_prefix='/product')
db = SQLAlchemy()

@product_rt.route('/',methods=["GET","POST"])
def main(request: Request):
    data = request.get_json()
    if request.method == "POST":
        db.session.execute(f"INSERT INTO PRODUCTS VALUES({data['name'],data['price'],data['stock']});")
    else:
        data = db.session.execute(f"SELECT * FROM PRODUCTS;")
        return jsonify(PendingDeprecationWarning)
    
@product_rt.route('/{id:str}',methods=["PUT"])
def update(id, request: Request):
    data = request.get_json()
    db.session.execute(f"UPDATE PRODUCTS SET price={data['price']} WHERE id={id};")
    
@product_rt.route('/{id:str}',methods=["DELETE"])
def delete(id, request: Request):
    data = request.get_json()
    db.session.execute(f"DELETE FROM PRODUCTS WHERE id={id};")
    