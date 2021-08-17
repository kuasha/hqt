import unittest
import  auth

class AuthTest(unittest.TestCase):
    def test_is_authorized(self):
        result = auth.is_authorized(None)
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()

