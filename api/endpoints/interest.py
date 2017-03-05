import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import json
import falcon
import uuid
import settings
import requests
from geopy.geocoders import Nominatim
class interest(object):
    interested = {}
    def proximity(self,req, resp, my_coordinates):
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
        post_data = json.load(req.stream)
        print post_data
        if "geometry" in post_data:
            self.proximity(req,resp, post_data["geometry"]["coordinates"])
        elif post_data["address"]:
            if "address" in post_data:
                my_coordinates = self.geopy_coordinates(post_data["address"],resp)
                self.proximity(req, resp, my_coordinates)
        else:
            falcon.HTTPMissingParam
            resp.body = """{ 'message' :
                'Please supply a address or coordinates (long,lat)'}"""



