"""Basic geometrical elements"""
import math
import random


class Point:
    """point at x,y"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def fromtuple(cls, t):
        """Make point from a pair x y"""
        return cls(t[0], t[1])

    def copy(self):
        """Return a copy of this point"""
        return Point(self.x, self.y)

    def move(self, dx, dy):
        """move myself by dx,dy"""
        self.x += dx
        self.y += dy

    def distxy(self, p):
        """distance to p of x and y"""
        return p.x - self.x, p.y - self.y

    def randomize(self, r):
        """randomize within distance r"""
        nd = random.uniform(0.0, r)
        na = random.uniform(0, 2 * math.pi)
        self.x += nd * math.cos(na)
        self.y += nd * math.sin(na)

    def rotate(self, x, y, a):
        """rotate by angle a around x,y"""
        s = math.sin(a)
        c = math.cos(a)
        nx = self.x - x
        ny = self.y - y
        self.x = (nx * c - ny * s) + x
        self.y = (nx * s + ny * c) + y

    def mirror(self, p):
        """Mirror point of p in regard of this point"""
        return Point(self.x + (self.x - p.x), self.y + (self.y - p.y))

    # Vector functions
    def substract(self, v):
        """substract another point"""
        return Point(self.x - v.x, self.y - v.y)

    def add(self, v):
        """add another point"""
        return Point(self.x + v.x, self.y + v.y)

    def multiply(self, v):
        """multiply with another point"""
        return self.x * v.x + self.y * v.y

    def scale(self, f):
        """scale (move) by factor f"""
        return Point(self.x * f, self.y * f)

    def cross(self, v):
        """cross product"""
        return self.x * v.y - self.y * v.x

    def is_equal(self, v):
        """has same coordinates"""
        return is_zero(self.x - v.x) and is_zero(self.y - v.y)

    def __repr__(self):
        """print data"""
        return f'Point[{self.x}, {self.y}]'


def polar2cartesian(t, r, ox=0, oy=0):
    """Convert polar coordinates to cartesian
    Args:
        t : angle
        r : distance
        ox, oy : origo of polar coordinates
    Returns:
        x, y : cartesian coordinates
    """
    return ox + r * math.cos(t), oy + r * math.sin(t)


def mid_point(p1, p2):
    """Point midway between p1 and p2"""
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

    def __repr__(self):
        """print data"""
        return f'BBox[{self.x0},{self.y0}]-[{self.x1},{self.y1}]'


class Rect:
    """Rectangle, width, height and position (Point)
    The position is the center of the rectangle"""

    def __init__(self, w, h, pos=Point(0.0, 0.0)):
        self.width = w
        self.height = h
        self.p = pos

    @property
    def position(self):
        return self.p

    @position.setter
    def position(self, p):
        self.p = p

    def scale(self, fx, fy):
        """scale by factors fx, fy"""
        self.width = self.width * fx
        self.height = self.height * fy

    def is_inside(self, p):
        """is point inside this rectangle"""
        dx, dy = self.p.distxy(p)
        return (dx >= -(self.width / 2)
                and dx <= self.width / 2
                and dy >= -(self.height / 2)
                and dy <= self.height / 2)

    def bbox(self):
        """bounding box"""
        tlx = self.p.x - self.width / 2
        tly = self.p.y - self.height / 2
        return BBox(tlx, tly, tlx + self.width, tly + self.height)

    def get_points(self):
        """get list of points that make up this rectangle"""
        topleft = Point(self.p.x - self.width / 2,
                        self.p.y - self.height / 2)
        return [topleft, Point(topleft.x, topleft.y + self.height),
                Point(topleft.x + self.width, topleft.y + self.height),
                Point(topleft.x + self.width, topleft.y)]

    def length(self):
        """total length of the edge of this rectangle"""
        return self.width * 2 + self.height * 2

    def point_at(self, dist):
        """get point on the edge at given distance along the edge"""
        p = self.get_points()
        dist = self.length() * dist
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

    def __repr__(self):
        return f'Rect[{self.width},{self.height},{self.p}]'


class Circle:
    """circle, defined by r and position"""

    def __init__(self, r, pos=Point(0.0, 0.0)):
        self.r = r
        self.p = pos

    @property
    def radius(self):
        return self.r

    @property
    def position(self):
        return self.p

    @position.setter
    def position(self, p):
        self.p = p

    def scale(self, factor):
        """scale by factor"""
        self.r = self.r * factor

    def copy(self):
        """return copy of myself"""
        return Circle(self.r, self.p)

    def is_inside(self, p):
        """is given point inside of the circle"""
        dx, dy = self.p.distxy(p)
        return math.sqrt(dx ** 2 + dy ** 2) <= self.r

    def bbox(self):
        """bounding box"""
        return BBox(self.p.x - self.r,
                    self.p.y - self.r,
                    self.p.x + self.r,
                    self.p.y + self.r)

    def get_points(self):
        """return list of points approximating the circle"""
        points = []
        t = 0.0
        while t < math.pi * 2:
            points.append(Point(self.p.x + self.r * math.cos(t),
                                self.p.y + self.r * math.sin(t)))
            t = t + math.pi / 8
        return points

    def length(self):
        """length of the circle edge"""
        return 2 * math.pi * self.r

    def point_at(self, dist):
        """return point at the edge at given distance"""
        t = 2 * math.pi * dist
        return Point(self.p.x + self.r * math.cos(t),
                     self.p.y + self.r * math.sin(t))

    def tangent_at(self, dist):
        """Tangent angle at given distance"""
        t = 2 * math.pi * dist
        return math.atan2(math.cos(t), -math.sin(t))

    def __repr__(self):
        return f'Circle[{self.r}, {self.p}]'


class Ellipse:
    """Ellipse"""

    def __init__(self, rx, ry, pos=Point(0.0, 0.0)):
        self.rx = rx
        self.ry = ry
        self.p = pos

    @property
    def position(self):
        return self.p

    @position.setter
    def position(self, p):
        self.p = p

    def scale(self, fx, fy):
        """scale by factor"""
        self.rx = self.rx * fx
        self.ry = self.ry * fy

    def copy(self):
        """return copy of myself"""
        return Ellipse(self.rx, self.ry, self.p)

    def is_inside(self, p):
        """is given point inside"""
        dx, dy = self.p.distxy(p)
        return dx ** 2 / self.rx ** 2 + dy ** 2 / self.ry ** 2 <= 1

    def bbox(self):
        """bounding box"""
        return BBox(self.p.x - self.rx,
                    self.p.y - self.ry,
                    self.p.x + self.rx,
                    self.p.y + self.ry)

    def get_points(self):
        """return list of points approximating the ellipse"""
        points = []
        t = 0.0
        while t < math.pi * 2:
            points.append(Point(self.p.x + self.rx * math.cos(t),
                                self.p.y + self.ry * math.sin(t)))
            t = t + math.pi / 8
        return points

    def length(self):
        """length of the edge"""
        amb2 = (self.rx - self.ry) ** 2
        apb2 = (self.rx + self.ry) ** 2
        return math.pi * (self.rx + self.ry) * \
            (3 * ((amb2)
                  / (apb2 * (math.sqrt(-3 * ((amb2 / apb2) + 4)) + 10))) + 1)

    def point_at(self, dist):
        """return point at the edge at given distance"""
        t = 2 * math.pi * dist
        p = Point(self.p.x + self.rx * math.cos(t),
                  self.p.y + self.ry * math.sin(t))
        return p

    def tangent_at(self, dist):
        """Tangent angle at given distance"""
        t = 2 * math.pi * dist
#        slope = -(self.ry * math.cos(t) / self.rx * math.sin(t))
        return math.atan2(self.ry * math.cos(t), - self.rx * math.sin(t))

    def __repr__(self):
        return f'Ellipse[{self.rx},{self.ry},{self.p}]'


class QuadraticCurve:
    """Quadratic bezier curve"""

    def __init__(self, p0, cp, p1):
        self.p0 = p0
        self.cp = cp
        self.p1 = p1
        self.len = 0

    @property
    def startpoint(self):
        return self.p0

    @property
    def endpoint(self):
        return self.p1

    @property
    def position(self):
        return self.p0

    @position.setter
    def position(self, p):
        dx, dy = self.p0.distxy(p)
        self.p0 = p
        self.cp.move(dx, dy)
        self.p1.move(dx, dy)

    def scale(self, f):
        """scale by factor"""
        self.p0 = self.p0.scale(f)
        self.cp = self.cp.scale(f)
        self.p1 = self.p1.scale(f)

    def copy(self):
        """return copy of myself"""
        return QuadraticCurve(self.p0, self.cp, self.p1)

    def point_at(self, t):
        d = 1 - t

        def comp(p0, cp, p1):
            return (d * d * p0) + (2 * d * t * cp) + (t * t * p1)
        x = comp(self.p0.x, self.cp.x, self.p1.x)
        y = comp(self.p0.y, self.cp.y, self.p1.y)
        return Point(x, y)

    def tangent_at(self, t):
        def bd1(p0, cp, p1):
            return 2 * (1 - t) * (cp - p0) + 2 * t * (p1 - cp)
        return math.atan2(bd1(self.p0.y, self.cp.y, self.p1.y),
                          bd1(self.p0.x, self.cp.x, self.p1.x))

    @property
    def length(self):
        if self.len == 0:
            self.len = approx_length(self)
        return self.len

    def __repr__(self):
        return f'QuadraticCurve[{self.p0},{self.cp},{self.p1}]'


class CubicCurve:
    """Cubic bezier curve"""

    def __init__(self, p0, c0, c1, p1):
        self.p0 = p0
        self.c0 = c0
        self.c1 = c1
        self.p1 = p1
        self.len = 0

    @property
    def startpoint(self):
        return self.p0

    @property
    def endpoint(self):
        return self.p1

    @property
    def position(self):
        return self.p0

    @position.setter
    def position(self, p):
        dx, dy = self.p0.distxy(p)
        self.p0 = p
        self.c0.move(dx, dy)
        self.c1.move(dx, dy)
        self.p1.move(dx, dy)

    def scale(self, f):
        """scale by factor"""
        self.p0 = self.p0.scale(f)
        self.p1 = self.p1.scale(f)
        self.c0 = self.c0.scale(f)
        self.c1 = self.c1.scale(f)

    def copy(self):
        """return copy of myself"""
        return CubicCurve(self.p0, self.c0, self.c1, self.p1)

    def point_at(self, t):
        d = 1 - t

        def comp(p0, c0, c1, p1):
            return (d ** 3 * p0) + (3 * d * d * t * c0) + \
                (3 * d * t * t * c1) + (t ** 3 * p1)
        x = comp(self.p0.x, self.c0.x, self.c1.x, self.p1.x)
        y = comp(self.p0.y, self.c0.y, self.c1.y, self.p1.y)
        return Point(x, y)

    def tangent_at(self, t):
        d = 1 - t

        def bd1(p0, c0, c1, p1):
            return 3 * d * d * (c0 - p0) + 6 * d * t * (c1 - c0) + \
                3 * t * t * (p1 - c1)
        return math.atan2(bd1(self.p0.y, self.c0.y, self.c1.y, self.p1.y),
                          bd1(self.p0.x, self.c0.x, self.c1.x, self.p1.x))

    @property
    def length(self):
        if self.len == 0:
            self.len = approx_length(self)
        return self.len

    def __repr__(self):
        return f'CubicCurve[{self.p0},{self.c0},{self.c1},{self.p1}]'


def approx_length(g, samples=10):
    step = 1.0 / samples
    p0 = g.startpoint
    d = 0
    for i in range(0, samples):
        p = g.point_at((i+1) * step)
        d += distance(p0, p)
        p0 = p
    return d


class Polygon:
    """Polygon"""

    def __init__(self, points):
        self.points = points
        bb = self.bbox()
        self.p = Point(bb.x0 + (bb.x1 - bb.x0) / 2,
                       bb.y0 + (bb.y1 - bb.y0) / 2)

    @property
    def position(self):
        return self.p

    @position.setter
    def position(self, p):
        dx, dy = self.p.distxy(p)
        self.move(dx, dy)

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
        return cls(r.get_points())

    def get_points(self):
        """get list of points"""
        return self.points

    def move(self, dx, dy):
        """move polygon points by dx, dy"""
        self.p.move(dx, dy)
        for p in self.points:
            p.move(dx, dy)

    def scale(self, fx, fy=0):
        """scale by fx, fy"""
        if fy == 0:
            fy = fx
        for p in self.points:
            p.x = (p.x - self.p.x) * fx + self.p.x
            p.y = (p.y - self.p.y) * fy + self.p.y

    def rotate(self, a):
        """rotate around x, y by given angle a"""
        for p in self.points:
            p.rotate(self.p.x, self.p.y, a)

    def mirror(self):
        """mirror by center of polygon"""
        for p in self.points:
            p.x = self.p.x + (self.p.x - p.x)

    def bbox(self):
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
        return BBox(x0, y0, x1, y1)

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
            q1 = q2
        return None

    def shrink_to_inside(self, poly):
        """shrink this polygon to be completely inside the given one"""
        # first find a starting point that is inside
        i = -1
        k = 0
        inside = True
        for p in self.points:
            if poly.is_inside(p):
                if i == -1:
                    i = k
            else:
                inside = False
            k += 1
        if i == -1:
            print("completely outside!")
            return False
        if inside:
            print("completely inside!")
            return False
        inters = None
        j = i
        p1 = self.points[j]
        j = (j + 1) % len(self.points)
        changed = False
        while j != i:
            p2 = self.points[j]
            inters = poly.intersection(p1, p2)
            if inters is not None:
                print("intersection, moving point", p2)
                print(inters)
                self.points[j] = inters
                p1 = inters
                changed = True
            else:
                print("no inters")
                p1 = p2
            j = (j + 1) % len(self.points)
        if not changed:
            print("no need to change")
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

    def point_at(self, dist):
        """point on the edge on given distance"""
        dist = self.length() * dist
        p = self.points
        i = 0
        n = len(p)
        p0 = p[0]
        p1 = p[1]
        d = distance(p0, p1)
        while dist > d:
            dist -= d
            i += 1
            j = (i + 1) % n
            p0 = p[i]
            p1 = p[j]
            d = distance(p0, p1)
        return Point(p0.x + (p1.x - p0.x) * (dist / d), p0.y + (p1.y - p0.y) * (dist / d))

    def __repr__(self):
        return f'Polygon[{self.points}]'


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
        # 2. If neither 0 <= (q - p) * r ??? r * r nor 0 <= (p - q) * s <= s * s
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
