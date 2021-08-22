import unittest
from unittest.mock import patch, Mock
import game

class MainTest(unittest.TestCase):
    def test_register_user_to_episode(self):
        pass

    def test_register_user_to_episode_already_registered(self):
        pass

    def test_eliminate_user_from_episode(self):
        pass

    def test_eliminate_user_from_episode_already_eliminated(self):
        pass

    def test_eliminate_user_from_episode_user_not_registered(self):
        pass

    def test_submit_answer_valid_case(self):
        pass

    def test_submit_answer_invalid_timeout(self):
        pass

    def test_submit_answer_invalid_game_ended(self):
        pass

    def test_submit_answer_invalid_wrong_episode(self):
        pass

    def test_submit_answer_invalid_user_not_registered(self):
        pass

    def test_create_new_episode_valid_case(self):
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
        pass

    def test_end_episode(self):
        pass

    def test_end_episode_invalid_wrong_id(self):
        pass

    def test_end_episode_invalid_wrong_state(self):
        pass

    def test_get_episode_statistics(self):
        pass

if __name__ == '__main__':
    unittest.main()
