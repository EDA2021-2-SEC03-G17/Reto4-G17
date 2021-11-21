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

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    itinerary = model.newItinerary()
    return itinerary

def loadAirport(catalog):

    start_time = time.process_time() 
    ufosfile = cf.data_dir + "airports_full.csv"
    #C:\Users\Admin\Documents\Universidad\4TO SEMESTRE\EDA\MODULO 3\Reto3-G17\
    input_file = csv.DictReader(open(ufosfile, encoding='utf-8'))
    for airport in input_file:
        model.add_airports(catalog, airport)
    stop_time = time.process_time() 
    elapsed_time_mseg = (stop_time - start_time)*1000  
    return elapsed_time_mseg

def loadRoutes(catalog):

    start_time = time.process_time() 
    ufosfile = cf.data_dir + "routes_full.csv"
    #C:\Users\Admin\Documents\Universidad\4TO SEMESTRE\EDA\MODULO 3\Reto3-G17\
    input_file = csv.DictReader(open(ufosfile, encoding='utf-8'))
    for route in input_file:
        model.add(catalog, route)
    stop_time = time.process_time() 
    elapsed_time_mseg = (stop_time - start_time)*1000  
    return elapsed_time_mseg

def loadCities(catalog):

    start_time = time.process_time() 
    ufosfile = cf.data_dir + "worldcities.csv"
    #C:\Users\Admin\Documents\Universidad\4TO SEMESTRE\EDA\MODULO 3\Reto3-G17\
    input_file = csv.DictReader(open(ufosfile, encoding='utf-8'))
    for city in input_file:
        model.addUFO(catalog, city)
    stop_time = time.process_time() 
    elapsed_time_mseg = (stop_time - start_time)*1000  
    return elapsed_time_mseg 
# Funciones para la carga de datos

def loadServices(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de aeropuertos que
    pertenecen a la misma y van en el mismo sentido.
    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    routesfile = cf.data_dir + 'routes_full.csv'
    input_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    lastroute = None
    for route in input_file:
        #if lastroute is not None:
            #sameAirline = lastroute['Airline'] == route['Airline']
            #sameDestiny = lastroute['Destination'] == route['Destination']
            #sameDeparture = lastroute['Departure'] == route['Airline']
            #if sameAirline and sameDestiny and not sameDeparture:
        model.addStopConnection(analyzer, route)
        lastroute = route
    model.addRouteConnections(analyzer)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)

def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)
