# Bronnen: wat is leidend?

Je hebt zeven boeken en zes frameworks. Zonder bronhiërarchie wordt leren
gokken. Deze pagina legt vast wat wanneer leidend is.

## De hiërarchie

| Prioriteit | Bron | Waarvoor | Voorbeeld |
|---|---|---|---|
| 1 | **Officiële documentatie en release notes** | API's, flags, versies, gedrag | PydanticAI 2.65 docs, Docker-docs |
| 2 | **AI Engineering (Huyen)** | Concepten, evaluatie, trade-offs, waarom | Waarom een judge bias heeft |
| 3 | **De zes frameworkboeken** | Concrete patronen en code per framework | Een PydanticAI-tool, een CrewAI-flow |
| 4 | **Standaarden en praktijk** | Security, SRE, compliance | OWASP LLM Top 10, Google SRE |
| 5 | **Je eigen tests en evaluaties** | Wat jouw systeem echt doet | `pytest`, eval-rapport, loadtest |

De volgorde is geen mening: een boek kan verouderd zijn, docs niet. Bij een
conflict wint de hoogste bron. Als je eigen test iets anders laat zien dan een
boek, wint je test — mits de test representatief is.

## Twee leeslagen per week

Elke week heeft:

1. **Concept (10 min):** een Huyen-selectie met één reflectievraag.
2. **Praktijk (10 min):** de frameworkpagina's die je voor de build nodig hebt.
3. **Naslag:** de rest van de hoofdstukken; je leest ze als de build daarom
   vraagt.

De Huyen-pagina's zijn **PDF-pagina's** van de editie in
`/home/yoda/Documents/Boeken/AI Engineering by Chip Huyen.pdf` (991 p.), geen
gedrukte paginanummers. De frameworkboeken gebruiken gedrukte pagina's. Zie
[READING-MAP.md](READING-MAP.md).

## De reflectie is bewijs

Na het conceptlezen schrijf je vijf regels antwoord op de vraag en voegt die toe:

```bash
aae evidence --week 3 --kind concept --ref "h.3: perplexity is geen kwaliteitsmetric"
```

De gate controleert dat er per week een conceptreflectie is. Zonder reflectie
geen groene gate. Dat is bewust: lezen zonder verwerken is geen studie.

## Bij een conflict

| Situatie | Wat je doet |
|---|---|
| Boek en docs verschillen over een API | Docs volgen; verschil noteren in je project-`NOTES.md` |
| Huyen en een frameworkboek verschillen over een concept | Beide lezen; kies op basis van je gemeten resultaat |
| Je test faalt terwijl het boek "zou moeten werken" | Test wint; determineer of de test of de aanname fout is |
| Een securityclaim staat alleen in een boek | Verifiëren tegen OWASP/NIST voordat je hem overneemt |
| Je weet het niet | Zeg "onverifieerd" en zoek de primaire bron |

## Versiecheck (10 min per week)

Doe aan het begin van elke week:

1. Welke versie noemt het boek?
2. Welke versie heb je geïnstalleerd? (`pip show`, `uv pip list`, `docker version`)
3. Wat zegt de docs over het verschil?
4. Noteer afwijkingen in `NOTES.md` van je projectrepo.

Dit is geen formaliteit. De boeken zijn van 2026, maar frameworks bewegen
sneller dan boeken.

## Wat je niet doet

- Niet alle zeven boeken cover-to-cover lezen.
- Geen achtste boek kopen voordat fase 1 klaar is.
- Een blogpost niet als primaire bron gebruiken voor een API.
- Een boekclaim niet overnemen zonder bron of test.
- De Huyen-track niet als "extra leeswerk" behandelen; hij is de meetlat.

## Bronnen

- AI Engineering — Chip Huyen (O'Reilly, 2025), PDF-editie in je boekenmap.
- [PydanticAI-documentatie](https://pydantic.dev/docs/ai/)
- [LlamaIndex-documentatie](https://docs.llamaindex.ai/)
- [CrewAI-documentatie](https://docs.crewai.com/)
- [LangChain/LangGraph-documentatie](https://docs.langchain.com/)
- [DSPy-documentatie](https://dspy.ai/)
- [Claude Code-documentatie](https://docs.anthropic.com/en/docs/claude-code/overview)
- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)
- [Google SRE](https://sre.google/books/)

De fase-1-vragen zijn geaudit tegen de PydanticAI 2.65-, Docker- en
Kubernetes-docs: zie [AUDITS/phase-1.md](AUDITS/phase-1.md).
