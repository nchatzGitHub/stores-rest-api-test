from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, json.loads(response.data))

    def test_created_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 400)
                self.assertEqual({'message': "A store with name 'test' already exists."}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')  # We create a store
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 200)  # 200 is default status_code that everything is ok
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')  # We create a store
                response = client.delete('/store/test') # client requests GET,POST,DELETE,PUT,PATCH, OPTIONS

                self.assertEqual(response.status_code, 200)
                self.assertEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 404)
                self.assertEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')  # We create a store
                # We could have create store by writing : StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()  # We create an item with same id with store_id

                response = client.get('/store/test')


                self.assertEqual(response.status_code, 200)  # 200 is default status_code that everything is ok
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99, 'store_id': 1}]},
                                        json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')  # We create a store
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': []}]}, json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')  # We create a store
                ItemModel('test', 19.99, 1).save_to_db()  # We create an item with same id with store_id
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99, 'store_id': 1}]
                                              }]}, json.loads(response.data))
