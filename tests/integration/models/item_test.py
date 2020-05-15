from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel(
                'test').save_to_db()  # We create an new Store(takes id=1) just because we create item with store_id=1.
            item = ItemModel('test', 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')  # All test_stores will have id==1 because we delete database of stores
            item = ItemModel('test', 19.99, 1)  # every time we finish a test with tearDown method in base_test

            item.save_to_db()
            store.save_to_db()

            self.assertEqual(item.store_id, store.id)
            self.assertEqual(item.store.name, 'test_store')
