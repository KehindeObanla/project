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
import re
import networkx as nx
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)
"""
  _   _ _____ _     ____  _____ ____
 | | | | ____| |   |  _ \| ____|  _ \
 | |_| |  _| | |   | |_) |  _| | |_) |
 |  _  | |___| |___|  __/| |___|  _ <
 |_| |_|_____|_____|_|   |_____|_| \_\

"""


def logg(data):
    with open("logg.log", "w") as logger:
        logger.write(json.dumps(data, indent=4))


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

    return jsonify(result)


def formatHelp(route):
    """ Gets the __doc__ text from a method and formats it
        for easier viewing. Whats "__doc__"? This text
        that your reading is!!
    """
    help = globals().get(str(route)).__doc__
    if help != None:
        help = help.split("\n")
        clean_help = []
        for i in range(len(help)):
            help[i] = help[i].rstrip()
            if len(help[i]) > 0:
                clean_help.append(help[i])
    else:
        clean_help = "No Help Provided."
    return clean_help


def isFloat(string):
    """ Helper method to test if val can be float
        without throwing an actual error.
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def isJson(data):
    """ Helper method to test if val can be json
        without throwing an actual error.
    """
    try:
        json.loads(data)
        return True
    except ValueError:
        return False


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

                    return list(data)
    return None

""" validates a json """
def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

""" creates bounding box """
def point_to_bbox(lng, lat, offset=.001):
    return (float(lng-offset), float(lat-offset), float(lng+offset), float(lat+offset))

""" loads rtee """
def build_index(path):
    eqks = glob.glob(path)
    del eqks[400:840]
    count = 0
    bad = 0
    uniqueueEarthhquakeid = {}

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
                uniqueueEarthhquakeid[count] = row
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
       
    return idx, uniqueueEarthhquakeid

 # returns a list of nearest neigh

""" finds nearest neghibours given a lng lat """
def nearestNeighbors(lng, lat):
    answer_Collection = {
        "type": "FeatureCollection",
        "features": []
    }
    left, bottom, right, top = point_to_bbox(lng, lat)
    nearestearthquakes = list(idx.nearest((left, bottom, right, top), 5))
    nearestearthquakeslist = []
    # for each id get all other properties from
    # rtee and add it to a list

    for item in nearestearthquakes:
        nearestearthquakeslist.append({
            'type': 'Feature',
            'geometry': rtreeid[item]['geometry'],
            'properties': rtreeid[item]['properties']
        })
    
   # add nearestearthquakeslist to a dictionary
   # to make it a geojson file
    answer_Collection['features'] = nearestearthquakeslist
    # convert into JSON:
    convertedtoProperGeojson = json.dumps(answer_Collection)
    # the result is a JSON string:
    # to be used as id in the frontend
    return convertedtoProperGeojson
""" retruns a geojson that includes the
latlng in a within a bounding box """
def intersection(left,bottom,right,top):
    left = round(float(left),4)
    bottom = round(float(bottom),4)
    right = round(float(right),4)
    top = round(float(top),4)
    answer_Collection = {
        "type": "FeatureCollection",
        "features": []
    }
   
    intersect = list(idx.intersection((left, bottom, right,top),objects=True))
    
    intersectid =[]
    for ids in intersect:
        intersectid.append(ids.id)
    intersectid = list(dict.fromkeys(intersectid))    
    
    withinboundinboxlist = []
    for item in intersectid:
        withinboundinboxlist.append({
            'type': 'Feature',
            'geometry': rtreeid[item]['geometry'],
            'properties': rtreeid[item]['properties']
        })
    # add nearestlist to a dictionary
    # to make it a geojson file
    answer_Collection['features'] = withinboundinboxlist
    # convert into JSON:
    convertedGeojson = json.dumps(answer_Collection)
    # the result is a JSON string:
    # to be used as id in the frontend
    return convertedGeojson
""" checks a valid geojson """
def checkgeojson(dic,value,key ="type"):
        answer ="True"
        if(key =="type" and value == "Feature"):
            flag = checkfeature(dic)
            if(flag ==True):
                return answer
            else:
                return "invalid geojson"
            
        elif(key =="type" and value == "FeatureCollection"):
            flag2 = checkFeatureCollection(dic)
            if(flag2 ==True):
                return answer
            else:
                return "invalid geojson"
        else:
            return "invalid geojson"
           
        
""" checks a valid feature geojson """
def checkfeature(dic):
    featuretype =["Point", "LineString", "Polygon", "MultiPoint", "MultiLineString","MultiPolygon"]
    propertyflag = False
    count = 0
    if("type" not in dic):
        count-=1
    if("geometry" not in dic):
        count-=1
    for key, value in dic.items() :
      
        if(key =="type" and value == "Feature"):
            count+=1
        elif(key =="geometry" and isinstance(value ,dict)):
            count+=1
            
            if("type" not in value):
                count-=1
            if("coordinates" not in value):
                count-=1
            for key, value in value.items() :
               
                if(key == "type"and value  not in featuretype):
                    count-=1
                if(key =="coordinates"and isinstance(value ,list)):
                    count+=1
       
        elif(key =="properties" and isinstance(value ,dict)):
            propertyflag=True
            count+=1
    
    if(count ==4 and propertyflag == True):
        return True
    elif(count ==3 and propertyflag == False):
        return True
    else:
        return False
    
""" checks a valid featurecollection geojson """
def checkFeatureCollection(dic):
    flag = False
    count =0
    if("type" not in dic):
        count-=1
    for key, value in dic.items() :
        if(key =="type" and value == "FeatureCollection"):
            count+=1
        if(key =="features"):
            if(isinstance(value,list)):
                
                for feat in value:
                    flag = checkfeature(feat)
                    if (flag == False):
                        return False
    if(flag == True and count == 1):
        return True
""" build rtree for primary roads """
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


        


    

"""
  ____    _  _____  _      ____    _    ____ _  _______ _   _ ____
 |  _ \  / \|_   _|/ \    | __ )  / \  / ___| |/ / ____| \ | |  _ \
 | | | |/ _ \ | | / _ \   |  _ \ / _ \| |   | ' /|  _| |  \| | | | |
 | |_| / ___ \| |/ ___ \  | |_) / ___ \ |___| . \| |___| |\  | |_| |
 |____/_/   \_\_/_/   \_\ |____/_/   \_\____|_|\_\_____|_| \_|____/

