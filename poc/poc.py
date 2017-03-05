import copy
import json
import os
from subprocess import check_output, CalledProcessError


def git_root_dir():
    ''' returns the absolute path of the repository root '''
    try:
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        base = check_output(['git', 'rev-parse', '--show-toplevel'])
    except CalledProcessError:
        raise IOError('Current working directory is not a git repository')
    return base.decode('utf-8').strip()

base_dir = git_root_dir()

json_journey_paths = [
    '{}/poc/journey_BellvilleToAtlantis.json'.format(base_dir),
    '{}/poc/journey_BellvilleToBelhar.json'.format(base_dir),
    '{}/poc/journey_BellvilleToBlackheath.json'.format(base_dir)
]


def list_of_journey_data(json_journey_paths):
    journeys = []
    for json_path in json_journey_paths:
        with open(json_path) as json_data:
            journeys.append(json.load(json_data))
    return journeys

# print type(list_of_journey_data(json_journey_paths))
journeys = list_of_journey_data(json_journey_paths)

"""
E.G. feature collection
-----------------------
{
  "type": "FeatureCollection",
  "features": [>>>***<<<]
}
"""

"""
E.G. feature
------------
{
  "type": "Feature",
  "properties": {},
  "geometry": {
    "type": "LineString",
    "coordinates": [>>>***<<<]
  }
}
"""


def get_journey_coords(journey):
    for itinery in journey['itineraries']:
        line_coordinates = []
        for leg in itinery['legs']:
            try:
                leg_line_mode = leg['line']['mode']
            except:
                pass
            else:
                if leg_line_mode == 'ShareTaxi':
                    line_coordinates.extend(leg['geometry']['coordinates'])

    return line_coordinates

feature_collection = {
  "type": "FeatureCollection",
  "features": []
}

feature = {
  "type": "Feature",
  "properties": {},
  "geometry": {
    "type": "LineString",
    "coordinates": []
  }
}


def get_geojsosn_feature_collection(journeys, feature_collection, feature):
    for journey in journeys:
        journey_coords = get_journey_coords(journey)
        feature_deepcopy = copy.deepcopy(feature)
        feature_deepcopy['geometry']['coordinates'].extend(journey_coords)
        if journey_coords:
            feature_collection['features'].append(feature_deepcopy)
    return feature_collection

geo_json_data = get_geojsosn_feature_collection(journeys, feature_collection, feature)

with open('{}/poc/geo_json_dump.json'.format(base_dir), 'w') as outfile:
    json.dump(geo_json_data, outfile)
