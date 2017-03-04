import json
import requests
API_URL = "https://platform.whereismytransport.com"
destination = ("-33.947272","18.4783663")


def get_session_token():
    payload = {'client_id': '781b4b4a-5921-4e90-ad34-ce4bfb9912c5', 'client_secret': '0lXwudYL6HdSdsQwSxQcFAxbLjh56PEls9Jiq3NGaSE='}

def get_my_geo():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat, lon

def post_my_journey():
    post_data = {
       "geometry": {
                   "type": "Multipoint",
                   "coordinates": [
                                   [],
                                   []
                               ]
               }
         ,"time": "2016-08-30T10:30:00Z",
            "omit": {
                        "modes": []
                    },
            "maxItineraries": 5
    }
    lat, lon = get_my_geo()
    post_data["geometry"]["coordinates"][0].append(lat)
    post_data["geometry"]["coordinates"][0].append(lon)
    post_data["geometry"]["coordinates"][1].append(destination[0])
    post_data["geometry"]["coordinates"][1].append(destination[1])
    print post_data
    req = requests.post(API_URL, json=post_data)
    print req.status_code
if __name__ == "__main__":
    post_my_journey()
    #req = requests.post(url=API_URL,json=post_data)
