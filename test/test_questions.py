
import unittest
import questions


class QuestionsTest(unittest.TestCase):
    def test_get_next_question_set(self):
        qset = questions.get_next_question_set()
        self.assertEqual(len(qset), 12)
        for q in qset:
            self.assertIsNotNone(q.get_id())
            self.assertIsNotNone(q.get_defn())
            self.assertTrue(len(q.get_options()) == 3)
            options = q.get_options()
            for o in options:
                self.assertIsNotNone(o)
            self.assertTrue(q.get_answer() >= 0 and q.get_answer() <= 2)


if __name__ == '__main__':
    unittest.main()
