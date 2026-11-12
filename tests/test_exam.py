import unittest
from datetime import date

from aae.exam import grade


QUESTIONS = [
    {
        "id": "q1",
        "type": "mcq",
        "prompt": "?",
        "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
        "answer": "B",
        "explanation": "b",
    },
    {
        "id": "q2",
        "type": "mcq",
        "prompt": "?",
        "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
        "answer": "C",
        "explanation": "c",
    },
    {
        "id": "q3",
        "type": "mcq",
        "prompt": "?",
        "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
        "answer": "A",
        "explanation": "a",
    },
    {
        "id": "q4",
        "type": "mcq",
        "prompt": "?",
        "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
        "answer": "D",
        "explanation": "d",
    },
    {
        "id": "q5",
        "type": "mcq",
        "prompt": "?",
        "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
        "answer": "B",
        "explanation": "b",
    },
    {
        "id": "q6",
        "type": "open",
        "prompt": "leg uit",
        "key_points": ["p1", "p2", "p3", "p4"],
        "model_answer": "model",
    },
]


def answers_all_correct():
    return {q["id"]: q["answer"] for q in QUESTIONS if q["type"] == "mcq"}


class ExamTest(unittest.TestCase):
    def test_perfect(self):
        result = grade(QUESTIONS, answers_all_correct(), {"q6": 4})
        self.assertEqual(result.score, 100.0)
        self.assertTrue(result.passed)
        self.assertEqual(result.mcq_correct, 5)

    def test_one_mcq_wrong_is_85(self):
        answers = answers_all_correct()
        answers["q1"] = "A"
        result = grade(QUESTIONS, answers, {"q6": 4})
        self.assertEqual(result.score, 85.0)
        self.assertTrue(result.passed)

    def test_two_wrong_fails(self):
        answers = answers_all_correct()
        answers["q1"] = "A"
        answers["q2"] = "A"
        result = grade(QUESTIONS, answers, {"q6": 4})
        self.assertEqual(result.score, 70.0)
        self.assertFalse(result.passed)

    def test_open_partial(self):
        result = grade(QUESTIONS, answers_all_correct(), {"q6": 2})
        self.assertEqual(result.score, 87.5)
        self.assertTrue(result.passed)

    def test_case_insensitive(self):
        answers = {k: v.lower() for k, v in answers_all_correct().items()}
        result = grade(QUESTIONS, answers, {"q6": 0})
        self.assertEqual(result.mcq_correct, 5)
        self.assertEqual(result.score, 75.0)

    def test_requires_both_types(self):
        with self.assertRaises(ValueError):
            grade([QUESTIONS[0]], {"q1": "B"}, {})


if __name__ == "__main__":
    unittest.main()
