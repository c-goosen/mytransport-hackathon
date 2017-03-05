import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from auth.mytransport_access import auth_mytransport
CLIENT_ID = "781b4b4a-5921-4e90-ad34-ce4bfb9912c5"
CLIENT_SECRET = "0lXwudYL6HdSdsQwSxQcFAxbLjh56PEls9Jiq3NGaSE="
API_URL = "https://platform.whereismytransport.com"
API_AUTH_URL = "https://identity.whereismytransport.com/connect/token"
ACCESS_TOKEN = auth_mytransport()
