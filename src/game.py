
class User:
    def __init__(self):
        pass

class EpisodeUser(User):
    def __init__(self):
        pass

class Question:
    def __init__(self):
        pass

class Episode:
    def __init__(self):
        pass

    def submit_answer(self, user, question, answer):
        pass

    def select_next_question(self):
        pass

    def add_user(self, user):
        pass

    def _eliminate_user(self, user):
        pass

class Game:
    def __init__(self):
        pass

    def create_new_episode(self):
        return Episode()
