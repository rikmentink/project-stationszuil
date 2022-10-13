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


class GUI(Tk):
    """
    Class die de root en de verschillende frames beheert.
    """

    def __init__(self, *args, **kwargs):
        # Initialiseer het Tkinter window
        Tk.__init__(self, *args, **kwargs)
        self.title('Test')

        # Maak een container frame en wijs hem toe aan het scherm
        container = Frame(self, width=1920, height=1080)
        container.pack(side='top', fill='both', expand=True)

        # Maak een grid aan in het container
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # Maak een dictionary met alle frames (verschillende windows).
        self.frames = {}
        for frame_class in (InfoScherm, SelectScherm):
            frame = frame_class(container, self)

            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        print(self.frames)

    def show_frame(self, container):
        frame = self.frames[container]
        if frame:
            frame.destroy()
        frame = self.frames[container]
        frame.pack()

    station = ''

    def get_stations(self):
        with open('stations.txt', 'r') as file:
            stations = file.read().splitlines()
            self.station = stations[0]
            return stations

    def get_station(self):
        if len(self.station) == 0:
            return self.get_stations()[0]
        else:
            return self.station

    def set_station(self, station):
        print(f'{self.station} wordt {station}')
        self.station = station

    def submit_station(self):
        self.show_frame(InfoScherm)


class SelectScherm(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        stations = controller.get_stations()
        placeholder = StringVar()
        placeholder.set(stations[0])

        # Maak een container aan voor SelectScherm, waar alle widgets in komen.
        container = Frame(self, width=600, height=400)
        container.pack_propagate(0)
        container.pack(fill=BOTH, expand=True)

        # Initialiseer widgets
        title = Label(
            container,
            text='Selecteer station',
            font=('Arial', 20, 'bold')
        )
        subtitle = Label(
            container,
            text='Selecteer hier het station waarop u zich momenteel bevindt.',
            font=('Arial', 13)
        )
        select = OptionMenu(
            container,
            placeholder,
            *stations,
            command=controller.set_station
        )
        submit = Button(
            container,
            text='Verder',
            command=controller.submit_station
        )
        title.pack(anchor=CENTER, pady=(100, 0))
        subtitle.pack(after=title, anchor=CENTER)
        select.pack(after=subtitle, pady=(30, 0), anchor=CENTER)
        submit.pack(after=select, anchor=CENTER)


class InfoScherm(Frame):
    def __init__(self, parent, controller):
        """
        Initialiseer alle standaard widgets op het stationsscherm.

        :param parent:
        """
        Frame.__init__(self, parent)
        print()
        title = Label(self, text=f'Info scherm station {controller.get_station()}')
        title.pack(padx=10, pady=10)


"""
Wanneer het bestand start wordt de functie main() uitgevoerd.
"""
if __name__ == "__main__":
    root = GUI()
    root.mainloop()
