import csv
import cutie
import psycopg2
from datetime import datetime as dt

"""
In deze module kunnen reviews die zijn achtergelaten in module 1 worden goed of afgekeurd. De goedgekeurde berichten zullen bij module 3 worden weergegeven.

Het .csv bestand vol met alle reviews wordt uitgelezen, en de reviews die nog niet beoordeeld zijn komen in deze module bij elkaar te staan. Hier krijg je dan de vraag of je hem goed of afkeurd.

Deze module slaat vervolgens de review op in een PostgreSQL database. Ook voegt hij een beoordeling toe aan de database, waar de beoordeling in staat, de datum en tijd, gegevens van de moderator en een foreign key van de review.

Zodra de gegevens naar de database geschreven zijn wordt het .csv bestand geleegd.

LET OP: Dit bestand moet via de terminal worden geopend (python moderatie.py).
"""

"""
Lees het .csv bestand uit en leeg hem daarna.
"""
with open('reviews.csv', 'r+') as file:
    reader = csv.reader(file, delimiter=',')
    reviews = list(reader)
    file.truncate(0)

"""
Maak verbinding met de database, controleer of kolom reviews en
beoordeling bestaan, anders maakt hij ze.
"""
try:
    db = psycopg2.connect(
        dbname='proj_a',
        user='dev',
        password='dev_connect!',
        host='localhost',
        port='5432'
    )
    cursor = db.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS reviews(id SERIAL PRIMARY KEY, bericht VARCHAR(140) NOT NULL, naam VARCHAR(40) NOT NULL, station VARCHAR(30) NOT NULL, datum VARCHAR(40) NOT NULL);"
        "CREATE TABLE IF NOT EXISTS beoordelingen(id SERIAL PRIMARY KEY, goedgekeurd BOOLEAN NOT NULL, datum VARCHAR(40) NOT NULL, review_id INTEGER NOT NULL);"
    )
    db.commit()

except Exception as e:
    print(e)

"""
Zet iedere review in de database met de juiste query
"""
print('Alle reviews importeren in de database...')
for review in reviews:
    cursor.execute(
        "INSERT INTO reviews(bericht, naam, station, datum) "
        "VALUES(%s, %s, %s, %s)", review
    )
    db.commit()

print('Klaar!\n')

"""
Login voor de moderator
"""
print('Moderator login\n---------------')
while True:
    naam = input('Wat is uw naam?\n')
    if len(naam) == 0:
        print('Vul uw naam in.')
        continue
    else:
        break

while True:
    email = input('Wat is uw e-mailadres?\n')
    if len(email) == 0:
        print('Vul uw e-mailadres in.')
        continue
    else:
        break

moderator = [naam, email]

"""
Krijg alle reviews uit de database welke nog niet beoordeeld zijn.
"""
cursor.execute(
    "SELECT r.id, r.bericht, r.naam "
    "FROM reviews r "
    "WHERE NOT EXISTS "
    "(SELECT * FROM beoordelingen b WHERE b.review_id = r.id)"
)
reviews = cursor.fetchall()

"""
Geef alle reviews 1 voor 1 weer, en vraag aan de moderator of hij
hem goed of af keurt.
"""
beoordelingen = ['Afkeuren', 'Goedkeuren']
antwoorden = ['afgekeurd', 'goedgekeurd']

print('Beoordeel de volgende reviews:\n------------------------------')
for review in reviews:
    print(review[1])
    index = cutie.select(beoordelingen, selected_index=1)

    # Verzamel datum en stel beoordeling samen
    beoordeling_datum = dt.now()
    beoordeling = [index, beoordeling_datum, review[0]]

    # Schrijf naar database en
    cursor.execute("INSERT INTO beoordelingen(goedgekeurd, datum, review_id) "
                   "VALUES('%s', %s, %s)", beoordeling)
    db.commit()

    print(f"Succesvol {antwoorden[beoordelingen.index(beoordelingen[index])]}.\n")

print(f"Alle reviews zijn beoordeeld. Bedankt {moderator[0]}!")

"""
Sluit de database verbinding
"""
cursor.close()
db.close()
