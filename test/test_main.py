import unittest
from unittest.mock import patch, Mock
import main

class MainTest(unittest.TestCase):
    def test_lambda_handler(self):
        mock = Mock()
        mock.return_value = "Hello, World!"
        with patch('router.route', mock) as mock1:
            msg = main.lambda_handler({},{})
            self.assertEqual(msg, 'Hello, World!')

if __name__ == '__main__':
    unittest.main()
