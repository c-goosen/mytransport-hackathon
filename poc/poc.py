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

"""
E.G. coordinate
---------------
[
  18.852539062499996,
  -34.016241889667015
]
"""


def convert_journey_to_coords(journey):
    for itinery in journey['itineraries']:
        print itinery['id']
        line_coordinates = []
        for leg in itinery['legs']:
            line_coordinates.extend(leg['geometry']['coordinates'])
    return line_coordinates

print convert_journey_to_coords(journeys[0])
