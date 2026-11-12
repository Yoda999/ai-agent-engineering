"""Poortwachter: bepaalt of een week bewezen is."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from . import db
from .content import Week


@dataclass
class Check:
    key: str
    label: str
    ok: bool
    detail: str
    remediation: str


@dataclass
class GateResult:
    week: int
    checks: list[Check]

    @property
    def passed(self) -> bool:
        return all(c.ok for c in self.checks)

    @property
    def failed(self) -> list[Check]:
        return [c for c in self.checks if not c.ok]


def _int_meta(progress: db.Progress, key: str) -> int:
    return int(db.meta(progress, key, "0") or 0)


def evaluate(
    progress: db.Progress,
    week: Week,
    today: date | None = None,
) -> GateResult:
    today = today or date.today()
    checks: list[Check] = []

    # 1. Voorgaande week moet bewezen zijn.
    if week.week == 1:
        checks.append(Check("prereq", "Startvoorwaarde", True, "week 1", ""))
    else:
        ok = db.gate_passed(progress, week.week - 1)
        checks.append(
            Check(
                "prereq",
                f"Week {week.week - 1} afgerond",
                ok,
                "behaald" if ok else "niet behaald",
                f"Rond eerst de gate van week {week.week - 1} af.",
            )
        )

    # 2. Examen.
    best = db.best_exam(progress, week.week)
    score = float(best["score"]) if best else 0.0
    passed_exam = bool(best) and score >= week.pass_score
    checks.append(
        Check(
            "exam",
            f"Examen >= {week.pass_score:.0f}%",
            passed_exam,
            f"{score:.1f}%" if best else "nog geen poging",
            f"Herhaal de leerstof en doe het examen opnieuw (drempel {week.pass_score:.0f}%).",
        )
    )

    # 3. Praktijkchallenge.
    ok = db.challenge_passed(progress, week.week)
    checks.append(
        Check(
            "challenge",
            "Challenge bewezen",
            ok,
            "geslaagd" if ok else "geen geslaagde run",
            "Lever de challenge op en laat de verificatie slagen.",
        )
    )

    # 4. Kaarten op niveau.
    min_reps = _int_meta(progress, "cards_min_reps")
    good = 0
    for card_id in week.card_ids:
        row = db.review_state(progress, card_id)
        if row and int(row["reps"]) >= min_reps and int(row["last_grade"] or 0) >= 2:
            good += 1
    total = len(week.card_ids)
    ok = total > 0 and good == total
    checks.append(
        Check(
            "cards",
            f"Kaarten op niveau ({good}/{total})",
            ok,
            f"minstens {min_reps} herhalingen en laatste score >= 2",
            "Review de openstaande kaarten tot alle kaarten van deze week op niveau zijn.",
        )
    )

    # 5. Studietijd: 5 dagen van >= 30 min in de laatste 7 dagen.
    rows = db.week_sessions(progress, week.week, today)
    min_sessions = _int_meta(progress, "min_sessions")
    min_session = _int_meta(progress, "min_session_minutes")
    min_week = _int_meta(progress, "min_week_minutes")
    active = [r for r in rows if int(r["minutes"]) >= min_session]
    total_min = sum(int(r["minutes"]) for r in rows)
    time_ok = len(active) >= min_sessions and total_min >= min_week
    checks.append(
        Check(
            "time",
            f"Studietijd ({len(active)} dagen, {total_min} min)",
            time_ok,
            f"doel: {min_sessions} dagen >= {min_session} min, samen >= {min_week} min",
            "Plan je 60-minutenblokken in en log ze met `aae log <minuten>`.",
        )
    )

    # 6. Bewijsstukken.
    min_evidence = _int_meta(progress, "min_evidence")
    count = db.evidence_count(progress, week.week)
    checks.append(
        Check(
            "evidence",
            f"Bewijsstukken ({count}/{min_evidence})",
            count >= min_evidence,
            "commit, testrun, demo of rapport",
            "Voeg bewijs toe: `aae evidence --week N --kind commit --ref <sha>`.",
        )
    )

    return GateResult(week=week.week, checks=checks)
