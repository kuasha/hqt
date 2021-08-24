from episode import Episode
import config
import logging


def handle_get(id):
    pass


def handle_post(data):
    keys = data.keys()
    assert("id" in keys)
    assert("qset" in keys)

    data["state"] = ""

    logging.ingo("Handler finished processing.")


class Game:
    def __init__(self, game_id, qset):
        self.game_id = game_id
        assert(len(qset) <= config.MAX_QUESTIONS_PER_EPISODE)
        self.qset = qset

    def create_new_episode(self):
        return Episode(self.game_id, self.qset)
