import falcon
import elasticsearch
from endpoints.interest import interest
from endpoints.root import root
app = falcon.API()

root = root()
interest = interest()
app.add_route('/interest', interest)
#root = root()
app.add_route('/', root)

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
    httpd.serve_forever()
