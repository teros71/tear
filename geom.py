"""Basic geometrical elements"""
import math
import random


class Point:
    # Point at x,y
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def move(self, dx, dy):
        return Point(self.x + dx, self.y + dy)

    def randomize(self, maxR):
        nd = random.uniform(0.0, maxR)
        na = random.uniform(0, 2 * math.pi)
        self.x = self.x + nd * math.cos(na)
        self.y = self.y + nd * math.sin(na)

    def rotate(self, x, y, a):
        s = math.sin(a)
        c = math.cos(a)
        self.x -= x
        self.y -= y
        self.x = (self.x * c - self.y * s) + x
        self.y = (self.x * s + self.y * c) + y

    def output(self):
        print(self.x, self.y)


def halfWayPoint(p1, p2):
    return Point(p1.x + (p2.x - p1.x) / 2, p1.y + (p2.y - p1.y) / 2)


def distance(p1, p2):
    return math.sqrt(math.pow(p2.y - p1.y, 2) + math.pow(p2.x - p1.x, 2))


def angle(p1, p2):
    return math.atan2(p2.y - p1.y, p2.x - p1.x)


class BBox:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def join(self, bb):
        self.x0 = min(self.x0, bb.x0)
        self.y0 = min(self.y0, bb.y0)
        self.x1 = max(self.x1, bb.x1)
        self.y1 = max(self.y1, bb.y1)


class Rect:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    def scale(self, drx, dry):
        self.width = self.width * drx
        self.height = self.height * dry

    def get_points(self, x, y):
        topleft = Point(x - self.width / 2, y - self.width / 2)
        return [topleft, Point(topleft.x, topleft.y + self.height),
                Point(topleft.x + self.width, topleft.y + self.height),
                Point(topleft.x + self.width, topleft.y)]


class Circle:
    def __init__(self, r):
        self.r = r

    def scale(self, rx, ry):
        self.r = self.r * rx

    def copy(self):
        return Circle(self.r)

    def get_points(self, x, y):
        points = []
        t = 0.0
        while t < math.pi * 2:
            points.append(Point(x + self.r * math.cos(t),
                                y + self.r * math.sin(t)))
            t = t + math.pi / 8
        return points


class Polygon:
    """Polygon"""

    def __init__(self, points):
        self.points = points

    @classmethod
    def fromstr(cls, lst):
        points = []
        for ps in lst.split(','):
            pl = ps.strip().split(' ')
            if len(pl) == 2:
                points.append(Point(float(pl[0]), float(pl[1])))
        return cls(points)

    def get_points(self, x, y):
        return [p.move(x, y) for p in self.points]

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

    def rotate(self, x, y, a):
        for p in self.points:
            p.rotate(x, y, a)

    def bbox(self):
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
        return BBox(x1, y1, x2 - x1, y2 - y1)

    def contains(self, p):

        def on_segment(p, q, r):
            if q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) \
                and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y):
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
        def do_intersect(p1, q1, p2, q2):
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
                    return 1 << o4
                if o4 == 0:
                    return 1 << o3
                return 1

            # Special Cases
            # p1, q1 and p2 are colinear and p2 lies on segment p1q1
            # Although all of the cases below also intersect, we are
            # only interested if the actual point p2 lies on the segment.
            if o1 == 0 and on_segment(p1, p2, q1):
                return 1
            return 0  # Doesn't fall in any of the above cases

        # Create a point for line segment from p to infinite
#        p = shape.Point(x, y)
        extreme = Point(0, p.y)
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
            doi = do_intersect(self.points[i], self.points[next], p, extreme)
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
