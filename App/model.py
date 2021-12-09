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
import math
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.Utils import error as error
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import graphstructure as gr
from DISClib.Algorithms.Graphs import dijsktra as djk
import folium
assert cf

# Construccion de modelos
def newItinerary():

    """ Inicializa el analizador
    Airports: Mapa con llave Iata y valor con diccionario con su informacion,
    Flights Network: Dígrafo en el cual se incluirán la totalidad de los aeropuertos y las rutas,
    Round Trip: Grafo con aeropuertos y las rutas que tengan tanto una ruta de ida entre los dos aeropuertos como uno de vuelta,
    City Airports: Grafo dirigido con ciudades y aeropuertos y la distancia.
    """
    try:
        itinerary = {
                    'CityInfo': None,
                    'Airports': None,
                    "Flights Network": None,
                    'Cities':None,
                    'City Airports':None
                    }
        itinerary['CityInfo'] = lt.newList("ARRAY_LIST")
        itinerary['AirportInfo'] = lt.newList('ARRAY_LIST')
        itinerary['Airports'] = m.newMap(numelements=14000, maptype='PROBING')
        itinerary['Flights Network'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=181,comparefunction=compareStopIds)
        itinerary['Cities'] = m.newMap(numelements=14000, maptype='PROBING', comparefunction=None)
        itinerary['City Airports'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=400000, comparefunction=compareStopIds)
        itinerary['Direct flights'] = gr.newGraph(datastructure='ADJ_LIST',directed=False,size=400000, comparefunction=compareStopIds)

        return itinerary

    except Exception as exp:
        error.reraise(exp, 'model:Itinerary')

# Funciones para creacion de datos

def addAirports (itinerary, airport):
    """
    Adiciona el vertice del IATA del aeropuerto al grafo Flights Network 
    y tambien guarda la informacion del aeropuerto en el mapa Airports
    """
    airportIATA = airport['IATA']
    lt.addLast(itinerary['AirportInfo'],airport)
    addVertex(itinerary['Flights Network'], airportIATA)
    addVertex(itinerary['Direct flights'], airportIATA)
    addAirportInfo(itinerary['Airports'], airportIATA, airport)
    addCityAirports(itinerary['Cities'], airportIATA, airport)

def addAirportInfo(airportMap,airportIATA, airport):
    """
    Agrega como llave el IATA y tambien guarda la informacion
    del aeropuerto como valor
    """
    airportInfo={"Name": airport['Name'],
                "City": airport["City"],
                "Country": airport["Country"],
                "Latitude": float(airport["Latitude"]),
                "Longitude": float(airport["Longitude"])}
    
    if m.get(airportMap,airportIATA)==None:
        m.put(airportMap, airportIATA, airportInfo)

def addCityAirports(cityMap,airportIATA, airport):
    """
    Agrega como llave la ciudad y tambien guarda en una lista los IATAS de 
    los aeropuertos de esa ciudad
    """
    cityIs=m.get(cityMap,airportIATA)
    if cityIs == None:
        listairports=lt.newList('SINGLE_LINKED')
        lt.addLast(listairports,airportIATA)
        m.put(cityMap, airport['Country']+'-'+airport["City"], listairports)

    else:
        listairports=cityIs['value']
        lt.addLast(listairports,airportIATA)

def addCity (itinerary, city):
    """
    Adiciona el nombre de la ciudad es ASCII al grafo City Airports
    """
    cityName = city['country']+'-'+city["city_ascii"]
    lt.addLast(itinerary['CityInfo'], city)
    addVertex(itinerary['City Airports'], cityName)
    addCityAiportsConnections(itinerary,city, cityName)

def addFlightConnections(itinerary, flight):

    try:
        origin = flight['Departure']
        destination = flight['Destination']
        cleanDistance(flight)
        distance = float(flight['distance_km'])
        distance = abs(distance)
        addArch(itinerary['Flights Network'], origin, destination, distance)
        LookDirectFlights(itinerary,origin, destination, distance)
        return itinerary

    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def LookDirectFlights(itinerary,origin,destination, distance):
    edgeOD = gr.getEdge(itinerary['Flights Network'],origin, destination)
    edgeDO = gr.getEdge(itinerary['Flights Network'],destination, origin)

    if edgeOD != None and edgeDO != None: 
        addArch(itinerary['Direct flights'],origin, destination, distance)

