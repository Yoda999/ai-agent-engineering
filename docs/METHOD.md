# Methode: leren met bewijs

Deze methode is gebaseerd op wat aantoonbaar werkt voor complexe vaardigheden:
actief ophalen, gespreid herhalen, afwisselen, directe feedback en oefenen op
het echte werk. Niet op herlezen en video's kijken.

## De vijf principes

### 1. Retrieval practice (actief ophalen)

Je leert meer van jezelf afvragen dan van opnieuw lezen. Daarom heeft elke week
een gesloten-boekexamen en beginnen we de dag met kaarten. Het ongemak van
"ik weet het niet meer" is het leermoment.

### 2. Spaced repetition (gespreid herhalen)

Kaarten komen terug op groeiende intervallen (SM-2). Een kaart die je goed kent,
zie je pas over weken terug; een kaart die je fout hebt, zie je dezelfde dag
opnieuw. Zo besteed je tijd aan zwakke plekken.

### 3. Interleaving (afwisselen)

De gate-examens mengen vragen uit eerdere weken. De kaartenpool groeit mee.
Daardoor leer je onderscheiden welke aanpak bij welk probleem hoort, in plaats
van een week lang hetzelfde trucje.

### 4. Deliberate practice (gerichte oefening)

Elke week heeft een Challenge met acceptatiecriteria die net boven je huidige
niveau ligt. Je oefent op het echte werk (bouwen, testen, deployen), met
directe feedback van tests en evaluaties. Niet op het makkelijke deel dat je al
kunt.

### 5. Directe feedback

De CLI geeft onmiddellijk score, de tests geven rood/groen, de loadtest geeft
p95, de eval geeft cijfers. Je hoeft niet te raden of je goed bezig bent.

## Het 60-minutenblok

| Min | Onderdeel | Wat je precies doet |
|---|---|---|
| 10 | Herhaling | `aae cards`; alle openstaande kaarten, scores 0-3 |
| 15 | Theorie | lees de pagina's; boek dicht; schrijf 5 punten en 3 vragen op |
| 25 | Hands-on | één buildstap, klein genoeg om af te maken; commit |
| 5 | Test | `aae exam --week N` of de challenge-tests |
| 5 | Log | `aae log 60`; bewijs toevoegen; 3 regels reflectie |

Regels:

- **Eén stap per blok.** Als de stap niet af kan, maak hem kleiner.
- **Eerst boek dicht, dan notities.** Anders kopieer je in plaats van denken.
- **Geen tabbladen-jacht.** Je leest de aangewezen pagina's; de rest is naslag.
- **Commit elke dag.** Een commit is je bewijs dat je iets hebt afgemaakt.

## Een hoofdstuk lezen dat blijft hangen

1. **Preview (2 min):** kop, tussenkopjes, figuren, samenvatting. Wat is de
   centrale vraag?
2. **Lees (8 min):** actief, pen erbij; markeer alleen wat je niet verwachtte.
3. **Sluit het boek (3 min):** schrijf uit je hoofd de 5 kernpunten en 3 vragen.
4. **Toets (2 min):** beantwoord je eigen vragen hardop of op papier.
5. **Pas toe (in het buildblok):** gebruik minstens één concept in code of test.

Als je de 5 punten niet uit je hoofd kunt opschrijven, heb je niet gelezen maar
gekeken. Opnieuw, met minder pagina's.

## Kaarten: regels

Een goede kaart:

- test **één** feit of verband;
- is in je eigen woorden, niet copy-paste;
- vraagt **waarom** of **wanneer**, niet alleen **wat**;
- heeft een bron (boek + pagina) zodat je kunt controleren;
- is kort genoeg om in 20 seconden te beantwoorden.

Scores:

| Score | Betekenis | Gevolg |
|---|---|---|
| 0 | Niet geweten | interval 0, ease omlaag |
| 1 | Met moeite | kort interval |
| 2 | Goed | normaal interval |
| 3 | Triviaal | lang interval |

**Belangrijk:** score 3 betekent "ik hoefde niet na te denken", niet "ik vond
het interessant". Wees streng; een te hoge score kost je later een herkansing.

## Het examen

- Gesloten boek, geen AI, geen notities, één keer antwoorden.
- 20 minuten voor 5 meerkeuzevragen en 1 open vraag.
- De open vraag beoordeel je zelf tegen kernpunten, maar pas **nadat** je je
  antwoord hebt opgeschreven. Niet terug aanpassen.
- Je moet 85% halen. Bij 5 MCQ (15 punten each) en 1 open vraag (25 punten)
  betekent dat: maximaal één MCQ fout en de open vraag volledig, of alles goed
  met een klein verlies op de open vraag.
- De uitslag wordt opgeslagen; herkansing is pas na 24 uur en na herstelwerk.

## De challenge

De challenge is het echte bewijs. Hij wordt niet beoordeeld op "het ziet er
goed uit", maar op criteria:

- de tests slagen;
- de acceptatiecriteria zijn aantoonbaar gehaald;
- het artifact is reproduceerbaar;
- er is bewijs (commit, CI, rapport, URL).

Lukt de challenge niet, dan is dat geen mislukking maar een specificatie van wat
je nog niet beheerst. Schrijf op welke aanname niet klopte en pas de aanpak aan.

## Falen: het protocol

1. **Stop.** Ga niet meteen opnieuw gokken.
2. **Diagnoseer.** Welke check faalde: kennis (examen), uitvoering (challenge),
   gewoonte (kaarten/tijd) of bewijs?
3. **Herstel.** Kennis: herlees de bronpagina's en maak nieuwe kaarten.
   Uitvoering: verklein de challenge en bouw hem opnieuw. Gewoonte: plan de
   blokken en log ze. Bewijs: verzamel het ontbrekende artifact.
4. **Wacht 24 uur.** Slapen consolideert; een tweede poging direct na een
   mislukking meet vooral frustratie.
5. **Doe de gate opnieuw.** Maximaal twee pogingen; daarna volgt een verplichte
   review en herhaal je de week met extra oefeningen.

## Bijhouden en bijsturen

- **Wekelijks:** `aae status` en `aae report`. Zijn uren, kaarten en gates op
  schema?
- **Per fase:** een retrospective van 15 minuten. Wat kostte te veel tijd? Welke
  aanname was fout? Wat schrap je?
- **Kalibratie:** vergelijk je verwachte examenscore met de werkelijke score.
  Overschat je jezelf systematisch, verhoog de moeilijkheid en de frequentie van
  ophalen.
- **Energie:** slaap en beweging zijn geen luxe; zonder consolidatie werkt
  gespreid herhalen niet.

## Anti-patronen

| Patroon | Waarom het faalt | Vervanging |
|---|---|---|
| Video's kijken zonder te bouwen | passief herkennen, geen vaardigheid | 25 min bouwen per blok |
| Tutorials kopiëren | werkt alleen in de tutorial | zelf de tests en foutpaden schrijven |
| Alles willen lezen | te veel input, te weinig output | leeskaart per week |
| Frameworkhopping | geen diepte | PydanticAI als kern, rest gericht |
| Gates overslaan | gat in je fundament | gate is de meetlat |
| Alleen groene tests | coverage zonder betekenis | eval + loadtest + security |
| "Later documenteren" | bewijs verdwijnt | meteen commit + rapport |
