import unittest
from unittest.mock import patch, Mock
import router
import json


class RouterTest(unittest.TestCase):
    def test_router(self):
        event = {
            "httpMethod": "POST",
            "pathParameters": {
                "resource": "episode/123"
            },
            "body": "{}",
            "headers": {
                "Authorization": "test"
            }
        }

        expected_output = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "body": json.dumps(event),
            "headers": {
                "content-type": "application/json"
            }
        }

        mock = Mock()
        mock.return_value = expected_output
        with patch('store.create_resource', mock):
            result = router.route(event, None)
            self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
