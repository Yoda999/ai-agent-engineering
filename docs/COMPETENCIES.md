# Competentiemodel

Tien domeinen, vier niveaus. De niveaus zijn observeerbaar gedrag, geen gevoel.
Gebruik dit model om jezelf te beoordelen en om bewijs te selecteren.

## Niveaus

| Niveau | Naam | Kern |
|---|---|---|
| 0 | Oriëntatie | kent begrippen, heeft voorbeelden gezien |
| 1 | Practitioner | bouwt een werkende oplossing met begeleiding |
| 2 | Production | bouwt, test, meet en deployt zelfstandig |
| 3 | Expert | ontwerpt onder onzekerheid, verdedigt trade-offs, leidt anderen |

Het programma brengt je op niveau 2 voor de meeste domeinen en op niveau 3 voor
de domeinen die je in je capstone kiest.

## De tien domeinen

### 1. Agentontwerp

| Niveau | Gedrag |
|---|---|
| 0 | Kan uitleggen wat een agent-loop en een tool-call zijn |
| 1 | Bouwt een agent met een schema en een tool |
| 2 | Kiest tussen workflow en autonome agent, met stopcondities en foutpaden |
| 3 | Ontwerpt een agentarchitectuur die schaal, kosten en veiligheid afweegt |

### 2. Prompting en context

| Niveau | Gedrag |
|---|---|
| 0 | Kent system/user prompts en few-shot |
| 1 | Schrijft een duidelijke instructie en een schema |
| 2 | Versioneert prompts, meet effect en beheerst de contextbudgetten |
| 3 | Ontwerpt contextstrategieën (compressie, retrieval, caching) met bewijs |

### 3. Tools en integratie

| Niveau | Gedrag |
|---|---|
| 0 | Kan een tool aanroepen |
| 1 | Schrijft een getypeerde tool |
| 2 | Ontwerpt contracten met idempotentie, time-outs en foutmodellen |
| 3 | Bouwt een veilige toolplatformlaag met permissies en auditing |

### 4. Retrieval en RAG

| Niveau | Gedrag |
|---|---|
| 0 | Kent embeddings en vectorstores |
| 1 | Bouwt een basis-RAG-pijplijn |
| 2 | Kiest chunking, hybride retrieval en rerank op basis van metingen |
| 3 | Ontwerpt retrieval met toegangscontrole, versies en evaluatie op schaal |

### 5. Evaluatie

| Niveau | Gedrag |
|---|---|
| 0 | Kent accuracy en een testset |
| 1 | Draait een eval op een kleine set |
| 2 | Bouwt een golden set, kiest metrics, stelt drempels en blokkeert regressies |
| 3 | Calibreert judges, meet causaliteit en koppelt evals aan productbeslissingen |

### 6. Testing en kwaliteit

| Niveau | Gedrag |
|---|---|
| 0 | Kan een unit-test lezen |
| 1 | Schrijft tests voor eigen code |
| 2 | Bouwt een testpiramide met fakes, contracttests en CI |
| 3 | Ontwerpt een kwaliteitsstrategie voor een heel platform |

### 7. Deployment en operatie

| Niveau | Gedrag |
|---|---|
| 0 | Kan een container starten |
| 1 | Deployt met Docker Compose |
| 2 | Bouwt CI/CD, healthchecks, rollback, SLO's en alerts |
| 3 | Ontwerpt multi-tenant operatie met DR, chaos en kostenbeheersing |

### 8. Security

| Niveau | Gedrag |
|---|---|
| 0 | Kent prompt-injectie als begrip |
| 1 | Past inputvalidatie en secret-hygiëne toe |
| 2 | Maakt een threat model, test injecties en sandboxt tools |
| 3 | Ontwerpt een securityarchitectuur met least privilege en audit |

### 9. Performance en kosten

| Niveau | Gedrag |
|---|---|
| 0 | Kent tokens en latency |
| 1 | Meet latency van een call |
| 2 | Meet p95, cachet, begroot tokens en berekent kosten per request |
| 3 | Bouwt een capaciteits- en kostenmodel voor groei en meerdere tenants |

### 10. Architectuur en communicatie

| Niveau | Gedrag |
|---|---|
| 0 | Kan een diagram lezen |
| 1 | Documenteert een eigen oplossing |
| 2 | Schrijft ADR's en verdedigt trade-offs |
| 3 | Reviewt andermans architectuur en overtuigt niet-technische stakeholders |

## Zelfbeoordeling

Doe dit aan het begin van elke fase en na elke fasepoort:

1. Scoor jezelf per domein (0-3) op basis van **bewijs**, niet van gevoel.
2. Schrijf per domein één artifact op dat je score onderbouwt.
3. Kies één domein om expliciet te verbeteren in de volgende fase.
4. Laat je score uitdagen door een reviewer of door je eigen capstone.

## Koppeling met het programma

| Fase | Domeinen die centraal staan |
|---|---|
| 1 | 1, 2, 3, 6, 7 |
| 2 | 2, 4, 5, 9 |
| 3 | 1, 3, 5, 6, 10 |
| 4 | 5, 7, 8, 9, 10 |
| 5 | alle, met nadruk op 10 |

## Bewijs per niveau

- **Niveau 1:** een werkende oplossing met tests.
- **Niveau 2:** een gedeployed systeem met eval, loadtest en runbook.
- **Niveau 3:** een ontwerp dat je onder kritiek kunt verdedigen, met gemeten
  trade-offs en een bewezen schaalpad.

Een niveau claimen zonder artifact is een 0.
