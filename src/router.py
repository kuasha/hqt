import json


def route(event, context):
    msg = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(event),
        "headers": {
            "content-type": "application/json"
        }
    }
    """
    path = event["requestContext"]["http"]["path"]
    method = event["requestContext"]["http"]["method"]
    body = event["body"]
    msg = {"path": path, "method": method, "body": body }
    """
    return msg