def addCityAiportsConnections (itinerary,city, cityName):
    """
    Se recorre el map de aeropuertos y se crean
    arcos entre el aeropuerto y la ciudad en la que se encuentran.
    """
    latCity = float(city['lat'])
    lngCity = float(city['lng'])

    InMap = m.get(itinerary["Cities"],cityName)
    if InMap !=None:
        Airports = me.getValue(InMap)
        for airport in lt.iterator(Airports):
            AirportsInfo=m.get(itinerary["Airports"],airport)["value"]
            latAirport = AirportsInfo["Latitude"]
            lngAirport = AirportsInfo["Longitude"]
            distancia = points2distance([latCity,lngCity],[latAirport,lngAirport])
            addVertex(itinerary['City Airports'],airport)
            addArch(itinerary['City Airports'],cityName,airport,distancia)

def addVertex(itinerary, newvertex):
    """
    Adiciona un vertice del grafo
    """
    try:
        if not gr.containsVertex(itinerary, newvertex):
            gr.insertVertex(itinerary, newvertex)
        return itinerary

    except Exception as exp:
        error.reraise(exp, 'model:addVertex')

def addArch(itinerary, origin, destination, distance):
    """
    Adiciona un arco entre dos vertices
    """
    #print(origin, "-",destination,"-", distance)
    edge = gr.getEdge(itinerary, origin, destination)
    if edge is None:
        gr.addEdge(itinerary, origin, destination, distance)
    return itinerary

def addAllArch(itinerary, origin, destination, distance):
    """
    Adiciona un arco entre dos vertices independientemente si este arco ya se encuentra en el grafo
    """
    #print(origin, "-",destination,"-", distance)
    gr.addEdge(itinerary, origin, destination, distance)
    return itinerary

#Requirement No.1

def moreFlights(flightsNetwork,airportdata):
    lstvert = gr.vertices(flightsNetwork)
    ordvert=lt.newList('SINGLE_LINKED')

    for vertex in lt.iterator(lstvert):
        indegree = gr.indegree(flightsNetwork,vertex)
        outdegree = gr.outdegree(flightsNetwork,vertex)
        degree=indegree+outdegree
        infovert={'Airport':vertex, 'Info': m.get(airportdata,vertex)['value'], 'Arch':int(degree), 'InBound':indegree, 'OutBound':outdegree}
        lt.addLast(ordvert,infovert)
    sa.sort(ordvert,maxarch)

    return lt.subList(ordvert,1,5)
    
def maxarch (airport1, airport2):
    return airport1['Arch']>airport2['Arch']

#Requirement No.2


#Requirement No.3

def SameNamesCityDestiny(city_destiny, itinerary):
    cities = itinerary['AirportInfo']
    city_destiny_information = []
    for city in lt.iterator(cities):
        if city['City'] == city_destiny:
            
            city_info = {'City':city['City'],
                         'Country':city['Country'],
                         'Latitude':city['Latitude'],
                         'Longitude':city['Longitude'],
                         'Airport': city['IATA']}
            city_destiny_information.append(city_info)
    return city_destiny_information


def oneairportoncity_nosearch(origin, destination,itinerary):
    graph=djk.Dijkstra(itinerary['Flights Network'],origin['Airport'])
    if djk.hasPathTo(graph,destination['Airport']):
        minRoute = djk.pathTo(graph,destination['Airport'])
        minDist = djk.distTo(graph,destination['Airport'])
    return minRoute, minDist

def getinfoAirport(itinerary,key):
    return m.get(itinerary['Airports'], key)['value']

def findclosestairport(itinerary,vertex1):
    lowest=10000000
    airport = ''
    key=vertex1['Country']+'-'+vertex1['City']
    vertexs=m.get(itinerary['Cities'],key)['value']
    for vertex in lt.iterator(vertexs):
        if gr.containsVertex(itinerary['City Airports'],vertex):
            edgeweight=gr.getEdge(itinerary['City Airports'],key,vertex)
            print(edgeweight)
            if edgeweight['weight'] < lowest:
                lowest=edgeweight
                airport = vertex
    vertex1['Airport']=airport
    return vertex1    

#Requirement No.3.2

def SameNamesCityDestiny2(city_destiny, itinerary):
    cities = itinerary['CityInfo']
    city_destiny_information = []
    for city in lt.iterator(cities):
        if city["city_ascii"] == city_destiny:
            city_info = {'City':city['city'],
                         'Country':city['country'],
                         'Latitude':city['lat'],
                         'Longitude':city['lng'],
                         'Airport': None
                         }

            city_destiny_information.append(city_info)
    return city_destiny_information


