# Agent Engineering Academy

Een bewijsgestuurd opleidingsprogramma van 24 weken (1 uur per dag) om
productieklare AI-agents te bouwen, te testen, te evalueren en te deployen —
met een harde poort tussen de weken.

> **Kernregel:** je gaat pas verder als je het bewijs hebt geleverd. Geen
> certificaat zonder examen, challenge, herhaling en bewijsstukken.

[![CI](https://github.com/Yoda999/ai-agent-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/Yoda999/ai-agent-engineering/actions/workflows/ci.yml)

## Wat dit is

Dit is geen verzameling tutorials. Het is een leer- en bewijssysteem:

- **24 weken**, 5 studietaken per week van 60 minuten, plus een gate-dag.
- **Zes boeken** als bron, met een hoofdstuk-naar-week leeskaart.
- **Per week:** 5 meerkeuzevragen + 1 open vraag, 5 geheugenkaarten en een
  praktijkchallenge met acceptatiecriteria.
- **Een gate** die examenscore (>= 85%), challenge, kaartbeheersing, studietijd
  en bewijsstukken combineert. Slagen geeft de volgende week vrij.
- **Een CLI** (`aae`) die je planning, herhaling (SM-2), examens, bewijs en
  voortgang bijhoudt in SQLite.
- **Vijf fasen** van getypeerde agents naar retrieval, multi-agent, productie
  en een capstone met eindverdediging.

## Waarom dit bestaat

De markt heeft geen tekort aan agent-demo's. Er is een tekort aan mensen die
kunnen aantonen dat een agent **betrouwbaar, veilig, betaalbaar en
observeerbaar** is onder echte belasting. Dit programma traint precies dat
bewijs: evaluaties, contracten, SLO's, kosten, rollbacks en postmortems.

De ambitie is een carrièrestap, niet een certificaat. Daarom is elk artifact
openbaar of deelbaar: commits, groene CI-runs, evaluatierapporten, loadtests,
architectuurbeslissingen en een live demo.

## De vijf fasen

| Fase | Weken | Kern | Fasebewijs |
|---|---|---|---|
| 1. Fundament | 1-6 | Getypeerde agent, tools, testen, CI/CD, VPS-deploy | Live agent met healthcheck, smoke-test en rollback |
| 2. Kennis | 7-11 | Ingestion, embeddings, retrieval, RAG-evaluatie, latency/kosten | RAG-service met golden set, eval-drempel en loadtest |
| 3. Orkestratie | 12-16 | CrewAI, MCP, memory, flows, multi-agent observability, DSPy | Multi-agent systeem met trajectory-evals en gemeten verbetering |
| 4. Productie | 17-20 | Security, evaluatie, queues, multi-tenancy, SLO's, incidenten | Securityrapport, loadtest, restore-drill en postmortem |
| 5. Capstone | 21-24 | Businessvalidatie, capstone, verdediging, portfolio | Live capstone + externe review + portfolio |

## Zo werkt een dag

```text
10 min  Herhaling: aae cards
15 min  Theorie: lees de pagina's, schrijf 5 punten + 3 vragen
25 min  Hands-on: bouw de stap en commit
 5 min  Test: aae exam of de challenge-tests
 5 min  Log: aae log 60 en voeg bewijs toe
```

De week eindigt met een **gate**: examen, challenge, kaarten, uren en bewijs.
Bij falen volgt een herstelplan en een verplichte wachttijd van 24 uur.

## Begin hier

Volg [START-HIER.md](START-HIER.md) voor je eerste zeven dagen. Twijfels of
praktische bezwaren? Zie [docs/FAQ.md](docs/FAQ.md).

## Quick start

```bash
git clone https://github.com/Yoda999/ai-agent-engineering.git
cd ai-agent-engineering
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

aae doctor          # omgeving controleren
aae today           # plan voor vandaag
aae plan            # alle 24 weken
aae cards           # kaarten herhalen
aae exam --week 1   # weekexamen
aae gate --week 1   # poort
aae status          # voortgang
aae report --write docs/PROGRESS.md
```

Zonder installatie:

```bash
PYTHONPATH=src python3 -m aae today
```

## Repository-structuur

```text
assessments/phase-*.yaml   # bron van waarheid: lezen, bouwen, examen, kaarten
curriculum/phase-*.md      # narratief per fase, valkuilen en extra oefeningen
docs/                      # strategie, methode, gates, bewijs, scaling, setup
src/aae/                   # CLI: planning, SRS, examens, gates, rapport
tests/                     # tests op de leer-machine zelf
.github/workflows/ci.yml   # inhoud valideren + tests
```

## De boeken

De selectie dekt de volledige keten: getypeerde agents (PydanticAI), retrieval
(LlamaIndex), orkestratie (CrewAI), integratie (LangChain), meten en
optimaliseren (DSPy) en agentic coding (Claude Code).

| Ref | Boek | Rol |
|---|---|---|
| `pydanticai` | PydanticAI: Building Production-Grade AI Agents | Kern voor getypeerde, geteste agents |
| `llamaindex` | Building Production-Ready AI Agents with LlamaIndex | RAG, retrieval en productiepatronen |
| `crewai` | CrewAI in Action | Multi-agent orkestratie, flows, MCP |
| `langchain` | Mastering LangChain for Python Development | Ecosysteem, chains, memory, productie |
| `dspy` | Programming with DSPy | Metrics, optimizers, systematische verbetering |
| `claudecode` | Mastering Claude Code | Agentic coding, verificatie, security, teams |

Je leest **niet** alle boeken volledig. De [leeskaart](docs/READING-MAP.md)
wijst per week de pagina's aan; de rest is naslagwerk.

## Eerlijk over "expert"

24 weken van 1 uur per dag is ongeveer **144 begeleide uren**. Dat is genoeg om
productiecompetent te worden en een baan als AI/agent engineer serieus te
kunnen voeren. Echte expertise (zelfstandig onbekende problemen oplossen,
architectuur verdedigen, anderen opleiden) vraagt doorgaans **12-18 maanden**
deliberate practice en meerdere projecten onder druk. Deze roadmap is het
fundament en het bewijs; de [12-maandenroute](ROADMAP.md#na-week-24) zet de
volgende stappen.

## Documentatie

| Document | Inhoud |
|---|---|
| [ROADMAP.md](ROADMAP.md) | 24 weken, fase-poorten, weekritme, 12-maandenroute |
| [docs/STRATEGY.md](docs/STRATEGY.md) | Carrièrethese, markt, positionering, succescriteria |
| [docs/METHOD.md](docs/METHOD.md) | Leerwetenschap, dagindeling, herhaling, falen |
| [docs/GATES.md](docs/GATES.md) | Exacte regels, drempels, herkansingen, integriteit |
| [docs/COMPETENCIES.md](docs/COMPETENCIES.md) | Competentiemodel met vier niveaus |
| [docs/EVIDENCE.md](docs/EVIDENCE.md) | Wat geldt als bewijs en hoe je het bewaart |
| [docs/READING-MAP.md](docs/READING-MAP.md) | Hoofdstukken en pagina's per week |
| [docs/SETUP.md](docs/SETUP.md) | Omgeving, API-keys, GitHub, VPS, backups |
| [docs/SCALING.md](docs/SCALING.md) | Van één VPS naar schaalbare architectuur |
| [docs/FAQ.md](docs/FAQ.md) | Bezwaren, tijdsbudget, AI-gebruik, falen |
| [START-HIER.md](START-HIER.md) | De eerste zeven dagen, dag voor dag |
| [docs/BASELINE.md](docs/BASELINE.md) | Nulmeting: waar sta je nu? |

## Status

- [x] 24 weken, 120 meerkeuzevragen, 24 open vragen, 120 kaarten
- [x] Gate-mechanisme met SRS, examens, challenges en bewijs
- [x] CLI met tests en CI
- [ ] Week 1 gestart (startdatum invullen)
- [ ] Fase 1 gate behaald
- [ ] Capstone en eindverdediging

De voortgang staat in [docs/PROGRESS.md](docs/PROGRESS.md) (gegenereerd met
`aae report --write docs/PROGRESS.md`).

## Licentie

MIT. De boeken zelf vallen onder hun eigen licentie; dit programma bevat alleen
verwijzingen en eigen oefenstof.
