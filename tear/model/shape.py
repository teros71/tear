"""Shape related stuff"""
import logging
import math
import random
import copy
import itertools
from tear.geometry import geom, path

log = logging.getLogger(__name__)


class Shape:
    """Shape wraps a geometrical element and adds appearance
    This is the object which algorithms are mostly working with
    so a lot is passed to the underlying geometry"""

    def __init__(self, g):
        self.g = g
        self.appearance = Appearence()
        self.angle = 0

    @property
    def position(self):
        return self.g.position

    @position.setter
    def position(self, p):
        self.g.position = p

    def set_position(self, x, y):
        """set absolute position to x,y"""
        self.g.position = geom.Point(x, y)

    def move(self, dx, dy):
        """move shape by dx, dy"""
        npx = self.g.position.x + dx
        npy = self.g.position.y + dy
        self.g.position = geom.Point(npx, npy)

    def scale(self, fx, fy=0):
        """scale shape"""
        if isinstance(self.g, geom.Circle):
            if fy not in (0, fx):
                self.g = geom.Ellipse(self.g.r, self.g.r)
                self.g.scale(fx, fy)
                return
            self.g.scale(fx)
            return
        if fy == 0:
            fy = fx
        self.g.scale(fx, fy)

    def rotate(self, a):
        """rotates by given angle a"""
        if isinstance(self.g, geom.Rect):
            # rectangle => convert to polygon
            self.g = geom.Polygon.fromrect(self.g)
        elif isinstance(self.g, geom.Ellipse):
            self.angle = a
            return
        self.g.rotate(math.radians(a))

    @classmethod
    def fromstr(cls, str):
        """shortcut for creating rects and circles
        format: x:y:r or x:y:w:h """
        sl = str.split(':')
        if len(sl) < 3:
            return None
        x = float(sl[0])
        y = float(sl[1])
        if len(sl) == 3:
            g = geom.Circle(float(sl[2]), geom.Point(x, y))
        else:
            g = geom.Rect(float(sl[2]), float(sl[3]), geom.Point(x, y))
        s = cls(g)
        return s

    def mirror(self):
        """mirror"""
        self.g.mirror()

    def bbox(self):
        """return bounding box"""
        return self.g.bbox()

    def is_inside(self, p):
        """is point inside of shape"""
        return self.g.is_inside(p)

    def get_points(self):
        """get list of points for the shape"""
        return self.g.get_points()

    def inherit(self, s):
        """inherit appearance and position from given shape"""
        self.appearance = copy.deepcopy(s.appearance)


class List:
    """shape list"""

    def __init__(self, ls):
        self.shapes = ls
        bb = self.bbox()
        self.p = geom.Point(bb.x0 + (bb.x1 - bb.x0) / 2,
                            bb.y0 + (bb.y1 - bb.y0) / 2)
        self.appearance = Appearence()

    def __iter__(self):
        return iter(self.shapes)

    @property
    def position(self):
        return self.p

    def set_position(self, x, y):
        """mark our position and move underlying shapes"""
        dx = x - self.p.x
        dy = y - self.p.y
        self.move(dx, dy)

    def move(self, dx, dy):
        """move shape by dx, dy"""
        self.p.move(dx, dy)
        for b in self.shapes:
            b.move(dx, dy)

    def scale(self, fx, fy=0):
        """scale"""
        for b in self.shapes:
            b.scale(fx, fy)

    def rotate(self, a):
        """rotate around x,y by given angle a"""
        for b in self.shapes:
            b.rotate(a)

    def mirror(self):
        """mirror"""
        for b in self.shapes:
            b.mirror()

    def bbox(self):
        """bounding box"""
        bb = None
        for b in self.shapes:
            if bb is None:
                bb = b.bbox()
            else:
                bb.join(b.bbox())
        return bb

    def inherit(self, s):
        """inherit appearance from given shape"""
        self.appearance = copy.deepcopy(s.appearance)
        self.set_position(s.position.x, s.position.y)


