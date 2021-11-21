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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import defaultfunction
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.Utils import error as error
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import graphstructure as gr
assert cf

# Construccion de modelos

def newItinerary():

    """ Inicializa el analizador
    Airport Routes: Tabla de Hash con los vertices del grafo
   Flights Network: Grafo para representar las rutas entre estaciones
    """
    try:
        itinerary = {
                    'Airports': None,
                    "Flights Network": None,
                    'Routes':None
                    }
        itinerary['Airports'] = m.newMap(numelements=14000, maptype='PROBING', comparefunction=compareStopIds)
        itinerary['Flights Network'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=100000 ,comparefunction=compareStopIds)
        return itinerary

    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para creacion de datos

def addStopConnection(itinerary, flight):
    """
    Adiciona las aeropuertos al grafo como vertices y arcos entre las
    estaciones adyacentes.
    Los vertices tienen por nombre el IATA del aeropuerto
    seguido de la aerolinea que sirve.  Por ejemplo:
    AER - 2B
    Si la estacion sirve otra ruta, se tiene: AER - DP
    """
    try:
        origin = formatVertex(flight)
        destination = flight ['Destination']
        cleanServiceDistance(flight)
        distance = float(flight['distance_km'])
        distance = abs(distance)
        addStop(itinerary, origin)
        addStop(itinerary, destination)
        addConnection(itinerary, origin, destination, distance)
        addRouteStop(itinerary, flight)
        return itinerary

    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def addStop(itinerary, airportIATA):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try:
        if not gr.containsVertex(itinerary['Flights Network'], airportIATA):
            gr.insertVertex(itinerary['Flights Network'], airportIATA)
        return itinerary

    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addRouteStop(itinerary, flight):
    """
    Agrega a un aeropuerto, una aerolinea que es servida en ese aeropuerto
    """
    entry = m.get(itinerary['Airports'], flight["Departure"])

    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, flight['Airline'])
        m.put(itinerary['Airports'], flight['Destination'], lstroutes)

    else:
        lstroutes = entry['value']
        info = flight['Airline']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return itinerary

def addRouteConnections(itinerary):
    """
    Por cada vertice (cada aeropuerto) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = m.keySet(itinerary['Airports'])
    for key in lt.iterator(lststops):
        lstroutes = m.get(itinerary['Airports'], key)['value']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(itinerary, prevrout, route, 0)
                addConnection(itinerary, route, prevrout, 0)
            prevrout = route

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    print(origin, "-",destination,"-", distance)
    
    edge = gr.getEdge(analyzer['Flights Network'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['Flights Network'], origin, destination, distance)
    return analyzer

# Funciones de consulta

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['Flights Network'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['Flights Network'])

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones Helper

def cleanServiceDistance(route):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if route['distance_km'] == '':
        route['distance_km'] = 0

def formatVertex(route):
    """
    Se formatea el nombre del vertice con el IATA del Aeropuerto
    seguido de la ruta.
    """
    name = route['Departure'] + '-'
    name = name + route['Airline']
    return name

# Funciones de ordenamiento

def compareStopIds(airport, keyvalueairport):
    """
    Compara dos aeropuertos
    """
    airportcode = keyvalueairport['key']
    if (airport == airportcode):
        return 0
    elif (airport > airportcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1