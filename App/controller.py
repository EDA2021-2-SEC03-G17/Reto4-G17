"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

import config as cf
import model
import csv
import time

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initItinerary():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    itinerary = model.newItinerary()
    return itinerary

# Funciones para la carga de datos

def loadItinerary(itinerary):
    start_time = time.process_time() 
    loadAirport(itinerary)
    loadFlights(itinerary)
    loadCities(itinerary)
    stop_time = time.process_time() 
    elapsed_time_mseg = (stop_time - start_time)*1000  
    return elapsed_time_mseg

def loadAirport(itinerary):

    airportsfile = cf.data_dir + "airports-utf8-small.csv"
    #C:\Users\Admin\Documents\Universidad\4TO SEMESTRE\EDA\MODULO 3\Reto3-G17\
    input_file = csv.DictReader(open(airportsfile, encoding='utf-8'))
    for airport in input_file:
        model.addAirports(itinerary, airport)
    print('Aiports: Done')
    
def loadCities(itinerary):

    citiesfile = cf.data_dir + "worldcities-utf8.csv"
    #C:\Users\Admin\Documents\Universidad\4TO SEMESTRE\EDA\MODULO 3\Reto3-G17\
    input_file = csv.DictReader(open(citiesfile, encoding='utf-8'))
    for city in input_file:
        model.addCity(itinerary, city)
    print('Cities: Done')

def loadFlights(itinerary):

    flightsfile = cf.data_dir + "routes-utf8-small.csv"
    #C:\Users\Admin\Documents\Universidad\4TO SEMESTRE\EDA\MODULO 3\Reto3-G17\
    input_file = csv.DictReader(open(flightsfile, encoding='utf-8'))
    for route in input_file:
        model.addFlightConnections(itinerary, route)
    print('Flights: Done')

#Requirement No.1

def moreFlights(itinerary):
    return model.moreFlights(itinerary['Flights Network'],itinerary['Airports'])

#Requirement No.2


#Requirement No.3
def findclosestairport(itinerary,vertex):
    return model.findclosestairport(itinerary,vertex)

def SameNamesOrigin(origin, itinerary):
    return model.SameNamesCityDestiny(origin,itinerary)

def SameNamesDestination(destination, itinerary):
    return model.SameNamesCityDestiny(destination,itinerary)

def MinRoute(origin, destination, itinerary):
    return model.MinRoute(origin, destination, itinerary) 

def MinRouteOneAirport(origin, destinatination, itinerary):
    return model.oneairportoncity_nosearch(origin, destinatination, itinerary)

def getinfoAirport (itinerary,key):
    return model.getinfoAirport(itinerary,key)
#Requirement No.4


#Requirement No.5

def closedAirport(itinerary,airport):
    return model.closedAirport(itinerary,airport)

def totalConnections5(itinerary):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(itinerary)

def totalAirports5(itinerary):
    """
    Total de paradas de autobus
    """
    return model.totalAirports(itinerary)

#Requirement No.6

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def totalAirports(itinerary):
    """
    Total de paradas de autobus
    """
    return model.totalAirports(itinerary['Flights Network'])

def totalConnections(itinerary):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(itinerary['Flights Network'])

def totalAirports2(itinerary):
    """
    Total de paradas de autobus
    """
    return model.totalAirports(itinerary['City Airports'])

def totalConnections2(itinerary):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(itinerary['City Airports'])

def totalConnections3(itinerary):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(itinerary['Direct flights'])

def totalAirports3(itinerary):
    """
    Total de paradas de autobus
    """
    return model.totalAirports(itinerary['Direct flights'])

def Firstairport(itinerary):
    return model.cityInfo(itinerary['AirportInfo'])

    return model.AirportsInfo(itinerary['Airports'])

# Requerimientos
#Req 2
def StronglyConnectedComponents(IATA1, IATA2, itinerary):
    return model.StronglyConnectedComponents(IATA1, IATA2, itinerary)


#Req 4
def TravelerMiles(origin, miles, itinerary):
    return model.TravelerMiles(origin, miles, itinerary)
def lastCity(itinerary):
    return model.cityInfo(itinerary["CityInfo"])
