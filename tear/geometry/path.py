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
        return self.segments[0].startpoint

    @property
    def endpoint(self):
        """End of the path"""
        return self.segments[-1].endpoint

    def point_at(self, t):
        """Point on the path
        Args:
            t : distance from start towards end in range [0,1]
        """
        s, t = self.find_segment(t)
        return s.point_at(t)

    def tangent_at(self, t):
        s, t = self.find_segment(t)
        return s.tangent_at(t)

    def find_segment(self, t):
        if len(self.segments) == 1:
            return self.segments[0], t
        total = 0
        for s in self.segments:
            total += s.length
        i = 0
        while t > self.segments[i].length / total:
            t -= self.segments[i].length / total
            i += 1
        print("point at", t, i)
        seg = self.segments[i]
        t = t * total / seg.length
        print("final t", t)
        return seg, t

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


def random_path_quadratic(startpoint, endpoint, count, av, min_d):
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
    cp = None
    for i in range(count - 1):
        p = generate_point(p0, endpoint, av, min_d, 0, (i+1) / count)
        if p is not None:
            if cp is None:
                # new control point
                cp = generate_point(p0, p, av, min_d, 0, 1)
            if cp is not None:
                cl.append(geom.QuadraticCurve(p0, cp, p))
                # next cp is mirror of previous
                cp = p.mirror(cp)
            p0 = p
    # last to the end
    if p0 is not None:
        if cp is None:
            cp = generate_point(p0, endpoint, av, min_d, 0, 1)
        if cp is not None:
            cl.append(geom.QuadraticCurve(p0, cp, endpoint))
    return Path(cl)


def random_path_cubic(startpoint, endpoint, count, av, min_d):
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
    c0 = None
    c1 = None
    for i in range(count - 1):
        p1 = generate_point(p0, endpoint, av, min_d, 0, (i+1) / count)
        if p1 is not None:
            if c0 is None:
                # new control point
                c0 = generate_point(p0, p1, av, min_d, 0, 1)
            c1 = generate_point(p1, p0, av, min_d, 0, 1)
            if c0 is not None and c1 is not None:
                cl.append(geom.CubicCurve(p0, c0, c1, p1))
                # next cp is mirror of previous
                c0 = p1.mirror(c1)
            p0 = p1
    # last to the end
    if p0 is not None:
        if c0 is None:
            # new control point
            c0 = generate_point(p0, endpoint, av, min_d, 0, 1)
        c1 = generate_point(endpoint, p0, av, min_d, 0, 1)
        if c0 is not None and c1 is not None:
            cl.append(geom.CubicCurve(p0, c0, c1, endpoint))
    return Path(cl)
