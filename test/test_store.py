import unittest
import  store
from game import User

class StoreTest(unittest.TestCase):
    def test_load_user(self):
        user = store.load_user("1224")
        self.assertTrue(isinstance(user, User))

if __name__ == '__main__':
    unittest.main()

