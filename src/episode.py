import os
import logging
import json
from exceptions import DuplicateRecordException, InvalidStateException, ResponseTimeoutException
import config
import utils
import ddbstore
import messaging

EPISODE_WORKER_SQS_QUEUE_URL = os.environ["EpisodeWorkerSQSURL"]


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
    episode = ddbstore.load_resource(config.EPISODE_RESOURCE_NAME, episode_id)

    if episode is not None:
        raise DuplicateRecordException("Episodes can not be updated")

    qset = data["qset"]
    for qid in qset:
        item = {
            "episode_id": episode_id,
            "question_id": qid
        }

        for onum in range(config.MAX_OPTIONS_IN_A_QUESTION):
            field = utils.get_answer_fieldname(onum)
            item[field] = 0

        ddbstore.create_resource_inddb(
            config.RESPONSE_STAT_RESOURCE_NAME, item)

    data["current_question_index"] = ""
    data["question_start_timestamp"] = 0
    data["state"] = ""
    data["participant_count"] = 0
    data["eliminated_count"] = 0

    msg = episode_id
    messaging.send_message(EPISODE_WORKER_SQS_QUEUE_URL,
                           msg, config.EPISODE_WORKER_MSG_DELAY)
    logging.info("Handler finished processing.")


CREATED = "CREATED"
ACCPETING_REGISTRATION = "ACCPETING_REGISTRATION"
STARTED = "STARTED"
ENDED = "ENDED"


class EpisodeData:
    def __init__(self, id, game_id, qset, current_question_index, state):
        self.id = id
        self.game_id = game_id
        self.current_question_index = current_question_index
        self.qset = qset
        self.state = state
        self.question_start_time = 0

    def accept_users(self):
        self.state = ACCPETING_REGISTRATION

    def start(self):
        if self.state < STARTED:
            self.select_next_question()
            self.state = STARTED
        else:
            raise InvalidStateException("Episode is already started.")

    def get_current_question(self):
        if self.current_question_index >= 0:
            return self.qset[self.current_question_index]
        return None

    def end(self):
        if self.state >= STARTED:
            if self.current_question_index != len(self.qset)-1:
                raise InvalidStateException(
                    "Last question has not been reached yet.")
            self.state = ENDED
        else:
            raise InvalidStateException("Episode has not started.")

    def _is_running(self):
        return self.state == STARTED

    def time_since_started(self):
        if self.question_start_time < 1:
            return 0

        return utils.get_time_delta_utc(self.question_start_time)

    def validate_can_accpet_answer(self):
        if self.time_since_started() > config.ANSWER_TIMEOUT:
            raise ResponseTimeoutException()

    def select_next_question(self):
        if self.current_question_index >= len(self.qset):
            raise IndexError()

        if self.current_question_index >= 0:
            pq = self.qset[self.current_question_index]
            if pq.time_since_started() < config.MIN_TIME_BETWEEN_QUESTIONS:
                raise InvalidStateException(
                    "Too early to start a new question.")

        self.current_question_index += 1

        assert(self.current_question_index >= 0
               and self.current_question_index < len(self.qset))

        qid = self.qset[self.current_question_index]
        self.question_start_time = utils.get_time_delta_utc()
        return qid


class Episode:
    def __init__(self, id, store):
        self.id = id
        self.store = store

    def submit_answer(self, user_id, question_id, answer):
        if not self._is_running():
            raise InvalidStateException("Episode has not started yet.")

        cur_q = self.qset[self.current_question_index]

        if question_id != cur_q.get_id():
            raise InvalidStateException(
                "That question is not being accepted in this episode.")

        if user_id not in self.users:
            logging.warning("User is not registered to the episode.")
            raise InvalidStateException(
                "User is not registered to the episode.")

        user = self.users[user_id]

        if user.is_eliminated():
            raise InvalidStateException()

        cur_q.validate_can_accpet_answer()

        if question_id in user.answers:
            raise InvalidStateException()

        user.answers[question_id] = answer

        if cur_q.is_correct_answer(answer):
            pass
        else:
            self._eliminate_user(user_id)

    def register_user(self, user):
        user_id = user.get_id()
        self.store.create_episode_user(self.id, user_id)

    def get_user(self, user_id):
        return self.store.load_episode_users(self.id, user_id)

    def _eliminate_user(self, user):
        user.set_eliminated()
        self.store.update_episode_user(user)
