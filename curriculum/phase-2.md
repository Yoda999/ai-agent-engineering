# Fase 2 — Kennis: retrieval, RAG en evaluatie

**Weken 7-11. Doel: een RAG-systeem dat aantoonbaar goede antwoorden geeft en
binnen je latency- en kostenbudget blijft.**

RAG is meer dan "embeddingen in een vectorstore". De kwaliteit wordt bepaald door
ingestion, chunking, metadata, retrieval, reranking en evaluatie. In deze fase
leer je elke laag meten en verbeteren.

## Wat je na deze fase kunt

- Een corpus idempotent ingesten, met metadata en versies.
- Embeddings en een vectorstore kiezen op basis van een benchmark.
- Hybride retrieval, reranking en metadatafilters toepassen.
- Een golden set bouwen en retrieval en generatie apart evalueren.
- Een eval-poort in CI zetten die regressies blokkeert.
- Latency, caching en kosten per query meten en bewaken.

## Kernconcepten

| Concept | Waarom het telt |
|---|---|
| Token en contextbudget | Bepaalt kosten en kwaliteit |
| Chunking en overlap | Bepaalt precisie versus context |
| Metadata | Filteren, citeren, toegang |
| Embeddingruimte | Een modelwissel vereist een rebuild |
| Recall@k en MRR | Retrievalkwaliteit meten |
| Faithfulness | Antwoord ondersteund door context |
| Hybride retrieval | Exacte termen plus semantiek |
| Reranker | Kwaliteit tegen extra latency |
| Golden set | Zonder dataset geen betrouwbare evaluatie |
| Cache-invalidatie | Verouderde of onbevoegde context voorkomen |
| p95 | De ervaring van trage gebruikers |

## Weekoverzicht

| Week | Onderwerp | Bouwen |
|---|---|---|
| 7 | Ingestion | Idempotente pipeline en chunkmatrix |
| 8 | Embeddings en index | Benchmark, persistentie, rebuild |
| 9 | Retrieval | Hybride, rerank, filters, citaties |
| 10 | Evaluatie | Golden set, metrics, CI-drempel |
| 11 | Observability en kosten | Traces, dashboard, cache, loadtest |

## Veelgemaakte fouten

1. **Chunkgrootte op gevoel.** Meet recall en antwoordkwaliteit per strategie.
2. **Embeddingmodel wisselen zonder rebuild.** Query- en documentvectoren komen
   dan uit verschillende ruimtes.
3. **Alleen vectorzoeken.** Exacte termen, codes en namen worden gemist.
4. **Geen metadata.** Dan kun je niet filteren, citeren of autoriseren.
5. **Evalueren met de vragen die je al kent.** De golden set moet de echte
   verdeling en randgevallen dekken.
6. **Een LLM als judge vertrouwen zonder calibratie.** Judges hebben bias.
7. **Cachen zonder invalidatie.** Je serveert verouderde of onbevoegde context.
8. **Alleen gemiddelde latency meten.** p95 en p99 verbergen zich daarachter.
9. **Geen "geen bewijs"-pad.** Een RAG-systeem moet durven zeggen dat het het
   niet weet.
10. **Kwaliteit en kosten apart optimaliseren.** Ze beïnvloeden elkaar.

## Extra oefeningen

1. Vergelijk drie chunkgroottes op dezelfde golden set.
2. Voeg een synoniemenlijst toe en meet het effect op recall.
3. Test een query met een zeldzame code; vergelijk vector-only en BM25.
4. Bouw een filter op datum en bewijs dat oude documenten verdwijnen.
5. Injecteer een regressie (slechtere prompt) en bewijs dat CI faalt.
6. Laat de judge twee keer beoordelen en meet de consistentie.
7. Cache een antwoord, wijzig het document en bewijs de invalidatie.
8. Draai een loadtest met 10, 50 en 100 gelijktijdige gebruikers.
9. Maak een kostenrapport per querytype (kort/lang/rerank).
10. Schrijf een postmortem over een query die een verkeerd antwoord gaf.

## Fasepoort 2

- [ ] Golden set >= 50 items, geversioneerd.
- [ ] Retrieval- en generatiemetrics apart gerapporteerd.
- [ ] CI faalt bij een geinjecteerde regressie.
- [ ] Loadtest met p95, foutpercentage en kosten per query.
- [ ] Bewezen `geen bewijs`-pad.
- [ ] RAG-service gedeployed en bereikbaar.

## Portfolio-artifact

Een RAG-casestudy met de ablatie (vector, hybrid, rerank), de golden set, de
metrics voor/na, het loadtestrapport en de kosten per query.
