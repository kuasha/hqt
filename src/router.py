import json
import store
from auth import authorize

GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"


@authorize
def route(event, context):
    resource = event["pathParameters"]["resource"]  # let fail otherwise
    method = event["httpMethod"]

    body = None
    if method in [POST, PUT]:
        body = event["body"]

    resource_parts = resource.split("/")
    resource_name = resource_parts[0]

    resource_id = None
    if method in [GET, PUT, DELETE]:
        resource_id = resource_parts[1]

    if method == POST:
        item = json.loads(body)
        response = store.create_resource(resource_name, item)

    if method == GET:
        response = store.load_resource(resource_name, resource_id)

    return response
