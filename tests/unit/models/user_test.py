from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test username', 'test password')

        self.assertEqual(user.username, 'test username',
                         "The username of the user after creation does not equal the constructor argument.")
        self.assertEqual(user.password, 'test password',
                         "The password of the user after creation does not equal the constructor argument.")
        self.assertIsNone(user.id)