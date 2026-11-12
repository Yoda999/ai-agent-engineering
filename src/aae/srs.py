"""Spaced repetition (SM-2 variant) voor geheugenkaarten."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

MIN_EASE = 1.3
MAX_EASE = 3.0


@dataclass
class CardState:
    interval: float = 0.0
    ease: float = 2.5
    reps: int = 0
    lapses: int = 0


def schedule(state: CardState, grade: int, today: date | None = None) -> tuple[CardState, date]:
    """Bereken nieuwe toestand en vervaldatum.

    grade: 0 = opnieuw, 1 = moeilijk, 2 = goed, 3 = makkelijk.
    """
    if grade not in (0, 1, 2, 3):
        raise ValueError("grade moet 0, 1, 2 of 3 zijn")
    today = today or date.today()
    interval = float(state.interval)
    ease = float(state.ease)
    reps = int(state.reps)
    lapses = int(state.lapses)

    if grade == 0:
        interval = 0.0
        ease = max(MIN_EASE, ease - 0.20)
        lapses += 1
    elif grade == 1:
        interval = 1.0 if reps == 0 else max(1.0, interval * 1.2)
        ease = max(MIN_EASE, ease - 0.15)
    elif grade == 2:
        if reps == 0:
            interval = 1.0
        elif reps == 1:
            interval = 3.0
        else:
            interval = max(1.0, interval * ease)
    else:  # grade == 3
        if reps == 0:
            interval = 3.0
        elif reps == 1:
            interval = 7.0
        else:
            interval = max(1.0, interval * ease * 1.3)

    reps += 1
    ease = min(MAX_EASE, max(MIN_EASE, ease))
    due = today + timedelta(days=round(interval))
    return CardState(interval=interval, ease=ease, reps=reps, lapses=lapses), due
