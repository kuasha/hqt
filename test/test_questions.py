
import unittest
import questions


class QuestionsTest(unittest.TestCase):
    def test_get_next_question_set(self):
        qset = questions.get_next_question_set()
        self.assertEqual(len(qset), 12)
        for q in qset:
            self.assertIsNotNone(q["id"])
            self.assertIsNotNone(q["question"])
            self.assertTrue(len(q["options"]) == 3)
            for o in q["options"]:
                self.assertIsNotNone(o)
            self.assertTrue(q["answer"] >= 0 and q["answer"] <= 2)


if __name__ == '__main__':
    unittest.main()
