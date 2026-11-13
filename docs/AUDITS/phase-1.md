# Bronaudit fase 1 — 13 november 2026

**Scope:** `assessments/phase-1.yaml`, weken 1-6: 30 meerkeuzevragen, 6 open
vragen, 30 kaarten en alle buildstappen.

**Methode:** elke API- en conceptclaim is opnieuw getoetst aan de officiële
PydanticAI-documentatie (release **v2.65.0**, 2 november 2026), de Docker- en
Kubernetes-documentatie. Daarna zijn alle antwoordsleutels opnieuw afgeleid en
zijn de vragen, uitleg, kaarten en buildstappen gecontroleerd op precisie.

**Resultaat:** **0 foute antwoordsleutels.** Wel 15 bevindingen en 49
gewijzigde regels in fase 1, vooral precisie: retrybudgetten, de rol van `TestModel`,
foutafhandeling bij tools, healthchecks en image-tags. Geen enkele drempel is
verlaagd; de testopdracht in week 1 is juist strenger geworden.

## Bevindingen

| # | Week | Bevinding | Correctie | Ernst |
|---|---|---|---|---|
| 1 | 1 | `Agent(output_type=...)` zonder model is toegestaan, maar onduidelijk voor een eerste agent. | Bouwstap maakt expliciet `Agent('test', ...)` voor tests en een provider-model voor de echte run. | midden |
| 2 | 1 | `TestModel` test geen ongeldige modeloutput: het genereert schema-geldige data en roept standaard alle tools aan. | Buildstap splitst contracttests (`TestModel`), inputvalidatie en een foutpad met `FunctionModel`. Challenge-eis uitgebreid. | **hoog** |
| 3 | 1 | De uitleg suggereerde een onbeperkte retry bij een validatiefout. | Retrybudget expliciet: standaard 1, configureerbaar met `Agent(retries={'output': N})`. | midden |
| 4 | 1 | Rubriekpunt "de agent is deterministisch" is onjuist: de agent is deterministisch *testbaar*. | Geformuleerd als "geïsoleerd en deterministisch testbaar met TestModel/fakes". | **hoog** |
| 5 | 2 | `UsageLimits` is breder dan requests en tokens. | Aangevuld met `request_limit`, `tool_calls_limit`, tokens en kosten; en dat SDK-/transportretries buiten `request_limit` vallen. | midden |
| 6 | 2 | "Timeout per run" noemde de API niet. | Concreet: `agent.run(..., timeout=...)`. | laag |
| 7 | 3 | De uitleg deed alsof je zelf een retry moet initiëren. | PydanticAI doet dit automatisch binnen het output-retrybudget (standaard 1); daarna fout of fallback. | midden |
| 8 | 3 | `NativeOutput` werd voorgesteld als algemeen beschikbaar. | Nuance: provider-afhankelijk; applicatievalidatie blijft nodig. | midden |
| 9 | 3 | "Fout JSON" testen is niet realistisch bij tool-output. | Ongeldige modeloutput simuleren met `FunctionModel`; inputs apart testen. | midden |
| 10 | 4 | "Fouten als data" was te algemeen: een gewone exception stopt de run. | `ModelRetry` voor correctie, `ToolFailed` voor terminale fout, gewone exception aborts. | **hoog** |
| 11 | 4 | Toolschema komt niet alleen uit type hints en docstring. | Ook parameterbeschrijvingen en `Field(description=...)` toevoegen. | laag |
| 12 | 5 | Trace-ID werd beschreven als causale volgorde. | Trace-ID correleert; de span-hiërarchie geeft de causale volgorde. | midden |
| 13 | 6 | Healthcheck en "verkeer mogen ontvangen" werden vereenzelvigd. | Docker/Compose gebruikt de healthstatus; Kubernetes gebruikt aparte liveness- en readiness-probes. | **hoog** |
| 14 | 6 | "Immutable tag" is geen standaard Docker-eigenschap. | Unieke tag of digest; tags zijn muteerbaar, digest niet. | midden |
| 15 | 1-5 | Referenties verwezen naar `ai.pydantic.dev`, dat is verhuisd. | Links bijgewerkt naar `pydantic.dev/docs/ai/...`; retry-referentie naar de echte retrypagina. | laag |

## Wat niet is gewijzigd

- **Geen antwoordsleutel** is veranderd; alle 30 MCQ-antwoorden blijven staan.
- **Geen examendrempel** of Challenge-criterium is verlaagd.
- De antwoordsleutels zijn ongewijzigd. Week 6 vraag 2 is opnieuw geformuleerd
  ("unieke tag of digest") en enkele opties zijn preciezer gemaakt; het juiste
  antwoord blijft C.
