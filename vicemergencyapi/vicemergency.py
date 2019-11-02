import json

import requests
import shapely

from .helpers import Decoder


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
