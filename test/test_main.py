import unittest
import main

class MainTest(unittest.TestCase):
    def test_lambda_handler(self):
        msg = main.lambda_handler({},{})
        self.assertEqual(msg["message"], 'Hello, World!')

if __name__ == '__main__':
    unittest.main()
