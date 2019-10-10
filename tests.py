from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_sock_product_id = ObjectId('5d9bb31719787e7024bbc0e4')
sample_sock_product = {
    'product_type': 'sock',
    'name': 'Standard Hawaii Sock',
    'pic_path': "/static/standard_hawaii_sock.jpg",
    'price': 25,
    'reviews_id': 456,
    'description': "Your go-to sock when travelling to the tropics",
    'inventory': 50
}

sample_hoodie_product_id = ObjectId('5d9bb31719787e7024bbc0e7')
sample_hoodie_product = {
    'product_type': 'hoodie',
    'name': 'Feel Good Hood',
    'pic_path': "/static/feel_good_hood.jpg",
    'price': 70,
    'reviews_id': 277,
    'description': "Wearing this hoodie will put you in the mood to feel good",
    'inventory': 100
}

sample_shirt_product_id = ObjectId('5d9bb31719787e7024bbc0eb')
sample_shirt_product = {
    'product_type': 'shirt',
    'name': 'Bad Boys Shirt',
    'pic_path': "/static/bad_boys_shirt.jpg",
    'price': 10,
    'reviews_id': 111,
    'description': "You also know who you are.",
    'inventory': 30
}

sample_review_data = {
    'product_id': '5d9bad142b3bd88348718a10',
    'name': 'Andrey',
    'content': 'jalksjd'
}

class ContractorProjectTests(TestCase):

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_product(self, mock_find):
        mock_find.return_value = sample_sock_product

        result = self.client.get("/store/{}".format(sample_sock_product_id))
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Standard Hawaii Sock', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_inventory(self, mock_find):
        mock_find.return_value = [sample_sock_product, sample_hoodie_product, sample_shirt_product]

        result = self.client.get("/")
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Standard Hawaii Sock', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_socks(self, mock_find):
        mock_find.return_value = sample_sock_product

        result = self.client.get("/store/socks")
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Standard Hawaii Sock', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_hoodies(self, mock_find):
        mock_find.return_value = sample_hoodie_product

        result = self.client.get("/store/hoodies")
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Feel Good Hood', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_shirts(self, mock_find):
        mock_find.return_value = sample_shirt_product

        result = self.client.get("/store/shirts")
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Bad Boys Shirt', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_cart(self, mock_find):
        mock_find.return_value = sample_sock_product

        result = self.client.get("/store/cart")
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Standard Hawaii Sock', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_review(self, mock_insert):
        result = self.client.post("/store/review", data=sample_review_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_review_data)

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


if __name__ == '__main__':
    unittest_main()
