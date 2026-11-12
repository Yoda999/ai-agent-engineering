# Curriculum

De inhoud staat in twee lagen:

1. **`assessments/phase-*.yaml`** is de bron van waarheid: per week de
   leesopdracht, build, challenge, het examen en de kaarten. De CLI leest deze
   bestanden.
2. **`phase-*.md`** is het narratief: waarom deze fase, de belangrijkste
   concepten, veelgemaakte fouten, extra oefeningen en de fasepoort.

| Fase | Weken | Narratief | Beoordeling |
|---|---|---|---|
| 1. Fundament | 1-6 | [phase-1.md](phase-1.md) | [phase-1.yaml](../assessments/phase-1.yaml) |
| 2. Kennis | 7-11 | [phase-2.md](phase-2.md) | [phase-2.yaml](../assessments/phase-2.yaml) |
| 3. Orkestratie | 12-16 | [phase-3.md](phase-3.md) | [phase-3.yaml](../assessments/phase-3.yaml) |
| 4. Productie | 17-20 | [phase-4.md](phase-4.md) | [phase-4.yaml](../assessments/phase-4.yaml) |
| 5. Capstone | 21-24 | [phase-5.md](phase-5.md) | [phase-5.yaml](../assessments/phase-5.yaml) |

## Een week toevoegen of wijzigen

1. Pas de week aan in het juiste `assessments/phase-*.yaml`-bestand.
2. Houd de structuur aan: 5 mcq + 1 open vraag, 5 kaarten, unieke ids.
3. Draai `aae validate`.
4. Draai `python -m unittest discover -s tests`.
5. Commit met een duidelijke boodschap.

De validator controleert aantallen, ids, antwoordsleutels en verplichte velden.
Inhoudelijke correctheid controleer je tegen de bronpagina's in de leeskaart.
