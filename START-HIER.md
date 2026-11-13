# Start hier: je eerste zeven dagen

Dit is de meest concrete route. Als je niets anders leest, lees dit en begin.

## Voor je begint (30-45 min, eenmalig)

- [ ] Python 3.11+, git en Docker geinstalleerd.
- [ ] Deze repo gekloond en `pip install -e ".[dev]"` gedaan.
- [ ] `aae doctor` is groen (Docker mag ontbreken als je lokaal blijft).
- [ ] Een API-key of lokale Ollama; een uitgavenlimiet staat aan.
- [ ] Een GitHub-account en een geldige PAT (zie [SETUP.md](docs/SETUP.md)).

## Dag 0 — Nulmeting (30 min, optioneel maar aanbevolen)

Doe de [nulmeting](docs/BASELINE.md) zonder boek of AI. Noteer je score; die
kalibreert je tempo en je verwachtingen. Je hoeft niets te installeren.

## Dag 1 — Omgeving en eerste agent (60 min)

**Lezen (15 min):** PydanticAI p. 4-25 (h.1-2), Claude Code p. 8-47 (h.1-3).
**Doen (35 min):**

```bash
mkdir agent-lab-01 && cd agent-lab-01
git init
python3 -m venv .venv && source .venv/bin/activate
pip install "pydantic-ai-slim[openai]" pytest
```

Maak `triage.py`:

```python
from enum import Enum
from pydantic import BaseModel, Field
from pydantic_ai import Agent

class Urgency(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"

class TicketClassification(BaseModel):
    urgency: Urgency
    summary: str = Field(min_length=3, max_length=200)
    needs_human: bool

agent = Agent(
    "test",
    output_type=TicketClassification,
    instructions="Classificeer het ticket. Wees kort en gebruik alleen het schema.",
)

def classify(text: str) -> TicketClassification:
    return agent.run_sync(text).output
```

**Bewijs (10 min):** eerste commit.

## Dag 2 — Tests zonder netwerk

**Lezen:** PydanticAI h.2 afronden; Claude Code h.3.
**Doen:** schrijf vijf tests met `TestModel`:

1. geldige output (inclusief `needs_human`);
2. enum-waarde;
3. maximale lengte van `summary`;
4. lege of te lange input (inputvalidatie);
5. een ongeldige modeloutput met `FunctionModel`, die gecontroleerd faalt of
   binnen het retrybudget herstelt.

```python
from pydantic_ai.models.test import TestModel

def test_schema():
    with agent.override(model=TestModel()):
        result = classify("Mijn factuur is dubbel betaald")
    assert isinstance(result, TicketClassification)
```

Zet `models.ALLOW_MODEL_REQUESTS = False` in je testconfig zodat een echte call
niet per ongeluk kan.

`TestModel` genereert schema-geldige data; het test dus je contract, niet je
foutpad. Gebruik `FunctionModel` voor de ongeldige output. Zie de
[PydanticAI testing-docs](https://pydantic.dev/docs/ai/guides/testing/).

**Bewijs:** `pytest -q` groen + commit.

## Dag 3 — CI

**Lezen:** Claude Code h.4 (promptbeleid) en h.6 (verificatie).
**Doen:** GitHub Actions-workflow:

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -e ".[dev]"
      - run: pytest -q
```

**Bewijs:** groene CI-run + badge.

## Dag 4 — Foutpaden

**Lezen:** PydanticAI h.4 (validatie en retries) en h.5 (tools).
**Doen:** voeg een `ModelRetry`-pad toe en test drie ongeldige outputs.
**Bewijs:** drie tests die bewijzen dat de agent gecontroleerd herstelt of stopt.

## Dag 5 — Challenge afronden

**Doen:**

- README met installatie, gebruik en testcommando;
- `.gitignore` met `.env`, `.venv`, `__pycache__`;
- challenge draaien:

```bash
aae challenge --week 1 --dir ../agent-lab-01 --cmd "python -m pytest -q"
```

**Bewijs:** challenge geslaagd + commit.

## Dag 6 — Examen en gate

```bash
aae cards --week 1 --early   # alle kaarten minstens twee keer
aae exam --week 1
aae evidence --week 1 --kind ci --ref "<CI-URL>"
aae gate --week 1
```

**Let op:** de gate eist 5 studiedagen van >= 30 min en 3 bewijsstukken. Log je
uren vanaf dag 1 met `aae log 60`.

## Dag 7 — Rust en vooruitkijken

- 15 minuten kaarten.
- Lees de week 2-opdracht.
- Noteer in drie regels: wat kostte te veel tijd, wat was makkelijker dan
  verwacht, wat wil je volgende week beter doen?

## Als je de gate niet haalt

Dat is normaal en het systeem is ervoor gebouwd:

1. `aae gate --week 1` toont welke check faalt.
2. Herstel precies dat punt (kennis, challenge, kaarten, tijd of bewijs).
3. Wacht 24 uur en probeer opnieuw.
4. Haal je het na twee pogingen niet, herhaal de week met de extra oefeningen
   uit [curriculum/phase-1.md](curriculum/phase-1.md).

## Wat je na week 1 hebt

- Een getypeerde agent met een echt schema.
- Vijf tests die zonder netwerk draaien.
- Een groene CI-pipeline.
- Een bewezen challenge.
- Een begin van je portfolio en je eerste casestudy.

Dat is meer dan de meeste "agent tutorials" je geven.
