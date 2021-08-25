import unittest
from unittest.mock import patch, Mock
import main


class MainTest(unittest.TestCase):
    def test_lambda_handler(self):
        expected = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "body": '"Hello, World!"',
            "headers": {"content-type": "application/json"}
        }
        mock = Mock()
        mock.return_value = "Hello, World!"
        with patch('router.route', mock):
            msg = main.lambda_handler({}, {})
            self.assertEqual(msg, expected)

    def test_lambda_handler_unauthorized_returns_401(self):
        pass


if __name__ == '__main__':
    unittest.main()
