import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from aae import db, gate
from aae.content import Week


def make_week(number=1, cards=2):
    return Week(
        week=number,
        phase=1,
        title="Testweek",
        outcome="Testen",
        reading=[{"book": "x", "ref": "x", "chapters": "1", "pages": "1-2"}],
        build={"goal": "g", "deliverable": "d"},
        challenge={"brief": "b", "acceptance": ["a"]},
        exam={"pass_score": 85, "questions": []},
        cards=[{"id": f"w{number}c{i}", "front": "f", "back": "b", "source": "s"} for i in range(cards)],
    )


class GateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.progress = db.connect(Path(self.tmp.name))
        self.week = make_week()
        today = date.today()
        for i in range(5):
            db.log_session(self.progress, 60, "studie", today - timedelta(days=i))
        for i in range(3):
            db.add_evidence(self.progress, 1, "commit", f"sha{i}")
        db.record_exam(self.progress, 1, 90.0, True, {})
        db.record_challenge(self.progress, 1, True, {})
        for card in self.week.cards:
            db.save_review(
                self.progress, card["id"], 1, today + timedelta(days=3), 3, 2.5, 2, 0, 2
            )

    def tearDown(self):
        self.progress.db.close()
        self.tmp.cleanup()

    def test_all_checks_pass(self):
        result = gate.evaluate(self.progress, self.week)
        self.assertTrue(result.passed, [c.detail for c in result.failed])
        self.assertEqual(len(result.checks), 6)

    def test_exam_too_low(self):
        self.progress.db.execute("UPDATE exams SET score = 60 WHERE week = 1")
        self.progress.db.commit()
        result = gate.evaluate(self.progress, self.week)
        self.assertFalse(result.passed)
        self.assertIn("exam", [c.key for c in result.failed])

    def test_cards_not_mature(self):
        self.progress.db.execute("UPDATE reviews SET reps = 1 WHERE week = 1")
        self.progress.db.commit()
        result = gate.evaluate(self.progress, self.week)
        self.assertFalse(result.passed)
        self.assertIn("cards", [c.key for c in result.failed])

    def test_missing_evidence(self):
        self.progress.db.execute("DELETE FROM evidence WHERE week = 1")
        self.progress.db.commit()
        result = gate.evaluate(self.progress, self.week)
        self.assertFalse(result.passed)
        self.assertIn("evidence", [c.key for c in result.failed])

    def test_too_few_sessions(self):
        self.progress.db.execute("DELETE FROM sessions WHERE day = ?", (date.today().isoformat(),))
        self.progress.db.execute("DELETE FROM sessions WHERE day = ?", ((date.today() - timedelta(days=1)).isoformat(),))
        self.progress.db.execute("DELETE FROM sessions WHERE day = ?", ((date.today() - timedelta(days=2)).isoformat(),))
        self.progress.db.commit()
        result = gate.evaluate(self.progress, self.week)
        self.assertFalse(result.passed)
        self.assertIn("time", [c.key for c in result.failed])

    def test_prerequisite(self):
        week2 = make_week(2)
        result = gate.evaluate(self.progress, week2)
        self.assertFalse(result.passed)
        self.assertIn("prereq", [c.key for c in result.failed])


if __name__ == "__main__":
    unittest.main()
