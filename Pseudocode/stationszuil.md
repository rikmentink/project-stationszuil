# Module 1: Stationszuil
Deze module is module 1 waarin reizigers hun review kunnen achterlaten.

Eerst moeten we de reizigers vragen om een review (bericht) en hun naam. Wanneer er geen naam
wordt ingevuld maken we hier 'Anoniem' van, het bericht is wel verplicht. Deze gegevens willen
we natuurlijk opslaan. Hiernaast moeten we ook de huidige datum en tijd erbij zetten, en een
willekeurig station uit een lijst (stations.txt).

Deze gegevens moeten we op een rijtje zetten en opslaan in een .csv bestand. Wanneer deze niet
bestaat maken we er een, en als ie wel bestaat voegen we een nieuwe row toe.

## Pseudocode

##### Vraag de reiziger eerst om zijn gegevens
vraag om bericht (max 140 karakters)
vraag om naam

als naam is niet ingevuld dan naam is anoniem

##### Geef automatisch extra gegevens door
datum is huidige datum en tijd

open stations.txt
index is random tussen 0 en aantal lines
station is index in bestand
sluit stations.txt

##### Sla de gegevens op in csv bestand, mits deze bestaat
gegevens is een nieuwe lijst van de 4 gegevens

als gegevens.csv niet bestaat maak een nieuwe aan
open gegevens.csv
schrijf gegevens op nieuwe regel
sluit gegevens.csv

##### Beeindigen programma
zeg bedankt etc...
