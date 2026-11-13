# Fase 1 — Fundament: getypeerd, getest, gedeployed

**Weken 1-6. Doel: één agent die je durft te deployen.**

> **Bronaudit (13 november 2026):** fase 1 is tegen de officiële PydanticAI-,
> Docker- en Kubernetes-docs gecontroleerd. Geen foute antwoordsleutels; 15
> precisiecorrecties. Zie [docs/AUDITS/phase-1.md](../docs/AUDITS/phase-1.md).

Deze fase lijkt misschien traag als je al agents hebt gebouwd. Dat is bewust.
De meeste agentprojecten falen niet door een gebrek aan frameworks, maar door
ontbrekende contracten, tests, foutpaden en een deploy die niemand kan
reproduceren. Hier leg je dat fundament.

## Wat je na deze fase kunt

- Een agent met een expliciet uitvoerschema bouwen en valideren.
- Model, prompt en kosten expliciet maken en begrenzen.
- Tools ontwerpen met idempotentie, time-outs en getypeerde fouten.
- Domeinlogica scheiden van infrastructuur met dependency injection.
- Een testpiramide toepassen: unit, contract, eval, e2e.
- Een container bouwen, via CI publiceren en op een VPS deployen met healthcheck,
  smoke-test en rollback.

## Kernconcepten

| Concept | Waarom het telt |
|---|---|
| Agent-loop | Je moet weten waar een run kan blijven hangen of geld verbranden |
| `output_type` | Een contract tussen model en applicatie |
| Validatie en retry | Ongeldige output is een verwachte fout, geen crash |
| Toolcontract | Een tool is een API met rechten, fouten en neveneffecten |
| Dependency injection | Testbaarheid en vervangbaarheid |
| Testpiramide | Snelle feedback plus bewijs op het echte systeem |
| Unieke tag of digest | Reproduceerbare deploy en betrouwbare rollback |
| Healthcheck en smoke-test | Bewijs dat de gedeployde versie echt werkt |

## Weekoverzicht

| Week | Onderwerp | Bouwen |
|---|---|---|
| 1 | Diagnose en eerste agent | Ticket-triage met schema en 5 tests |
| 2 | Model, prompt, kosten | Budgetguard en A/B-rapport |
| 3 | Structured output | Factuurextractie met fouttaxonomie |
| 4 | Tools | Drie tools met idempotentie |
| 5 | DI en observability | Fakes, traces, testpiramide |
| 6 | Deploy | Docker, GHCR, VPS, rollback |

## Veelgemaakte fouten

1. **De prompt als contract gebruiken.** "Je moet JSON teruggeven" is geen
   schema. Gebruik een typed model en valideer.
2. **Geen foutpad.** De demo werkt; de time-out, rate limit en ongeldige input
   zijn niet getest.
3. **Alles in één functie.** Model, prompt, HTTP-call en database in één blok:
   niet te testen en niet te vervangen.
4. **Testen met de echte LLM.** Traag, duur en niet deterministisch. Gebruik
   `TestModel` en fakes; test de echte provider apart.
5. **`latest` deployen.** Dan weet je niet wat er draait en kun je niet
   terugrollen.
6. **Secrets in het image.** Eén lek en je key staat in de geschiedenis.
7. **Coverage najagen.** 100% coverage met zwakke assertions bewijst niets.

## Extra oefeningen (bij herstel of versnelling)

1. Bouw dezelfde agent met een tweede provider en vergelijk latency en kosten.
2. Maak een schema dat een lijst van geneste objecten vereist en test een lege
   lijst, één item en 100 items.
3. Voeg een `dry_run`-modus toe aan een tool met neveneffecten.
4. Schrijf een test die bewijst dat een retry niet dubbel schrijft.
5. Injecteer een time-out in een fake en bewijs dat de agent gecontroleerd stopt.
6. Maak een `Makefile` met `test`, `lint`, `run` en `deploy`.
7. Voeg een minimale trace toe en toon de volgorde van stappen in een run.
8. Simuleer een mislukte deploy en oefen de rollback hardop.
9. Schrijf een ADR over de keuze voor je outputschema.
10. Laat iemand anders je README volgen; noteer waar die struikelt.

## Fasepoort 1

- [ ] Live service op de VPS, bereikbaar via Tailscale of localhost.
- [ ] `/health` geeft 200.
- [ ] Smoke-test van het kritieke pad slaagt.
- [ ] CI bouwt en pusht een image met unieke tag of digest.
- [ ] Rollback is uitgevoerd en gelogd.
- [ ] Runbook: deploy, verify, rollback, secrets, back-up.

## Portfolio-artifact

Een casestudy van 1-2 pagina's: probleem, architectuur, schema, testaanpak,
deploybewijs, rollback, wat je anders zou doen. Link naar de commit, CI-run en
het image.
