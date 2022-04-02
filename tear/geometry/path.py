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
    OPEN_END = 0
    CLOSED_SHARP = 1
    CLOSED_PETAL = 2
    CLOSED_ROUND = 3

    @classmethod
    def str2mode(cls, s):
        if s == "closed-round":
            return Path.CLOSED_ROUND
        if s == "closed-sharp":
            return Path.CLOSED_SHARP
        if s == "closed-petal":
            return Path.CLOSED_PETAL
        else:
            return Path.OPEN_END

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
        seg = self.segments[i]
        t = t * total / seg.length
        return seg, t

    def bbox(self):
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


def random_path_quadratic(startpoint, endpoint, count, av, min_d,
                          mode=Path.OPEN_END):
    """Generate random path from curves
    Args:
        startpoint
        endpoint
        count : how many segments
        av : anglevariation for randomizing
        min_d : minimum distance between segment start and end points
        mode :
            OPEN_END = only start -> end
            CLOSED_SHARP = start -> end -> start, with an independent control
                point when starting end -> start segments, thus giving sharp
                points on both ends
            CLOSED_PETAL = same as CLOSED_SHARP except that control point
                follows the mirroring pattern all the way giving round path
                with sharp point at start
            CLOSED_ROUND = same as CLOSED_PETAL except that the last segment
                is fitted to make the control point mirroring perfectly circular
                giving fully rounded path with no sharp points
    """
    cl = []
    def make_segment(p0, end, p1, cp, max_df):
        if p1 is None:
            p1 = generate_point(p0, end, av, min_d, 0, max_df)
        if cp is None:
            cp = generate_point(p0, p1, av, min_d, 0, 1)
        return geom.QuadraticCurve(p0, cp, p1)

    def make_round(start, end, cp):
        p0 = start
#        cp = None
        for i in range(count - 1):
            seg = make_segment(p0, end, None, cp, (i+1) / count)
            cp = seg.p1.mirror(seg.cp)
            p0 = seg.p1
            cl.append(seg)
        # last to the end
        seg = make_segment(p0, end, end, cp, 1)
        cl.append(seg)

    make_round(startpoint, endpoint, None)
    if mode != Path.OPEN_END:
        if mode == Path.CLOSED_SHARP:
            # independent end -> start path
            make_round(endpoint, startpoint, None)
        elif mode == Path.CLOSED_PETAL:
            # end -> start with first control point mirrored from previous
            make_round(endpoint, startpoint, cl[-1].p1.mirror(cl[-1].cp))
        else:
            # end -> start with first control point mirrored from previous
            make_round(endpoint, startpoint, cl[-1].p1.mirror(cl[-1].cp))
            # adjust the last segment start point so that control points
            # are symmetrical
            ncp = cl[0].p0.mirror(cl[0].cp)
            cl[-1].p0 = geom.mid_point(ncp, cl[-1].p0.mirror(cl[-1].cp))
            cl[-2].p1 = cl[-1].p0
            cl[-1].cp = ncp

    return Path(cl)


def random_path_cubic(startpoint, endpoint, count, av, min_d,
                      mode=Path.OPEN_END):
    """Generate random path from curves
    Args:
        startpoint
        endpoint
        count : how many segments
        av : anglevariation for randomizing
        min_d : minimum distance between segment start and end points
    """
    cl = []
    def make_segment(p0, end, p1, c0, c1, max_df):
        if p1 is None:
            p1 = generate_point(p0, end, av, min_d, 0, max_df)
        if c0 is None:
            c0 = generate_point(p0, p1, av, min_d, 0, 1)
        if c1 is None:
            c1 = generate_point(p1, p0, av, min_d, 0, 1)
        return geom.CubicCurve(p0, c0, c1, p1)

    def make_round(start, end, c0, c1):
        p0 = start
        for i in range(count - 1):
            seg = make_segment(p0, end, None, c0, None, (i+1) / count)
            c0 = seg.p1.mirror(seg.c1)
            p0 = seg.p1
            cl.append(seg)
        # last to the end
        seg = make_segment(p0, end, end, c0, c1, 1)
        cl.append(seg)

    make_round(startpoint, endpoint, None, None)
    if mode != Path.OPEN_END:
        if mode == Path.CLOSED_SHARP:
            # independent end -> start path
            make_round(endpoint, startpoint, None, None)
        elif mode == Path.CLOSED_PETAL:
            # end -> start with first control point mirrored from previous
            make_round(endpoint, startpoint, cl[-1].p1.mirror(cl[-1].c1), None)
        else:
            # end -> start with first control point mirrored from previous,
            # last control point mirrored from first
            make_round(endpoint, startpoint,
                       cl[-1].p1.mirror(cl[-1].c1), cl[0].p0.mirror(cl[0].c0))

    return Path(cl)


def path_around(points, av):
    cl = []
    p0 = points[-1]
    c0 = None
    last_c1 = None
    for p1 in points:
        if c0 is None:
            c0 = generate_point(p0, p1, av, 2, 0, 1)
        c1 = generate_point(p1, p0, av, 2, 0, 1)
        seg = geom.CubicCurve(p0, c0, c1, p1)
        c0 = p1.mirror(c1)
        p0 = p1
        cl.append(seg)
    cl[0].c0 = cl[-1].p1.mirror(cl[-1].c1)
    return Path(cl)
