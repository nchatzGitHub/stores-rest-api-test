from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test store')

        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            StoreModel(
                'test').save_to_db()  # We create an new Store(takes id=1) just because we create item with store_id=1.
            store = StoreModel('test store')

            self.assertIsNone(StoreModel.find_by_name('test store'),
                              "Found an store with name {}, but expected not to.".format(store.name))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test store'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test store'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')  # All test_stores will have id==1 because we delete database of stores
            item = ItemModel('test_item', 19.99, 1)  # every time we finish a test with tearDown method in base_test

            item.save_to_db()
            store.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json(self):
        store = StoreModel('test store')
        expected = {
            'id': None,
            'name': 'test store',
            'items': []
        }

        self.assertDictEqual(
            store.json(),
            expected,
            "The JSON export of the store is incorrect. Received {}, expected {}.".format(store.json(), expected))

    def test_store_json_mult_items_ruturn(self):
        with self.app_context():
            store = StoreModel('test store')  # All test_stores will have id==1 because we delete database of stores
            item = ItemModel('test_item', 19.99, 1)  # every time we finish a test with tearDown method in base_test

            item.save_to_db()
            store.save_to_db()

            expected = {
                'id': 1,
                'name': 'test store',
                'items': [{'name': 'test_item', 'price': 19.99, 'store_id': 1}]
            }

            self.assertDictEqual(
                store.json(),
                expected,
                "The JSON export of the store is incorrect. Received {}, expected {}.".format(store.json(), expected))
