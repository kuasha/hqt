import ddbstore
from auth import authorize


@authorize
def route(event, context):
    resource = event["pathParameters"]["resource"]
    method = event["httpMethod"]

    body = None
    if method == "POST" or method == "PUT":
        body = event["body"]

    resource_parts = resource.split("/")
    resource_name = resource_parts[0]

    resource_id = None
    if method == "PUT" or method == "GET" or method == "DELETE":
        resource_id = resource_parts[1]

    if method == "POST":
        response = ddbstore.create_resource(resource_name, body)

    if method == "GET":
        response = ddbstore.load_resource(resource_name, resource_id)

    return response
