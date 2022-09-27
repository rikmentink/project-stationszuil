import csv
import locale
import os
import random
import time

"""
Deze module is module 1 waarin reizigers hun review kunnen achterlaten.

Eerst moeten we de reizigers vragen om een review (bericht) en hun naam. Wanneer er geen naam
wordt ingevuld maken we hier 'Anoniem' van, het bericht is wel verplicht. Deze gegevens willen
we natuurlijk opslaan. Hiernaast moeten we ook de huidige datum en tijd erbij zetten, en een
willekeurig station uit een lijst (stations.txt).

Deze gegevens moeten we op een rijtje zetten en opslaan in een .csv bestand. Wanneer deze niet
bestaat maken we er een, en als ie wel bestaat voegen we een nieuwe row toe.
"""


"""
Vraag om bericht, en probeer opnieuw wanneer het bericht te lang is.
"""
while True:
    bericht = input('Laat hier uw bericht achter (max 140 tekens):\n')

    if len(bericht) > 140:
        print('Fout: uw bericht mag maximaal 140 tekens zijn.')
        continue
    elif len(bericht.strip()) == 0:
        print('Fout: u moet een bericht invullen.')
        continue
    else:
        break


"""
Vraag om naam, en zonder input naam Anoniem instellen
"""
naam = input('Wat is uw naam? (niet verplicht)\n')

if len(naam.strip()) == 0:
    naam = 'Anoniem'


"""
Haal de huidige datum op met juiste format uit Nederland
"""
locale.setlocale(locale.LC_TIME, "nl_NL")
datum = time.strftime('%A %d %B %Y, %H:%M:%S').capitalize()


"""
Lees stations.txt uit en zet stations in een list.
"""
with open('stations.txt', 'r') as bestand:
    lines = bestand.readlines()
    stations = []

    # Stript bij elk station de new line characters
    for line in lines:
        stations.append(line.replace('\n', ''))

    bestand.close()


"""
Wijs een random station aan uit de lijst
"""
index = random.randint(0, len(stations))
station = stations[index]


"""
Vat review samen en sla op in het reviews.csv bestand als deze 
bestaat, anders maken we een nieuw bestand aan.
"""
review = [bericht, naam, station, datum]

if not os.path.exists('reviews.csv'):
    method = 'x'
else:
    method = 'a'

try:
    with open('reviews.csv', method) as file:
        writer = csv.writer(file)
        writer.writerow(review)
        file.close()
    print('Gelukt! Bedankt voor uw bericht.')
except Exception as e:
    # Vang errors op bij het schrijven
    print('Er is iets misgegaan, onze excuses voor het ongemak.')