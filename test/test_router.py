import unittest
import  router
import json


class RouterTest(unittest.TestCase):
    def test_router(self):
        event = {
            "requestContext": {
                "http": {
                    "path": "/login",
                    "method": "GET"
                }
            },
            "body": "test body"
        }

        expected_output = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "body": json.dumps(event),
            "headers": {
                "content-type": "application/json"
            }
        }
        result = router.route(event, None)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

