import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import json
import falcon
import uuid
import settings
import requests
from geopy.geocoders import Nominatim
import geopy.distance
from geopy.distance import vincenty
radius = []

class interest(object):
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
    def geojson_io_prox(self, resp, my_coordinates, user_name):
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
                'people': []
                        }
        #self.radius.apppend(radius_dict)
            radius.append(radius_dict)
        #print radius
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
        if response_data == "[]":
            resp.status = falcon.HTTP_200
            resp.body = """{'message' :
                'No stops in your area, adding you to interest area'}"""
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
            print x['geometry']
            message_dict["maps"] = map_list
            resp.body = "{}".format(message_dict)
            resp.status = falcon.HTTP_200
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
        print req.headers
        user_name = ""
        post_data = json.load(req.stream)
        print post_data
        if "user_name" in post_data:
            user_name = post_data["name"]
        if "geometry" in post_data:
            self.geojson_io_prox(resp, post_data["geometry"]["coordinates"],user_name)
            self.proximity(req,resp, post_data["geometry"]["coordinates"],user_name)
            i#self.geojson_io_prox(resp, post_data["geometry"]["coordinates"])
        elif post_data["address"]:
            if "address" in post_data:
                my_coordinates = self.geopy_coordinates(post_data["address"],resp)
                self.geojson_io_prox(resp,my_coordinates, user_name)
                self.proximity(req, resp, my_coordinates, user_name)
        else:
            falcon.HTTPMissingParam
            resp.body = """{ 'message' :
                'Please supply a address or coordinates (long,lat)'}"""



