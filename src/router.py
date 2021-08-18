import json

def route(event, context):
    path = event["requestContext"]["http"]["path"]
    method = event["requestContext"]["http"]["method"]
    body = event["body"]
    msg = {"path": path, "method": method, "body": body }
    return msg
