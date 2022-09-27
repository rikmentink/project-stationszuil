# Module 3: Stationshalscherm
Deze module wordt weergegeven in de stationshal en bevat wat informatie. De volgende data moet netjes worden weergegeven:
1. 5 goedgekeurde reviews op volgorde van datum
2. Beschikbare faciliteiten van het huidige station met iconen (uit database)
3. Actuele weersvoorspelling van het huidige station via OpenWeatherMap API

De reviews worden uit de database gehaald, de 5 nieuwste. Deze worden vervolgens achter elkaar weergegeven. De faciliteiten worden met iconen naast elkaar neergezet, deze faciliteiten worden opgehaald uit de database, en is per station verschillend. Voor de weersvoorspelling wordt er een API-koppeling gemaakt met als locatie het huidige station.

Deze module wordt gemaakt als GUI door middel van Tkinter. We maken elementen handmatig aan en positioneren deze in de GUI.

## Pseudocode

##### Aanmaken van de GUI
`initialiseer Tkinter`  
`positioneren van standaard kolommen en velden`

##### Gegevens ophalen uit de database
`open database verbinding`  
`reviews is select 5 reviews op volgorde van datum`  
`faciliteiten is select faciliteiten op huidig station`  
`sluit database verbinding`

##### Weergeven gegevens 
`voor alle reviews maak een label aan`  
`positioneer labels en geef ze een voor een weer`  

`voor alle faciliteiten maak een label aan`  
`laad het bijbehorende icoon in`  
`positioneer iconen naast elkaar`

##### Weerbericht koppeling
`maak api-verzoek met huidige locatie van station`  
`formatteer weerinformatie`
`positioneer weerinformatie op scherm`

`mainloop om GUI draaiend te houden`