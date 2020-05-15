from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
from models.user import UserModel
import json


class TestItem(BaseTest):
    def setUp(self):
        super(TestItem, self).setUp() # We super the setUp method from BaseTest
        with self.app() as client:
            with self.app_context():
                # Below we see how we can do authorization if @jwt_required() for a method
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})

                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'price': 19.99, 'store_id': 1}, json.loads(response.data))

    def test_created_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 20.20, 1).save_to_db()
                response = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.put('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)
                self.assertIsNotNone(ItemModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'price': 19.99, 'store_id': 1}, json.loads(response.data))

    def test_put_item_update(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 20.22, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 20.22)

                response = client.put('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(ItemModel.find_by_name('test'))
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)
                self.assertDictEqual({'name': 'test', 'price': 19.99, 'store_id': 1}, json.loads(response.data))

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.get('/item/test', headers={'Authorization': self.access_token})
                # headers is for authorization. See setUp() method

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'test', 'price': 19.99, 'store_id': 1}, json.loads(response.data))

    def test_item_no_auth(self):
        with self.app() as client:
            response = client.get('/item/test')
            self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():

                response = client.get('/item/test', headers={'Authorization': self.access_token})
                # headers is for authorization. See setUp() method

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Item not found'}, json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 20.20, 1).save_to_db()
                response = client.delete('/item/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.get('/items')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'items': [{'name': 'test', 'price': 19.99, 'store_id': 1}]},
                                     json.loads(response.data))
