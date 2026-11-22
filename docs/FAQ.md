# FAQ en bezwaren

## Is één uur per dag genoeg?

Voor de begeleide route wel: 24 weken x 6 dagen x 1 uur is 144 uur, plus
portfolio- en capstonewerk. Je wordt productiecompetent, niet in één klap
wereldexpert. De laatste fase en de maanden daarna vragen meer tijd. Zie
[ROADMAP.md](../ROADMAP.md).

## Kan ik sneller?

Ja, door meerdere blokken per dag te doen. Nee, door gates over te slaan. De
gate is de meetlat, niet de administratie. Sneller mag alleen als je het bewijs
levert.

## Moet ik alle zeven boeken lezen?

Nee. *AI Engineering* (Huyen) is de conceptuele track: je leest de
weekselecties en beantwoordt de reflectievraag. Van de zes frameworkboeken lees
je de pagina's die bij de build horen. De [leeskaart](READING-MAP.md) wijst
ongeveer 700 frameworkpagina's en 350 Huyen-PDF-pagina's aan. De rest is
naslag. Je leest om te bouwen, niet om een boek uit te hebben.

## Ik heb weinig tijd. Kan het korter?

Ja, maar niet door de gate te skippen. De minimale route per dag is:

1. 10 min kaarten;
2. 10 min Huyen-concept + 5 regels reflectie;
3. 25 min build;
4. 5 min test;
5. 5 min loggen.

Sla de optionele frameworkpagina's over en lees alleen wat de build nodig heeft.
De concepttrack en de build zijn niet optioneel; de rest is naslag.

## Ik ben nog niet begonnen, maar heb al een nulmeting.

Gebruik `aae start`. Dat zet de startdatum op vandaag, zonder je gelogde uren,
kaarten of bewijs te wissen. Je hoeft de database niet te verwijderen.

## Heb ik een betaalde API nodig?

Nee. Je kunt veel testen met `TestModel`, fakes en Ollama. Voor evaluaties en
kwaliteitsvergelijkingen heb je af en toe een echt model nodig; gebruik dan een
goedkoop model en een harde limiet. Reken op enkele euro's per week, niet
tientallen.

## Ik heb nog geen VPS.

Fase 1 kan grotendeels lokaal. De fasepoort vraagt een live service; je kunt
daarvoor ook een tijdelijke cloudinstantie of je eigen netwerk gebruiken. De
ervaring met secrets, healthchecks en rollback is belangrijker dan de provider.
Zie [SETUP.md](SETUP.md).

## Mag ik AI gebruiken tijdens het leren?

Ja, en je moet het leren gebruiken: dat is de vaardigheid. De regels:

- **Bij bouwen:** gebruik AI als pair programmer, maar je moet elke regel kunnen
  uitleggen en de tests moeten echt zijn.
- **Bij examens:** geen AI, geen boek, geen notities. Anders meet je niets.
- **Bij bewijs:** nooit verzinnen. Een nep-CI-run of nep-URL is fraude.
- **Bij twijfel:** vraag AI om je antwoord aan te vallen, niet om het te geven.

## De code in het boek is verouderd.

Boeken lopen achter op releases. Het concept is leidend; de API vind je in de
officiële documentatie. Voor Huyen geldt hetzelfde: de concepten zijn sterk,
maar de voorbeelden kunnen verouderd zijn. Pin je versies en noteer afwijkingen in je README. Een
goede oefening: laat AI het verschil uitleggen en verifieer dat tegen de docs.

## Ik faal steeds op dezelfde gate.

- Diagnoseer eerst: is het kennis, uitvoering, gewoonte of bewijs?
- Verklein de challenge; een kleinere werkende stap verslaat een grote halve.
- Zoek de zwakke kaarten op en herhaal ze met score 0 of 1.
- Vraag een review (mentor, community, of een opname van je uitleg).
- Na twee pogingen: herhaal de week met de extra oefeningen. Dat is geen
  achterstand, dat is kwaliteit.

## Hoe bewijs ik dit aan een werkgever?

Met een portfolio van vijf casestudy's, live demo's, eval-rapporten,
loadtesten, een securityreview en een postmortem. Zie [EVIDENCE.md](EVIDENCE.md)
en [STRATEGY.md](STRATEGY.md). Een recruiter ziet het verschil tussen "ik heb
een agent gebouwd" en "hier is het bewijs dat hij onder belasting blijft werken".

## Is dit genoeg voor een carrièrestap?

Het geeft je een geloofwaardig portfolio en een meetbare basis. De stap zelf
vraagt ook netwerk, gesprekken en vaak een eerste opdracht. Fase 5 en de
12-maandenroute zijn daarop gericht. Niemand wordt aangenomen op een curriculum;
mensen worden aangenomen op bewijs en communicatie.

## Waarom zo streng?

Omdat de markt streng is. Een agent die 80% van de tijd werkt, is in productie
een incident. De gate meet niet of je "gemotiveerd" bent, maar of je een systeem
kunt bouwen dat je durft te verdedigen.

## Kan ik dit met een team doen?

Ja. Gebruik dezelfde repo, laat elkaar de examens afnemen en review elkaars
challenges. De gate blijft persoonlijk: iedereen levert eigen bewijs. Een
studiegroep verhoogt de slaagkans vooral door externe feedback.
