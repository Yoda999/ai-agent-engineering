"""Voortgangsoverzicht en bewijsrapport (markdown)."""

from __future__ import annotations

from datetime import date
from typing import Any

from . import db
from .content import Week


def status_rows(progress: db.Progress, weeks: list[Week]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for week in weeks:
        exam = db.best_exam(progress, week.week)
        reviews = db.week_reviews(progress, week.week)
        good = sum(
            1 for r in reviews if int(r["reps"]) >= 2 and int(r["last_grade"] or 0) >= 2
        )
        rows.append(
            {
                "week": week.week,
                "phase": week.phase,
                "title": week.title,
                "exam": float(exam["score"]) if exam else None,
                "challenge": db.challenge_passed(progress, week.week),
                "cards_good": good,
                "cards_total": len(week.cards),
                "gate": db.gate_passed(progress, week.week),
            }
        )
    return rows


def totals(progress: db.Progress) -> dict[str, Any]:
    minutes = progress.db.execute(
        "SELECT COALESCE(SUM(minutes), 0) AS m, COUNT(DISTINCT day) AS d FROM sessions"
    ).fetchone()
    reviews = db.all_reviews(progress)
    mature = sum(1 for r in reviews if float(r["interval"]) >= 21)
    gates = progress.db.execute(
        "SELECT COUNT(*) AS n FROM gates WHERE passed = 1"
    ).fetchone()
    return {
        "minutes": int(minutes["m"]),
        "days": int(minutes["d"]),
        "cards": len(reviews),
        "mature": mature,
        "gates": int(gates["n"]),
        "current_week": db.current_week(progress),
    }


def markdown(progress: db.Progress, weeks: list[Week]) -> str:
    t = totals(progress)
    rows = status_rows(progress, weeks)
    lines = [
        "# Voortgang en bewijs",
        "",
        f"Gegenereerd op {date.today().isoformat()}.",
        "",
        "## Kerncijfers",
        "",
        "| Meting | Waarde |",
        "|---|---|",
        f"| Huidige week | {t['current_week']} / {len(weeks)} |",
        f"| Studietijd | {t['minutes'] // 60} u {t['minutes'] % 60} min |",
        f"| Studiedagen | {t['days']} |",
        f"| Kaarten gezien | {t['cards']} |",
        f"| Kaarten 'mature' (>= 21 dagen) | {t['mature']} |",
        f"| Bewezen gates | {t['gates']} |",
        "",
        "## Weken",
        "",
        "| Week | Fase | Onderwerp | Examen | Challenge | Kaarten | Gate |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        exam = f"{r['exam']:.0f}%" if r["exam"] is not None else "-"
        cards = f"{r['cards_good']}/{r['cards_total']}"
        lines.append(
            f"| {r['week']} | {r['phase']} | {r['title']} | {exam} | "
            f"{'ja' if r['challenge'] else '-'} | {cards} | "
            f"{'PASS' if r['gate'] else '-'} |"
        )

    evidence = list(
        progress.db.execute(
            "SELECT week, kind, ref, note, ts FROM evidence ORDER BY id DESC LIMIT 50"
        )
    )
    lines += ["", "## Bewijs (laatste 50)", ""]
    if not evidence:
        lines.append("_Nog geen bewijs vastgelegd._")
    else:
        lines += ["| Week | Soort | Referentie | Datum |", "|---|---|---|---|"]
        for e in evidence:
            ref = str(e["ref"]).replace("|", "\\|")
            lines.append(f"| {e['week']} | {e['kind']} | {ref} | {str(e['ts'])[:10]} |")

    failed = [r for r in rows if not r["gate"]]
    if failed:
        nxt = failed[0]
        lines += [
            "",
            "## Volgende actie",
            "",
            f"Rond week {nxt['week']} af: **{nxt['title']}**.",
            "",
            "```bash",
            f"aae today              # plan voor vandaag",
            f"aae cards --week {nxt['week']}   # kaarten op niveau brengen",
            f"aae exam --week {nxt['week']}    # examen",
            f"aae gate --week {nxt['week']}    # poort",
            "```",
        ]
    else:
        lines += ["", "## Volgende actie", "", "Alle 24 weken zijn bewezen. Tijd voor de eindverdediging."]
    lines.append("")
    return "\n".join(lines)
