"""SQLite-opslag voor voortgang, herhalingen, examens en bewijs."""

from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL,
    minutes INTEGER NOT NULL,
    note TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS reviews (
    card_id TEXT PRIMARY KEY,
    week INTEGER NOT NULL,
    due TEXT NOT NULL,
    interval REAL NOT NULL DEFAULT 0,
    ease REAL NOT NULL DEFAULT 2.5,
    reps INTEGER NOT NULL DEFAULT 0,
    lapses INTEGER NOT NULL DEFAULT 0,
    last_grade INTEGER,
    last_review TEXT
);
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week INTEGER NOT NULL,
    ts TEXT NOT NULL,
    score REAL NOT NULL,
    passed INTEGER NOT NULL,
    detail TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week INTEGER NOT NULL,
    ts TEXT NOT NULL,
    passed INTEGER NOT NULL,
    detail TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS gates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week INTEGER NOT NULL,
    ts TEXT NOT NULL,
    passed INTEGER NOT NULL,
    detail TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week INTEGER NOT NULL,
    kind TEXT NOT NULL,
    ref TEXT NOT NULL,
    note TEXT NOT NULL DEFAULT '',
    ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS unlocks (
    week INTEGER PRIMARY KEY,
    ts TEXT NOT NULL
);
"""

DEFAULTS = {
    "current_week": "1",
    "min_sessions": "5",
    "min_session_minutes": "30",
    "min_week_minutes": "240",
    "min_evidence": "3",
    "cards_min_reps": "2",
}


@dataclass
class Progress:
    db: sqlite3.Connection
    home: Path


def db_path(home: Path | None = None) -> Path:
    if home is None:
        env = os.environ.get("AAE_HOME")
        home = Path(env).expanduser() if env else Path.cwd() / ".aae"
    return Path(home) / "progress.db"


def connect(home: Path | None = None) -> Progress:
    path = db_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    for key, value in DEFAULTS.items():
        conn.execute(
            "INSERT OR IGNORE INTO meta(key, value) VALUES (?, ?)", (key, value)
        )
    conn.execute(
        "INSERT OR IGNORE INTO meta(key, value) VALUES ('start_date', ?)",
        (date.today().isoformat(),),
    )
    conn.commit()
    return Progress(db=conn, home=path.parent)


def meta(progress: Progress, key: str, default: str | None = None) -> str | None:
    row = progress.db.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def set_meta(progress: Progress, key: str, value: str) -> None:
    progress.db.execute(
        "INSERT INTO meta(key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )
    progress.db.commit()


def current_week(progress: Progress) -> int:
    return int(meta(progress, "current_week", "1") or 1)


def start_date(progress: Progress) -> date:
    return date.fromisoformat(str(meta(progress, "start_date", date.today().isoformat())))


def log_session(progress: Progress, minutes: int, note: str = "", day: date | None = None) -> None:
    day = day or date.today()
    progress.db.execute(
        "INSERT INTO sessions(day, minutes, note) VALUES (?, ?, ?)",
        (day.isoformat(), minutes, note),
    )
    progress.db.commit()


def week_sessions(progress: Progress, week: int, today: date | None = None) -> list[sqlite3.Row]:
    today = today or date.today()
    end = today
    begin = today - timedelta(days=6)
    return list(
        progress.db.execute(
            "SELECT day, SUM(minutes) AS minutes FROM sessions "
            "WHERE day BETWEEN ? AND ? GROUP BY day ORDER BY day",
            (begin.isoformat(), end.isoformat()),
        )
    )


def add_evidence(
    progress: Progress, week: int, kind: str, ref: str, note: str = ""
) -> None:
    progress.db.execute(
        "INSERT INTO evidence(week, kind, ref, note, ts) VALUES (?, ?, ?, ?, ?)",
        (week, kind, ref, note, datetime.now().isoformat(timespec="seconds")),
    )
    progress.db.commit()


def evidence_count(progress: Progress, week: int) -> int:
    row = progress.db.execute(
        "SELECT COUNT(*) AS n FROM evidence WHERE week = ?", (week,)
    ).fetchone()
    return int(row["n"])


def record_exam(
    progress: Progress, week: int, score: float, passed: bool, detail: dict[str, Any]
) -> None:
    progress.db.execute(
        "INSERT INTO exams(week, ts, score, passed, detail) VALUES (?, ?, ?, ?, ?)",
        (
            week,
            datetime.now().isoformat(timespec="seconds"),
            score,
            1 if passed else 0,
            json.dumps(detail, ensure_ascii=False),
        ),
    )
    progress.db.commit()


def best_exam(progress: Progress, week: int) -> sqlite3.Row | None:
    return progress.db.execute(
        "SELECT * FROM exams WHERE week = ? ORDER BY score DESC, id DESC LIMIT 1",
        (week,),
    ).fetchone()


def record_challenge(
    progress: Progress, week: int, passed: bool, detail: dict[str, Any]
) -> None:
    progress.db.execute(
        "INSERT INTO challenges(week, ts, passed, detail) VALUES (?, ?, ?, ?)",
        (
            week,
            datetime.now().isoformat(timespec="seconds"),
            1 if passed else 0,
            json.dumps(detail, ensure_ascii=False),
        ),
    )
    progress.db.commit()


def challenge_passed(progress: Progress, week: int) -> bool:
    row = progress.db.execute(
        "SELECT COUNT(*) AS n FROM challenges WHERE week = ? AND passed = 1", (week,)
    ).fetchone()
    return int(row["n"]) > 0


def record_gate(
    progress: Progress, week: int, passed: bool, detail: dict[str, Any]
) -> None:
    progress.db.execute(
        "INSERT INTO gates(week, ts, passed, detail) VALUES (?, ?, ?, ?)",
        (
            week,
            datetime.now().isoformat(timespec="seconds"),
            1 if passed else 0,
            json.dumps(detail, ensure_ascii=False),
        ),
    )
    progress.db.commit()


def gate_passed(progress: Progress, week: int) -> bool:
    row = progress.db.execute(
        "SELECT COUNT(*) AS n FROM gates WHERE week = ? AND passed = 1", (week,)
    ).fetchone()
    return int(row["n"]) > 0


def last_gate_attempt(progress: Progress, week: int) -> sqlite3.Row | None:
    return progress.db.execute(
        "SELECT * FROM gates WHERE week = ? ORDER BY id DESC LIMIT 1", (week,)
    ).fetchone()


def unlock(progress: Progress, week: int) -> None:
    progress.db.execute(
        "INSERT OR REPLACE INTO unlocks(week, ts) VALUES (?, ?)",
        (week, datetime.now().isoformat(timespec="seconds")),
    )
    set_meta(progress, "current_week", str(max(current_week(progress), week)))


def review_state(progress: Progress, card_id: str) -> sqlite3.Row | None:
    return progress.db.execute(
        "SELECT * FROM reviews WHERE card_id = ?", (card_id,)
    ).fetchone()


def save_review(
    progress: Progress,
    card_id: str,
    week: int,
    due: date,
    interval: float,
    ease: float,
    reps: int,
    lapses: int,
    grade: int,
) -> None:
    progress.db.execute(
        "INSERT INTO reviews(card_id, week, due, interval, ease, reps, lapses, last_grade, last_review) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(card_id) DO UPDATE SET week=excluded.week, due=excluded.due, "
        "interval=excluded.interval, ease=excluded.ease, reps=excluded.reps, "
        "lapses=excluded.lapses, last_grade=excluded.last_grade, last_review=excluded.last_review",
        (
            card_id,
            week,
            due.isoformat(),
            interval,
            ease,
            reps,
            lapses,
            grade,
            date.today().isoformat(),
        ),
    )
    progress.db.commit()


def due_cards(progress: Progress, week: int, today: date | None = None) -> list[sqlite3.Row]:
    today = today or date.today()
    return list(
        progress.db.execute(
            "SELECT * FROM reviews WHERE week <= ? AND due <= ? ORDER BY due",
            (week, today.isoformat()),
        )
    )


def week_reviews(progress: Progress, week: int) -> list[sqlite3.Row]:
    return list(
        progress.db.execute("SELECT * FROM reviews WHERE week = ?", (week,))
    )


def all_reviews(progress: Progress) -> list[sqlite3.Row]:
    return list(progress.db.execute("SELECT * FROM reviews"))
