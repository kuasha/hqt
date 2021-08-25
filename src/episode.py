import logging
from exceptions import DuplicateRecordException
import config
import utils
import store
import messaging


CREATED = "CREATED"
ACCPETING_REGISTRATION = "ACCPETING_REGISTRATION"
STARTED = "STARTED"
ENDED = "ENDED"


def handle_get(id):
    pass


def handle_post(data):
    keys = data.keys()
    assert("id" in keys)
    assert("game_id" in keys)
    assert("qset" in keys)
    assert("min_participant" in keys)
    # TODO: other validations

    episode_id = data["id"]
    episode = store.load_resource(config.EPISODE_RESOURCE_NAME, episode_id)

    if episode is not None:
        raise DuplicateRecordException("Episodes can not be updated")

    qset = data["qset"]
    assert(len(qset) <= config.MAX_QUESTIONS_PER_EPISODE)
    for qid in qset:
        item = {
            "episode_id": episode_id,
            "question_id": qid
        }

        for onum in range(config.MAX_OPTIONS_IN_A_QUESTION):
            field = utils.get_answer_fieldname(onum)
            item[field] = 0

        store.create_raw_resource(
            config.RESPONSE_STAT_RESOURCE_NAME, item)

    data["current_question_index"] = int(-1)  # why? FIXME
    data["question_start_timestamp"] = int(0)
    data["state"] = ""
    data["participant_count"] = int(0)
    data["eliminated_count"] = int(0)

    msg = episode_id
    messaging.send_message(config.EPISODE_WORKER_SQS_QUEUE_NAME,
                           msg, config.EPISODE_WORKER_MSG_DELAY)
    logging.info("Handler finished processing.")
