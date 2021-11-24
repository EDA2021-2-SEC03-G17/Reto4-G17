"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import time
import config
import threading
from App import controller
from DISClib.ADT import stack
assert config

def printMenu():
    print("\n")
    print("____________________________________________________________")
    print("                   Welcome to AirTravel                     ")
    print('''
            _______
            _\ _~-\___
    =  = ==(____AA____D
                \_____\___________________,-~~~~~~~`-.._
                /     o O o o o o O O o o o o o o O o  |\_
                `~-.__        ___..----..                  )
                      `---~~\___________/------------`````
                      =  ===(_________D''')
    print("\n1- Start Itinerary ")
    print("2- Load flights and aiports information.")
    print("3- ")
    print("4- ")
    print("5- ")
    print("6-  ")
    print("7-  ")
    print("0- Exit.")
    print("____________________________________________________________")


def loadData(itinerary):
    print("\n Loading airport and route information ....")
    controller.loadItinerary(itinerary)
    numedges = controller.totalConnections(itinerary)
    numvertex = controller.totalAirports(itinerary)
    print("\nFlights Network")
    print('Number of airport: ' + str(numvertex))
    print('Number of flights: ' + str(numedges))
    print(' ')
    numedges = controller.totalConnections2(itinerary)
    numvertex = controller.totalAirports2(itinerary)
    print("\nCities Airports")
    print('Number of airport and Cities: ' + str(numvertex))
    print('Number of flights: ' + str(numedges))

"""
Menu principal
"""
itinerary = None

def thread_cycle():
    while True:
        printMenu()
        inputs = input('Select an option to continue: ')

        if int(inputs[0]) == 1:
            print("\nStarting....")
            # cont es el controlador que se usará de acá en adelante
            itinerary = controller.initItinerary()

        elif int(inputs[0]) == 2:
            loadData(itinerary)

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()