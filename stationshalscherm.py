from tkinter import *

"""
Deze module wordt weergegeven in de stationshal en bevat wat informatie. De 
volgende data moet netjes worden weergegeven:
1. 5 goedgekeurde reviews op volgorde van datum
2. Beschikbare faciliteiten van het huidige station met iconen (uit database)
3. Actuele weersvoorspelling van het huidige station via OpenWeatherMap API

De reviews worden uit de database gehaald, de 5 nieuwste. Deze worden 
vervolgens achter elkaar weergegeven. De faciliteiten worden met iconen naast
elkaar neergezet, deze faciliteiten worden opgehaald uit de database, en is
per station verschillend. Voor de weersvoorspelling wordt er een API-koppeling
gemaakt met als locatie het huidige station.

Deze module wordt gemaakt als GUI door middel van Tkinter. We maken elementen
handmatig aan en positioneren deze in de GUI.
"""


class SelectieScherm:
    def __init__(self, root):
        # Maak een container aan voor SelectScherm, waar alle widgets in komen.
        self.root = root
        self.root.title('Selecteer station')
        self.container = Frame(self.root, width=600, height=400)
        self.container.pack_propagate(0)
        self.container.pack(fill=BOTH, expand=True)

        # Initialiseer selectie menu
        stations = self.get_stations()
        placeholder = StringVar()
        placeholder.set(stations[0])
        self.selected_station = stations[0]

        # Initialiseer widgets
        self.title = Label(
            self.container,
            text='Selecteer uw station',
            font=('Arial', 20, 'bold')
        )
        self.subtitle = Label(
            self.container,
            text='Selecteer hier het station waarop u zich momenteel bevindt.',
            font=('Arial', 13)
        )
        self.select = OptionMenu(
            self.container,
            placeholder,
            *stations,
            command=self.set_selected_station
        )
        self.submit = Button(
            self.container,
            text='Verder',
            command=self.submit_station
        )
        self.title.pack(anchor=CENTER, pady=(100, 0))
        self.subtitle.pack(after=self.title, anchor=CENTER)
        self.select.pack(after=self.subtitle, pady=(30, 0), anchor=CENTER)
        self.submit.pack(after=self.select, anchor=CENTER)

    def get_stations(self):
        with open('stations.txt') as file:
            return file.read().splitlines()

    def set_selected_station(self, station):
        self.selected_station = station

    def submit_station(self):
        self.root.destroy()
        self.root = Tk()
        self.app = InfoScherm(self.root, self.selected_station)

class InfoScherm():
    def __init__(self, root, station):
        """
        Initialiseer alle standaard widgets op het stationsscherm.
        """
        self.root = root
        self.root.title('Stationsinformatie')
        self.root.geometry('1920x1080')
        self.station = station

        self.title = Label(self.root, text=f'Info scherm station {self.station}')
        self.title.pack(padx=10, pady=10)


"""
Wanneer het bestand start wordt de functie main() uitgevoerd.
"""
if __name__ == "__main__":
    root = Tk()
    app = SelectieScherm(root)
    root.mainloop()
