# Schalen: van één VPS naar een schaalbaar platform

De huidige opzet (Docker Compose op één VPS) is bewust. Voor een eerste product
met tientallen gebruikers is dat vaak genoeg. Schalen is geen doel op zich; het
is een reactie op gemeten grenzen.

## Het principe

**Bouw nu voor één machine, met naden die later kunnen scheuren.**

Concreet:

- stateless proceslogica, state in een database of queue;
- geen lokale bestanden als waarheid;
- configuratie via env, geen hardcoded paden;
- idempotente taken;
- healthchecks en metrics vanaf dag 1;
- een duidelijke grens tussen domein, adapters en transport.

Als je die naden goed legt, is de stap naar meerdere workers of een managed
platform een configuratiewijziging, geen herschrijving.

## De vijf stadia

### Stadium 0 — één VPS (nu)

```text
        Tailscale / localhost
                |
        ┌───────▼────────┐
        │  reverse proxy │
        └───┬────────┬───┘
            │        │
      ┌─────▼──┐  ┌──▼─────┐
      │  api   │  │ worker │
      └────┬───┘  └──┬─────┘
           │         │
        ┌──▼─────────▼──┐
        │ SQLite (WAL)  │
        └───────────────┘
```

- **Geschikt voor:** 1-50 gebruikers, één tenant, lage gelijktijdigheid.
- **Bewaking:** p95, foutpercentage, schijf, geheugen, back-up.
- **Niet doen:** horizontaal schalen van SQLite, lange taken in de request-cyclus.

### Stadium 1 — geharde single node

- 4-8 GB RAM, 2-4 vCPU.
- Postgres in plaats van SQLite als meerdere processen schrijven.
- Redis of een database-queue voor achtergrondtaken.
- Object storage (S3-compatible) voor documenten en artefacten.
- Managed back-ups en een geteste restore.
- Rate limiting en tokenbudgetten per gebruiker.

**Trigger:** schrijfacties van meerdere processen, of back-up/restore wordt
riskant, of de wachtrij groeit.

### Stadium 2 — gescheiden componenten

```text
              ┌──────────────┐
   clients ──▶│ load balancer│
              └──┬────────┬──┘
          ┌──────▼──┐  ┌──▼───────┐
          │ api x N │  │ dashboard│
          └────┬────┘  └────┬─────┘
               │            │
        ┌──────▼────────────▼──────┐
        │ Postgres + queue (Redis) │
        └──────┬───────────┬───────┘
          ┌────▼────┐  ┌───▼─────┐
          │worker xN│  │ vector  │
          └─────────┘  └─────────┘
```

- API is stateless; workers schalen onafhankelijk.
- Queue met idempotency keys, retries, dead-letter queue en backpressure.
- Vectorstore apart (pgvector is vaak genoeg; dedicated store bij grote schaal).
- Observability: traces over API, queue en worker.

**Trigger:** API en workers concurreren om dezelfde resources, of de queue
loopt achter, of je wilt onafhankelijk deployen.

### Stadium 3 — managed platform of orchestratie

- Managed containers (Fly.io, Render, Cloud Run, ECS) of Kubernetes.
- Autoscaling op queue depth en latency, niet op CPU alleen.
- Managed Postgres met replicas en point-in-time recovery.
- CDN en edge caching voor statische delen.
- Per-tenant quotas en kostenallocatie.

**Trigger:** meerdere tenants, elasticiteit nodig, of het beheren van servers
kost meer dan het oplevert.

### Stadium 4 — enterprise en multi-regio

- Dataresidentie en tenant-isolatie op database- of regio-niveau.
- SSO/SAML, audit logging, sleutelbeheer.
- Disaster recovery met RPO/RTO-afspraken.
- FinOps: kosten per tenant, per taak en per model.

**Trigger:** contractuele eisen, compliance, of significante groei.

## Wanneer schalen? Meetbare triggers

