# Bewijs: wat telt en hoe je het bewaart

Bewijs is een artifact dat een andere persoon kan controleren zonder jou te
vertrouwen. "Het werkt" is geen bewijs; een commit, een groene CI-run, een
reproduceerbaar rapport en een URL zijn dat wel.

## De vier eisen

1. **Reproduceerbaar:** iemand kan het opnieuw draaien met dezelfde invoer.
2. **Verifieerbaar:** er is een objectieve uitkomst (exitcode, score, metric).
3. **Gekoppeld aan een versie:** commit, image-digest of datasetversie.
4. **Geïnterpreteerd:** je legt uit wat het resultaat betekent en wat je ervan
   leerde.

## Soorten bewijs

| Soort | Voorbeeld | Sterkte |
|---|---|---|
| Commit | `git show <sha>` met een betekenisvolle diff | basis |
| CI-run | URL naar een groene job op die commit | sterk |
| Testrapport | `pytest -q` output, coverage per module | sterk |
| Evalrapport | JSON/markdown met metrics, datasetversie en drempels | zeer sterk |
| Loadtest | p50/p95/p99, foutpercentage, doorvoer, bottleneck | zeer sterk |
| Demo | live URL of opname van het kritieke pad | sterk |
| ADR | beslissing, alternatieven, gevolgen | sterk |
| Postmortem | tijdlijn, oorzaak, impact, preventie | zeer sterk |
| Securityrapport | threat model, injectietests, secret scan | zeer sterk |
| Restore-drill | back-up teruggezet en geverifieerd | zeer sterk |
| Kostenmodel | kosten per request/tenant met aannames | sterk |

## Wat niet telt

- Een screenshot zonder datum, context of commando.
- "Werkt op mijn machine" zonder reproduceerbare stappen.
- Een demo die alleen het gelukkige pad toont.
- Een coverage-cijfer zonder betekenisvolle assertions.
- Een prompt die "beter voelt" zonder vergelijking op dezelfde set.
- Een geplakte output die niet herleidbaar is tot een run.
- Een URL die na een week niet meer bestaat (maak een opname of export).

## Bewijs per fase

### Fase 1

- [ ] Commit van de agent met schema en tests.
- [ ] Groene CI-run op die commit.
- [ ] Image-digest in GHCR.
- [ ] Healthcheck-output van de VPS.
- [ ] Smoke-testoutput.
- [ ] Rollback-log met de vorige digest.
- [ ] Runbook (deploy, verify, rollback, secrets).

### Fase 2

- [ ] Golden set (50+ items) met versie en herkomst.
- [ ] Eval-rapport met recall@k, MRR, faithfulness en correctheid.
- [ ] CI-run die aantoont dat een regressie wordt geblokkeerd.
- [ ] Ablatie-rapport (vector, hybrid, rerank).
- [ ] Loadtestrapport met p95 en kosten per query.
- [ ] Bewijs van het `geen bewijs`-pad.

### Fase 3

- [ ] 20 trajectory-evaluaties met rubric en scores.
- [ ] Trace-export met per-agent latency en kosten.
- [ ] Failure-injection- en deadlocktests.
- [ ] DSPy before/after op dezelfde dataset.
- [ ] CI-regressiepoort voor kwaliteit.

### Fase 4

- [ ] Threat model met aanvalspaden en maatregelen.
- [ ] Prompt-injectiesuite met resultaten.
- [ ] Judge-calibratie tegen menselijke labels.
- [ ] Loadtest op 10x belasting met bottleneck.
- [ ] Restore-drill en chaos-test.
- [ ] Postmortem met preventieve maatregel.

### Fase 5

- [ ] 10 klantinterviews met citaten en conclusies.
- [ ] Capstone-spec met probleem, doelgroep en succescriteria.
- [ ] Live capstone met SLO-dashboard.
- [ ] Kostenmodel en schaalplan.
- [ ] Externe review met rubric.
- [ ] Portfolio met 5 casestudy's.

## Casestudy-sjabloon

Elke portfolio-casestudy volgt hetzelfde stramien:

```markdown
# <Naam systeem>

## Probleem
Voor wie, welke pijn, hoe vaak, wat kost het nu?

## Constraints
Budget, latency, data, compliance, team, deadline.

## Aanpak
Architectuur, belangrijkste keuzes, alternatieven die je verwierp.

## Bewijs
- Eval: <metrics, dataset, drempels>
- Loadtest: <p95, foutpercentage, doorvoer>
- Security: <threat model, tests>
- Operatie: <SLO, alerts, rollback, restore>

## Resultaat
Voor/na, kosten per taak, betrouwbaarheid, gebruikersfeedback.

## Wat ik anders zou doen
Eerlijke trade-offs en geleerde lessen.
```

## Bewaarplaats

- **Code en docs:** in de repo van het project.
- **Runs en rapporten:** `docs/evidence/` in de projectrepo, of een link naar de
  CI/het dashboard met een export.
- **Voortgang:** de CLI-database (`.aae/progress.db`) en `docs/PROGRESS.md`.
- **Vertrouwelijk:** geen klantdata, secrets of persoonsgegevens in bewijs.
  Redigeer en bewaar alleen wat nodig is.

## Commando's

```bash
aae evidence --week 6 --kind ci --ref "https://github.com/.../actions/runs/123"
aae evidence --week 6 --kind rollback --ref "docs/evidence/rollback-2026-11-20.log"
aae report --write docs/PROGRESS.md
```

De gate vereist minstens drie bewijsstukken per week. Kwaliteit gaat boven
kwantiteit: drie sterke artifacts verslaan tien screenshots.