Helper classes to act as our data backend.
"""

STATES = load_data(
    "assignments\\A04\\assets\\json\\countries_states\\states.json")
STATE_BBOXS = load_data(
    "assignments\\A04\\assets\\json\\countries_states\\us_states_bbox.csv")
CITIES = load_data(
    "assignments\\A04\\assets\\json\\countries_states\\major_cities.geojson")
EQK = glob.glob("assignments\\A04\\assets\\json\\us_railroads\\*.geojson")
roadgeojsonpath = "assignments\\A04\\assets\\json\\Primary_Roads.geojson\\Primary_Roads.geojson"
idx = index.Index()
idx2 = index.Index()
eqrthquakepath = "assignments\\A04\\Assets\\json\\earthquake_data\\earthquakes\\*.json"
idx, rtreeid= build_index(eqrthquakepath)
idx2, rtreeroadid = build_indexPrima(roadgeojsonpath)
majorRoadsRelative ="assignments\\A04\\assets\\json\\shapefile\\primaryroadshap.shp"
""" shape file to graph """
shapefileToGraph = nx.read_shp(majorRoadsRelative,simplify=False,geom_attrs=True,strict=True)
G2 = shapefileToGraph.to_undirected()

"""
   ____   ___  _   _ _____ _____ ____  
  |  _ \ / _ \| | | |_   _| ____/ ___| 
  | |_) | | | | | | | | | |  _| \___ \ 
  |  _ <| |_| | |_| | | | | |___ ___) |
  |_| \_\\___/ \___/  |_| |_____|____/ 
