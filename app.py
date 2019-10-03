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



if __name__ == "__main__":
    app.run(debug=True)
