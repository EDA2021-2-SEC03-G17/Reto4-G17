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
from DISClib.ADT import list as lt
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
    print("\n1- Start Itinerary. ")
    print("2- Load flights and aiports information.")
    print("3- Air interconnection points. ")
    print("4- ")
    print("5- ")
    print("6-  ")
    print("7-  ")
    print("0- Exit.")
    print("____________________________________________________________")

def loadData(itinerary):
    print("\nLoading airport and route information ....")
    controller.loadItinerary(itinerary)
    numedges = controller.totalConnections(itinerary)
    numvertex = controller.totalAirports(itinerary)
    print("\n=== Flights Network DiGraph===" )
    print('Number of airport: ' + str(numvertex))
    print('Number of flights: ' + str(numedges))
    print(' ')

    numedges = controller.totalConnections3(itinerary)
    numvertex = controller.totalAirports3(itinerary)
    #No son 39 rutas puesto que no hay arcos repetidos pues no se tienen en cuenta las aerolineas
    print("\n === Direct Flights Graph===")
    print('Number of airports: ' + str(numvertex) + '/' + '    Number of flights: ' + str(numedges))
    
    numedges = controller.totalConnections2(itinerary)
    numvertex = controller.totalAirports2(itinerary)
    #No son 16 rutas puesto que no hay arcos repetidos pues no se tienen en cuenta las aerolineas
    print("\nCities Airports")
    print('Number of airport and Cities: ' + str(numvertex)+ '/' + '    Number of flights: ' + str(numedges))
    
    print('\nThe total number of cities is: ' + str(lt.size(itinerary['CityInfo'])))
    print('The first and last city loaded were '+ str(controller.lastCity(itinerary)))

    print('\nThe total number of airports is: ')
    print('The first airport loaded was ' + str(controller.Firstairport(itinerary)))
   

#Requirement No.1

def moreFlights (itinerary):
    points = controller.moreFlights(itinerary)
    print('\n')
    for point in lt.iterator(points):
        print(point)

#Requirement No.2


#Requirement No.3

def shortRoute (itinerary):
    route = controller.shortRoute(itinerary)
    print(route)

#Requirement No.4


#Requirement No.5


#Requirement No.6

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
            itinerary = controller.initItinerary()

        elif int(inputs[0]) == 2:
            loadData(itinerary)

        elif int(inputs[0]) == 3:
            moreFlights(itinerary)

        elif int(inputs[0]) == 4:
            pass

        elif int(inputs[0]) == 5:
            shortRoute(itinerary)

        elif int(inputs[0]) == 6:
            pass

        elif int(inputs[0]) == 7:
            pass

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()