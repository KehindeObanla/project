import sys
import os
from rtree import index
from flask import Flask
from flask import request
from flask import jsonify
from json import loads
from flask_cors import CORS
from misc_functions import *
import glob
import json
import math
from rtree import index
import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import open_file

idx = index.Index()
idx2 = index.Index()
pathRoad ='assignments\\A04\\assets\\json\\Primary_Roads.geojson\\Primary_Roads.geojson'
def finddistance():
    """ Description: return a distance between two points
        Params:
            None
        Example: http://localhost:8080/distance/?lnglat=
    """
    lng, lat, lng1, lat1 = -124.000, 34.000, -124.0020, 34.0020
    lnglat = (float(lng), float(lat))
    lnglat1 = (float(lng1), float(lat1))
    return haversine(lnglat, lnglat1, miles=True)


def load_data(path):
    """ Given a path, load the file and handle it based on its
        extension type. So far I have code for json and csv files.
    """
    _, ftype = os.path.splitext(path)   # get fname (_), and extenstion (ftype)

    if os.path.isfile(path):            # is it a real file?
        with open(path) as f:

            if ftype == ".json" or ftype == ".geojson":  # handle json
                data = f.read()
                if isJson(data):
                    return json.loads(data)

            elif ftype == ".csv":       # handle csv with csv reader
                with open(path, newline='') as csvfile:
                    data = csv.DictReader(csvfile)


def isJson(data):
    """ Helper method to test if val can be json
        without throwing an actual error.
    """
    try:
        json.loads(data)
        return True
    except ValueError:
        return False


CITIES = load_data(
    "assignments\\A04\\assets\\json\\countries_states\\major_cities.geojson")
STATES = load_data(
    "assignments\\A04\\assets\\json\\countries_states\\states.json")
majorRoadsRelative ="assignments\\A04\\assets\\json\\shapefile\\primaryroadshap.shp"
majormerged ="assignments\\A04\\assets\\json\\orimerge.shp"
populatedplaces = "ne_10m_populated_places\\ne_10m_populated_places.shp"


 """ shape file to graph """
""" shapefileToGraph2 = nx.read_shp(majormerged,simplify=False,geom_attrs=True,strict=True) """
shapefileToGraph = nx.read_shp(majorRoadsRelative,simplify=False,geom_attrs=True,strict=True)
G2 = shapefileToGraph.to_undirected()

citiesGraph = nx.read_shp(populatedplaces,simplify=True,geom_attrs=True,strict=True)
undirectedcities = citiesGraph.to_undirected()
undirectedcities.add_edges_from(G2.edges)

def cities():
    """ Description: return a list of US state names
        Params:
            None
        Example: http://localhost:8080/cities
    """
    """ filter = request.args.get('filter',None) """
    results = []

    for city in CITIES["features"]:
        answers = {
            "Name": city["properties"]["name"],
            "Coordinates": city["geometry"]["coordinates"]
        }
        results.append(answers)
    print(results[0])


def sub():
    filter = ''
    results = []
    if (filter):

        for city in CITIES["features"]:
            if filter.lower() == city["properties"]["name"].lower():
                answers = {
                    "Name": city["properties"]["name"],
                    "Coordinates": city["geometry"]["coordinates"]
                }
                results.append(answers)
    else:
        for city in CITIES["features"]:
            answers = {
                "Name": city["properties"]["name"],
                "Coordinates": city["geometry"]["coordinates"]
            }
            results.append(answers)
    print(results[0])
    return handle_response(results)


def handle_response(data, params=None, error=None):
    """ handle_response
    """
    success = True
    if data:
        if not isinstance(data, list):
            data = [data]
        count = len(data)
    else:
        count = 0
        error = "Data variable is empty!"

    result = {"success": success, "count": count,
              "results": data, "params": params}

    if error:
        success = False
        result['error'] = error

    return (jsonify(result))


def states():
    """ Description: return a list of US state names
        Params:
            None
        Example: http://localhost:8080/states?filter=mis
    """
    filter = "texas"

    if filter:
        results = []
        for state in STATES:
            if filter.lower() == state['name'][:len(filter)].lower():
                results.append(state)
                print(state)
    else:
        results = STATES


