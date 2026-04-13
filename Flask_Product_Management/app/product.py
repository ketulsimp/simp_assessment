from flask import Flask
from database import mysql_cursor

app=Flask(__name__)

#Create product
@app.route('/products')
def create_product():
    mysql_cursor.execute("SELECT * FROM products")
    products = mysql_cursor.fetchall()
    return str(products)

#Get One Product
@app.route('/products/<int:product_id>')
def get_product(product_id):
    mysql_cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = mysql_cursor.fetchone()
    if product:
        return str(product)
    else:
        return "Product not found", 404 
    
#Update Product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    mysql_cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = mysql_cursor.fetchone()
    if product:
        # Update the product details here
        return "Product updated successfully"
    else:
        return "Product not found", 404
    
#Delete Product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id): 
    mysql_cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = mysql_cursor.fetchone()
    if product:
        return "Product deleted successfully"
    else:
        return "Product not found", 404
    

@app.errorhandler(404)
def not_found(error):
    return "page Not Found"

@app.errorhandler(400)
def bad_request(error):
    return "Bad Request"


if __name__ == '__main__':
    app.run(debug=True)