| Signaal | Drempel | Eerste actie |
|---|---|---|
| p95 latency | boven SLO bij normaal verkeer | profileren, cachen, query's optimaliseren |
| CPU | > 70% gedurende 15 min | verticale upgrade of workers splitsen |
| Geheugen | > 80% structureel | lekken zoeken, index/embedding verplaatsen |
| Queue depth | groeit 30 min onafgebroken | meer workers, backpressure |
| Foutpercentage | > 1% | rollback of fix, pas daarna schalen |
| Gelijktijdige gebruikers | boven getest maximum | loadtest, dan horizontaal |
| Databasegrootte | > 50 GB of trage queries | partitioneren, replicas, aparte store |
| Aantal tenants | > 20 met strikte isolatie | tenant-model herzien |
| Kosten per taak | boven je marge | model/caching/architectuur |

**Regel:** schaal nooit op een gevoel. Een loadtest met een cijfer is de basis.

## Multi-tenancy

| Model | Isolatie | Kosten | Wanneer |
|---|---|---|---|
| Gedeelde database, `tenant_id` | laag | laag | vroege fase, laag risico |
| Schema per tenant | middel | middel | compliance, middelgrote klanten |
| Database per tenant | hoog | hoog | enterprise, strikte scheiding |
| Eigen deployment per tenant | zeer hoog | zeer hoog | uitzonderingen, dedicated |

Kies op basis van **data-gevoeligheid en contracten**, niet van gemak. Leg de
keuze vast in een ADR en test dat een tenant nooit data van een ander ziet.

## De queue als ruggengraat

Een productiewaardige agent doet niet alles in het request:

- **Idempotency key** per taak, zodat een retry geen dubbele actie geeft.
- **Retries** met backoff en een maximum.
- **Dead-letter queue** voor taken die blijven falen.
- **Backpressure** als de wachtrij te lang wordt.
- **Timeout per taak** en een maximale looptijd.
- **Prioriteit** voor interactieve taken boven batch.
- **Tokenbudget** per taak, tenant en dag.

## Data en retrieval op schaal

- Begin met Postgres + pgvector; dat is één systeem minder.
- Stap over naar een dedicated vectorstore als recall/latency of datasetgrootte
  dat eist, niet omdat het hip is.
- Houd een corpusversie en een indexversie bij; herbouw is een routine, geen
  incident.
- Partitioneer documenten per tenant en pas toegangsfilters toe in de query,
  niet in de prompt.

## Kostenmodel

```text
kosten per taak =
  tokens_in * prijs_in
+ tokens_uit * prijs_uit
+ embeddings
+ rerank
+ infra / taken
+ opslag
+ egress
```

Maak dit meetbaar per tenant en per taak. Zet alarmen op de marge, niet alleen op
de omzet. Een agent die 0,02 euro per taak kost en 0,01 euro oplevert, schaalt
zichzelf kapot.

## Wat je niet doet

- Kubernetes op dag 1.
- Microservices zonder gemeten grens.
- Multi-regio voordat je één regio betrouwbaar hebt.
- Een eigen vectorstore bouwen.
- Schalen voordat de foutpercentages onder controle zijn.
- Een platform bouwen voordat drie gebruikers het probleem bevestigen.

## Checklist voor de schaalbeslissing

- [ ] Ik heb een loadtest met p95, foutpercentage en doorvoer.
- [ ] Ik weet welke resource de bottleneck is.
- [ ] Ik heb de kosten per taak en per tenant.
- [ ] Ik heb een rollback en een restore getest.
- [ ] Ik heb de tenant- en data-isolatie getest.
- [ ] Ik heb een ADR met de gekozen stap en de verworpen alternatieven.
- [ ] Ik heb een trigger gedefinieerd voor de volgende stap.

## Migratiepad vanuit de huidige repo's

1. Behoud de domeinlogica en tests; vervang alleen de adapters.
2. Haal state uit het proces: database, queue, object storage.
3. Maak elk proces idempotent en herstartbaar.
4. Voeg health, metrics en traces toe aan elk proces.
5. Scheid API en worker; deploy ze onafhankelijk.
6. Verplaats naar managed Postgres en object storage.
7. Zet autoscaling op queue depth, niet op CPU.
8. Bewijs met een loadtest en een chaos-test.

Elke stap is een aparte PR met een eigen bewijsstuk. Geen big bang.
