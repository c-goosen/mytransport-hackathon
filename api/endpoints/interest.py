import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import json
import falcon
import uuid
import settings
import requests
class interest(object):
    interested = {}
    def proximity(self,req):
       # print settings.API_URL
        query_params = {"point":"-33.947272,18.4783663","radius":"1000"
                      }
        endpoint ="api/stops"
        headers = {"Authorization": "Bearer {}".format(settings.ACCESS_TOKEN)}
        request = requests.get("{}/{}".format(settings.API_URL,endpoint), 
                               params=query_params, 
                               headers=headers)
        print request.status_code
        print request.text
        print json.load(request.text)

    def on_get(self, req, resp):
        resp.body = '{"message":"Post request needed with GeoLocation data"}'
        resp.status = falcon.HTTP_200
    def on_post(self, req, resp):
        print req.headers
        post_data = json.load(req.stream)
        print post_data
        if not post_data["geometry"]:
            falcon.HTTPMissingParam
        else:
            self.proximity(req)
        pass


