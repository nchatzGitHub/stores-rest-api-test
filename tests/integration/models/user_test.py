from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'abcd')

            self.assertIsNone(UserModel.find_by_username('test'),
                              "Found a user with username {}, but expected not to.".format(user.username))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('test'))
            self.assertIsNotNone(UserModel.find_by_id(1))

            user.delete_from_db()

            self.assertIsNone(UserModel.find_by_username('test'))
            self.assertIsNone(UserModel.find_by_id(1))

# We don't need to write tests for find_by_username or find_by_id methods,
# because we already test them above that they work properly
