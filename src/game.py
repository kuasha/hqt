import config
import logging


def handle_get(id):
    pass


def handle_post(data):
    keys = data.keys()
    assert("id" in keys)
    assert("qset" in keys)
    assert(len(data["qset"]) <= config.MAX_QUESTIONS_PER_EPISODE)

    data["state"] = ""

    logging.ingo("Handler finished processing.")
