# Roadmap: 24 weken naar aantoonbare agent-expertise

Deze roadmap is de uitvoerbare vorm van de strategie. Elke week heeft een
onderwerp, bronpagina's, een bouwopdracht en een gate met bewijs. Je kunt pas
naar de volgende week als de gate groen is.

## Ontwerpprincipes

1. **Bewijs boven beleving.** "Ik snap het" telt niet; een examen, een werkende
   challenge, een trace en een commit tellen.
2. **Eerst meten, dan bouwen.** Elke fase begint met een baseline en eindigt met
   een meetbaar resultaat.
3. **Klein en af.** Eén uur levert één afgeronde stap op, geen half werk.
4. **Productie is de norm.** Vanaf week 1 zijn tests, CI en foutpaden geen
   bijzaak.
5. **Geen stille achterstand.** Falen is informatie; de gate dwingt herstel af.

## Tijdsbudget

| Post | Uren |
|---|---|
| 24 weken x 6 dagen x 1 uur | 144 |
| Gate-dagen (24 x 1 uur, inbegrepen) | — |
| Portfolio- en capstone-werk buiten de blokken | 60-100 |
| **Totaal tot einde programma** | **200-250** |

Eén uur per dag is het minimum, niet het maximum. De capstone vraagt in de
laatste fase meer tijd; plan die bewust in.

## Weekritme

| Dag | Focus | Bewijs |
|---|---|---|
| Ma | Theorie + eerste buildstap | Commit + 5 punten samenvatting |
| Di | Buildstap 2 | Commit + test |
| Wo | Buildstap 3 | Commit + test |
| Do | Buildstap 4 | Commit + test |
| Vr | Integratie + challenge | Challenge-run |
| Za | Examen + gate + retrospective | Examenscore + gate |
| Zo | Rust of lichte herhaling (15 min) | Optioneel |

## De 24 weken

### Fase 1 — Fundament: getypeerd, getest, gedeployed (week 1-6)

| Week | Thema | Lezen | Bouwen | Gatebewijs |
|---|---|---|---|---|
| 1 | Diagnose en eerste getypeerde agent | PydanticAI 1-2; Claude Code 1-3 | Ticket-triage-agent met schema en 5 tests | Groene CI + tests |
| 2 | Modelkeuze, promptbeleid en kosten | PydanticAI 3; Claude Code 4 | Kosten- en latencyguard + A/B-rapport | Budget limiet + kostenlog |
| 3 | Structured output en foutmodellen | PydanticAI 4 | Factuurextractie met validators en fouttaxonomie | 10 fouttests |
| 4 | Tools met contracten | PydanticAI 5 | Drie tools met idempotentie en retries | Toolcontracttests |
| 5 | Dependencies, testing en observability | PydanticAI 6, 8; Claude Code 6 | DI, fakes, traces, testpiramide | Traceerbare run |
| 6 | Workflow, container, CI/CD en VPS | PydanticAI 7, 11; Claude Code 9 | Docker, GHCR, compose, deploy, rollback | Live health + rollback |

**Fasepoort 1:** een live agent op de VPS met healthcheck, groene CI, smoke-test
en een uitgevoerde rollback. Zonder deze poort start fase 2 niet.

### Fase 2 — Kennis: retrieval, RAG en evaluatie (week 7-11)

| Week | Thema | Lezen | Bouwen | Gatebewijs |
|---|---|---|---|---|
| 7 | Tokens, context en ingestion | LlamaIndex 1, 3 | Idempotente pipeline met chunkmatrix | Chunkrapport + manifest |
| 8 | Embeddings, vectorstores, indexversie | LlamaIndex 4 | Benchmark, persistente index, rebuild | Recall@5 + rollback |
| 9 | Hybrid, rerank en filters | LlamaIndex 5-6 | RAG met citaties en filters | Ablatie-rapport |
| 10 | RAG-evaluatie | LlamaIndex 11; DSPy 7; LangChain 7 | Golden set, metrics, CI-drempel | Eval-rapport + regressiepoort |
| 11 | Observability, latency en kosten | LlamaIndex 12-13; LangChain 10 | Traces, dashboard, cache, loadtest | p95 + kosten per query |

**Fasepoort 2:** een gedeployde RAG-service met een geversioneerde golden set,
eval-drempels in CI en een loadtestrapport.

### Fase 3 — Orkestratie: multi-agent en optimalisatie (week 12-16)

| Week | Thema | Lezen | Bouwen | Gatebewijs |
|---|---|---|---|---|
| 12 | CrewAI: rollen, taken en crews | CrewAI 1-2; Claude Code 8 | Drie-rollen crew met fake-LLM-tests | Gevalideerd rapport |
| 13 | Tools, MCP en memory | CrewAI 4-6 | MCP-tool, memory, permissiematrix | Permissie- en memorytests |
| 14 | Flows en event-driven orchestration | CrewAI 8-9, 11 | Flow met retries, HITL en failure injection | Hersteltest + approval |
| 15 | Multi-agent testen en observability | CrewAI 12-13; LlamaIndex 10 | Trajectory-evals, traces, deadlocktests | 20 trajecten + trace-rapport |
| 16 | DSPy: meten en optimaliseren | DSPy 1-8, 18 | Signature, metric, optimizer, CI-regressie | >= 10% winst of -30% kosten |

