# Module 2: Moderatie
In deze module kunnen reviews die zijn achtergelaten in module 1 worden goed of afgekeurd. De goedgekeurde berichten zullen bij module 3 worden weergegeven.

Het .csv bestand vol met alle reviews wordt uitgelezen, en de reviews die nog niet beoordeeld zijn komen in deze module bij elkaar te staan. Hier krijg je dan de vraag of je hem goed of afkeurd. 

Deze module slaat vervolgens de review op in een PostgreSQL database. Ook voegt hij een beoordeling toe aan de database, waar de beoordeling in staat, de datum en tijd, gegevens van de moderator en een foreign key van de review.

Zodra de gegevens naar de database geschreven zijn wordt het .csv bestand geleegd.

## Pseudocode

##### Lees het .csv bestand uit
`open reviews.csv`  
`nieuwe lijst met alle reviews`

##### Zet de reviews in de database
`maak verbinding met de database via psycopg2`
`controleer of kolom reviews bestaat en anders aanmaken met de juiste attributen`  
`execute query insert naar de kolom reviews`  

##### Login voor de moderator
`vraag om naam`  
`vraag om emailadres`

##### Geef iedere review die niet beoordeeld is weer achter elkaar
`execute query select alle reviews`  
`vraag of je de review goedkeurt`  
`geef een lijst weer met de antwoorden ja of nee en wacht op selectie`  
`datum is huidige datum`  
`maak variabele beoordeling met foreign key van review, gegevens moderator, datum` 

##### Sluit de applicatie
`wanneer reviews leeg is zeg er zijn geen reviews om te beoordelen`  
`sluit verbinding met de database`