"""


@app.route("/token", methods=["GET"])
def getToken():
    """ getToken: this gets mapbox token
    """
    token = {'token': 'pk.eyJ1Ijoia2VoaW5kZW9iYW5sYSIsImEiOiJja2ZuNm42b3kxamwzMndrdXIyNHkzOG8wIn0.qe4TrmVMMfi1Enpcvk5GfQ'}

    return token


@app.route("/", methods=["GET"])
def getRoutes():
    """ getRoutes: this gets all the routes to display as help for developer.
    """
    routes = {}
    for r in app.url_map._rules:

        routes[r.rule] = {}
        routes[r.rule]["functionName"] = r.endpoint
        routes[r.rule]["help"] = formatHelp(r.endpoint)
        routes[r.rule]["methods"] = list(r.methods)

    routes.pop("/static/<path:filename>")
    routes.pop("/")

    response = json.dumps(routes, indent=4, sort_keys=True)
    response = response.replace("\n", "<br>")
    return "<pre>"+response+"</pre>"




@app.route('/nearestNeighbors/')
def click():
    """ Description: return a list of US nearest negihbours
        Params: 
            None
        Example:http://localhost:8080/nearestNeighbors/?lngLat="
    """
    lng, lat = request.args.get("lngLat", None).split(",")
    return nearestNeighbors(float(lng), float(lat))


@app.route('/cities', methods=["GET"])
def cities():
    """ Description: return a list of US ciyies names and long lat
        Params: 
            None
        Example: http://localhost:8080/cities?filter=mis
    """
    filter = request.args.get('filter', None)
    results = []
    if (filter):

        for city in CITIES["features"]:
            if filter.lower() == city["properties"]["name"][:len(filter)].lower():
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

    return handle_response(results)


""" using halversine function to find distance """


@app.route('/distance/', methods=["GET"])
def finddistance():
    """ Description: return a distance between two points
        Params: 
            None
        Example: http://localhost:8080/distance/?lnglat=
    """
    lng, lat, lng1, lat1 = request.args.get('lnglat', None).split(",")
    checkformiORkm = request.args.get('lnglat', None).split(";")
    lng, lat, lng1, lat1 = checkformiORkm[0].split(",")
    mile = checkformiORkm[1]
    if(mile == 'mile'):
        lnglat = (float(lng), float(lat))
        lnglat1 = (float(lng1), float(lat1))
        answer = haversine(lnglat, lnglat1, miles=True)
        return str(answer)

    else:
        lnglat = (float(lng), float(lat))
        lnglat1 = (float(lng1), float(lat1))
        answer = haversine(lnglat, lnglat1, miles=False)
        return str(answer)


@app.route('/states', methods=["GET"])
def states():
    """ Description: return a list of US state names
        Params: 
            None
        Example: http://localhost:8080/states?filter=mis
    """
    filter = request.args.get('filter', None)

    if filter:
        results = []
        for state in STATES:
            if filter.lower() == state['name'][:len(filter)].lower():
                results.append(state)
    else:
        results = STATES

    return handle_response(results)




@app.route('/StatesRailroad/', methods=["GET"])
def railroad():
    """ Description: returns a geojson of rail roads given a state name
        Params: 
            None
        Example: http://localhost:8080/StatesRailroad?state=mis
    """
    answer_Collection ={
        "type" :"Feature",
        "features": [],
       " properties": {},
        "geometry": {
        "type": "LineString",
        "coordinates": None
        }
    }
    """ filter = request.args.get('state', None) """
    state = request.args.get('state', None)
    state = state.lower()
    
    results = []
   
    for efile in EQK:

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
    if(answer_Collection["geometry"]["coordinates"]) :
        return answer_Collection
        
    return handle_response(answer_Collection) 
@app.route('/interSection/')
def inter():
    """ Description: takes a bounding box and returns a feature collection with
        Params: 
            None
        Example:http://localhost:8080/interSection/?lngLat="
    """
    coord= request.args.get("lngLat", None).split(",")
    left = coord[0]
    bottom = coord[1]
    right = coord[2]
    top = coord[3]
     
    return intersection(left, bottom, right, top)
@app.route('/ValidGeoJson/', methods=["GET"])
def Create():
    """ Description: returns true or false
        Params: 
            None
        Example:http://localhost:8080/ValidGeoJson/?value="

    """

    parts= request.args.get("value", None).split(";")
    send = json.loads(parts[0])
    featureorFC = parts[1]
    return checkgeojson(send,featureorFC)

@app.route('/Travel/', methods=["GET"])
def Travel():
    """ Description: returns a geojson of rail roads given a state name
        Params: 
            None
        Example: http://localhost:8080/Travel/?lnglat=
    """
    answer_Collection = {
        "type": "FeatureCollection",
        "features": [ ]
    }
    results = []
    lng, lat, lng1, lat1 = request.args.get('lnglat', None).split(",")
    checkformiORkm = request.args.get('lnglat', None).split(";")
    lng, lat, lng1, lat1 = checkformiORkm[0].split(",")
    lnglat = nearestNeighborsRoads(float(lng), float(lat))
    lnglat1 = nearestNeighborsRoads(float(lng1), float(lat1))
    path = nx.shortest_path(G2, source = tuple(lnglat[0]), target = tuple(lnglat1[0]), weight = None, method = 'dijkstra')
    if isinstance(path, list):
        for point in path:
            results.append(list(point))
        answer_Collection["features"].append({"type":"Feature",
          "properties": {},
            "geometry":
            {
            "type": "LineString",
            "coordinates": results
            }})
        convertedGeojson = json.dumps(answer_Collection)
        with open('data.json', 'w') as outfile:
            json.dump(answer_Collection, outfile)
        return convertedGeojson
    else:
        answer = path
    return answer
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