**Fasepoort 3:** een multi-agent systeem met trajectory-evaluaties en een
cijfermatig bewezen verbetering tegen een baseline.

### Fase 4 — Productie: security, schaal en betrouwbaarheid (week 17-20)

| Week | Thema | Lezen | Bouwen | Gatebewijs |
|---|---|---|---|---|
| 17 | Security en threat modeling | PydanticAI 10; Claude Code 11; CrewAI 9 | Threat model, injectiesuite, sandbox | Red-team-rapport |
| 18 | Evaluatie en continuous improvement | PydanticAI 15; DSPy 18; LlamaIndex 11 | Judge-calibratie, regressiedashboard | Judge-agreement + rapport |
| 19 | Performance, queues en multi-tenancy | PydanticAI 9; LlamaIndex 13; LangChain 10 | Queue, rate limits, tenant-isolatie | Loadtest 10x |
| 20 | Reliability, SLO's en incidenten | Claude Code 10; PydanticAI 11; CrewAI 13 | SLO's, alerts, restore-drill, chaos | Restore + postmortem |

**Fasepoort 4:** een productie-review: securityrapport, SLO-dashboard, restore-
en chaosbewijs en een postmortem met preventieve maatregelen.

### Fase 5 — Capstone en carrière (week 21-24)

| Week | Thema | Lezen | Bouwen | Gatebewijs |
|---|---|---|---|---|
| 21 | Businessidee naar architectuur | Claude Code 12; PydanticAI 12 | 10 interviews, unit economics, ADR's | Capstone-spec |
| 22 | Capstone sprint 1: verticale slice | PydanticAI 15; LlamaIndex 11 | End-to-end slice met eval en CI | Demo + evalrapport |
| 23 | Capstone sprint 2: productie | PydanticAI 9, 11; LlamaIndex 13 | Deploy, loadtest, security, observability | Live URL + SLO-bewijs |
| 24 | Verdediging en carrière | Claude Code 13; PydanticAI 12 | Architectuurreview, demo, portfolio, CV | Externe review |

**Eindpoort:** een externe reviewer beoordeelt architectuur, evaluatie, kosten,
security en communicatie. De rubric staat in [docs/COMPETENCIES.md](docs/COMPETENCIES.md).

## Versnellen en vertragen

- **Versnellen** mag alleen door een gate te halen. Je kunt een week in minder
  dagen doen, maar niet zonder examen, challenge, kaarten en bewijs.
- **Vertragen** is normaal. Bij een mislukte gate herhaal je de week met gerichte
  oefeningen; de CLI blokkeert de volgende week.
- **Twee mislukte pogingen** op dezelfde gate: stop, analyseer de foutoorzaak,
  doe de herstelopdrachten en plan een 1-op-1 review (met jezelf of een mentor)
  voordat je een derde poging doet.
- **Ziekte of drukte:** schuif de kalender, niet de lat. Een week inhalen mag;
  een gate overslaan niet.

## Na week 24

De eerste 24 weken leveren een productiecompetent profiel op. De weg naar
expertise loopt daarna door:

| Maand | Focus | Bewijs |
|---|---|---|
| 7 | Twee weken vakantie, daarna een nieuw agentproject vanaf nul | Live project + postmortem |
| 8 | Open source: één bijdrage aan PydanticAI, LlamaIndex of DSPy | Gemergede PR |
| 9 | Specialisatie kiezen: evaluatie, RAG, security of platform | Diepgaand rapport of talk |
| 10 | Twee capstones uitbreiden naar echte gebruikers | Gebruiksdata + iteratie |
| 11 | Freelance- of sollicitatieronde; 20 gesprekken | Portfolio + casestudy's |
| 12 | Eindexamen: een onbekend agentprobleem in 4 uur oplossen | Opname + rubric |

## Wat je elke week vastlegt

1. **Commit** met een betekenisvolle boodschap.
2. **CI-run** of testoutput.
3. **Challengebewijs**: log, rapport, URL of demo.
4. **Reflectie**: 5 regels: wat werkte, wat niet, wat meet ik volgende week.

`aae report --write docs/PROGRESS.md` bundelt dit tot een deelbaar bewijsrapport.

## Start vandaag

- [ ] `aae doctor` is groen (behalve optionele API-keys).
- [ ] `aae today` toont week 1.
- [ ] De repo `agent-lab-01` bestaat en de eerste commit staat erin.
- [ ] Je hebt 60 minuten in je agenda geblokkeerd, elke dag, op een vast uur.
- [ ] Je startdatum staat in de database (`aae status` toont week 1).
