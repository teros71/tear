import math
import random
import json
import copy
import shape


class Polygon:
    def __init__(self, points):
        self.points = points

    @classmethod
    def fromstr(cls, lst):
        points = []
        for ps in lst.split(','):
            pl = ps.strip().split(' ')
            if len(pl) == 2:
                points.append(shape.Point(float(pl[0]), float(pl[1])))
        return cls(points)

    def toPolygon(self):
        return self.points

    def move(self, dx, dy):
        for p in self.points:
            p.x = p.x + dx
            p.y = p.y + dy

    def scale(self, rx, ry=0):
        if ry == 0:
            ry = rx
        for p in self.points:
            p.x = p.x * rx
            p.y = p.y * ry

    def setPosition(self, x, y):
        bb = self.bBox()
        dx = x - (bb.width / 2)
        dy = y - (bb.height / 2)
        if dx != 0 or dy != 0:
            self.move(dx, dy)

    def rotate(self, x, y, a):
        for p in self.points:
            p.rotate(x, y, a)

    def bBox(self):
        p = self.points[0]
        x1 = p.x
        y1 = p.y
        x2 = p.x
        y2 = p.y
        for p in self.points:
            if p.x < x1:
                x1 = p.x
            if p.x > x2:
                x2 = p.x
            if p.y < y1:
                y1 = p.y
            if p.y > y2:
                y2 = p.y
        return shape.Rect(x1, y1, x2 - x1, y2 - y1)

    def contains(self, p):

        def onSegment(p, q, r):
            if q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y):
                return True
            return False

        # To find orientation of ordered triplet (p, q, r).
        # The function returns following values
        # 0 --> p, q and r are colinear
        # 1 --> Clockwise
        # 2 --> Counterclockwise
        def orientation(p, q, r):
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if val == 0:
                return 0  # colinear
            if val > 0:
                return 1  # clock wise
            return 2  # counterclock wise

        # Returns for line segments 'p1q1' and 'p2q2':
        # 0 = don't intersect
        # 1 = intersects
        # 2 = at endpoint with orientation 1
        # 4 = at endpoint with orientation 2
        def doIntersect(p1, q1, p2, q2):
            # Find the four orientations needed for general and
            # special cases
            o1 = orientation(p1, q1, p2)
            o2 = orientation(p1, q1, q2)
            o3 = orientation(p2, q2, p1)
            o4 = orientation(p2, q2, q1)
            # General case
            # Note that if o3 or o4 are colinear, our point is at corner
            # => count corner only once (o3 => true, o4 => false)
            if o1 != o2 and o3 != o4:
                if o3 == 0:
                    return (1 << o4)
                if o4 == 0:
                    return (1 << o3)
                return 1

            # Special Cases
            # p1, q1 and p2 are colinear and p2 lies on segment p1q1
            # Although all of the cases below also intersect, we are
            # only interested if the actual point p2 lies on the segment.
            if o1 == 0 and onSegment(p1, p2, q1):
                return 1
            return 0  # Doesn't fall in any of the above cases

        # Create a point for line segment from p to infinite
#        p = shape.Point(x, y)
        extreme = shape.Point(0, p.y)
        # Count intersections of the above line with sides of polygon
        count = 0
        i = 0
        next = 1
        po = 0
        n = len(self.points)
        while i < n:
            next = (i + 1) % n
            # Check if the line segment from 'p' to 'extreme' intersects
            # with the line segment from 'polygon[i]' to 'polygon[next]'
            doi = doIntersect(self.points[i], self.points[next], p, extreme)
            if doi > 0:
                count += 1
                if po == 0:
                    po = doi & 6
                elif doi > 1:
                    if (doi & po) == 0:
                        count += 1
                    po = 0
            i += 1
        # Return true if count is odd, false otherwise
        if count % 2 == 1:
            return True
        return False


class Generator():
    """Generator for shapes"""

    def __init__(self, range_r, range_points):
        self.rangeR = range_r
        self.rangePoints = range_points

    def __iter__(self):
        return self

    def __next__(self):
        count = self.rangePoints.__next__()
        return random_polygon(self.rangeR.min, self.rangeR.max, count)


def random_polygon(minR, maxR, count):
    slicea = (2 * math.pi) / count
    points = []
    for i in range(0, count):
        s = i * slicea
        a = random.uniform(s, s + slicea)
        d = random.uniform(minR, maxR)
        points.append(shape.Point(d * math.cos(a), d * math.sin(a)))
    return Polygon(points)
