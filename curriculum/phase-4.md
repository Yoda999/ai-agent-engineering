# Fase 4 — Productie: security, schaal en betrouwbaarheid

**Weken 17-20. Doel: een systeem dat je durft open te zetten voor echte
gebruikers en dat je kunt verdedigen bij een security- of operations-review.**

Tot nu toe heb je gebouwd en gemeten. Nu harden je: aanvalsoppervlak, evaluatie
op schaal, gelijktijdigheid, multi-tenancy, SLO's en herstel.

## Wat je na deze fase kunt

- Een threat model maken voor een agent met tools en gevoelige data.
- Prompt-injectie en toolmisbruik testen en mitigeren.
- Een eval-harness met judge-calibratie en regressiebeleid beheren.
- Een queue, rate limits en tenant-isolatie ontwerpen.
- SLO's, alerts en een incidentproces opzetten.
- Een back-up restore en een chaos-test uitvoeren en beoordelen.

## Kernconcepten

| Concept | Waarom het telt |
|---|---|
| Threat modeling | Je kunt niet mitigeren wat je niet benoemt |
| Prompt-injectie | Elk document en elke tool-output is potentieel vijandig |
| Least privilege | Beperk de impact van een gecompromitteerde tool |
| Sandboxing | Voer onbetrouwbare code/data geïsoleerd uit |
| Judge-calibratie | Een judge is een meetinstrument, geen orakel |
| Datasetversie | Zonder versie geen reproduceerbare evaluatie |
| Queue en backpressure | Voorkomt omvallen onder piekbelasting |
| Multi-tenancy | Data-isolatie is een contract, geen instelling |
| SLO en error budget | Maakt betrouwbaarheid een meetbare afspraak |
| Restore-drill | Een back-up die je nooit test, is geen back-up |
| Chaos-test | Bewijst dat je systeem tegen een echte fout kan |
| Postmortem | Leert zonder schuld; voorkomt herhaling |

## Weekoverzicht

| Week | Onderwerp | Bouwen |
|---|---|---|
| 17 | Security | Threat model, injectiesuite, sandbox |
| 18 | Evaluatie op schaal | Judge-calibratie, regressiedashboard |
| 19 | Performance en tenancy | Queue, rate limits, loadtest 10x |
| 20 | Reliability | SLO's, alerts, restore, chaos, postmortem |

## Veelgemaakte fouten

1. **Security als checklist.** Een threat model zonder aanvalspaden is een
   formaliteit.
2. **Injectie alleen in de prompt zoeken.** Documenten, tool-output en
   e-mailteksten zijn evengoed invoer.
3. **Tools met te veel rechten.** Eén SQL-tool met schrijfrechten kan je hele
   database kosten.
4. **Judge blind vertrouwen.** Meet de agreement met menselijke labels.
5. **Dataset in een spreadsheet zonder versie.** Dan is een regressie niet
   reproduceerbaar.
6. **Rate limits per IP alleen.** Tenants en gebruikers hebben eigen quota nodig.
7. **SLO's zonder alert of eigenaar.** Een dashboard dat niemand bekijkt is
   decoratie.
8. **Back-up zonder restore.** De eerste restore is te laat als hij faalt.
9. **Chaos zonder hypothese.** Test een concreet faalscenario met een verwachting.
10. **Postmortem met een schuldige.** Dan verbergt de volgende persoon de fout.

## Extra oefeningen

1. Schrijf een threat model voor een agent die e-mail leest en agenda's wijzigt.
2. Bouw een injectietest met een kwaadaardig document en bewijs de mitigatie.
3. Geef een tool read-only rechten en test dat een schrijfactie faalt.
4. Laat een judge 50 antwoorden beoordelen en vergelijk met 10 menselijke labels.
5. Versioneer een dataset, wijzig één label en bewijs het verschil in uitkomst.
6. Test een queue met 100 taken en een falende worker; bewijs de retry en DLQ.
7. Isoleer twee tenants en test een query die data van de ander probeert te lezen.
8. Stel een SLO in en simuleer een burn rate die een alert triggert.
9. Voer een restore uit op een schone machine en meet de RTO.
10. Draai een chaos-test (database traag, provider 503) en schrijf een postmortem.

## Fasepoort 4

- [ ] Threat model met reele aanvalspaden en maatregelen.
- [ ] Geslaagde prompt-injectiesuite.
- [ ] Judge-calibratie met menselijke steekproef.
- [ ] Loadtest op 10x verwachte belasting.
- [ ] Restore-drill en chaos-test uitgevoerd.
- [ ] Postmortem met preventieve maatregel.

## Portfolio-artifact

Een productie-review: threat model, SLO-dashboard, loadtestgrafiek,
restore-log, chaos-resultaat en postmortem. Dit is het bewijs dat je een
systeem kunt draaien, niet alleen bouwen.
