"""Command-line interface van de Agent Engineering Academy."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from . import content, db, gate, report
from .exam import grade
from .srs import CardState, schedule

WEEK_LABELS = {1: "MA", 2: "DI", 3: "WO", 4: "DO", 5: "VR", 6: "ZA", 7: "ZO"}


# --------------------------------------------------------------------------- helpers
def _progress(args: argparse.Namespace) -> db.Progress:
    progress = db.connect(getattr(args, "home", None))
    progress.root = content.find_root(getattr(args, "root", None))  # type: ignore[attr-defined]
    return progress


def _weeks(args: argparse.Namespace) -> list[content.Week]:
    return content.load_all(getattr(args, "root", None))


def _week(args: argparse.Namespace, number: int | None = None) -> content.Week:
    weeks = _weeks(args)
    number = number or db.current_week(_progress(args))
    for week in weeks:
        if week.week == number:
            return week
    raise content.ContentError(f"Week {number} bestaat niet (1-{content.TOTAL_WEEKS}).")


def _ask(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        return ""


def _multiline(prompt: str) -> str:
    print(prompt)
    lines: list[str] = []
    while True:
        line = _ask("> ")
        if not line.strip():
            break
        lines.append(line)
    return " ".join(lines).strip()


def _print_checks(result: gate.GateResult) -> None:
    print(f"\nGate week {result.week}\n" + "-" * 60)
    for check in result.checks:
        mark = "OK  " if check.ok else "FAIL"
        print(f"[{mark}] {check.label:<32} {check.detail}")
    print("-" * 60)
    if result.passed:
        print("RESULTAAT: GESLAAGD - volgende week is vrijgegeven.")
    else:
        print("RESULTAAT: NIET GESLAAGD - herstel de FAIL-punten.")
        for check in result.failed:
            print(f"  -> {check.remediation}")


def _due_for_week(
    progress: db.Progress, week: content.Week, include_all: bool = False
) -> list[dict[str, Any]]:
    """Nieuwe kaarten van deze week plus alle kaarten die volgens SRS aan de beurt zijn."""
    weeks = content.load_all(getattr(progress, "root", None))
    by_id: dict[str, dict[str, Any]] = {
        str(card["id"]): card for w in weeks for card in w.cards
    }
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    rows = db.week_reviews(progress, week.week) if include_all else db.due_cards(progress, week.week)
    for row in rows:
        card = by_id.get(str(row["card_id"]))
        if card:
            items.append(dict(row, card=card))
            seen.add(str(row["card_id"]))
    for w in weeks:
        if w.week > week.week:
            break
        for card in w.cards:
            cid = str(card["id"])
            if cid not in seen:
                items.append(
                    {
                        "card_id": cid,
                        "week": w.week,
                        "due": date.today().isoformat(),
                        "interval": 0.0,
                        "ease": 2.5,
                        "reps": 0,
                        "lapses": 0,
                        "last_grade": None,
                        "last_review": None,
                        "card": card,
                    }
                )
                seen.add(cid)
    return items


# --------------------------------------------------------------------------- commando's
def cmd_today(args: argparse.Namespace) -> int:
    progress = _progress(args)
    weeks = _weeks(args)
    number = db.current_week(progress)
    day = date.today()
    if args.date:
        day = date.fromisoformat(args.date)
    if number > content.TOTAL_WEEKS:
        print("Alle 24 weken zijn afgerond. Werk aan je eindverdediging en portfolio.")
        return 0
    week = weeks[number - 1]
    offset = (day - db.start_date(progress)).days
    due = len(_due_for_week(progress, week))
    result = gate.evaluate(progress, week, day)

    print("=" * 68)
    print(f"WEEK {week.week} - FASE {week.phase} - {week.title}")
    print(f"Dag {offset + 1} van je programma | {day.isoformat()} | kaarten te herhalen: {due}")
    print("=" * 68)
    print(f"\nDoel: {week.outcome}\n")
    print("Lezen:")
    for item in week.reading:
        print(f"  - {item.get('book')} | {item.get('chapters')} | p. {item.get('pages')}")
    print("\nBouwen:")
    print(f"  {week.build.get('goal', '')}")
    for step in week.build.get("steps", []):
        print(f"  - {step}")
    print("\nBlok van 60 minuten:")
    print("  10 min  Herhaling: aae cards")
    print("  15 min  Theorie: lees de opgegeven pagina's, schrijf 5 punten + 3 vragen")
    print("  25 min  Hands-on: werk aan de build-stap en commit")
    print("   5 min  Test: aae exam --week %d of de challenge-tests" % week.week)
    print("   5 min  Log: aae log 60 --note \"...\" en bewijs toevoegen")
    print("\nGate-status:")
    for check in result.checks:
        print(f"  [{'OK' if check.ok else '  '}] {check.label} ({check.detail})")
    if week.references:
        print("\nReferenties:")
        for ref in week.references:
            print(f"  - {ref.get('title')}: {ref.get('url')}")
    print("\nVolgende stap: `aae cards` en daarna `aae exam --week %d`." % week.week)
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    if args.minutes <= 0 or args.minutes > 300:
        print("Aantal minuten moet tussen 1 en 300 liggen.")
        return 2
    progress = _progress(args)
    day = date.fromisoformat(args.date) if args.date else date.today()
    db.log_session(progress, args.minutes, args.note or "", day)
    today_total = progress.db.execute(
        "SELECT COALESCE(SUM(minutes),0) AS m FROM sessions WHERE day = ?",
        (day.isoformat(),),
    ).fetchone()["m"]
    print(f"Gelogd: {args.minutes} min op {day.isoformat()} (vandaag totaal {today_total} min).")
    return 0


def cmd_cards(args: argparse.Namespace) -> int:
    progress = _progress(args)
    week = _week(args, args.week)
    due = _due_for_week(progress, week, include_all=args.early)
    if not due:
        print(f"Geen kaarten te herhalen voor week {week.week}. Mooi.")
        return 0
    print(f"{len(due)} kaart(en) te herhalen voor week {week.week}.")
    if not sys.stdin.isatty():
        for item in due:
            card = item["card"]
            print(f"- {card['front'] if card else item['card_id']}")
        return 0

    for index, item in enumerate(due, start=1):
        card = item["card"]
        if not card:
            continue
        print(f"\n[{index}/{len(due)}] {card['front']}")
        _ask("Enter om het antwoord te zien... ")
        print(f"ANTWOORD: {card['back']}")
        print(f"Bron: {card['source']}")
        while True:
            raw = _ask("Score 0=opnieuw 1=moeilijk 2=goed 3=makkelijk: ").strip()
            if raw in {"0", "1", "2", "3"}:
                grade_value = int(raw)
                break
            print("Kies 0, 1, 2 of 3.")
        state = CardState(
            interval=float(item["interval"]),
            ease=float(item["ease"]),
            reps=int(item["reps"]),
            lapses=int(item["lapses"]),
        )
        new_state, due_date = schedule(state, grade_value)
        db.save_review(
            progress,
            str(item["card_id"]),
            week.week,
            due_date,
            new_state.interval,
            new_state.ease,
            new_state.reps,
            new_state.lapses,
            grade_value,
        )
    print("\nHerhaling opgeslagen.")
    return 0


def cmd_exam(args: argparse.Namespace) -> int:
    progress = _progress(args)
    week = _week(args, args.week)
    if week.week > 1 and not db.gate_passed(progress, week.week - 1):
        print(
            f"Let op: de gate van week {week.week - 1} is nog niet behaald. "
            "Dit examen telt wel mee, maar de gate blijft dicht."
        )
    questions = week.exam.get("questions", [])
    print("=" * 68)
    print(f"EXAMEN WEEK {week.week}: {week.title}")
    print(f"Gesloten boek, geen AI. Drempel: {week.pass_score:.0f}%. Tijd: ~{week.minutes} min.")
    print("=" * 68)

    answers: dict[str, str] = {}
    open_hits: dict[str, int] = {}

    for number, q in enumerate(questions, start=1):
        print(f"\nVraag {number} ({'meerkeuze' if q['type'] == 'mcq' else 'open'})")
        print(q["prompt"])
        if q["type"] == "mcq":
            for letter, text in q["options"].items():
                print(f"  {letter}. {text}")
            while True:
                given = _ask("Antwoord (A/B/C/D): ").strip().upper()
                if given in q["options"]:
                    break
                print("Ongeldig antwoord.")
            answers[q["id"]] = given
        else:
            answer = _multiline("Je antwoord (einde met lege regel):")
            answers[q["id"]] = answer
            print("\nBeoordeel jezelf streng. Modelantwoord en kernpunten:")
            print(f"MODEL: {q['model_answer']}")
            hits = 0
            for point in q["key_points"]:
                raw = _ask(f"  Bevatte je antwoord dit punt? [j/n] {point}: ").strip().lower()
                if raw.startswith("j"):
                    hits += 1
            open_hits[q["id"]] = hits

    result = grade(questions, answers, open_hits, week.pass_score)
    print("\n" + "=" * 68)
    print(
        f"SCORE: {result.score:.1f}%  |  MCQ {result.mcq_correct}/{result.mcq_total}  |  "
        f"open {result.open_hits}/{result.open_total} kernpunten"
    )
    for item in result.per_question:
        if item["type"] == "mcq" and not item["ok"]:
            q = next(q for q in questions if q["id"] == item["id"])
            print(f"  FOUT {item['id']}: juist was {q['answer']} - {q['explanation']}")
    verdict = "GESLAAGD" if result.passed else "NIET GESLAAGD"
    print(f"RESULTAAT: {verdict} (drempel {week.pass_score:.0f}%)")
    if not result.passed:
        print("Herhaal de zwakke punten en probeer opnieuw. Bekijk de bronnen van je fouten.")
    print("=" * 68)

    db.record_exam(
        progress,
        week.week,
        result.score,
        result.passed,
        {
            "answers": answers,
            "per_question": result.per_question,
            "mcq_correct": result.mcq_correct,
            "open_hits": result.open_hits,
        },
    )
    db.add_evidence(
        progress,
        week.week,
        "examen",
        f"score={result.score:.1f}%",
        "geslaagd" if result.passed else "niet geslaagd",
    )
    return 0 if result.passed else 1


def cmd_challenge(args: argparse.Namespace) -> int:
    progress = _progress(args)
    week = _week(args, args.week)
    evidence = list(args.evidence or [])

    if args.manual:
        if not args.yes:
            print("Handmatige goedkeuring vereist --yes en ten minste één --evidence.")
            return 2
        if not evidence:
            print("Geef minstens één --evidence op (commit, URL, rapport).")
            return 2
        db.record_challenge(progress, week.week, True, {"manual": True, "evidence": evidence})
        for ref in evidence:
            db.add_evidence(progress, week.week, "challenge", ref, "handmatig beoordeeld")
        print(f"Challenge week {week.week} handmatig goedgekeurd.")
        return 0

    command = args.cmd or week.challenge.get("verify")
    if not command:
        print(
            "Deze challenge heeft geen automatische verificatie. "
            "Gebruik --cmd '<commando>' of --manual --evidence <ref> --yes."
        )
        return 2
    workdir = Path(args.dir).expanduser().resolve()
    if not workdir.is_dir():
        print(f"Map bestaat niet: {workdir}")
        return 2
    print(f"Uitvoeren in {workdir}: {command}")
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=900,
        )
        output = (proc.stdout or "") + (proc.stderr or "")
        passed = proc.returncode == 0
    except subprocess.TimeoutExpired:
        output = "TIME-OUT na 900 seconden"
        passed = False
    print(output[-4000:])
    print(f"\nResultaat: {'GESLAAGD' if passed else 'NIET GESLAAGD'} (exit={0 if passed else 1})")
    db.record_challenge(
        progress,
        week.week,
        passed,
        {"command": command, "dir": str(workdir), "tail": output[-2000:]},
    )
    if passed:
        db.add_evidence(progress, week.week, "challenge", command, "automatisch geverifieerd")
    return 0 if passed else 1


def cmd_gate(args: argparse.Namespace) -> int:
    progress = _progress(args)
    week = _week(args, args.week)
    if db.gate_passed(progress, week.week):
        print(f"Gate week {week.week} is al behaald.")
        return 0

    last = db.last_gate_attempt(progress, week.week)
    if last and not int(last["passed"]) and not args.force:
        attempted = datetime.fromisoformat(str(last["ts"]))
        wait_until = attempted + timedelta(hours=24)
        if datetime.now() < wait_until:
            remaining = wait_until - datetime.now()
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            print(
                "Je laatste poging was minder dan 24 uur geleden. "
                f"Wacht nog {hours}u {minutes}m of gebruik --force na het doen van de herstelopdrachten."
            )
            return 2

    result = gate.evaluate(progress, week, date.today())
    _print_checks(result)
    db.record_gate(
        progress,
        week.week,
        result.passed,
        {"checks": [c.__dict__ for c in result.checks]},
    )
    if result.passed:
        if week.week < content.TOTAL_WEEKS:
            db.unlock(progress, week.week + 1)
            print(f"Week {week.week + 1} is nu vrijgegeven.")
        else:
            db.unlock(progress, content.TOTAL_WEEKS + 1)
            print("Alle weken zijn bewezen. Start de eindverdediging.")
        return 0
    return 1


def cmd_status(args: argparse.Namespace) -> int:
    progress = _progress(args)
    weeks = _weeks(args)
    rows = report.status_rows(progress, weeks)
    t = report.totals(progress)
    print(f"Huidige week: {t['current_week']}/{len(weeks)} | "
          f"{t['minutes'] // 60}u {t['minutes'] % 60}m | {t['days']} studiedagen | "
          f"{t['gates']} gates")
    print("-" * 78)
    print(f"{'Week':<5}{'Fase':<6}{'Examen':<8}{'Chall':<7}{'Kaarten':<9}{'Gate':<6}Onderwerp")
    print("-" * 78)
    for r in rows:
        exam = f"{r['exam']:.0f}%" if r["exam"] is not None else "-"
        cards = f"{r['cards_good']}/{r['cards_total']}"
        print(
            f"{r['week']:<5}{r['phase']:<6}{exam:<8}"
            f"{'ja' if r['challenge'] else '-':<7}{cards:<9}"
            f"{'PASS' if r['gate'] else '-':<6}{r['title']}"
        )
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    if args.check:
        errors = content.validate(getattr(args, "root", None))
        if errors:
            for error in errors:
                print(f"FOUT: {error}")
            return 1
        print("Inhoud is geldig.")
        return 0
    progress = _progress(args)
    weeks = _weeks(args)
    text = report.markdown(progress, weeks)
    if args.write:
        path = Path(args.write).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"Rapport geschreven naar {path}")
    else:
        print(text)
    return 0


def cmd_evidence(args: argparse.Namespace) -> int:
    progress = _progress(args)
    week = args.week or db.current_week(progress)
    db.add_evidence(progress, week, args.kind, args.ref, args.note or "")
    print(f"Bewijs toegevoegd voor week {week}: {args.kind} -> {args.ref}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors = content.validate(getattr(args, "root", None))
    if errors:
        for error in errors:
            print(f"FOUT: {error}")
        print(f"\n{len(errors)} fout(en).")
        return 1
    print("Alle 24 weken zijn structureel geldig.")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    for week in _weeks(args):
        refs = ", ".join(f"{r['ref']} p.{r['pages']}" for r in week.reading)
        print(f"W{week.week:02d} [fase {week.phase}] {week.title}")
        print(f"     lezen: {refs}")
        print(f"     bouwen: {week.build.get('deliverable', '')}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    checks: list[tuple[str, bool, str, bool]] = []
    checks.append(("Python >= 3.11", sys.version_info >= (3, 11), sys.version.split()[0], True))
    try:
        import yaml  # noqa: F401

        checks.append(("PyYAML", True, "geinstalleerd", True))
    except Exception as exc:  # pragma: no cover
        checks.append(("PyYAML", False, str(exc), True))
    try:
        root = content.find_root()
        checks.append(("Curriculum gevonden", True, str(root), True))
    except content.ContentError as exc:
        checks.append(("Curriculum gevonden", False, str(exc), True))
    checks.append(("Git", bool(shutil.which("git")), shutil.which("git") or "niet gevonden", True))
    checks.append(
        (
            "Docker",
            bool(shutil.which("docker")),
            shutil.which("docker") or "niet gevonden (nodig vanaf week 6)",
            False,
        )
    )
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY"):
        present = bool(os.environ.get(key))
        checks.append((key, present, "gezet" if present else "niet gezet (optioneel)", False))
    print("Omgevingscheck")
    print("-" * 64)
    for label, ok, detail, required in checks:
        mark = "OK  " if ok else ("FAIL" if required else "--  ")
        print(f"[{mark}] {label:<24} {detail}")
    failed = [label for label, ok, _, required in checks if required and not ok]
    if failed:
        print("\nOntbrekend (verplicht): " + ", ".join(failed))
        return 1
    print("\nVerplichte onderdelen zijn in orde.")
    return 0


# --------------------------------------------------------------------------- parser
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aae",
        description="Agent Engineering Academy - bewijsgestuurd leren.",
    )
    parser.add_argument("--home", type=Path, default=None, help="map voor progress.db")
    parser.add_argument("--root", type=Path, default=None, help="repo-root")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("today", help="plan van vandaag")
    p.add_argument("--date", help="simuleer een datum (YYYY-MM-DD)")
    p.set_defaults(func=cmd_today)

    p = sub.add_parser("log", help="studietijd loggen")
    p.add_argument("minutes", type=int)
    p.add_argument("--note", default="")
    p.add_argument("--date", help="YYYY-MM-DD")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("cards", help="geheugenkaarten herhalen")
    p.add_argument("--week", type=int)
    p.add_argument("--early", action="store_true", help="ook kaarten die nog niet aan de beurt zijn")
    p.set_defaults(func=cmd_cards)

    p = sub.add_parser("exam", help="weekexamen maken")
    p.add_argument("--week", type=int)
    p.set_defaults(func=cmd_exam)

    p = sub.add_parser("challenge", help="praktijkchallenge verifieren")
    p.add_argument("--week", type=int)
    p.add_argument("--dir", default=".")
    p.add_argument("--cmd", default=None)
    p.add_argument("--manual", action="store_true")
    p.add_argument("--evidence", action="append")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_challenge)

    p = sub.add_parser("gate", help="weekpoort evalueren")
    p.add_argument("--week", type=int)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_gate)

    p = sub.add_parser("status", help="voortgang tonen")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("report", help="bewijsrapport genereren")
    p.add_argument("--write", default=None)
    p.add_argument("--check", action="store_true")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("evidence", help="bewijsstuk toevoegen")
    p.add_argument("--week", type=int)
    p.add_argument("--kind", required=True)
    p.add_argument("--ref", required=True)
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_evidence)

    p = sub.add_parser("validate", help="inhoud valideren")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("plan", help="24-wekenplan tonen")
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("doctor", help="omgevingscheck")
    p.set_defaults(func=cmd_doctor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except content.ContentError as exc:
        print(f"Inhoudsfout: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
