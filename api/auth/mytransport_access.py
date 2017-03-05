import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import settings
import json, requests
def auth_mytransport():
        payload = {
                    'client_id': '781b4b4a-5921-4e90-ad34-ce4bfb9912c5',
                    'client_secret' : '0lXwudYL6HdSdsQwSxQcFAxbLjh56PEls9Jiq3NGaSE=',
                    'grant_type' : 'client_credentials',
                    'scope':'transportapi:all'
                }
        request = requests.post(settings.API_AUTH_URL, data=payload)
        creds = json.loads(request.text)
        print request.status_code
        return creds["access_token"]
