"""Basic geometrical elements"""
import math
import random


class Point:
    """point at x,y"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        """return copy of this point"""
        return Point(self.x, self.y)

    def move(self, dx, dy):
        """return a new point moved by dx,dy"""
        return Point(self.x + dx, self.y + dy)

    def randomize(self, maxR):
        """randomize within distance maxR"""
        nd = random.uniform(0.0, maxR)
        na = random.uniform(0, 2 * math.pi)
        self.x = self.x + nd * math.cos(na)
        self.y = self.y + nd * math.sin(na)

    def rotate(self, x, y, a):
        """rotate angle a by around x,y"""
        s = math.sin(a)
        c = math.cos(a)
        nx = self.x - x
        ny = self.y - y
        self.x = (nx * c - ny * s) + x
        self.y = (nx * s + ny * c) + y

    # Vector functions
    def substract(self, v):
        """substract another point"""
        return Point(self.x - v.x, self.y - v.y)

    def add(self, v):
        """add another point"""
        return Vector(self.x + v.x, self.y + v.y)

    def multiply(self, v):
        """multiply with another point"""
        return self.x * v.x + self.y * v.y

    def scale(self, f):
        """move by factor f"""
        return Vector(self.x * f, self.y * f)

    def cross(self, v):
        """cross product"""
        return self.x * v.y - self.y * v.x

    def is_equal(self, v):
        """has same coordinates"""
        return is_zero(self.x - v.x) and is_zero(self.y - v.y)

    def print(self):
        """print data"""
        print(self.x, self.y)


def mid_point(p1, p2):
    return Point(p1.x + (p2.x - p1.x) / 2, p1.y + (p2.y - p1.y) / 2)


def distance(p1, p2):
    """distance between the given points"""
    return math.sqrt(math.pow(p2.y - p1.y, 2) + math.pow(p2.x - p1.x, 2))


def angle(p1, p2):
    """angle of vector between points"""
    return math.atan2(p2.y - p1.y, p2.x - p1.x)


def is_zero(d):
    """is close enough to zero"""
    return math.fabs(d) < 1e-10


class BBox:
    """Bounding box, x0,y0 - x1,y1"""

    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def join(self, bb):
        """grow by given box"""
        self.x0 = min(self.x0, bb.x0)
        self.y0 = min(self.y0, bb.y0)
        self.x1 = max(self.x1, bb.x1)
        self.y1 = max(self.y1, bb.y1)

    def print(self):
        """print data"""
        print(f'bbox;[{self.x0},{self.y0}]-[{self.x1},{self.y1}]')


class Rect:
    """Rectangle, width, height"""

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def scale(self, fx, fy):
        """scale by factors fx, fy"""
        self.width = self.width * fx
        self.height = self.height * fy

    def is_inside(self, p):
        """is point inside this rectangle"""
        return (p.x >= -(self.width / 2) and p.x <= self.width / 2
                and p.y >= -(self.height / 2) and p.y <= self.height / 2)

    def bbox(self, origo):
        """bounding box of rectangle for given origo"""
        tlx = origo.x - self.width / 2
        tly = origo.y - self.height / 2
        return BBox(tlx, tly, tlx + self.width, tly + self.height)

    def get_points(self, origo):
        """get list of points that make up this rectangle, with given origo"""
        topleft = Point(origo.x - self.width / 2, origo.y - self.height / 2)
        return [topleft, Point(topleft.x, topleft.y + self.height),
                Point(topleft.x + self.width, topleft.y + self.height),
                Point(topleft.x + self.width, topleft.y)]

    def length(self):
        """total length of the edge of this rectangle"""
        return self.width * 2 + self.height * 2

    def point_at(self, origo, dist):
        """get point on the edge at given distance along the edge"""
        p = self.get_points(origo)
        dist = dist % self.length()
        if dist < self.height:
            return Point(p[0].x, p[0].y + dist)
        dist -= self.height
        if dist < self.width:
            return Point(p[1].x + dist, p[1].y)
        dist -= self.width
        if dist < self.height:
            return Point(p[2].x, p[2].y - dist)
        dist -= self.height
        return Point(p[3].x - dist, p[3].y)


class Circle:
    """circle, defined by r"""

    def __init__(self, r):
        self.r = r

    def scale(self, fx, fy):
        """scale by fx, ignore fy"""
        self.r = self.r * fx

    def copy(self):
        """return copy of myself"""
        return Circle(self.r)

    def is_inside(self, p):
        """is given point inside of the circle"""
        return math.sqrt(p.x ** 2 + p.y ** 2) <= self.r

    def bbox(self, origo):
        """bounding box with given origo"""
        return BBox(origo.x - self.r,
                    origo.y - self.r,
                    origo.x + self.r,
                    origo.y + self.r)

    def get_points(self, origo):
        """return list of points approximating the circle"""
        points = []
        t = 0.0
        while t < math.pi * 2:
            points.append(Point(origo.x + self.r * math.cos(t),
                                origo.y + self.r * math.sin(t)))
            t = t + math.pi / 8
        return points

    def length(self):
        """length of the circle edge"""
        return 2 * math.pi * self.r

    def point_at(self, origo, dist):
        """return point at the edge at given distance"""
        dist %= self.length()
        t = (2 * math.pi) * (dist / self.length())
        return Point(origo.x + self.r * math.cos(t), origo.y + self.r * math.sin(t))


class Polygon:
    """Polygon"""

    def __init__(self, points):
        self.points = points

    @classmethod
    def fromstr(cls, lst):
        """read polygon points from string"""
        points = []
        for ps in lst.split(','):
            pl = ps.strip().split(' ')
            if len(pl) == 2:
                points.append(Point(float(pl[0]), float(pl[1])))
        return cls(points)

    @classmethod
    def fromrect(cls, r):
        """make polygon from rect object"""
        return cls(r.get_points(Point(0, 0)))

    def get_points(self, origo):
        """get list of points with given origo"""
        return [p.move(origo.x, origo.y) for p in self.points]

    def move(self, dx, dy):
        """move polygon points by dx, dy"""
        for p in self.points:
            p.x = p.x + dx
            p.y = p.y + dy

    def scale(self, fx, fy=0):
        """scale by fx, fy"""
        if fy == 0:
            fy = fx
        for p in self.points:
            p.x = p.x * fx
            p.y = p.y * fy

    def rotate(self, x, y, a):
        """rotate around x, y by given angle a"""
        for p in self.points:
            p.rotate(x, y, a)

    def mirror(self):
        """mirror by center of polygon"""
        bb = self.bbox(Point(0, 0))
        x = bb.x0 + ((bb.x1 - bb.x0) / 2)
        for p in self.points:
            p.x = x + (x - p.x)

    def bbox(self, origo):
        """bounding box with given origo"""
        p = self.points[0]
        x0 = p.x
        y0 = p.y
        x1 = p.x
        y1 = p.y
        for p in self.points:
            if p.x < x0:
                x0 = p.x
            if p.x > x1:
                x1 = p.x
            if p.y < y0:
                y0 = p.y
            if p.y > y1:
                y1 = p.y
        return BBox(x0 + origo.x, y0 + origo.y, x1 + origo.x, y1 + origo.y)

    def is_inside(self, p):
        """is point inside of the polygon"""

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
        extreme = Point(-10**7, p.y)
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

    def intersection(self, p1, p2):
        """return intersecting point for the give line segment"""
        q1 = self.points[len(self.points) - 1]
        for q2 in self.points:
            inters = intersect(p1, p2, q1, q2)
            if inters is not None:
                return inters
        return None

    def shrink_to_inside(self, poly):
        """shrink this polygon to be completely inside the given one"""
        # first find a starting point that is inside
        i = 0
        while i < len(self.points) and not poly.is_inside(self.points[i]):
            i += 1
        if i >= len(self.points):
            return False
        inters = None
        j = i
        p1 = self.points[j]
        j = (j + 1) % len(self.points)
        while j != i:
            p2 = self.points[j]
            inters = poly.intersection(p1, p2)
            if inters is not None:
                self.points[j] = inters
                p1 = inters
            else:
                p1 = p2
            j = (j + 1) % len(self.points)
        return True

    def length(self):
        """total length of the polygon edges"""
        i = 0
        n = len(self.points)
        d = 0.0
        while i < n:
            j = (i + 1) % n
            d += distance(self.points[i], self.points[j])
            i += 1
        return d

    def point_at(self, origo, dist):
        """point on the edge on given distance"""
        dist %= self.length()
        p = self.get_points(origo)
        i = 0
        n = len(p)
        j = 1
        p0 = p[0]
        p1 = p[1]
        d = distance(p0, p1)
        while dist > d:
            print(dist, p0.x, p0.y, p1.x, p1.y, d)
            dist -= d
            i += 1
            j = (i + 1) % n
            p0 = p[i]
            p1 = p[j]
            d = distance(p0, p1)
        print(dist, p0.x, p0.y, p1.x, p1.y, d)
        return Point(p0.x + (p1.x - p0.x) * (dist / d), p0.y + (p1.y - p0.y) * (dist / d))


def intersect(p1, p2, q1, q2):
    """Test whether two line segments intersect. If so, calculate the
    intersection point.
    <see cref="http://stackoverflow.com/a/14143738/292237"/>
    <param name="p1">Vector to the start point of p.</param>
    <param name="p2">Vector to the end point of p.</param>
    <param name="q1">Vector to the start point of q.</param>
    <param name="q2">Vector to the end point of q.</param>
    Returns the point of intersection, if any.
    considerOverlapAsIntersect: Do we consider overlapping lines as
    intersecting?
    """
    r = p2.substract(p1)
    s = q2.substract(q1)
    rxs = r.cross(s)
    qmp = q1.substract(p1)
    qpxr = qmp.cross(r)

    # If r x s = 0 and (q - p) x r = 0, then the two lines are collinear.
    if is_zero(rxs):
        # if is_zero(qpxr):
        # 1. If either  0 <= (q - p) * r <= r * r or 0 <= (p - q) * s <= * s
        # then the two lines are overlapping,
        #        if (considerOverlapAsIntersect)
        #            if ((0 <= (q - p) * r && (q - p) * r <= r * r) ||
        #            (0 <= (p - q) * s & & (p - q) * s <= s * s))
        #                return true;
        # 2. If neither 0 <= (q - p) * r ≤ r * r nor 0 <= (p - q) * s <= s * s
        # then the two lines are collinear but disjoint.
        # No need to implement this expression, as it follows from the
        # expression above.
        return None

    # 3. If r x s = 0 and (q - p) x r != 0, then the two lines are parallel and
    # non-intersecting.
#    if is_zero(rxs) and !is_zero(qpxr)
#        return None

    # t = (q - p) x s / (r x s)
    t = qmp.cross(s) / rxs

    # u = (q - p) x r / (r x s)
    u = qpxr / rxs

    # 4. If r x s != 0 and 0 <= t <= 1 and 0 <= u <= 1
    # the two line segments meet at the point p + t r = q + u s.
    if (not is_zero(rxs)) and 0 <= t and t <= 1 and 0 <= u and u <= 1:
        # We can calculate the intersection point using either t or u.
        intersection = p1.add(r.scale(t))

        # An intersection was found.
        return intersection

    # 5. Otherwise, the two line segments are not parallel but do not intersect.
    return None
