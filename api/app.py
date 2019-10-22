import falcon
import elasticsearch
from endpoints.interest import interest
from endpoints.root import root
import settings
import requests
import json
app = falcon.API()

root = root()
interest = interest()
app.add_route('/interest', interest)
#root = root()
app.add_route('/', root)

##### GLobal VARS
ACCESS_TOKEN = ""
#CLIENT_ID = "781b4b4a-5921-4e90-ad34-ce4bfb9912c5"
#CLIENT_SECRET = "0lXwudYL6HdSdsQwSxQcFAxbLjh56PEls9Jiq3NGaSE="

if __name__ == "__main__":
    from wsgiref import simple_server
    from wsgiref.handlers import SimpleHandler
    from wsgiref.simple_server import (
                           WSGIServer,
                           WSGIRequestHandler,
                           ServerHandler
                       )
    httpd = simple_server.make_server(
        '127.0.0.1', 8081, app
        )
    print('[INFO] Server Ready')
    ACCESS_TOKEN = settings.ACCESS_TOKEN

    httpd.serve_forever()