- De boekverwijzingen (hoofdstuk en pagina) zijn ongewijzigd; de boeken blijven
  de bron voor de weekstof, de docs de bron voor de API.

## Kernbewijs uit de documentatie

- **TestModel:** "unit tests check your own code around the model: tools,
  dependencies, output validation and failure handling, with no model requests
  and the same result every run."
  ([testing](https://pydantic.dev/docs/ai/guides/testing/))
- **Standaard output:** "In the default Tool Output mode, the output JSON schema
  of each output type [...] is provided to the model as the parameters schema of
  a special output tool."
  ([output](https://pydantic.dev/docs/ai/core-concepts/output/))
- **Retrybudget:** "The default retry count is **1** but can be altered for the
  entire agent with `retries`."
  ([agent](https://pydantic.dev/docs/ai/core-concepts/agent/))
- **Toolfouten:** "Any other exception propagates out of the agent run and is
  not sent back to the model." `ModelRetry` vraagt om correctie, `ToolFailed`
  meldt een terminale fout.
  ([tools-advanced](https://pydantic.dev/docs/ai/tools-toolsets/tools-advanced/))
- **UsageLimits:** "limit your usage (tokens, requests, tool calls, and cost) on
  model runs."
  ([agent](https://pydantic.dev/docs/ai/core-concepts/agent/#usage-limits))
- **Docker:** "The HEALTHCHECK instruction tells Docker how to test a container
  to check that [...] process is still running."
  ([Docker](https://docs.docker.com/reference/dockerfile/#healthcheck))
- **Kubernetes:** liveness, readiness en startup zijn aparte probes; Kubernetes
  gebruikt de Docker-healthcheck niet als readiness-signaal.
  ([Kubernetes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/))

## Nuances die je moet kennen

1. **Boeken versus docs.** De boeken zijn van september-oktober 2026 en noemen
   PydanticAI 2.x; de docs lopen sneller. Bij een conflict wint de docs. Noteer
   afwijkingen in je project-`NOTES.md`.
2. **TestModel is deterministisch, niet semantisch.** Het genereert schema-geldige
   data en roept tools aan. Of het antwoord inhoudelijk goed is, meet je met
   evals, niet met `TestModel`.
3. **Retrybudgetten stapelen.** PydanticAI-outputretries, toolretries,
   provider-SDK-retries en transportretries hebben eigen budgetten. Kies één
   eigenaar voor het retrybeleid en begrens de rest.
4. **`UsageLimits` begrenst niet alles.** Het telt committed modelresponses;
   SDK- en transportretries eronder vallen erbuiten. Gebruik ook timeouts en
   providerinstellingen.
5. **`NativeOutput` is niet overal beschikbaar.** Sommige providers hebben
   beperkingen of schema-complexiteitslimieten; valideer altijd zelf.
6. **Docker-healthcheck ≠ Kubernetes-readiness.** Docker/Compose gebruikt de
   healthstatus; Kubernetes negeert `HEALTHCHECK` en gebruikt probes.
7. **Tags zijn muteerbaar.** Gebruik een digest of een unieke tag en zet
   registry-immutabiliteit aan waar dat kan.

## Bronnen

- PydanticAI — Unit testing: https://pydantic.dev/docs/ai/guides/testing/
- PydanticAI — Output modes en retries: https://pydantic.dev/docs/ai/core-concepts/output/
- PydanticAI — Agent en UsageLimits: https://pydantic.dev/docs/ai/core-concepts/agent/
- PydanticAI — Retries: https://pydantic.dev/docs/ai/core-concepts/retries/
- PydanticAI — Tool failures: https://pydantic.dev/docs/ai/tools-toolsets/tools-advanced/
- PydanticAI — Timeouts: https://pydantic.dev/docs/ai/core-concepts/timeouts/
- Docker — HEALTHCHECK: https://docs.docker.com/reference/dockerfile/#healthcheck
- Kubernetes — Liveness, readiness en startup probes:
  https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

## Verificatie

Na de correcties:

```bash
PYTHONPATH=src python3 -m aae validate
# Alle 24 weken zijn structureel geldig.

PYTHONPATH=src python3 -m unittest discover -s tests
# Ran 30 tests ... OK
```

## Conclusie

Fase 1 is inhoudelijk bruikbaar om mee te starten. De antwoorden waren juist; de
correcties gaan over precisie en over hoe je de concepten in code toepast. De
belangrijkste les voor de learner: **een groene test met `TestModel` bewijst je
contract, niet de kwaliteit van je agent.** Daarvoor heb je evals en
`FunctionModel`-scenario's nodig.
