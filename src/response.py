import store
import logging
import utils
import config

from exceptions import DuplicateRecordException, InvalidStateException, ResponseTimeoutException


def handle_get(data, id):
    pass


def handle_post(data):
    keys = data.keys()
    assert("episode_id" in keys)
    assert("user_id" in keys)
    assert("question_id" in keys)
    assert("answer" in keys)

    episode_id = data["episode_id"]
    user_id = data["user_id"]
    question_id = data["question_id"]
    answer = data["answer"]

    episode = store.load_resource("episode", episode_id)
    participant = store.load_participant(episode_id, user_id)
    question = store.load_resource("question", question_id)

    assert(episode is not None)
    assert(participant is not None)
    assert(question is not None)

    if participant["eliminated"]:
        raise InvalidStateException(
            "User has been eliminated from this episode.")

    current_question_index = int(episode["current_question_index"])
    assert(current_question_index >=
           0 and current_question_index < len(episode["qset"]))

    current_question_id = episode["qset"][current_question_index]

    if current_question_id != question_id:
        raise InvalidStateException(
            "The question is not from this round: {}".format(question_id))
    question_start_timestamp = float(episode["question_start_timestamp"])

    time_delta = utils.get_time_delta_utc(question_start_timestamp)

    if time_delta < 0:
        raise InvalidStateException(
            "Question start time is in future.")

    if time_delta > config.ANSWER_TIMEOUT:
        raise ResponseTimeoutException("Its too late for the response.")

    response = store.load_response(episode_id, user_id, question_id)
    if response:
        raise DuplicateRecordException(
            "User has already submitted response for this question")

    if question["answer"] != answer:
        store.eliminate_participant(participant)

    logging.info("Handler finished processing.")


def process(event, context):
    for r in event["Records"]:
        try:
            if r["eventName"] == "INSERT":
                raw_resp = r["dynamodb"]["NewImage"]
                resp = {
                    "episode_id": raw_resp["episode_id"]["S"],
                    "question_id": raw_resp["question_id"]["S"],
                    "user_id": raw_resp["user_id"]["S"],
                    "answer": raw_resp["answer"]["S"]
                }

                store.update_response_statistics(resp)
        except KeyError:
            pass  # ignore malformed record for now (TODO)
