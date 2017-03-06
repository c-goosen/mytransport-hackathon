import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
# Dont love the above solution, but allows to import module on
# parent directory 
import settings
import json, requests
import os
# Better to remove hard coded API keys
# Deleted the keys on the platform anyway
# Add environment variables in your shell to access API
client_id = os.environ("MY_TRANSPORT_CLIENT_ID")
client_secret = os.environ("MY_TRANSPORT_CLIENT_SECRETi")
def auth_mytransport():
        payload = {
                    'client_id': client_id,
                    'client_secret' : client_secret,
                    'grant_type' : 'client_credentials',
                    'scope':'transportapi:all'
                }
        request = requests.post(settings.API_AUTH_URL, data=payload)
        creds = json.loads(request.text)
        print request.status_code
        return creds["access_token"]
