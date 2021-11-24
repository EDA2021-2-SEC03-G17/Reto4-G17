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
                    'Airports': None,
                    "Flights Network": None,
                    'Round Trip':None,
                    'City Airports':None
                    }
        itinerary['CityInfo'] = lt.newList("ARRAY_LIST")
        itinerary['Airports'] = m.newMap(numelements=14000, maptype='PROBING', comparefunction=compareStopIds)
        itinerary['Flights Network'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=400000 ,comparefunction=compareStopIds)
        itinerary['Round Trip'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=400000 ,comparefunction=compareStopIds)
        itinerary['Cities'] = m.newMap(numelements=14000, maptype='PROBING', comparefunction=compareStopIds)
        itinerary['City Airports'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=400000 ,comparefunction=compareStopIds)

        return itinerary

    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para creacion de datos

def addAirports (itinerary, airport):
    """
    Adiciona el vertice del IATA del aeropuerto al grafo Flights Network 
    y tambien guarda la informacion del aeropuerto en el mapa Airports
    """
    airportIATA = airport['IATA']
    addVertex(itinerary['Flights Network'], airportIATA)
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
        m.put(cityMap, airport["City"], listairports)

    else:
        listairports=cityIs['values']
        lt.addLast(airportIATA)

def addCity (itinerary, city):
    """
    Adiciona el nombre de la ciudad es ASCII al grafo City Airports
    """
    cityName = city["city_ascii"]
    lt.addLast(itinerary['CITIES'], city)
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
        return itinerary

    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

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

# No es buena idea

def addCity2 (itinerary, city):
    """
    Adiciona el nombre de la ciudad es ASCII al grafo City Airports
    """
    cityName = city["city_ascii"]
    listairports=lt.newList()
    m.put(itinerary['City Airports2'], cityName, listairports)

    lstAirports = m.keySet(itinerary['Airports'])
    for key in lt.iterator(lstAirports):
        AirportsInfo = m.get(itinerary['Airports'], key)['value']
        m.put(itinerary['City Airports2'], AirportsInfo['City'], key)

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
            addArch(itinerary['City Airports'],city["city_ascii"],airport,distancia)

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