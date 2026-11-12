"""Beoordeling van examens: 5 meerkeuzevragen (15 pt) + 1 open vraag (25 pt)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MCQ_POINTS = 15.0
OPEN_POINTS = 25.0


@dataclass
class ExamResult:
    score: float
    mcq_correct: int
    mcq_total: int
    open_hits: int
    open_total: int
    passed: bool
    per_question: list[dict[str, Any]]


def grade(
    questions: list[dict[str, Any]],
    answers: dict[str, str],
    open_hits: dict[str, int],
    pass_score: float = 85.0,
) -> ExamResult:
    mcq = [q for q in questions if q.get("type") == "mcq"]
    open_qs = [q for q in questions if q.get("type") == "open"]
    if not mcq or not open_qs:
        raise ValueError("examen vereist zowel mcq- als open vragen")

    per_question: list[dict[str, Any]] = []
    correct = 0
    earned = 0.0
    for q in mcq:
        given = (answers.get(q["id"]) or "").strip().upper()
        ok = given == str(q["answer"]).strip().upper()
        correct += int(ok)
        earned += MCQ_POINTS if ok else 0.0
        per_question.append({"id": q["id"], "type": "mcq", "ok": ok, "given": given})

    hits_total = 0
    points_total = 0
    for q in open_qs:
        key_points = q.get("key_points", [])
        hits = max(0, min(int(open_hits.get(q["id"], 0)), len(key_points)))
        hits_total += hits
        points_total += len(key_points)
        earned += OPEN_POINTS * (hits / len(key_points) if key_points else 0.0)
        per_question.append(
            {
                "id": q["id"],
                "type": "open",
                "ok": hits == len(key_points),
                "hits": hits,
                "total": len(key_points),
            }
        )

    score = round(earned, 1)
    return ExamResult(
        score=score,
        mcq_correct=correct,
        mcq_total=len(mcq),
        open_hits=hits_total,
        open_total=points_total,
        passed=score >= pass_score,
        per_question=per_question,
    )
