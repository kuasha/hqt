import logging
import json
import store
from exceptions import DuplicateRecordException, RecordNotFoundException
import config


def handle_get(id):
    pass


def handle_post(data):
    keys = data.keys()
    assert("episode_id" in keys)
    assert("user_id" in keys)

    episode_id = data["episode_id"]
    episode = store.load_resource(config.EPISODE_RESOURCE_NAME, episode_id)

    if episode is None:
        raise RecordNotFoundException("Episodes not found")

    user_id = data["user_id"]
    participant = store.load_participant(episode_id, user_id)
    if participant is not None:
        raise DuplicateRecordException(
            "User has already registered to the episode.")

    data["eliminated"] = False

    logging.info("Handler finished processing.")


def process(event, context):
    logging.warn(json.dumps(event))
    for r in event["Records"]:
        try:
            if r["eventName"] == "INSERT":
                raw_participant = r["dynamodb"]["NewImage"]
                participant = {
                    "episode_id": raw_participant["episode_id"]["S"],
                    "user_id": raw_participant["user_id"]["S"]
                }
                store.update_participant_statistics(participant)
            elif r["eventName"] == "MODIFY":
                raw_participant = r["dynamodb"]["NewImage"]
                eliminated = raw_participant["eliminated"]["BOOL"]
                if eliminated:  # TODO: make sure only one event comes
                    episode_id = raw_participant["episode_id"]["S"]
                    user_id = raw_participant["user_id"]["S"]
                    store.update_eliminated_statistics(episode_id, user_id)
        except KeyError:
            pass  # ignore malformed record for now (TODO)
