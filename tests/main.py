from context import vicemergencyapi
from vicemergencyapi.vicemergency import VicEmergency

from geographiclib.geodesic import Geodesic
from shapely.geometry import Point


def geoDistance(p1, p2):
    return Geodesic.WGS84.Inverse(p1.y, p1.x, p2.y, p2.x)['s12']


melbourne = Point(144.962272, -37.812274)

def compare(f):
    return geoDistance(f.getLocation(), melbourne)

for i in sorted(VicEmergency.getItems(), key=compare):

    print(i.properties["sourceTitle"])
    print(i.properties["category1"])
    print(i.properties["location"])
    print("{:.0f}km".format(geoDistance(i.getLocation(), melbourne) / 1000))

    print("============================")
