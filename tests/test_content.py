import unittest

from aae import content


class ContentTest(unittest.TestCase):
    def test_curriculum_is_valid(self):
        errors = content.validate()
        self.assertEqual(errors, [], "\n".join(errors))

    def test_all_weeks_present(self):
        weeks = content.load_all()
        self.assertEqual(len(weeks), 24)
        self.assertEqual([w.week for w in weeks], list(range(1, 25)))
        self.assertEqual({w.phase for w in weeks}, {1, 2, 3, 4, 5})

    def test_question_and_card_counts(self):
        weeks = content.load_all()
        questions = [q for w in weeks for q in w.exam["questions"]]
        mcq = [q for q in questions if q["type"] == "mcq"]
        open_q = [q for q in questions if q["type"] == "open"]
        self.assertEqual(len(mcq), 120)
        self.assertEqual(len(open_q), 24)
        self.assertEqual(sum(len(w.cards) for w in weeks), 120)

    def test_ids_unique(self):
        weeks = content.load_all()
        ids = [q["id"] for w in weeks for q in w.exam["questions"]]
        ids += [c["id"] for w in weeks for c in w.cards]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_week_has_a_gate(self):
        for week in content.load_all():
            self.assertGreaterEqual(week.pass_score, 85)
            self.assertTrue(week.challenge.get("verify"))


if __name__ == "__main__":
    unittest.main()
