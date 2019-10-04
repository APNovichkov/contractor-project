from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


client = MongoClient()
db = client['contractor']
products = db['products']
cart = db['cart']

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "inventory_show.html",
        products=products.find(),
        cart_size=cart.count())


@app.route("/store/<product_id>")
def show_product(product_id):
    # print("Product: {}".format(products.find({'_id': product_id})))
    return render_template(
        "product_show.html",
        product=products.find_one({'_id': ObjectId(product_id)}),
        cart_size=cart.count())

@app.route("/store/<product_id>", methods=['POST'])
def add_to_cart(product_id):
    product_to_add = {
        'product_id': product_id,
        'name': products.find_one({'_id': ObjectId(product_id)})['name'],
        'pic_id': products.find_one({'_id': ObjectId(product_id)})['pic_id'],
        'price': products.find_one({'_id': ObjectId(product_id)})['price'],
        'reviews_id': products.find_one({'_id': ObjectId(product_id)})['reviews_id'],
        'description': products.find_one({'_id': ObjectId(product_id)})['description'],
        'inventory': products.find_one({'_id': ObjectId(product_id)})['inventory']
    }
    products.find_one_and_update({'_id': ObjectId(product_id)}, {'$inc': {'inventory': -1}})
    cart.insert_one(product_to_add)
    return redirect(url_for('index'))

@app.route("/store/cart")
def show_cart():
    return render_template(
        "cart_show.html",
        cart_items=cart.find(),
        cart_size=cart.count())

@app.route("/store/cart/<product_id>", methods=['POST'])
def cart_item_delete(product_id):
    products.find_one_and_update({'_id': ObjectId(cart.find_one({'_id': ObjectId(product_id)})['product_id'])}, {'$inc': {'inventory': 1}})
    cart.delete_one({'_id': ObjectId(product_id)})
    return redirect(url_for("show_cart"))


if __name__ == "__main__":
    app.run(debug=True)
