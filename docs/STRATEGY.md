# Strategie: van agent-bouwer naar bewijsbare expert

## De these

De vraag naar "mensen die een agent kunnen demoën" daalt. De vraag naar mensen
die een agent **kunnen verantwoorden** stijgt: onder belasting, met gevoelige
data, binnen een budget, met een rollback en een postmortem. Dat is de
carrièreniche van dit programma.

Een agent in productie is geen prompt. Het is een systeem met:

- een expliciet contract en getypeerde uitvoer;
- evaluaties op een representatieve dataset;
- observeerbare runs en kosten;
- een veiligheidsmodel voor tools en data;
- een deployment-, rollback- en incidentproces;
- een architecture dat mee kan groeien met gebruik.

Wie die zes dingen kan aantonen, is schaars. Wie alleen een demo kan tonen,
concurreert met iedereen die een API-key heeft.

## Waar de markt op afknapt

De meeste agentprojecten stranden niet op het model, maar op de omgeving:

| Faalwijze | Wat er ontbreekt | Wat jij levert |
|---|---|---|
| "Het werkt lokaal" | reproduceerbare deploy en CI | image, digest, healthcheck, rollback |
| "Soms geeft hij onzin" | evaluatie en drempels | golden set, metrics, CI-poort |
| "Het is duur" | kostenmodel en caching | kosten per query, budgetten, alerts |
| "Het is traag" | loadtest en tracing | p95, bottleneck, schaalbesluit |
| "Het mag niet met klantdata" | threat model en isolatie | tenant-isolatie, filters, audit |
| "Niemand weet wat hij doet" | observability | traces, logs, runbook, SLO's |
| "Het werkt niet meer" | regressiebeheer | versiebeheer, evals, postmortem |

Dit zijn de onderwerpen die in sollicitatiegesprekken en klantgesprekken het
verschil maken. Het zijn ook precies de gate-onderwerpen van dit programma.

## Rollen en wat ze vragen

| Rol | Kernvraag | Bewijs dat je levert |
|---|---|---|
| AI Engineer | Kan je een LLM-systeem bouwen dat betrouwbaar is? | getypeerde agents, tests, evals, deploy |
| Agent Engineer | Kan je tools, planning en orkestratie beheersen? | toolcontracten, flows, failure handling |
| LLM Platform Engineer | Kan je dit voor meerdere teams/tenants draaien? | queues, isolatie, observability, SLO's |
| AI Product Engineer | Kan je een probleem valideren en snel itereren? | interviews, unit economics, capstone |
| Evaluation Specialist | Kan je kwaliteit meten en bewijzen? | golden sets, judge-calibratie, rapporten |

Je hoeft niet alle rollen te kiezen. Het programma geeft je de basis voor de
eerste drie en laat je in fase 5 een specialisatie kiezen.

## Jouw positionering

Werk toe naar een profiel als **agent reliability engineer**: iemand die een
agent niet alleen bouwt, maar ook meet, beveiligt, betaalbaar houdt en
operationeel maakt. Dat profiel is geloofwaardig als je het volgende kunt tonen:

1. **Drie gedeployde systemen** met een live URL of demo.
2. **Evaluatierapporten** met een baseline, metrics en een verbetering.
3. **Een SLO-dashboard** en een loadtest met een benoemde bottleneck.
4. **Een securityrapport** met een threat model en geslaagde injectietests.
5. **Een postmortem** met een echte oorzaak en een preventieve maatregel.
6. **Een capstone** met gebruikers, kostenmodel en een schaalplan.

Dat is je portfolio. Niet een lijst frameworks, maar een lijst bewezen
beslissingen.

## Businessidee: pas na het probleem

Een businessidee is geen startpunt; het is de uitkomst van een scherp probleem.
Daarom zit validatie pas in week 21, als je technisch kunt beoordelen wat
haalbaar en betaalbaar is.

Gebruik dit filter voordat je bouwt:

| Vraag | Bewijs |
|---|---|
| Wiens probleem is dit, en hoe vaak doet het pijn? | 10 interviews met concrete voorbeelden |
| Wat kost het probleem nu? | uren, fouten, omzetverlies, compliance-risico |
| Waarom nu, en waarom jij? | technische verandering, jouw toegang, unieke data |
| Wat is de kleinste waardevolle slice? | één workflow, één gebruiker, één meetbaar resultaat |
| Wat is de unit economics? | prijs, variabele kosten per taak, marge |
| Wat is de verdedigbaarheid? | data, integratie, workflow, niet "betere prompt" |
| Wat is het schaalpad? | [docs/SCALING.md](SCALING.md): VPS -> queue -> multi-tenant |

De regel: **geen platform bouwen voordat drie gebruikers het probleem hebben
bevestigd en een handmatige oplossing waardevol vinden.**

## Succescriteria

Het programma is geslaagd als je op het einde:

- [ ] 24 gates hebt behaald, met een examengemiddelde >= 90%.
- [ ] Minstens 3 systemen hebt gedeployed (agent, RAG, multi-agent/capstone).
- [ ] Voor elk systeem een evaluatierapport met drempels kunt tonen.
- [ ] Een loadtest en een restore-drill hebt uitgevoerd.
- [ ] Een securityreview met reele aanvalspaden kunt presenteren.
- [ ] Een capstone met 10 klantinterviews en een kostenmodel hebt.
- [ ] Een externe review met een voldoende op architectuur en communicatie hebt.
- [ ] Een portfolio van 5 casestudy's en een bijgewerkte CV/LinkedIn hebt.
- [ ] In een mock-interview een onbekend agentprobleem in 45 minuten kunt
      analyseren en verdedigen.

## Eerlijke risico's

| Risico | Realiteit | Tegenmaatregel |
|---|---|---|
| Tijd | 1 uur per dag is krap voor de capstone | bescherm de blokken; plan extra uren in week 21-24 |
| Hype | tools veranderen elke maand | leer principes en contracten, niet alleen API's |
| Modelveroudering | modellen en prijzen schuiven | provider-agnostisch ontwerpen en evalueren |
| Bekendheid | niemand ziet je werk | publieke repo's, rapporten, posts, demo's |
| Isolatie | alleen leren werkt niet | externe review, mock-interviews, gebruikers |
| Verkeerde diepte | veel tutorials, weinig bewijs | elke week een artifact en een gate |

## Wat je niet doet

- Geen tutorial-marathon zonder artifact.
- Geen frameworkhopping: PydanticAI is je kern; de rest is gericht verkennen.
- Geen platform bouwen voor een probleem dat je niet hebt gevalideerd.
- Geen "expert" claimen zonder bewijs.
- Geen gate overslaan omdat je het "al snapt".

## De kern in één zin

**Je verkoopt geen agents; je verkoopt de zekerheid dat ze werken.**
