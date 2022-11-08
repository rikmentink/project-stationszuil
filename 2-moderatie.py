import csv
import cutie
import locale
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


def createConnection():
    """
    Maakt verbinding met de database en maakt de standaard tabellen aan, mits
    deze nog niet bestaan.

    :returns De database verbinding
    """
    with psycopg2.connect(
            dbname='proj_a',
            user='dev',
            password='dev_connect!',
            host='localhost',
            port='5432'
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS review (id SERIAL PRIMARY KEY, bericht VARCHAR(140) NOT NULL, "
                "naam VARCHAR(40) NOT NULL, station VARCHAR(30) NOT NULL, datum TIMESTAMP NOT NULL); "
    
                "CREATE TABLE IF NOT EXISTS moderator (email VARCHAR(255) PRIMARY KEY, naam VARCHAR(40) NOT NULL);"
    
                "CREATE TABLE IF NOT EXISTS beoordeling (review_id INTEGER PRIMARY KEY REFERENCES review, goedgekeurd "
                "BOOLEAN NOT NULL, datum TIMESTAMP NOT NULL, moderator_email VARCHAR(255) REFERENCES moderator); "
            )

        return conn


def closeConnection(conn):
    """
    Sluit de database verbinding

    :param conn: De database verbinding
    """
    conn.close()


def insertReviews(conn):
    """
    Leest het reviews bestand uit, leegt het bestand, en zet vervolgens alle
    reviews in de database.

    :param conn: De database verbinding
    """
    try:
        with open('reviews.csv', 'r+') as reviews_file:
            reader = csv.reader(reviews_file, delimiter=',')
            reviews = list(reader)
            reviews_file.truncate(0)

            if len(reviews) > 0:
                print('Alle reviews importeren in de database...')
                with conn.cursor() as cur:
                    for review in reviews:
                        cur.execute(
                            "INSERT INTO review (bericht, naam, station, datum) "
                            "VALUES (%s, %s, %s, %s)", review
                        )
                    conn.commit()
                    print('Klaar!\n')
            else:
                print('Geen reviews om te importeren.')
    except FileNotFoundError:
        print('Geen reviews om te importeren.')


def getReviews(conn):
    """
    Returned een lijst met alle reviews die nog niet zijn beoordeeld.

    :param conn: De database verbinding
    :returns: Een lijst met tuples met daarin de gegevens van de review
    """
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * "
            "FROM review r "
            "WHERE NOT EXISTS "
            "(SELECT * FROM beoordeling b WHERE b.review_id = r.id);"
        )
        return cur.fetchall()


def getModeratorName(conn, moderator_email):
    """
    Controleert of de moderator al bestaat in de database en returned de naam
    van deze moderator als dat zo is. Zo nee, dan wordt er niks gereturned.

    :param conn: De database verbinding
    :param moderator_email: De e-mail van de moderator
    :return: De naam van de moderator of niks
    """
    with conn.cursor() as cur:
        cur.execute("SELECT naam FROM moderator "
                    "WHERE moderator.email = %s;", [moderator_email])
        data = cur.fetchone()

        if data:
            return data[0]


def insertModerator(conn, moderator_email, moderator_naam):
    """
    Zet een nieuwe moderator in de database.

    :param conn: De database verbinding
    :param moderator_email: De e-mail van de moderator
    :param moderator_naam: De naam van de moderator
    """
    with conn.cursor() as cur:
        cur.execute("INSERT INTO moderator (email, naam) "
                    "VALUES (%s, %s);", [moderator_email, moderator_naam])
        conn.commit()


def insertBeoordeling(conn, beoordeling):
    """
    Zet een beoordeling in de database
    It inserts a rating into the database

    :param conn: the connection to the database
    :param beoordeling: a tuple containing the following values:
    """
    with conn.cursor() as cur:
        cur.execute("INSERT INTO beoordeling (review_id, goedgekeurd, datum, moderator_email) "
                    "VALUES (%s, %s, %s, %s)", beoordeling)
        conn.commit()


"""
Maak een database verbinding en zet alle reviews vanuit het bestand in de 
database.

Vervolgens kan de moderator inloggen met zijn e-mailaders. Als dat e-mailadres 
nog niet bestaat in de database, wordt de moderator om zijn naam gevraagd en
wordt hij in de database gezet.
"""
conn = createConnection()
insertReviews(conn)

print('Moderator login\n---------------')
while True:
    moderator_email = input('Wat is uw e-mailadres?\n')
    if len(moderator_email.strip()) == 0:
        print('Vul uw e-mailadres in.')
        continue
    else:
        moderator_naam = getModeratorName(conn, moderator_email)
        if moderator_naam:
            print(f'Welkom terug, {moderator_naam}!\n')
        else:
            while True:
                moderator_naam = input('Wat is uw naam?\n')
                if len(moderator_naam.strip()) == 0:
                    print('Vul uw naam in.')
                    continue
                else:
                    insertModerator(conn, moderator_email, moderator_naam)
                    print(f'Welkom, {moderator_naam}!\n')
                    break
        break

"""
Zet de locale op Nederland, voor de juiste datum format
"""
locale.setlocale(locale.LC_TIME, 'nl_NL')

"""
Alle reviews worden 1 voor 1 weergegeven, en er wordt aan de moderator 
gevraagd of hij deze goed of af keurt. Daarna wordt de database 
verbinding gesloten.
"""
beoordelingen = ['Afkeuren', 'Goedkeuren']
antwoorden = ['afgekeurd', 'goedgekeurd']

print('Beoordeel de volgende reviews:\n------------------------------')
for review in getReviews(conn):
    print(f'{review[2]} zei op {dt.strftime(review[4], "%w %B %Y, %H:%M:%S")} in {review[3]}:\n{review[1]}')
    index = cutie.select(beoordelingen, selected_index=1)

    # Verzamel datum en stel beoordeling samen
    beoordeling_datum = dt.now()
    beoordeling = [review[0], str(index), beoordeling_datum, moderator_email]

    # Schrijf naar database
    insertBeoordeling(conn, beoordeling)
    print(f"Succesvol {antwoorden[beoordelingen.index(beoordelingen[index])]}.\n")

print(f"Alle reviews zijn beoordeeld. Bedankt {moderator_naam}!")
closeConnection(conn)
