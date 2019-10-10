from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from populate_product_collection import SetupStore
import os
import hashlib

# instantialize mongo database and collections
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
products = db['products']
cart = db['cart']
reviews = db['reviews']

# setup the store. This populates the product database
st = SetupStore(products)
st.populate_products()

app = Flask(__name__)

@app.route("/")
def index():
    """Return main inventory page."""
    return render_template(
        "inventory_show.html",
        product_list=products.find(),
        cart_size=cart.count_documents({}))

@app.route("/store/socks")
def show_socks():
    """Show the sock inventory page."""
    socks = products.find({'product_type': 'sock'})
    return render_template(
        "socks_show.html",
        cart_size=cart.count_documents({}),
        product_list=socks)

@app.route("/store/shirts")
def show_shirts():
    """Show the shirt inventory page."""
    shirts = products.find({'product_type': 'shirt'})
    return render_template(
        "shirts_show.html",
        cart_size=cart.count_documents({}),
        product_list=shirts)

@app.route("/store/hoodies")
def show_hoodies():
    """Show the hoodie inventory page."""
    hoodies = products.find({'product_type': 'hoodie'})
    return render_template(
        "hoodies_show.html",
        cart_size=cart.count_documents({}),
        product_list=hoodies)

@app.route("/store/review", methods=['POST'])
def add_review():
    """Add reviews, gets variables from form."""
    # create review based on form that comes in
    review = {
        'product_id': request.form.get('product_id'),
        'name': request.form.get('name'),
        'content': request.form.get('content')
    }

    reviews.insert_one(review)
    return redirect(url_for("show_product", product_id=review['product_id']))

@app.route("/store/cart/checkout")
def checkout_cart():
    """Checkout the cart."""
    cart.delete_many({})
    return redirect(url_for("show_cart"))


@app.route("/store/<product_id>")
def show_product(product_id):
    """Show an individual product by the product_id that comes in with the route."""
    return render_template(
        "product_show.html",
        product=products.find_one({'_id': ObjectId(product_id)}),
        cart_size=cart.count_documents({}),
        reviews=reviews.find({'product_id': product_id}),
        num_of_reviews=reviews.find({'product_id': product_id}).count(),
        message=request.args.get("message"))

@app.route("/store/<product_id>", methods=['POST'])
def add_to_cart(product_id):
    """Add product to cart collection based on the product id being passed with the route."""
    # create product to add
    product_to_add = {
        'product_id': product_id,
        'name': products.find_one({'_id': ObjectId(product_id)})['name'],
        'pic_path': products.find_one({'_id': ObjectId(product_id)})['pic_path'],
        'price': products.find_one({'_id': ObjectId(product_id)})['price'],
        'reviews_id': products.find_one({'_id': ObjectId(product_id)})['reviews_id'],
        'description': products.find_one({'_id': ObjectId(product_id)})['description'],
        'inventory': products.find_one({'_id': ObjectId(product_id)})['inventory']
    }
    # subtract one from the product inventory size
    products.find_one_and_update({'_id': ObjectId(product_id)}, {'$inc': {'inventory': -1}})
    cart.insert_one(product_to_add)
    return redirect(url_for('show_product', product_id=product_id))

@app.route("/store/cart")
def show_cart():
    """Show cart inventory."""
    return render_template(
        "cart_show.html",
        product_list=cart.find(),
        cart_size=cart.count_documents({}))

@app.route("/store/cart/<product_id>", methods=['POST'])
def cart_item_delete(product_id):
    """Delete item from cart based on product id being passed with the route."""
    # add one to the product inventory size
    products.find_one_and_update({'_id': ObjectId(cart.find_one({'_id': ObjectId(product_id)})['product_id'])}, {'$inc': {'inventory': 1}})
    cart.delete_one({'_id': ObjectId(product_id)})
    return redirect(url_for("show_cart"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
