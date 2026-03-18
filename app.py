from flask import Flask,request,render_template,redirect
from pymongo import MongoClient
from auth.routes import auth

app=Flask(__name__)

client=MongoClient("mongodb://localhost:27017/")
db=client["my_db"]
products=db["product"]

app.register_blueprint(auth)

@app.route("/")
def product():
    all_products=products.find()
    return render_template("index.html",products=all_products)

@app.route("/add",methods=["GET","POST"])
def get_product():
    if request.method=="POST":
        products.insert_one({
            "name":request.form["name"],
            "price":request.form["price"]
        })
        return redirect("/")
    return redirect("add_expense.html")

@app.route("/edit/<name",methods=["GET","POST"])
def update_product(name):

    product=products.find({"name":name})
    if request.method=="POST":
        new_name=request.form["name"]
        new_price=request.form["price"]

        products.update_one({"name":name},{"$set":{"name":new_name,"price":new_price}})
        return redirect("/")
    return render_template("edit_expense.html",product=product)

@app.route("/delete/<name>")
def delete_product(name):
    products.delete_one({"name":name})
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)