def railroad2():
    answer_Collection = {
        "type": "Feature",
        "features": [],
       " properties": {},
        "geometry": {
        "type": "LineString",
        "coordinates": None
        }
    }
    """ filter = request.args.get('state', None) """
    state = "North Carolina"
    state = state.lower()
    results = []
    eqks = glob.glob("assignments\\A04\\assets\\json\\us_railroads\\*.geojson")
    for efile in eqks:

        with open(efile, 'r', encoding='utf-8') as f:
            data = f.read()
            convertedGeojson = json.loads(data)
            for rail in convertedGeojson["features"]:
                statesinRail = rail["properties"]["states"]
                statesinRail = [item.lower() for item in statesinRail]
                if(state in statesinRail):
                    for coord in rail["geometry"]["coordinates"]:
                        results.append(coord)
           
            answer_Collection["geometry"]["coordinates"] = results
    for key, value in answer_Collection.items() :
        print (key)
   


def railroad():
    """ Description: return a list of US state names
                     with railroads
        Params: 
            None
        Example: http://localhost:8080/railroad?filter=mis
    """

    filter = None
    results = []
    count = 0
    eqks = glob.glob("assignments\\A04\\assets\\json\\us_railroads\\*.geojson")
    for efile in eqks:

        with open(efile, 'r', encoding='utf-8') as f:
            data = f.read()
            convertedGeojson = json.loads(data)
            if(filter):
                for rail in convertedGeojson["features"]:
                    statesinRail = rail["properties"]["states"]
                    for state in statesinRail:
                        if filter.lower() == state[:len(filter)].lower():
                            results.append(state)
            else:

                for rail in convertedGeojson["features"]:
                    count += 1
                    statesinRail = rail["properties"]["states"]
                    for state in statesinRail:
                        results.append(state)
    mylist = list(dict.fromkeys(results))
    print(mylist)
    print(count)
def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True
def point_to_bbox(lng, lat, offset=.001):
    #(left, bottom, right, top)

    return (float(lng-offset), float(lat-offset), float(lng+offset), float(lat+offset))
def build_index():
    #(left, bottom, right, top)

    eqks = glob.glob(
        "assignments\\A04\\Assets\\json\\earthquake_data\\earthquakes\\*.json")
    del eqks[350:840]
    count = 0
    bad = 0
    earthquakeUniqueid = {}

    for efile in eqks:
        minlat = 999
        minlng = 999
        maxlat = -999
        maxlng = -999
        with open(efile, 'r', encoding='utf-8') as f:
            data = f.readlines()

        for row in data[2:]:
            row = row.strip()
            row = row.strip(",")
            if validateJSON(row):
                row = json.loads(row)
                lng, lat, _ = row["geometry"]["coordinates"]
                earthquakeUniqueid[count] = row
                if lng < minlng:
                    minlng = lng
                if lat < minlat:
                    minlat = lat
                if lng > maxlng:
                    maxlng = lng
                if lat > maxlat:
                    maxlat = lat

                left, bottom, right, top = point_to_bbox(lng, lat)
                idx.insert(count, (left, bottom, right, top))
                count += 1
            else:
                bad += 1
        """  print(count) """
    return idx, earthquakeUniqueid
def nearestNeighbors(lng, lat):
    answer_Collection = {
        "type": "FeatureCollection",
        "features": []
    }
    answer_CollectionpolyGon = {
        "type": "FeatureCollection",
        "features": [
            {

            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates':[]
            }
            }
          
       ]
    }

    idx, rtreeid = build_index()
    left, bottom, right, top = point_to_bbox(lng, lat)
    nearest = list(idx.nearest((left, bottom, right, top), 2))
    print(nearest)
    nearestlist = []

    dic ={}
    polygon =[]
    
    # for each id get all other properties from
    # rtee and add it to a list

    for item in nearest:
        nearestlist.append({
            'type': 'Feature',
            'geometry': rtreeid[item]['geometry'],
            'properties': rtreeid[item]['properties']
        })
        
        dic = rtreeid[item]['geometry']
        for key,value in dic.items():
            if key =='coordinates':
                lnglat =[]
                lnglat.append(value[0])
                lnglat.append(value[1])
        polygon.append(lnglat)
                
    for item in answer_CollectionpolyGon['features']:
        item['geometry']['coordinates'].append( polygon)
    print( answer_CollectionpolyGon)
   # add nearestlist to a dictionary
   # to make it a geojson file
    answer_Collection['features'] = nearestlist
    # convert into JSON:
    convertedGeojson = json.dumps(answer_CollectionpolyGon)
    print( convertedGeojson)
    # the result is a JSON string:
    # to be used as id in the frontend
