from pymongo import MongoClient
from bson.objectid import ObjectId

test_product_1 = {
    'product_type': 'sock',
    'name': 'Standard Hawaii Sock',
    'pic_path': "/static/standard_hawaii_sock.jpg",
    'price': 25,
    'reviews_id': 456,
    'description': "Your go-to sock when travelling to the tropics",
    'inventory': 50
}

test_product_2 = {
    'product_type': 'sock',
    'name': 'Fruit Loop Sock',
    'pic_path': "/static/fruit_loop_sock.jpg",
    'price': 30,
    'reviews_id': 113,
    'description': "For when you are feeling qwerky",
    'inventory': 10
}

test_product_3 = {
    'product_type': 'sock',
    'name': 'Coder Sock',
    'pic_path': "/static/coder_sock.jpg",
    'price': 10,
    'reviews_id': 990,
    'description': "If you code, you need to wear this sock at all times",
    'inventory': 2
}

test_product_4 = {
    'product_type': 'hoodie',
    'name': 'Feel Good Hood',
    'pic_path': "/static/feel_good_hood.jpg",
    'price': 70,
    'reviews_id': 277,
    'description': "Wearing this hoodie will put you in the mood to feel good",
    'inventory': 100
}

test_product_5 = {
    'product_type': 'hoodie',
    'name': 'Spooky Hoodie',
    'pic_path': "/static/spooky_hoodie.jpg",
    'price': 100,
    'reviews_id': 132,
    'description': "Its spooky szn. Period.",
    'inventory': 20
}

test_product_6 = {
    'product_type': 'hoodie',
    'name': 'Moody Hoodie',
    'pic_path': "/static/moody_hoodie.jpg",
    'price': 20,
    'reviews_id': 901,
    'description': "For the rainy days",
    'inventory': 40
}

test_product_7 = {
    'product_type': 'shirt',
    'name': 'Three Comma Club Shirt',
    'pic_path': "/static/three_comma_club_shirt.jpg",
    'price': 1000000000,
    'reviews_id': 111,
    'description': "You know who you are. ",
    'inventory': 1
}

test_product_8 = {
    'product_type': 'shirt',
    'name': 'Bad Boys Shirt',
    'pic_path': "/static/bad_boys_shirt.jpg",
    'price': 10,
    'reviews_id': 111,
    'description': "You also know who you are.",
    'inventory': 30
}

test_product_9 = {
    'product_type': 'shirt',
    'name': 'Semicolon Shirt',
    'pic_path': "/static/semicolon_shirt.jpg",
    'price': 40,
    'reviews_id': 444,
    'description': "Period plus a comma, what else could you want?",
    'inventory': 40
}

product_list = [
    test_product_1,
    test_product_2,
    test_product_3,
    test_product_4,
    test_product_5,
    test_product_6,
    test_product_7,
    test_product_8,
    test_product_9]

class SetupStore():
    def __init__(self, products, cart):
        self.products = products
        self.cart = cart

    def populate_products(self):
        print("Clearing the products collection in contractor db...")
        self.products.delete_many({})
        print("Cleared the products collection in contractor db")

        print("Clearing the cart collection in contractor db...")
        self.cart.delete_many({})
        print("Cleared the cart collection in contractor db")

        self.products.insert_many(product_list)
        print("Inserted these products: ")
        for product in self.products.find():
            print(product)

    def setup_store(self):
        print("Clearing session collection in contractor DB...")
        self.session.delete_many({})
        print("cleared the session collection in contractor DB")
