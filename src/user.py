class User:
    def __init__(self, **attributes):
        self.id = attributes["user_id"]

    def get_id(self):
        return self.id


class EpisodeUser(User):
    def __init__(self, **attributes):
        User.__init__(self, **attributes)
        self.eliminated = False
        self.answers = {}

    def set_eliminated(self):
        self.eliminated = True

    def is_eliminated(self):
        return self.eliminated