class Appearence:
    """Appearance for a shape: colour, opacity and stroke attributes"""

    def __init__(self):
        self.colour = 'black'
        self.opacity = 1
        self.stroke = 'none'
        self.stroke_width = 0
        self.shadow = False
        self.blur = False
        self.clip = None
        self.mask = None

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, c):
        self._colour = c

    def set(self, o, s, sw, shad=False, blur=False):
        """set appearance attributes"""
        self.opacity = o
        self.stroke = s
        self.stroke_width = sw
        self.shadow = shad
        self.blur = blur


class Path:
    """Path
    Only geometry.path.Path geometry.geom.Curve object is supported,
    plus it is assumed to have absolute
    coordinates, not relative to 0,0.
    """

    def __init__(self, g, step, angle=False):
        if not isinstance(g, (path.Path, geom.QuadraticCurve, geom.CubicCurve,
                              geom.Ellipse)):
            raise ValueError("path: unsupported geometry type", g)
        self.g = g
        if step > 1.0:
            self.step = 1.0 / step
        else:
            self.step = step
        self.current = 0.0
        self.angle = angle

    @property
    def next(self):
        p = self.g.point_at(self.current)
        ang = 0
        if self.angle:
            ang = self.g.tangent_at(self.current)
        self.current += self.step
        if self.current > 1.0:
            self.current = 0.0
        if self.angle:
            return p, ang
        return p

    @classmethod
    def fromshape(cls, shap, step, angle=False):
        # find the underlying geometry
        def get_geom(s):
            if isinstance(s, List):
                return get_geom(s.shapes[0])
            if isinstance(s, Shape):
                return s.g
            raise ValueError("path from shape: unsupported shape type")
        g = get_geom(shap)
        return cls(g, step, angle)


class RectGenerator:
    """Generator for rectangle shapes"""

    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __iter__(self):
        return self

    def __next__(self):
        return Shape(geom.Rect(self.w.next, self.h.next))


class CircleGenerator:
    """Generator for circle shapes"""

    def __init__(self, r):
        self.r = r

    def __iter__(self):
        return self

    def __next__(self):
        return Shape(geom.Circle(self.r.next))


class EllipseGenerator:
    """Generator for ellipse shapes"""

    def __init__(self, rx, ry):
        self.rx = rx
        self.ry = ry

    def __iter__(self):
        return self

    def __next__(self):
        return Shape(geom.Ellipse(self.rx.next, self.ry.next))


class PolygonGenerator():
    """Generator for polygon shapes"""

    def __init__(self, r, corners):
        self.r = r
        self.corners = corners

    def __iter__(self):
        return self

    def __next__(self):
        count = self.corners.next
        return Shape(random_polygon(self.r, count))


def random_polygon(r, count):
    """return random polygon with given parameters:
    r is distance from the center, count is number of points"""
    # slice circle
    slicea = (2 * math.pi) / count
    points = []
    # generate points
    for i in range(0, count):
        s = i * slicea
        # get random angle within slice
        a = random.uniform(s, s + slicea)
        # get distance
        d = r.next
        points.append(geom.Point(d * math.cos(a), d * math.sin(a)))
    return geom.Polygon(points)


class PathGenerator:
    def __init__(self, curve_type, start, end, count, av, mode):
        self.curve_type = curve_type
        self.start = start
        self.end = end
        self.count = count
        self.av = av
        self.mode = path.Path.str2mode(mode)

    def __iter__(self):
        return self

    def __next__(self):
        s = self.start.next
        e = self.end.next
        if self.curve_type == 'cubic':
            return Shape(path.random_path_cubic(s, e,
                                                self.count, self.av, 2.0,
                                                self.mode))
        return Shape(path.random_path_quadratic(s, e,
                                                self.count, self.av, 2.0,
                                                self.mode))

class PathGenerator2:
    def __init__(self, ps, count, av):
        self.points = list(itertools.islice(ps, count))
        self.av = av

    def __iter__(self):
        return self

    def __next__(self):
        return Shape(path.path_around(self.points, self.av))
