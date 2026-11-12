import unittest
from datetime import date, timedelta

from aae.srs import CardState, schedule


class SRSTest(unittest.TestCase):
    def test_new_card_good(self):
        state, due = schedule(CardState(), 2, date(2026, 1, 1))
        self.assertEqual(state.reps, 1)
        self.assertEqual(state.interval, 1)
        self.assertEqual(due, date(2026, 1, 2))

    def test_good_progression(self):
        state, due = schedule(CardState(), 2, date(2026, 1, 1))
        state, due = schedule(state, 2, date(2026, 1, 2))
        self.assertEqual(state.interval, 3)
        self.assertEqual(due, date(2026, 1, 5))
        state, due = schedule(state, 2, date(2026, 1, 5))
        self.assertGreaterEqual(state.interval, 7)
        self.assertEqual(state.reps, 3)

    def test_again_resets_interval(self):
        state = CardState(interval=10, ease=2.5, reps=3, lapses=0)
        state, due = schedule(state, 0, date(2026, 1, 10))
        self.assertEqual(state.interval, 0)
        self.assertEqual(state.reps, 4)
        self.assertEqual(state.lapses, 1)
        self.assertLess(state.ease, 2.5)
        self.assertEqual(due, date(2026, 1, 10))

    def test_easy_new_card(self):
        state, due = schedule(CardState(), 3, date(2026, 1, 1))
        self.assertEqual(state.interval, 3)
        self.assertEqual(due, date(2026, 1, 4))

    def test_ease_bounds(self):
        state = CardState(ease=1.3)
        state, _ = schedule(state, 1, date(2026, 1, 1))
        self.assertGreaterEqual(state.ease, 1.3)
        state = CardState(ease=3.0)
        state, _ = schedule(state, 3, date(2026, 1, 1))
        self.assertLessEqual(state.ease, 3.0)

    def test_invalid_grade(self):
        with self.assertRaises(ValueError):
            schedule(CardState(), 4)


if __name__ == "__main__":
    unittest.main()
