import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from aae import db, report
from aae.cli import main
from aae.content import load_all


def run(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = main(list(argv))
    return code, out.getvalue()


class CliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = str(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_today_starts_at_week_one(self):
        code, output = run("--home", self.home, "today")
        self.assertEqual(code, 0)
        self.assertIn("WEEK 1", output)
        self.assertIn("Blok van 60 minuten", output)

    def test_log_and_status(self):
        code, _ = run("--home", self.home, "log", "60", "--note", "test")
        self.assertEqual(code, 0)
        code, output = run("--home", self.home, "status")
        self.assertEqual(code, 0)
        self.assertIn("1/24", output)

    def test_gate_locked_in_fresh_state(self):
        code, output = run("--home", self.home, "gate", "--week", "1")
        self.assertEqual(code, 1)
        self.assertIn("NIET GESLAAGD", output)

    def test_validate(self):
        code, output = run("--home", self.home, "validate")
        self.assertEqual(code, 0)
        self.assertIn("geldig", output)

    def test_report_markdown(self):
        progress = db.connect(Path(self.home))
        db.log_session(progress, 60, "studie")
        text = report.markdown(progress, load_all())
        progress.db.close()
        self.assertIn("# Voortgang en bewijs", text)
        self.assertIn("| 1 |", text)

    def test_invalid_week_is_rejected(self):
        code, output = run("--home", self.home, "exam", "--week", "99")
        self.assertEqual(code, 1)
        self.assertIn("bestaat niet", output)

    def test_doctor_runs(self):
        code, output = run("--home", self.home, "doctor")
        self.assertIn("Omgevingscheck", output)


if __name__ == "__main__":
    unittest.main()
