import csv
import cutie
import psycopg2
from datetime import datetime as dt

"""
In deze module kunnen reviews die zijn achtergelaten in module 1 worden goed of 
afgekeurd. De goedgekeurde berichten zullen bij module 3 worden weergegeven.

Het .csv bestand vol met alle reviews wordt uitgelezen, en de reviews die nog 
niet beoordeeld zijn komen in deze module  bij elkaar te staan. Hier krijg je 
dan de vraag of je hem goed of afkeurd.

Deze module slaat vervolgens de review op in een PostgreSQL database. Ook 
voegt hij een beoordeling toe aan de database, waar de beoordeling in staat, de 
datum en tijd, gegevens van de moderator en een foreign key van de review.

Zodra de gegevens naar de database geschreven zijn wordt het .csv bestand 
geleegd.

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
        "CREATE TABLE IF NOT EXISTS review (id SERIAL PRIMARY KEY, bericht VARCHAR(140) NOT NULL, naam VARCHAR(40) "
        "NOT NULL, station VARCHAR(30) NOT NULL, datum VARCHAR(40) NOT NULL); "
        
        "CREATE TABLE IF NOT EXISTS moderator (email VARCHAR(255) PRIMARY KEY, naam VARCHAR(40) NOT NULL);"
        
        "CREATE TABLE IF NOT EXISTS beoordeling (review_id INTEGER PRIMARY KEY REFERENCES review, goedgekeurd "
        "BOOLEAN NOT NULL, datum VARCHAR(40) NOT NULL, moderator_email VARCHAR(255) REFERENCES moderator); "
    )
    db.commit()

except psycopg2.OperationalError as e:
    print('Er kon geen verbinding worden gemaakt met de database.')
    db = None
    cursor = None

"""
Zet iedere review in de database met de juiste query
"""
print('Alle reviews importeren in de database...')
for review in reviews:
    cursor.execute(
        "INSERT INTO review (bericht, naam, station, datum) "
        "VALUES (%s, %s, %s, %s)", review
    )
    db.commit()

print('Klaar!\n')

"""
Login voor de moderator. Wanneer deze moderator nog niet geregistreerd is 
wordt er een nieuwe gemaakt in de database.
"""
print('Moderator login\n---------------')
moderator_email = ''
moderator_naam = ''

while True:
    moderator_email = input('Wat is uw e-mailadres?\n')
    if len(moderator_email) == 0:
        print('Vul uw e-mailadres in.')
        continue
    else:
        break

cursor.execute("SELECT naam FROM moderator "
               "WHERE moderator.email = %s;", [moderator_email])
data = cursor.fetchone()

if data:
    moderator_naam = data[0]
    print(f'Welkom terug, {moderator_naam}!\n')
else:
    while True:
        moderator_naam = input('Wat is uw naam?\n')
        if len(moderator_naam) == 0:
            print('Vul uw naam in.')
            continue
        else:
            cursor.execute("INSERT INTO moderator (email, naam) "
                           "VALUES (%s, %s);", [moderator_email, moderator_naam])
            db.commit()
            break


"""
Krijg alle reviews uit de database welke nog niet beoordeeld zijn.
"""
cursor.execute(
    "SELECT r.id, r.bericht, r.naam "
    "FROM review r "
    "WHERE NOT EXISTS "
    "(SELECT * FROM beoordeling b WHERE b.review_id = r.id);"
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
    beoordeling = [review[0], str(index), beoordeling_datum, moderator_email]

    # Schrijf naar database en
    cursor.execute("INSERT INTO beoordeling (review_id, goedgekeurd, datum, moderator_email) "
                   "VALUES (%s, %s, %s, %s)", beoordeling)
    db.commit()

    print(f"Succesvol {antwoorden[beoordelingen.index(beoordelingen[index])]}.\n")

print(f"Alle reviews zijn beoordeeld. Bedankt {moderator_naam}!")

"""
Sluit de database verbinding
"""
cursor.close()
db.close()
