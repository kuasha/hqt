import json
import logging


def worker_handler(event, context):
    logging.warning(
        "No handler for canary.worker_handler. Event: {}".format(json.dumps(event)))
    # TODO: implement API calls and attach to an alarm to notify on-call team on failure
