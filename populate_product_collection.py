from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client['contractor']
products = db['products']

print("Clearing the products collection in contractor db...")
products.delete_many({})
print("Cleared the products collection in contractor db")


test_product_1 = {
    'product_type': 'sock',
    'name': 'Standard Hawaii Sock',
    'pic_id': 123,
    'price': 25,
    'reviews_id': 456,
    'description': "Your go to sock when travelling to the tropics",
    'inventory': 50
}

test_product_2 = {
    'product_type': 'sock',
    'name': 'Fruit Loop Sock',
    'pic_id': 234,
    'price': 30,
    'reviews_id': 113,
    'description': "For when you are feeling qwerky",
    'inventory': 10
}

test_product_3 = {
    'product_type': 'sock',
    'name': 'Coder Sock',
    'pic_id': 345,
    'price': 10,
    'reviews_id': 990,
    'description': "If you code, you need to wear this sock at all times",
    'inventory': 2
}

test_product_4 = {
    'product_type': 'hoodie',
    'name': 'Feel Good Hood',
    'pic_id': 784,
    'price': 70,
    'reviews_id': 277,
    'description': "Wearing this hoodie will put you in the mood to feel good",
    'inventory': 100
}

product_list = [test_product_1, test_product_2, test_product_3, test_product_4]

products.insert_many(product_list)

print("Inserted these products: ")
for product in products.find():
    print(product)
