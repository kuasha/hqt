import logging
from exceptions import InvalidStateException
import config

CREATED = 0
ACCPETING_REGISTRATION = 10
STARTED = 100
ENDED = 1000


class Episode:
    def __init__(self, game_id, qset):
        self.users = {}
        self.game_id = game_id
        self.current_question_index = -1
        # copy the questions so that change does not effect started episode
        self.qset = qset.copy()
        self.state = CREATED

    def accept_users(self):
        self.state = ACCPETING_REGISTRATION

    def start(self):
        if self.state < STARTED:
            self.select_next_question()
            self.state = STARTED
        else:
            raise InvalidStateException("Episode is already started.")

    def end(self):
        if self.state >= STARTED:
            self.state = ENDED
        else:
            raise InvalidStateException("Episode has not started.")

    def _is_running(self):
        return self.state == STARTED

    def submit_answer(self, user_id, question_id, answer):
        if not self._is_running():
            raise InvalidStateException("Episode has not started yet.")

        cur_q = self.qset[self.current_question_index]

        if question_id != cur_q.get_id():
            raise InvalidStateException("That question is not being accepted in this episode.")

        if user_id not in self.users:
            logging.warning("User is not registered to the episode.")
            raise InvalidStateException("User is not registered to the episode.")

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

    def select_next_question(self):
        if self.current_question_index >= len(self.qset):
            raise IndexError()

        if self.current_question_index >= 0:
            pq = self.qset[self.current_question_index]
            if pq.time_since_started() < config.MIN_TIME_BETWEEN_QUESTIONS:
                raise InvalidStateException("Too early to start a new question.")

        self.current_question_index += 1

        assert(self.current_question_index >= 0
               and self.current_question_index < len(self.qset))

        q = self.qset[self.current_question_index]
        q.set_start_time()

    def get_current_question(self):
        if self.current_question_index >= 0:
            return self.qset[self.current_question_index]
        return None

    def register_user(self, user):
        user_id = user.get_id()
        if user_id in self.users:
            logging.warning("User {} is already registered".format(user_id))
            return
        else:
            self.users[user_id] = user

    def get_users(self):
        # WARNING: caller will be able to modify this
        return self.users

    def get_user(self, user_id):
        if user_id in self.users:
            return self.users[user_id]

        return None

    def _eliminate_user(self, user_id):
        user = self.users[user_id]
        user.set_eliminated()
