import falcon
import uuid

class interest(object):

    def on_get(self, req, resp):
        resp.body = '{"message":"Post request needed with GeoLocation data"}'
        resp.status = falcon.HTTP_200
    def on_post(self, req, resp):
        pass
