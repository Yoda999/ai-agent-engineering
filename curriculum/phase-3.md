# Fase 3 — Orkestratie: multi-agent en optimalisatie

**Weken 12-16. Doel: een multi-agent systeem dat je kunt testen, observeren en
aantoonbaar verbeteren.**

Multi-agent systemen zijn geen automatisch betere systemen. Ze voegen
coördinatie, kosten en faalmodi toe. Je leert wanneer je ze nodig hebt, hoe je
ze deterministisch maakt en hoe je ze meet.

## Wat je na deze fase kunt

- Rollen, taken en crews ontwerpen en de proceskeuze onderbouwen.
- Tools en een MCP-server integreren met een permissiematrix.
- Memory (kort en lang) toevoegen zonder geheimen of ruis te lekken.
- Een deterministische flow bouwen met events, retries en human-in-the-loop.
- Multi-agent trajecten evalueren en per agent kosten en latency meten.
- DSPy gebruiken om een programma te compileren en de winst te bewijzen.

## Kernconcepten

| Concept | Waarom het telt |
|---|---|
| Role, task, crew | De basis van CrewAI; slechte taken geven slechte output |
| Sequential vs hierarchical | Deterministisch versus dynamisch; kies bewust |
| MCP | Gestandaardiseerde tooltoegang met eigen permissies |
| Memory | Korte termijn, lange termijn, en wat je niet mag bewaren |
| Flow vs autonome agent | Voorspelbaarheid versus flexibiliteit |
| Event-driven | Losse koppeling, retries, herbouwbaarheid |
| Human-in-the-loop | Goedkeuring bij risicovolle acties |
| Failure injection | Bewijs dat je systeem niet stilletjes vastloopt |
| Trajectory-eval | Beoordeel de weg, niet alleen het eindantwoord |
| DSPy signature | Een getypeerd contract voor een LM-taak |
| Optimizer | Prompt/programma verbeteren op een metric, niet op gevoel |

## Weekoverzicht

| Week | Onderwerp | Bouwen |
|---|---|---|
| 12 | CrewAI basis | Drie-rollen crew met fake-LLM-tests |
| 13 | Tools, MCP, memory | MCP-tool, memory, permissiematrix |
| 14 | Flows en events | Flow met retries, HITL, failure injection |
| 15 | Testen en observability | 20 trajectory-evals, traces, deadlocktests |
| 16 | DSPy | Signature, metric, optimizer, CI-regressie |

## Veelgemaakte fouten

1. **Multi-agent als doel.** Begin met één agent en voeg rollen toe als de taak
   echt verschillende expertise of verantwoordelijkheden vraagt.
2. **Taken te vaag.** Een taak zonder concreet deliverable en acceptatiecriteria
   geeft eindeloze gesprekken.
3. **Geen stopconditie.** Zonder maximum stappen en time-out loop je vast of
   verbrand je tokens.
4. **Memory als vuilnisbak.** Bewaar geen secrets, ruwe PII of irrelevante
   gesprekken.
5. **MCP zonder permissies.** Een MCP-server is een aanvalsoppervlak; beperk
   tools en rechten.
6. **Flows en crews verwarren.** Een flow is deterministisch; een crew is
   flexibel. Kies op basis van de eis, niet van de demo.
7. **Alleen het eindantwoord beoordelen.** Een goed antwoord via een gevaarlijk
   pad is nog steeds fout.
8. **DSPy zonder dataset.** Optimaliseren zonder representatieve set is
   overfitting op ruis.
9. **Geen baseline.** Zonder before/after kun je geen winst bewijzen.
10. **Kosten negeren.** Meer agents betekent meer calls; meet de prijs van de
    kwaliteitswinst.

## Extra oefeningen

1. Bouw dezelfde taak met één agent en met drie rollen; vergelijk kwaliteit,
   latency en kosten.
2. Voeg een reviewer-rol toe die output afkeurt en een herziening afdwingt.
3. Maak een taak met een harde maximumduur en test de time-out.
4. Injecteer een valse toolrespons en test of de crew herstelt.
5. Bouw een MCP-server met twee tools en een read-only permissie.
6. Test memory: wat wordt bewaard, wat niet, en hoe verwijder je het?
7. Laat een flow wachten op goedkeuring en test beide paden.
8. Evalueer 20 trajecten met een rubric en bereken de inter-beoordelaar-
   betrouwbaarheid.
9. Compileer een DSPy-programma met 30 voorbeelden en test op 20 unseen.
10. Vergelijk een handgeschreven prompt met een geoptimaliseerde prompt op
    dezelfde set en rapporteer kosten en kwaliteit.

## Fasepoort 3

- [ ] 20 trajectory-evaluaties met rubric.
- [ ] Per-agent traces en kosten.
- [ ] Timeout-, deadlock- en failure-injection-tests.
- [ ] DSPy before/after op dezelfde dataset.
- [ ] >= 10% kwaliteitswinst of >= 30% kostenreductie bij gelijke kwaliteit.
- [ ] CI-regressiepoort voor kwaliteit.

## Portfolio-artifact

Een multi-agent casestudy met het rolontwerp, de flow, de trace van een
mislukking en het herstel, de trajectory-scores en de DSPy-vergelijking.
