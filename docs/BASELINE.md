# Nulmeting: waar sta je nu?

Doe deze meting **voor** je begint, gesloten boek, zonder AI. Het is geen
examen en er hangt geen gate aan; het kalibreert je startpunt en je planning.
Schrijf je antwoorden op en vergelijk ze met de sleutel onderaan.

## De vragen (30 minuten)

1. Wat is het verschil tussen een LLM-call en een agent-loop?
2. Waarom is een expliciet outputschema beter dan "geef JSON terug" in de prompt?
3. Wat doet een retry bij een validatiefout, en wanneer stop je?
4. Noem drie eigenschappen van een goede tooldefinitie.
5. Wat is idempotentie en waarom is het belangrijk bij tools met neveneffecten?
6. Wat is het verschil tussen een unit-test, een contracttest en een evaltest?
7. Wat bewijst een groene CI-run wel en niet?
8. Waarom is `latest` als image-tag gevaarlijk in productie?
9. Wat is een embeddingsmodel en wat gebeurt er als je van model wisselt?
10. Noem twee retrievalmetrics en twee generatiemetrics.
11. Wat is prompt-injectie en noem twee mitigaties.
12. Wat is een SLO en hoe verschilt die van een SLA?
13. Wanneer is een multi-agent systeem een slechte keuze?
14. Wat doet een optimizer in DSPy, en wat heb je nodig om hem eerlijk te
    evalueren?
15. Noem drie dingen die een agentproductiechecklist minimaal moet bevatten.

## Sleutel (kort)

1. Een LLM-call is één modelaanroep; een agent-loop herhaalt modelbeslissingen en
   toolresultaten tot een eindantwoord of stopconditie.
2. Een schema is een contract dat je valideert en test; een promptinstructie is
   een verzoek dat het model kan negeren.
3. Je stuurt de validatiefout terug en probeert opnieuw binnen een maximum;
   daarna fallback of gecontroleerd falen.
4. Duidelijke naam en beschrijving, getypeerde argumenten, begrensde rechten,
   time-out, gedocumenteerde fouten.
5. Dezelfde operatie met dezelfde sleutel heeft eenmalig effect, ook bij retries.
6. Unit: geïsoleerde logica; contract: afspraak met een adapter/tool; eval:
   kwaliteit op een dataset.
7. Dat build en tests reproduceerbaar slagen; niet dat de businesslogica of
   veiligheid correct is.
8. Je weet niet welke versie draait en kunt niet betrouwbaar terugrollen.
9. Een model dat tekst naar vectoren vertaalt; een wissel vereist opnieuw
   embedden en indexeren.
10. Retrieval: recall@k, MRR. Generatie: faithfulness, answer correctness
    (of een judge-score).
11. Kwaadaardige instructies in invoer/documenten/tooloutput; mitigeer met
    scheiding van data en instructies, input/output-guards, least privilege en
    sandboxing.
12. Een SLO is een intern betrouwbaarheidsdoel; een SLA is een contractuele
    afspraak met consequenties.
13. Als het werk niet opdeelbaar is, één agent volstaat, of de coördinatie- en
    kostenlast niet tegen de kwaliteitswinst opweegt.
14. Een programma compileren/verbeteren op een metric met voorbeelden; je hebt
    een representatieve dataset, een baseline en een hold-out set nodig.
15. Bijvoorbeeld: secrets buiten code/image, usage limits, guardrails, rate
    limits, healthcheck, rollback, observability, backup.

## Interpretatie

| Score | Betekenis | Start |
|---|---|---|
| 0-4 | Veel is nieuw | Week 1, normaal tempo |
| 5-8 | Basis aanwezig, gaten | Week 1, extra aandacht voor testen/deploy |
| 9-12 | Ervaren | Week 1, maar je kunt twee blokken per dag doen |
| 13-15 | Sterk | Week 1 versneld; gates blijven verplicht |

Ook bij een hoge score sla je geen gate over. De waarde zit in het bewijs, niet
in het tempo. Een hoge nulmeting betekent wel dat je sneller door de theorie
kunt en meer tijd aan de challenge kunt besteden.

## Bewaar je score

```bash
aae log 30 --note "nulmeting: X/15"
aae evidence --week 1 --kind nulmeting --ref "score X/15"
```

Vergelijk na fase 1 je score met je examenresultaten. Als je nulmeting hoog was
maar je examens laag, is er een verschil tussen herkennen en kunnen toepassen;
dat is precies wat de gates meten.
