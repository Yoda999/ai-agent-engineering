# Fase 5 — Capstone en carrière

**Weken 21-24. Doel: één systeem dat je trots kunt demonstreren, verdedigen en
verkopen—en een concreet plan voor de volgende stap.**

Je hebt nu de bouwstenen. Deze fase dwingt je om van features naar een product
te gaan: een echt probleem, echte gebruikers, een kostenmodel en een
verdediging tegen kritiek.

## Week 21 — Van idee naar architectuur

Een businessidee is pas bruikbaar als het probleem scherp is. Deze week praat je
met mensen, niet met een AI.

**Opdracht:**

- 10 interviews van 20-30 minuten met mensen die het probleem echt hebben.
- Een probleemstelling in één alinea: wie, wat, hoe vaak, wat kost het nu.
- Een kleinste waardevolle slice (één workflow, één gebruiker, één resultaat).
- Unit economics: prijs, variabele kosten per taak, marge.
- Een architectuurkeuze met een [schaalpad](../docs/SCALING.md) en ADR's.

**Interviewvragen die werken:**

1. Wanneer deed dit probleem zich voor het laatst voor?
2. Wat deed je toen, stap voor stap?
3. Hoeveel tijd of geld kostte dat?
4. Wat heb je al geprobeerd, en waarom werkte dat niet?
5. Wie beslist over een oplossing, en welk budget is er?
6. Wat zou een oplossing onbruikbaar maken?

**Vermijd:** "Zou je dit gebruiken?" (altijd ja) en vragen over je oplossing in
plaats van over hun probleem.

## Week 22 — Capstone sprint 1: verticale slice

Bouw de dunste werkende keten, end-to-end:

- invoer -> agent -> tool -> opslag -> antwoord;
- getypeerde output en een expliciet foutpad;
- een eval-harness met een kleine golden set;
- CI die tests en eval draait;
- een demo-opname van 2 minuten.

**Definition of done:** een gebruiker kan de slice uitvoeren, en je kunt de
kwaliteit met een cijfer onderbouwen.

## Week 23 — Capstone sprint 2: productie

- Deploy op de VPS met healthcheck en rollback.
- Loadtest op 10x verwachte belasting.
- Securityreview: threat model, injectietest, secret scan.
- Observability: traces, dashboard, SLO en alert.
- Runbook en kostenmodel.

**Definition of done:** een live URL, een groene CI, een loadtestrapport en een
rollback die je hebt uitgevoerd.

## Week 24 — Verdediging en carrière

De eindverdediging is een gesprek van 45-60 minuten met een externe reviewer:

1. **Probleem en gebruiker** (5 min): wie, wat, waarom nu.
2. **Architectuur** (10 min): grenzen, data, tools, foutpaden, schaalpad.
3. **Evaluatie** (10 min): dataset, metrics, drempels, resultaten, fouten.
4. **Operatie en security** (10 min): SLO's, incidenten, threat model, restore.
5. **Demo** (10 min): het kritieke pad, inclusief een foutscenario.
6. **Kritiek** (10 min): de reviewer valt je aannames aan; jij verdedigt of
   herziet ze.

**Rubric:** zie [docs/COMPETENCIES.md](../docs/COMPETENCIES.md) en
[docs/GATES.md](../docs/GATES.md). Een 1 op security of operatie is een harde
fail.

## Portfolio

Vijf casestudy's, elk volgens hetzelfde sjabloon:

1. De getypeerde agent met deploy en rollback (fase 1).
2. De RAG-service met evaluatie en loadtest (fase 2).
3. Het multi-agent systeem met trajectory-evals (fase 3).
4. De productie-review met security en SLO's (fase 4).
5. De capstone met gebruikers, kosten en schaalplan (fase 5).

Elke casestudy bevat: probleem, constraints, aanpak, bewijs, resultaat en wat je
anders zou doen. Geen screenshots zonder cijfers.

## CV en LinkedIn

- **Kop:** "AI/agent engineer — betrouwbare LLM-systemen die ik kan meten,
  beveiligen en deployen."
- **Bewijs:** links naar repo's, live demo's, eval-rapporten en casestudy's.
- **Resultaten:** "p95 van 4,2 s naar 1,1 s", "kosten per taak -38%",
  "faithfulness 0,93 op 120 gelabelde vragen".
- **Vaardigheden:** PydanticAI, LlamaIndex, CrewAI, DSPy, Python, Docker,
  GitHub Actions, Postgres, OpenTelemetry, evaluatie, security.
- **Geen:** "leergierig", "passie voor AI", een lijst van 30 frameworks.

## Solliciteren en freelance

| Stap | Actie | Bewijs |
|---|---|---|
| 1 | 20 gerichte gesprekken (niet 200 sollicitaties) | lijst met namen en data |
| 2 | Per gesprek één casestudy op maat | gedeelde link |
| 3 | Mock-interview: agent-systemdesign in 45 min | opname + feedback |
| 4 | Proefopdracht of betaald pilotproject | oplevering + evaluatie |
| 5 | Onderhandelen op waarde, niet op uurtarief | marge en risico |

**Prijszetting:** kijk naar de waarde (uren of omzet die je bespaart), niet naar
je uurtarief. Reken de variabele kosten (tokens, infra, support) mee in je marge.
Begin met een pilot met een vaste scope en een meetbaar resultaat.

## Na week 24: de 12-maandenroute

| Maand | Focus |
|---|---|
| 7 | Nieuw project vanaf nul, zonder curriculum |
| 8 | Open source-bijdrage (PydanticAI, LlamaIndex of DSPy) |
| 9 | Specialisatie: evaluatie, RAG, security of platform |
| 10 | Capstone met echte gebruikers en iteratie op data |
| 11 | Sollicitatie- of freelance-ronde met portfolio |
| 12 | Eindexamen: onbekend agentprobleem in 4 uur |

Blijf je kaarten herhalen en je eval-datasets onderhouden. Expertise is een
praktijk, geen diploma.

## De laatste checklist

- [ ] 24 gates behaald.
- [ ] 5 casestudy's gepubliceerd.
- [ ] Capstone live met SLO-dashboard.
- [ ] Externe review met gemiddeld >= 3,0.
- [ ] CV en LinkedIn bijgewerkt met cijfers.
- [ ] 20 gesprekken gevoerd of gepland.
- [ ] Een concreet plan voor de volgende 90 dagen.
