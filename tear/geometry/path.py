"""Path handling"""

import math
import random
from tear.geometry import geom


def generate_point(p1, p2, av, min_d, min_df, max_df):
    """Generate point between p1 and p2
    Args:
        av : angle variation for direction from p1
        min_d : minimum distance
        min_df : minimum distance factor (how far at least)
        max_df : maximum distance factor (how far at most)
    """
    d = geom.distance(p1, p2)
    a = geom.angle(p1, p2)
    if d < min_d:
        # not enough distance
        return None
    # calculate distance
    mind = max(d * min_df, min_d)
    maxd = max(d * max_df, min_d)
    nd = random.uniform(mind, maxd)
    # calculate angle
    na = random.uniform(a - av, a + av)
    x = p1.x + nd * math.cos(na)
    y = p1.y + nd * math.sin(na)
    return geom.Point(x, y)


class Path:
    """Path
    Only curve object is supported, plus it is assumed to have absolute
    coordinates, not relative to 0,0.
    """

    def __init__(self, s):
        self.segments = s

    @property
    def startpoint(self):
        """Start of the path"""
        return self.segments[0].p0

    @property
    def endpoint(self):
        """End of the path"""
        return self.segments[-1].p1

    def point_at(self, d):
        """Point on the path
        Args:
            d : distance from start towards end [0,1]
        """
        n = math.ceil(d * len(self.segments)) - 1
        d = (d - n / len(self.segments)) * len(self.segments)
        print("point at", d, n)
        return self.segments[n].point_at(d)

    def bbox(self, p):
        """Bounding box"""
        return geom.BBox(self.startpoint.x, self.startpoint.y,
                         self.endpoint.x, self.endpoint.y)

    def get_points(self, origo, count=25):
        """Get points that approximate the curve"""
        ps = [self.startpoint]
        ds = (1 / count * i for i in range(1, count + 1))
#        for seg in self.segments:
        for d in ds:
            ps.append(self.point_at(d))
        return ps

    def __repr__(self):
        return f'Path[{self.segments}]'


def random_path(startpoint, endpoint, count, av, min_d):
    """Generate random path from curves
    Args:
        startpoint
        endpoint
        count : how many segments
        av : anglevariation for randomizing
        min_d : minimum distance between segment start and end points
    """
    cl = []
    p0 = startpoint
    for i in range(count - 1):
        p = generate_point(p0, endpoint, av, min_d, 0, (i+1) / count)
        if p is not None:
            cp = generate_point(p0, p, av, min_d, 0, 1)
            if cp is not None:
                cl.append(geom.Curve(p0, p, cp))
        p0 = p
    # last to the end
    if p0 is not None:
        cp = generate_point(p0, endpoint, av, min_d, 0, 1)
        if cp is not None:
            cl.append(geom.Curve(p0, endpoint, cp))
    return Path(cl)
