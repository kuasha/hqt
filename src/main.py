import json
import logging
from exceptions import UnauthorizedException
import router
import response
import participant
from utils import CustomeEncoder
import worker


def lambda_handler(event, context):
    statusCode = 200
    body = ""
    try:
        response = router.route(event, context)
        body = json.dumps(response, cls=CustomeEncoder)
    except UnauthorizedException:
        statusCode = 401
        body = '{"error": "Unauthorized"}'
    # TODO: handle other exceptions

    msg = {
        "isBase64Encoded": False,
        "statusCode": statusCode,
        "body": body,
        "headers": {
            "content-type": "application/json"
        }
    }

    return msg


def response_handler(event, context):
    return response.process(event, context)


def participant_handler(event, context):
    return participant.process(event, context)


def worker_handler(event, context):
    return worker.process(event, context)


def episode_handler(event, context):
    return worker.episode_handler(event, context)
