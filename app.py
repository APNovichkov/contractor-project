from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from populate_product_collection import SetupStore
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
products = db['products']
cart = db['cart']

st = SetupStore(products)
st.populate_products()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "inventory_show.html",
        product_list=products.find(),
        cart_size=cart.count())

@app.route("/store/socks")
def show_socks():
    socks = products.find({'product_type': 'sock'})
    return render_template(
        "socks_show.html",
        cart_size=cart.count(),
        product_list=socks)

@app.route("/store/shirts")
def show_shirts():
    shirts = products.find({'product_type': 'shirt'})
    return render_template(
        "shirts_show.html",
        cart_size=cart.count(),
        product_list=shirts)

@app.route("/store/hoodies")
def show_hoodies():
    hoodies = products.find({'product_type': 'hoodie'})
    return render_template(
        "hoodies_show.html",
        cart_size=cart.count(),
        product_list=hoodies)


@app.route("/store/<product_id>")
def show_product(product_id):
    # print("Product: {}".format(products.find({'_id': product_id})))
    return render_template(
        "product_show.html",
        product=products.find_one({'_id': ObjectId(product_id)}),
        cart_size=cart.count(),
        message=request.args.get("message"))

@app.route("/store/<product_id>", methods=['POST'])
def add_to_cart(product_id):
    product_to_add = {
        'product_id': product_id,
        'name': products.find_one({'_id': ObjectId(product_id)})['name'],
        'pic_path': products.find_one({'_id': ObjectId(product_id)})['pic_path'],
        'price': products.find_one({'_id': ObjectId(product_id)})['price'],
        'reviews_id': products.find_one({'_id': ObjectId(product_id)})['reviews_id'],
        'description': products.find_one({'_id': ObjectId(product_id)})['description'],
        'inventory': products.find_one({'_id': ObjectId(product_id)})['inventory']
    }
    products.find_one_and_update({'_id': ObjectId(product_id)}, {'$inc': {'inventory': -1}})
    cart.insert_one(product_to_add)
    return redirect(url_for('show_product', product_id=product_id))

@app.route("/store/cart")
def show_cart():
    return render_template(
        "cart_show.html",
        product_list=cart.find(),
        cart_size=cart.count())

@app.route("/store/cart/<product_id>", methods=['POST'])
def cart_item_delete(product_id):
    products.find_one_and_update({'_id': ObjectId(cart.find_one({'_id': ObjectId(product_id)})['product_id'])}, {'$inc': {'inventory': 1}})
    cart.delete_one({'_id': ObjectId(product_id)})
    return redirect(url_for("show_cart"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
