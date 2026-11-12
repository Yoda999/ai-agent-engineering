# Gates: de exacte regels

Een gate is de enige manier om een week af te sluiten. De CLI berekent hem
objectief; er is geen "ik voel me klaar".

## Weeksgate: zes checks

| # | Check | Drempel | Hoe je hem haalt |
|---|---|---|---|
| 1 | Vorige week | gate gehaald | `aae gate --week N-1` |
| 2 | Examen | >= 85% | `aae exam --week N` |
| 3 | Challenge | geslaagde run | `aae challenge --week N --cmd ...` |
| 4 | Kaarten | alle kaarten reps >= 2 en laatste score >= 2 | `aae cards --week N` |
| 5 | Studietijd | 5 dagen >= 30 min in 7 dagen, samen >= 240 min | `aae log 60` |
| 6 | Bewijs | >= 3 bewijsstukken | `aae evidence` of automatisch |

Alle zes moeten groen zijn. `aae gate --week N` toont per check de status en
een concrete herstelopdracht.

### Examen

- 5 meerkeuzevragen (elk 15 punten) en 1 open vraag (25 punten).
- De open vraag wordt gescoord op kernpunten (0-4), proportioneel.
- Drempel 85%. Bijvoorbeeld: één MCQ fout (15 punten verlies) en de open vraag
  volledig goed is precies 85%.
- Geen boek, geen AI, geen notities. Eén antwoord per vraag.
- De uitslag en je antwoorden worden opgeslagen.

### Challenge

- De `verify`-opdracht moet slagen (exitcode 0) in de opgegeven map.
- Die map is de repo van je **project** (`--dir ../agent-lab-01`), niet deze
  curriculumrepo. De scripts (`scripts/verify-*.sh`, `pytest`) horen bij je
  project en staan in je eigen repo.
- Of, bij een handmatige review: `--manual --evidence <ref> --yes`, met
  minimaal één concreet bewijsstuk.
- Een challenge zonder bewijs is geen bewijs. Screenshots zonder context,
  "werkt bij mij" en niet-reproduceerbare demo's tellen niet.

### Kaarten

- Elke kaart van de week moet minstens twee keer zijn herhaald en de laatste
  score moet 2 of 3 zijn.
- Score 0 of 1 betekent: opnieuw, dezelfde dag of de volgende dag.
- Er is geen "ik ken hem" zonder review; de CLI telt alleen opgeslagen reviews.

### Studietijd

- In de laatste 7 dagen: minstens 5 dagen met >= 30 minuten.
- Samen minstens 240 minuten (4 uur).
- Eén sessie van 4 uur op zondag telt dus niet als 5 studiedagen; de gate meet
  consistentie, niet alleen volume.

### Bewijs

- Minstens 3 bewijsstukken voor de week.
- Soorten: commit, CI-run, testrapport, evalrapport, loadtest, demo-URL,
  architectuurbeslissing, postmortem.
- Standaard: zie [EVIDENCE.md](EVIDENCE.md).

## Herkansingen

| Situatie | Regel |
|---|---|
| Eerste mislukking | 24 uur wachten en herstelopdrachten doen |
| Tweede mislukking | week herhalen met extra oefeningen; daarna opnieuw |
| Derde poging | alleen na een 1-op-1 review (mentor of zelf met opname) |
| Poging forceren | `--force` mag, maar wordt gelogd en telt als rode vlag |

De CLI blokkeert een herkansing binnen 24 uur. `--force` bestaat voor noodgevallen,
niet als standaardroute.

## Fasepoorten

Naast de weeksgate zijn er vier fasepoorten met extra bewijs.

### Fase 1: live agent

- [ ] Live URL of Tailscale-bereikbare service op de VPS.
- [ ] `/health` geeft 200 en de smoke-test slaagt.
- [ ] CI bouwt en pusht een immutable image.
- [ ] Rollback is minstens één keer uitgevoerd en gelogd.
- [ ] Runbook met deploy, verify, rollback en secrets.

### Fase 2: meetbare RAG

- [ ] Golden set >= 50 items, geversioneerd.
- [ ] Retrieval- en generatiemetrics apart gerapporteerd.
- [ ] CI faalt bij een geinjecteerde regressie.
- [ ] Loadtest met p95, foutpercentage en kosten per query.
- [ ] Bewezen `geen bewijs`-pad.

### Fase 3: multi-agent met bewijs

- [ ] Minstens 20 trajectory-evaluaties met rubric.
- [ ] Per-agent traces en kosten.
- [ ] Timeout-, deadlock- en failure-injection-tests.
- [ ] DSPy-optimalisatie met before/after op dezelfde set.
- [ ] >= 10% kwaliteitswinst of >= 30% kostenreductie bij gelijke kwaliteit.

### Fase 4: productie-review

- [ ] Threat model en geslaagde prompt-injectiesuite.
- [ ] Judge-calibratie met menselijke steekproef.
- [ ] Loadtest op 10x verwachte belasting.
- [ ] Restore-drill en chaos-test uitgevoerd.
- [ ] Postmortem met oorzaak en preventieve maatregel.

## Eindverdediging (week 24)

Een externe reviewer (mentor, oud-collega, community) beoordeelt op zes assen,
elk van 1 tot 4:

| As | 1 (onvoldoende) | 2 (basis) | 3 (productie) | 4 (expert) |
|---|---|---|---|---|
| Architectuur | geen scheiding | werkt, fragiel | heldere grenzen, schaalpad | eenvoudig, verdedigd, trade-offs |
| Evaluatie | geen metrics | losse tests | golden set + drempels | causaliteit, judge-calibratie |
| Security | geen model | checklist | threat model + tests | aanvalspaden, mitigaties, review |
| Operatie | handmatig | basisdeploy | SLO's, alerts, rollback | chaos, restore, kostenmodel |
| Communicatie | vaag | begrijpelijk | helder en beknoopt | overtuigt, beantwoordt kritiek |
| Business | geen idee | idee | validatie + unit economics | schaalpad en verdedigbaarheid |

**Slagen:** minstens 3 op alle assen en gemiddeld >= 3,0. Een 1 op security of
operatie is een harde fail, ongeacht de rest.

## Integriteit

- Het examen is gesloten boek. AI-gebruik tijdens het examen maakt de uitslag
  ongeldig.
- De challenge mag je met AI bouwen; dat is juist de bedoelde vaardigheid. Maar
  je moet elke regel kunnen uitleggen en de tests moeten echt zijn.
- Bewijs mag nooit verzonnen zijn. Een niet-bestaande CI-run of URL is fraude.
- Zelfbedrog is de duurste vorm: je betaalt later met een mislukte sollicitatie.

## Als het leven ingrijpt

- **Drukke week:** schuif de week, niet de gate. Haal de uren in waar het kan.
- **Ziek:** pauzeer; hervat met een lichte herhalingsdag.
- **Motivatie:** lees je rapport en je fasebewijs. Je bouwt een portfolio, geen
  huiswerk.
- **Vastgelopen:** verklein de stap, vraag review, of ga terug naar de vorige
  gate en zoek het gat.

## Commando's

```bash
aae gate --week 3        # evalueer
aae gate --week 3 --force  # noodrem, wordt gelogd
aae status               # alle gates
aae report               # bewijsrapport
```
