import unittest
from unittest.mock import patch, Mock
from game import Game
from user import EpisodeUser
from episode import Episode, ENDED
import questions
import config
import exceptions


class MainTest(unittest.TestCase):
    def test_register_user_to_episode(self):
        episode1 = Episode("12312312", {})
        user1 = EpisodeUser(user_id="1234567")
        user2 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        got_users = episode1.get_users()
        self.assertTrue(len(got_users.keys()) == 1)
        episode1.register_user(user2)
        got_users = episode1.get_users()
        self.assertTrue(len(got_users.keys()) == 2)
        # test for already registered
        episode1.register_user(user1)
        got_users = episode1.get_users()
        self.assertTrue(len(got_users.keys()) == 2)

    def test_eliminate_user_from_episode(self):
        episode1 = Episode("12312312", {})
        user1 = EpisodeUser(user_id="1234567")
        user2 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        episode1.register_user(user2)
        episode1._eliminate_user(user1.get_id())
        got_users = episode1.get_users()
        self.assertTrue(len(got_users.keys()) == 2)

        self.assertTrue(got_users[user1.get_id()].is_eliminated())

    def test_eliminate_user_from_episode_already_eliminated(self):
        episode1 = Episode("12312312", {})
        user1 = EpisodeUser(user_id="1234567")
        user2 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        episode1.register_user(user2)
        episode1._eliminate_user(user1.get_id())
        episode1._eliminate_user(user1.get_id())
        episode1._eliminate_user(user2.get_id())
        got_users = episode1.get_users()
        self.assertTrue(len(got_users.keys()) == 2)

        self.assertTrue(got_users[user1.get_id()].is_eliminated())
        self.assertTrue(got_users[user2.get_id()].is_eliminated())

    def test_eliminate_user_from_episode_user_not_registered(self):
        episode1 = Episode("12312312", {})
        user1 = EpisodeUser(user_id="1234567")
        user2 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        episode1.register_user(user2)
        try:
            episode1._eliminate_user("674373")
            self.fail("Expecting exception")
        except KeyError:
            pass

        got_users = episode1.get_users()
        self.assertTrue(len(got_users.keys()) == 2)

        self.assertFalse(got_users[user1.get_id()].is_eliminated())
        self.assertFalse(got_users[user2.get_id()].is_eliminated())

    def test_new_game_episode(self):
        game_id = "1216326432"
        qset = questions.get_next_question_set()
        game = Game(game_id, qset)
        episode1 = game.create_new_episode()
        self.assertTrue(isinstance(episode1, Episode))

        episode1.select_next_question()
        q = episode1.get_current_question()
        self.assertTrue(q.get_id() == qset[0].get_id())

    def test_submit_answer_valid_case(self):
        game_id = "1216326432"
        qset = questions.get_next_question_set()
        game = Game(game_id, qset)
        episode1 = game.create_new_episode()

        user1 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        episode1.start()
        q = episode1.get_current_question()
        episode1.submit_answer(user1.get_id(), q.get_id(), 0)

    def test_submit_answer_invalid_timeout(self):
        game_id = "1216326432"
        qset = questions.get_next_question_set()
        game = Game(game_id, qset)
        episode1 = game.create_new_episode()

        user1 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        episode1.start()
        q = episode1.get_current_question()
        mock = Mock()
        mock.return_value = config.MAX_QUESTIONS_PER_EPISODE + 1
        with patch('utils.get_time_delta_utc', mock):
            with self.assertRaises(exceptions.ResponseTimeoutException):
                episode1.submit_answer(user1.get_id(), q.get_id(), 0)

    def test_submit_answer_invalid_game_ended(self):
        game_id = "1216326432"
        qset = questions.get_next_question_set()
        game = Game(game_id, qset)
        episode1 = game.create_new_episode()

        user1 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        episode1.start()
        q = episode1.get_current_question()
        episode1.end()
        with self.assertRaises(exceptions.InvalidStateException):
            episode1.submit_answer(user1.get_id(), q.get_id(), 0)

    def test_submit_answer_invalid_episode_not_started(self):
        game_id = "1216326432"
        qset = questions.get_next_question_set()
        game = Game(game_id, qset)
        episode1 = game.create_new_episode()
        episode_wrong = game.create_new_episode()

        user1 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        episode1.start()
        q = episode1.get_current_question()
        with self.assertRaises(exceptions.InvalidStateException) as context:
            episode_wrong.submit_answer(user1.get_id(), q.get_id(), 0)
        self.assertEqual("Episode has not started yet.",
                         str(context.exception))

    def test_submit_answer_invalid_user_not_registered(self):
        # make sure that users are registered in only one episode1
        game_id = "1216326432"
        qset = questions.get_next_question_set()
        game = Game(game_id, qset)
        episode1 = game.create_new_episode()
        episode_wrong = game.create_new_episode()

        user1 = EpisodeUser(user_id="1234568")
        episode_wrong.register_user(user1)
        episode1.start()
        q = episode1.get_current_question()
        with self.assertRaises(exceptions.InvalidStateException) as context:
            episode1.submit_answer(user1.get_id(), q.get_id(), 0)
        self.assertEqual(
            "User is not registered to the episode.", str(context.exception))

    def test_create_new_episode_valid_case(self):
        # episode1 starts after N users automatically
        pass

    def test_create_new_episode_invalid_wrong_game_id(self):
        pass

    def test_create_new_episode_invalid_invalid_game(self):
        pass

    def test_start_episode_valid_case(self):
        pass

    def test_start_episode_invalid_episode_id(self):
        pass

    def test_start_episode_invalid_wrong_state(self):
        pass

    def test_select_next_question(self):
        pass

    def test_select_next_question_invalid_episode_not_started(self):
        pass

    def test_select_next_question_invalid_before_time(self):
        game_id = "1216326432"
        qset = questions.get_next_question_set()
        game = Game(game_id, qset)
        episode1 = game.create_new_episode()

        user1 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        episode1.start()
        mock = Mock()
        mock.return_value = config.MIN_TIME_BETWEEN_QUESTIONS - 1
        with patch('utils.get_time_delta_utc', mock):
            with self.assertRaises(exceptions.InvalidStateException):
                episode1.select_next_question()

    def test_end_episode(self):
        game_id = "1216326432"
        qset = questions.get_next_question_set()
        game = Game(game_id, qset)
        episode1 = game.create_new_episode()

        user1 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        episode1.start()
        episode1.end()
        self.assertEqual(episode1.state, ENDED)

    def test_end_episode_invalid_wrong_id(self):
        pass

    def test_end_episode_invalid_wrong_state(self):
        game_id = "1216326432"
        qset = questions.get_next_question_set()
        game = Game(game_id, qset)
        episode1 = game.create_new_episode()

        user1 = EpisodeUser(user_id="1234568")
        episode1.register_user(user1)
        with self.assertRaises(exceptions.InvalidStateException):
            episode1.end()

    def test_get_episode_statistics(self):
        pass


if __name__ == '__main__':
    unittest.main()
