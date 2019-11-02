import requests
import json
import shapely
from shapely.geometry import Point
from geographiclib.geodesic import Geodesic

# sudo apt-get install libgeos-c1v5
# sudo pip3 install shapely
# sudo pip3 install geographiclib


def geoDistance(p1, p2):
    return Geodesic.WGS84.Inverse(p1.y, p1.x, p2.y, p2.x)['s12']

# Why?
# Some floats in the JSON are encoded as strings!
class Decoder(json.JSONDecoder):

    def decode(self, s):
        result = super().decode(s)
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str):

            # Check if o contains a decimal point and tryparse as float
            if '.' in o:
                try:
                    return float(o)
                except:
                    return o

            try:
                return int(o)
            except:
                pass

            return o

        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o

class VicEmergency():

    ENDPOINT = "https://emergency.vic.gov.au/public/osom-geojson.json"
    ENCODING = "utf-8"
    HEADERS = { 'accept-encoding': 'gzip' }

    class Item():

        def __init__(self, geom, props, shape):
            self.properties = props
            self.geometry = geom
            self.shape = shape

        def getLocation(self):

            if self.shape.geom_type == 'Polygon' or self.shape.geom_type == 'MultiPolygon':
                return self.shape.centroid

            return self.shape

    @classmethod
    def getItems(self):

        response = requests.get(self.ENDPOINT, headers=self.HEADERS)
        response.encoding = self.ENCODING
        obj = json.loads(response.text, cls=Decoder)

        items = []

        for f in obj["features"]:

            p = f["properties"]
            g = f["geometry"]

            # Take the first one as the location
            if g["type"] == 'GeometryCollection':
                s = shapely.geometry.asShape(g["geometries"][0])
            else:
                s = shapely.geometry.asShape(g) 

            newItem = self.Item(g, p, s)

            items.append(newItem)

        return items


melbourne = Point(144.962272, -37.812274)
items = VicEmergency.getItems()

def compare(f):
    return geoDistance(f.getLocation(), melbourne)

closest = sorted(items, key=compare)

for i in closest:

    print(i.properties["sourceTitle"])
    print(i.properties["category1"])
    print(i.properties["location"])
    print("{:.0f}km".format(geoDistance(i.getLocation(), melbourne) / 1000))

    print("============================")