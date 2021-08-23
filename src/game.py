from episode import Episode
import config


class Game:
    def __init__(self, game_id, qset):
        self.game_id = game_id
        assert(len(qset) <= config.MAX_QUESTIONS_PER_EPISODE)
        self.qset = qset

    def create_new_episode(self):
        return Episode(self.game_id, self.qset)
