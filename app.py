from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


client = MongoClient()
db = client['contractor']
products = db['products']

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("inventory_show.html", products=products.find())


@app.route("/store/<product_id>")
def show_product(product_id):
    # print("Product: {}".format(products.find({'_id': product_id})))
    return render_template("product_show.html", product=products.find_one({'_id': ObjectId(product_id)}))


if __name__ == "__main__":
    app.run(debug=True)
