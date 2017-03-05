import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import json
import falcon
import urllib
import uuid
import settings
import requests
from geopy.geocoders import Nominatim
import geopy.distance
from geopy.distance import vincenty
import datetime
radius = []
geoJSON_template = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          
        ]
      }
    }
  ]
}

class interest(object):
    global radius
    interested = {}
    #radius = []i
    def proximity_to_others(self, my_coordinates):
        if radius:
            for x in radius:
                radius_center = (x['center'][0],x['center'][1])
                my_coordinates = (my_coordinates[0], my_coordinates[1])
                distance = vincenty(radius_center, my_coordinates).kilometers
                print "Proximity distance"
                print distance
                return distance, x["center"]
        else:
            return 0, []
    def geojson_io_prox(self, resp, my_coordinates, user_name):
        global radius
        distance = 0
        radius = []
        try:
            distance,radius  = self.proximity_to_others(my_coordinates)
        except Exception as e:
            print e
        if not distance or distance < 1:
            points = []
            start = geopy.Point(my_coordinates[0], my_coordinates[1])
            d = geopy.distance.VincentyDistance(kilometers = 1)
            for x in range(0,360, 10):
                points.append(d.destination(point=start, bearing=x))
            print "\n\n POINTS"
        #print points
            print "\n\n"
            radius_dict = {
                'center': my_coordinates,
                'radius': points,
                'people': [user_name,],
                'created_date': datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
                        }
        #self.radius.apppend(radius_dict)
            radius.append(radius_dict)
            print "\n\n RADIUS: "
            print radius
            print "\n\n"

        else:
            for x in radius:
                if x["center"] == radius:
                    x['people'].append(
                        {'name': user_name,
                         'coordinates':
                         my_coordinates}
                    )

    def proximity(self,req, resp, my_coordinates, user_name):
       # print settings.API_URL
        google_map_url = "http://www.google.com/maps/place/"
        query_params = {"point":"{},{}".format(my_coordinates[0], my_coordinates[1]),
                        "radius":"1000"}
        endpoint ="api/stops"
        headers = {"Authorization": "Bearer {}".format(settings.ACCESS_TOKEN)}
        request = requests.get("{}/{}".format(settings.API_URL,endpoint),
                               params=query_params,
                               headers=headers)
        print "Response from api/stops"
        print request.status_code
        response_data = request.json()
        print "response_data type"
        print type(response_data)
        if not response_data:
            print 'response_data == "[]"'
            resp.status = falcon.HTTP_200
            resp.body = """{'message' :
                'No stops in your area, adding you to interest area'}"""
            return False
        else:
            map_list = []
            message_dict = {"message":"", "maps":[]}
            for x in response_data:
                print x
                if 'geometry' in x:
                    coordinates = x["geometry"]["coordinates"]
                    map_list.append("{}{},{}".format(google_map_url, 
                                                     coordinates[1], 
                                                     coordinates[0]))
            #print x['geometry']
            message_dict["maps"] = map_list
            if message_dict:
                message_dict["message"] = """You have existing stops within 1km 
                of your location"""
            else:
                message_dict["messsage"] = """You\shave no existing stops nearby, 
                we will combine your interest in a stop with others in the area"""
            resp.body = "{}".format(message_dict)
            resp.status = falcon.HTTP_200
            return True
            #return True
        #print json.load(request.text)

    def geopy_coordinates(self, address,resp):
        try:
            geolocator = Nominatim()
            location = geolocator.geocode(address)
            if location.latitude and location.longitude:
                return [location.latitude, location.longitude]
        except Exception as e:
            print e
            resp.body = """{'message':'Bad address,
            try being more specific and try agai'}"""
            resp.status = falcon.HTTP_400


    def on_get(self, req, resp):
        resp.body = '{"message":"Post request needed with GeoLocation data"}'
        resp.status = falcon.HTTP_200
    def on_post(self, req, resp):
        global radius
        print req.headers
        user_name = ""
        post_data = json.load(req.stream)
        print post_data
        if "name" in post_data:
            user_name = post_data["name"]
            print "Username IF statement"
            print user_name
        if "geometry" in post_data:
            #self.geojson_io_prox(resp, post_data["geometry"]["coordinates"],user_name)
            if not self.proximity(req,resp, post_data["geometry"]["coordinates"],user_name):
                self.geojson_io_prox(resp, post_data["geometry"]["coordinates"],user_name)
            #self.geojson_io_prox(resp, post_data["geometry"]["coordinates"])
        elif post_data["address"]:
            if "address" in post_data:
                my_coordinates = self.geopy_coordinates(post_data["address"],resp)
                #self.geojson_io_prox(resp,my_coordinates, user_name)
                print "BASED ON ADDRESS"
                proximity = self.proximity(req, resp, my_coordinates, user_name)
                print "PROXIMITY"
                print proximity
                if proximity == False:
                    print "NO routes"
                    self.geojson_io_prox(resp,my_coordinates, user_name)
                    #print "No routes"
        else:
            falcon.HTTPMissingParam
            resp.body = """{ 'message' :
                'Please supply a address or coordinates (long,lat)'}"""
        
        print "Current Radius"
        print radius
        radius_list = []
        radius_maps = []
        for x in radius:
            for y in x['radius']:
                radius_list.append([y[0],y[1]])
            radius_list.append([x['radius'][0][0],x['radius'][0][1]])
            geoJSON_template['features'][0]['geometry']['coordinates'].append(radius_list)
            radius_maps.append( {
                'center': x['center'],
                'geoJSON': geoJSON_template,
                'geoJSON_url' : "http://geojson.io/#map=5/{}/{}&data=data:application/json,{}".format(
                x['center'][0], x['center'][1], urllib.quote(json.dumps(geoJSON_template).encode()) )
            }
            )
        resp.body
        print radius_maps
        #print geoJSON_template
