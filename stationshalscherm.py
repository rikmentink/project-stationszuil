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


def get_stations():
    with open('stations.txt') as file:
        return file.read().splitlines()


class SelectieScherm:
    def __init__(self, root):
        # Maak een container aan voor SelectScherm, waar alle widgets in komen.
        self.root = root
        self.root.title('Selecteer station')
        self.container = Frame(self.root, width=600, height=400)
        self.container.pack_propagate(0)
        self.container.pack(fill=BOTH, expand=True)

        # Initialiseer selectie menu
        stations = get_stations()
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

    def set_selected_station(self, station):
        self.selected_station = station

    def submit_station(self):
        self.root.destroy()
        self.root = Tk()
        self.app = InfoScherm(self.root, self.selected_station)


class InfoScherm():
    def __init__(self, root, station):
        """
        Initialiseer het stationsscherm.
        """
        self.root = root
        self.root.title('Stationsinformatie')
        self.root.geometry('1920x1080')
        self.station = station

        """
        Creeer een container met daarin een grid
        """
        self.container = Frame(self.root, width=1920, height=1080)
        self.container.pack_propagate(0)
        self.container.pack(fill=BOTH, expand=True)

        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.columnconfigure(2, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=3)
        self.container.rowconfigure(2, weight=3)

        """
        Maak de bovenste header aan.
        """
        self.header = Frame(self.container, width=1920, height=150, background='blue')

        # TODO: Juiste achtergrond fixen voor de header
        self.header.grid(column=0, row=0, columnspan=5, rowspan=1, sticky=N)
        self.header.columnconfigure(0, weight=1)
        self.header.rowconfigure(0, weight=1)

        self.title = Label(
            self.header,
            text=f'Welkom op station {self.station}.',
            font=('Arial', 20, 'bold'),
            foreground='black'
        )
        self.title.grid(column=0, row=0, sticky=CENTER)


"""
Wanneer het bestand start wordt de functie main() uitgevoerd.
"""
if __name__ == "__main__":
    root = Tk()
    app = SelectieScherm(root)
    root.mainloop()
