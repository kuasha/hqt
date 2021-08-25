import logging
from exceptions import UnauthorizedException


def is_authorized(token):
    logging.warning("TODO: Authorization is skipped.")
    return True


def authorize(func):
    def handler(event, context):
        headers = event["headers"]
        if "Authorization" not in headers.keys():
            raise UnauthorizedException("Authorization token missing")

        token = headers["Authorization"]

        if not is_authorized(token):
            raise UnauthorizedException("Authorization token invalid")

        # TODO: check user is authorized to perform this operation

        return func(event, context)
    return handler
