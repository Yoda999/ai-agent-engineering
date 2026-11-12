"""Inhoud van het opleidingsprogramma: assessments en weekmetadata."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

TOTAL_WEEKS = 24


class ContentError(Exception):
    """Ongeldige of ontbrekende curriculuminhoud."""


def find_root(start: Path | None = None) -> Path:
    """Vind de repo-root (map met assessments/)."""
    env = os.environ.get("AAE_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "assessments").is_dir():
            return candidate
    pkg_root = Path(__file__).resolve().parents[2]
    if (pkg_root / "assessments").is_dir():
        return pkg_root
    raise ContentError(
        "Kan de curriculumroot niet vinden. Run vanuit de repo of zet AAE_ROOT."
    )


@dataclass
class Week:
    week: int
    phase: int
    title: str
    outcome: str
    reading: list[dict[str, Any]] = field(default_factory=list)
    build: dict[str, Any] = field(default_factory=dict)
    challenge: dict[str, Any] = field(default_factory=dict)
    references: list[dict[str, str]] = field(default_factory=list)
    exam: dict[str, Any] = field(default_factory=dict)
    cards: list[dict[str, Any]] = field(default_factory=list)

    @property
    def pass_score(self) -> float:
        return float(self.exam.get("pass_score", 85))

    @property
    def minutes(self) -> int:
        return int(self.exam.get("minutes", 20))

    @property
    def card_ids(self) -> list[str]:
        return [str(c["id"]) for c in self.cards]


def _phase_files(root: Path) -> list[Path]:
    files = sorted((root / "assessments").glob("phase-*.yaml"))
    if not files:
        raise ContentError(f"Geen assessments/phase-*.yaml gevonden in {root}")
    return files


def load_all(root: Path | None = None) -> list[Week]:
    root = root or find_root()
    weeks: dict[int, Week] = {}
    for path in _phase_files(root):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "weeks" not in data:
            raise ContentError(f"{path.name}: verwacht een 'weeks'-lijst")
        for raw in data["weeks"]:
            week = Week(
                week=int(raw["week"]),
                phase=int(raw.get("phase", data.get("phase", 0))),
                title=str(raw["title"]),
                outcome=str(raw.get("outcome", "")),
                reading=list(raw.get("reading", [])),
                build=dict(raw.get("build", {})),
                challenge=dict(raw.get("challenge", {})),
                references=list(raw.get("references", [])),
                exam=dict(raw.get("exam", {})),
                cards=list(raw.get("cards", [])),
            )
            if week.week in weeks:
                raise ContentError(f"Week {week.week} komt dubbel voor")
            weeks[week.week] = week
    missing = [n for n in range(1, TOTAL_WEEKS + 1) if n not in weeks]
    if missing:
        raise ContentError(f"Ontbrekende weken: {missing}")
    return [weeks[n] for n in range(1, TOTAL_WEEKS + 1)]


def load_week(number: int, root: Path | None = None) -> Week:
    for week in load_all(root):
        if week.week == number:
            return week
    raise ContentError(f"Week {number} bestaat niet")


def validate(root: Path | None = None) -> list[str]:
    """Structurele controle. Retourneert een lijst met fouten (leeg = ok)."""
    errors: list[str] = []
    try:
        weeks = load_all(root)
    except ContentError as exc:
        return [str(exc)]

    seen_ids: set[str] = set()
    for week in weeks:
        label = f"week {week.week}"
        if not week.title or not week.outcome:
            errors.append(f"{label}: title/outcome ontbreekt")
        if not week.reading:
            errors.append(f"{label}: geen reading opgegeven")
        for item in week.reading:
            for key in ("book", "ref", "pages"):
                if not item.get(key):
                    errors.append(f"{label}: reading mist '{key}'")
        if not week.build.get("goal") or not week.build.get("deliverable"):
            errors.append(f"{label}: build.goal/build.deliverable ontbreekt")
        if not week.challenge.get("brief") or not week.challenge.get("acceptance"):
            errors.append(f"{label}: challenge.brief/acceptance ontbreekt")

        questions = week.exam.get("questions", [])
        open_count = sum(1 for q in questions if q.get("type") == "open")
        mcq_count = sum(1 for q in questions if q.get("type") == "mcq")
        if mcq_count != 5:
            errors.append(f"{label}: verwacht 5 mcq-vragen, gevonden {mcq_count}")
        if open_count != 1:
            errors.append(f"{label}: verwacht 1 open vraag, gevonden {open_count}")

        for q in questions:
            qid = str(q.get("id", ""))
            if not qid:
                errors.append(f"{label}: vraag zonder id")
            elif qid in seen_ids:
                errors.append(f"{label}: dubbele vraag-id {qid}")
            seen_ids.add(qid)
            if week.pass_score < 50 or week.pass_score > 100:
                errors.append(f"{label}: ongeldige pass_score")
            if q.get("type") == "mcq":
                options = q.get("options", {})
                if len(options) != 4:
                    errors.append(f"{label}/{qid}: verwacht 4 opties")
                if q.get("answer") not in options:
                    errors.append(f"{label}/{qid}: answer niet in opties")
                if not q.get("explanation"):
                    errors.append(f"{label}/{qid}: explanation ontbreekt")
            elif q.get("type") == "open":
                points = q.get("key_points", [])
                if len(points) < 3:
                    errors.append(f"{label}/{qid}: minstens 3 key_points nodig")
                if not q.get("model_answer"):
                    errors.append(f"{label}/{qid}: model_answer ontbreekt")
            else:
                errors.append(f"{label}/{qid}: onbekend type {q.get('type')}")

        if len(week.cards) < 4:
            errors.append(f"{label}: minstens 4 kaarten nodig")
        for card in week.cards:
            cid = str(card.get("id", ""))
            if not cid:
                errors.append(f"{label}: kaart zonder id")
            elif cid in seen_ids:
                errors.append(f"{label}: dubbele kaart-id {cid}")
            seen_ids.add(cid)
            for key in ("front", "back", "source"):
                if not card.get(key):
                    errors.append(f"{label}/{cid}: kaart mist '{key}'")
    return errors
