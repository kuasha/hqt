import unittest
import  router

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
        expected_output = {'path': '/login', 'method': 'GET', 'body': 'test body'}
        result = router.route(event, None)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