def intersection(left,bottom,right,top):
  
    print(type( left))
   
    answer_Collection = {
        "type": "FeatureCollection",
        "features": []
    }
    idx, rtreeid = build_index()
    intersect = list(idx.intersection((left, bottom, right, top),objects=True))
    intersectid =[]
    for ids in intersect:
        intersectid.append(ids.id)
    intersectid = list(dict.fromkeys(intersectid))    
    
    nearestlist = []
    for item in intersectid:
        dic = rtreeid[item]['geometry']
        for key,value in dic.items():
            if key =='coordinates':
                lng = value[0]
                lat = value[1]
                flag = inboundingBox(bottom,left,top,right,lng,lat)
                if flag ==True:
                    nearestlist.append({
                    'type': 'Feature',
                    'geometry': rtreeid[item]['geometry'],
                    'properties': rtreeid[item]['properties']
                    })
      
    # add nearestlist to a dictionary
    # to make it a geojson file
    answer_Collection['features'] = nearestlist
    # convert into JSON:
    convertedGeojson = json.dumps(answer_Collection)
    # the result is a JSON string:
    # to be used as id in the frontend
    return convertedGeojson

def inboundingBox(x1, y1, x2,y2, x, y) : 
    if (x > x1 and x < x2 and y > y1 and y < y2) : 
        return True
    else : 
        return False



def randomcolorgenerator():
    r = lambda: random.randint(0,255)
    print('#%02X%02X%02X' % (r(),r(),r()))
    
def checkgeojson():
    json ={
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [125.6, 10.1]
  },
  "properties": {
    "name": "Dinagat Islands"
  }
} 
def build_indexPrima(path):
    uniqueueRoadid = {}
    count =0
    minlat = 999
    minlng = 999
    maxlat = -999
    maxlng = -999
    data = load_data(path)
    feature = data['features']
    for row in feature:
        resultlist= row["geometry"]["coordinates"]
        for coord in resultlist:
            lng, lat= coord[0]
            uniqueueRoadid[count] = row
            if lng < minlng:
                minlng = lng
            if lat < minlat:
                 minlat = lat
            if lng > maxlng:
                maxlng = lng
            if lat > maxlat:
                maxlat = lat
            left, bottom, right, top = point_to_bbox(lng, lat)
            idx2.insert(count, (left, bottom, right, top))
            count += 1
    """ print(len(uniqueueRoadid)) """
    return idx2, uniqueueRoadid  
idx2, rtreeroadid = build_indexPrima(pathRoad)
def nearestNeighborsRoads(lng, lat):
    left, bottom, right, top = point_to_bbox(lng, lat)
    nearest = list(idx2.nearest((left, bottom, right, top), 1))
    print(len(nearest))
    print(nearest)
    nearestlist = []
    for item in nearest:
        coords = rtreeroadid[item]['geometry']["coordinates"]
        listed = coords[0]
        nearestlist.append(
        listed[0])
  
    return nearestlist

def Travel(lng ,lat,lng1,lat1):
    results = []
    lnglat = nearestNeighborsRoads(lng,lat)
    lnglat1 = nearestNeighborsRoads(lng1,lat1)
    path = nx.shortest_path(G2,source = tuple(lnglat[0]), target = tuple(lnglat1[0]),weight = None, method = 'dijkstra')
    if isinstance(path, list):
        for point in path:
            results.append(list(point))
        return results
    else:
        answer = (path)
    return(answer)
def intersection2(left,bottom,right,top):
    left = round(float(left),4)
    bottom = round(float(bottom),4)
    right = round(float(right),4)
    top = round(float(top),4)
    intersect = list(idx2.intersection((left, bottom, right,top),objects=True))
    
    intersectid =[]
    for ids in intersect:
        intersectid.append(ids.id)
    intersectid = list(dict.fromkeys(intersectid))    
    
    withinboundinboxlist = []
    for item in intersectid:
        coords = rtreeroadid[item]['geometry']["coordinates"]
        listed = coords[0]
        withinboundinboxlist.append(listed[0])

def checkcitiesGraph():
    

def completegraph()
    listofnodes = list(citiesGraph.nodes)
    length = len(listofnodes)
    array = []
    array.append(Point(firctcoor[0],firstcor[[1]])
    for city in listofnodes:
        for i in range(1,length):
            lnglat1 = listofnodes[i]
            lng1 = lnglat1[0]
            lat1 = lnglat1[1]
            lng = city[0]
            lat = city[1]
            lineSegment = Travel(lng,lat,lng1,lat1)


                

    
    
        

    

    
   
if __name__ == '__main__':
    checkcitiesGraph()
   
    
   
   