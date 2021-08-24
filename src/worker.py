import os
import json
import logging
import ddbstore
from episode import ACCPETING_REGISTRATION, ENDED, STARTED
import messaging
import config
import utils

EPISODE_WORKER_SQS_QUEUE_URL = os.environ["EpisodeWorkerSQSURL"]


def process(event, context):
    logging.warning(
        "No handler for worker.process. Event: {}".format(json.dumps(event)))


def episode_handler(event, context):
    # This handler only process the state of a single episode at a time (with 10 in a single batch)
    for r in event["Records"]:
        episode_id = r["body"]
        logging.info("Processing episode {}".format(episode_id))
        episode = ddbstore.load_resource(
            config.EPISODE_RESOURCE_NAME, episode_id)
        if not episode:
            logging.warn(
                "Could not load episode with id: {}".format(episode_id))
            continue
        cur_state = episode["state"]
        min_participant = episode["min_participant"]
        participant_count = episode["participant_count"]
        can_start = participant_count >= min_participant
        if not cur_state:
            ddbstore.update_episode_state(episode_id, ACCPETING_REGISTRATION)
        elif cur_state == ACCPETING_REGISTRATION and can_start:
            ddbstore.update_episode_state_qindex(episode_id, STARTED, 0)
        elif cur_state == STARTED:
            question_start_timestamp = int(episode["question_start_timestamp"])
            time_since_last_question = int(
                utils.get_time_delta_utc(question_start_timestamp))
            if time_since_last_question >= config.MIN_TIME_BETWEEN_QUESTIONS:
                new_state = cur_state
                current_question_index = int(episode["current_question_index"])
                qset = episode["qset"]
                next_qindex = current_question_index + 1
                if next_qindex >= len(qset):
                    new_state = ENDED
                ddbstore.update_episode_state_qindex(
                    episode_id, new_state, next_qindex)

        if cur_state == ENDED:
            logging.info("Episode has ended. Ending thde worker loop.")
        else:
            msg = episode_id
            messaging.send_message(
                EPISODE_WORKER_SQS_QUEUE_URL, msg, config.EPISODE_WORKER_MSG_DELAY)
