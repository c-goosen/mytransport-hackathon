import falcon

class root(object):
        def on_get(self, req, res):
            print("Entered the class")
            """Handles all GET requests."""
            res.status = falcon.HTTP_200  # This is the default status
            res.body = '{"message": "Ride demand API! Welcome. Try our /interest endpoint}'