def oneairportoncity_nosearch2(origin, destination,itinerary):
    graph=djk.Dijkstra(itinerary['Flights Network'],origin['Airport'])
    if djk.hasPathTo(graph,destination['Airport']):
        minRoute = djk.pathTo(graph,destination['Airport'])
        minDist = djk.distTo(graph,destination['Airport'])
    return minRoute, minDist

def getinfoAirport2(itinerary,key):
    return m.get(itinerary['Airports'], key)['value']

def findclosestairport2(itinerary,vertex1):
    lowest=10000000
    airport = ''
    key=vertex1['Country']+'-'+vertex1['City']
    vertexs=m.get(itinerary['Cities'],key)['value']
    for vertex in lt.iterator(vertexs):
        if gr.containsVertex(itinerary['City Airports'],vertex):
            edgeweight=gr.getEdge(itinerary['City Airports'],key,vertex)
            print(edgeweight)
            if edgeweight['weight'] < lowest:
                lowest=edgeweight
                airport = vertex
    vertex1['Airport']=airport
    return vertex1    

#Requirement No.4


#Requirement No.5

def closedAirport(itinerary,airport):
    listNoAir = gr.adjacents(itinerary['Flights Network'],airport)
    sublist=lt.subList(listNoAir,1,5)
    num = archingraph (itinerary['Direct flights'],airport)
    return sublist,num

def archingraph(itinerary,airport):
    indegree = gr.indegree(itinerary,airport)
    outdegree = gr.outdegree(itinerary,airport)
    degree=indegree+outdegree
    return degree
    

#Requirement No.6

# Funciones de consulta

def totalAirports(itinerary):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(itinerary)

def totalConnections(itinerary):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(itinerary)

def cityInfo(itinerary):
    return dict(lt.firstElement(itinerary)),dict(lt.lastElement(itinerary))

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones Helper

def cleanDistance(route):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if route['distance_km'] == '':
        route['distance_km'] = 0

def decdeg2dms(dd):
    mnt,sec = divmod(dd*3600,60)
    deg,mnt = divmod(mnt,60)
    return deg,mnt,sec

def recalculate_coordinate(val,  _as=None):

  deg,  min,  sec = val
  # pass outstanding values from right to left
  min = (min or 0) + int(sec) / 60
  sec = sec % 60
  deg = (deg or 0) + int(min) / 60
  min = min % 60
  # pass decimal part from left to right
  dfrac,  dint = math.modf(deg)
  min = min + dfrac * 60
  deg = dint
  mfrac,  mint = math.modf(min)
  sec = sec + mfrac * 60
  min = mint
  if _as:
    sec = sec + min * 60 + deg * 3600
    if _as == 'sec': return sec
    if _as == 'min': return sec / 60
    if _as == 'deg': return sec / 3600
  return deg,  min,  sec
      
def points2distance(start,  end):
    lngcity=decdeg2dms(start[1])
    lngAiport=decdeg2dms(end[1])
    latcity=decdeg2dms(start[0])
    latAiport=decdeg2dms(end[0])

    start_long = math.radians(recalculate_coordinate(lngcity,  'deg'))
    start_latt = math.radians(recalculate_coordinate(latcity,  'deg'))
    end_long = math.radians(recalculate_coordinate(lngAiport,  'deg'))
    end_latt = math.radians(recalculate_coordinate(latAiport,  'deg'))
    d_latt = end_latt - start_latt
    d_long = end_long - start_long
    a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return 6371 * c

'''FUNCIONES TOMADAS DE http://www.codecodex.com/wiki/Calculate_Distance_Between_Two_Points_on_a_Globe#Python'''

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

#Requerimiento 3

def SameNamesOrigin(origin, itinerary):
    cities = itinerary['CityInfo']
    origin_information = []
    for city in lt.iterator(cities):
        if city['city_ascii'] == origin:
            city_info = {'City':city['city_ascii'],
                         'Country':city['country'],
                         'Latitude':city['lat'],
                         'Longitude':city['lng']}
            origin_information.append(city_info)
    return origin_information

def SameNamesDestination(destination, itinerary):
    cities = itinerary['CityInfo']
    destination_information = []
    for city in lt.iterator(cities):
        if city['city_ascii'] == destination:
                city_info = {'City':city['city_ascii'],
                            'Country':city['country'],
                            'Latitude':city['lat'],
                            'Longitude':city['lng']}
                destination_information.append(city_info)
    return destination_information
