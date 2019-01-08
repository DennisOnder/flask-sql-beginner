from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initiailize DB
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    desc = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    
    def __init__(self, name, desc, price, qty):
        self.name = name
        self.desc = desc
        self.price = price
        self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'desc', 'qty')

# Initialize Schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(strict=True, many=True)

# Routes

# METHOD:   POST
# ACCESS:   PUBLIC
# DESC:     Create product
@app.route('/product', methods=['POST'])
def create_product():
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']
    new_product = Product(name, desc, price, qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

# METHOD:   GET
# ACCESS:   PUBLIC
# DESC:     Fetch products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

# METHOD:   GET
# ACCESS:   PUBLIC
# DESC:     Fetch single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# METHOD:   PUT
# ACCESS:   PUBLIC
# DESC:     Update product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']
    product.name = name
    product.desc = desc
    product.price = price
    product.qty = qty
    db.session.commit()
    return product_schema.jsonify(product)

# METHOD:   DELETE
# ACCESS:   PUBLIC
# DESC:     DELETE product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

# Run server
if __name__ == '__main__':
    app.run(debug=True)