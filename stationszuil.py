from datetime import datetime
import locale
import random

"""
Deze module is module 1 waarin reizigers hun review kunnen achterlaten.

Eerst moeten we de reizigers vragen om een review (bericht) en hun naam. Wanneer er geen naam
wordt ingevuld maken we hier 'Anoniem' van, het bericht is wel verplicht. Deze gegevens willen
we natuurlijk opslaan. Hiernaast moeten we ook de huidige datum en tijd erbij zetten, en een
willekeurig station uit een lijst (stations.txt).

Deze gegevens moeten we op een rijtje zetten en opslaan in een .csv bestand. Wanneer deze niet
bestaat maken we er een, en als ie wel bestaat voegen we een nieuwe row toe.
"""


def promptName():
    """
    Vraagt de gebruiker om zijn of haar naam, en als er geen naam is ingevuld
    wordt deze op Anoniem gezet.

    :return: De naam van de reiziger of Anoniem.
    """
    naam = input('Wat is uw naam? (niet verplicht)\n')

    if len(naam.strip()) == 0:
        naam = 'Anoniem'

    return naam


def getCurrentDate():
    """
    Functie om de huidige datum en tijd op te halen, voor in de database.

    :return: Huidige datum en tijd.
    """
    return datetime.now()


def getRandomStation():
    """
    Leest het bestand met alle stations, zet alle stations vervolgens in een
    lijst en selecteert een random station uit die lijst.

    :return: Een random station uit de lijst met stations.
    """
    with open('stations.txt', 'r+') as stations_file:
        stations = stations_file.read().splitlines()
        return random.choice(stations)


"""
Vraag om bericht, en probeer opnieuw wanneer het bericht te lang is. Als het 
bericht is goedgekeurd wordt deze in een string samengevat en direct 
weggeschreven naar het bestand.
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
        review = f'{bericht},{promptName()},{getRandomStation()},{getCurrentDate()}\n'

        with open('reviews.csv', 'a+') as reviews_file:
            reviews_file.write(review)
            print('Gelukt! Bedankt voor uw bericht.')
            break
