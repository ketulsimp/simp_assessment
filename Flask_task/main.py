from flask import Flask
from Flask_task.Blueprints.product import product_rt, db


app = Flask(__name__)


with app.app_context():
    db.create_all()

app.register_blueprint(product_rt)

@app.get('/')
def hello():
    return "Hello World"

@app.errorhandler(400)
def error():
    return "ERROR 400"

@app.errorhandler(404)
def error_another():
    return "ERROR 404"