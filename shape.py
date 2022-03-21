"""Shape related stuff"""
import math
import random
import json
import copy
import geom


class Shape:
    """Shape wraps a base geometrical element and adds position
    and appearance"""

    def __init__(self, base):
        self.base = base
        self.position = geom.Point(0, 0)
        self.appearance = Appearence()

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
            base = geom.Circle(float(sl[2]))
        else:
            base = geom.Rect(float(sl[2]), float(sl[3]))
        s = cls(base)
        s.set_position(x, y)
        return s

    def move(self, dx, dy):
        """move shape by dx, dy"""
        self.position.x += dx
        self.position.y += dy

    def set_position(self, x, y):
        """set absolute position to x,y"""
        self.position.x = x
        self.position.y = y

    def scale(self, fx, fy=0):
        """scale base shape"""
        if isinstance(self.base, geom.Circle):
            if fy != 0 and fy != fx:
                self.base = geom.Ellipse(self.base.r, self.base.r)
                self.base.scale(fx, fy)
                return
            self.base.scale(fx)
            return
        if fy == 0:
            fy = fx
        self.base.scale(fx, fy)

    def rotate(self, x, y, a):
        """rotates around x,y by given angle a"""
        if isinstance(self.base, (geom.Rect, geom.Ellipse)):
            # rectangle => convert to polygon
            self.base = geom.Polygon.fromrect(self.base)
        self.base.rotate(x, y, math.radians(a))

    def mirror(self):
        """mirror"""
        self.base.mirror()

    def bbox(self):
        """return bounding box"""
        return self.base.bbox(self.position)

    def is_inside(self, p):
        """is point inside of shape"""
        pp = p.move(-self.position.x, -self.position.y)
        return self.base.is_inside(pp)

    def get_points(self):
        """get list of points for the shape"""
        return self.base.get_points(geom.Point(0, 0))

    def get_rendering_points(self):
        """get rendering points for the shape"""
        return self.base.get_points(self.position)

    def inherit(self, s):
        """inherit appearance and position from given shape"""
        self.appearance = copy.deepcopy(s.appearance)
        self.position = copy.deepcopy(s.position)


class List:
    """shape list"""

    def __init__(self, ls):
        self.shapes = ls
        bb = self.bbox()
        self.position = geom.Point(bb.x0 + (bb.x1 - bb.x0) / 2,
                                   bb.y0 + (bb.y1 - bb.y0) / 2)
        self.appearance = Appearence()

    def __iter__(self):
        return iter(self.shapes)

    def move(self, dx, dy):
        """move shape by dx, dy"""
        self.position.move(dx, dy)
        for b in self.shapes:
            b.move(dx, dy)

    def set_position(self, x, y):
        """mark our position and move underlying shapes"""
        dx = x - self.position.x
        dy = y - self.position.y
        self.move(dx, dy)

    def scale(self, fx, fy=0):
        """scale"""
        if fy == 0:
            fy = fx
        for b in self.shapes:
            b.scale(fx, fy)

    def rotate(self, x, y, a):
        """rotate around x,y by given angle a"""
        for b in self.shapes:
            b.rotate(x, y, a)

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
        """inherit appearance and position from given shape"""
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


class ShapePath:
    def __init__(self, s, count):
        self.s = s
        self.len = s.base.length()
        self.step = self.len / count
        self.current = 0

    def next(self):
        p = self.s.base.point_at(self.s.position, self.current)
        self.current += self.step
        if self.current > self.len:
            self.current = 0
        return p


class RectGenerator:
    """Generator for rectangle shapes"""

    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __iter__(self):
        return self

    def __next__(self):
        return Shape(geom.Rect(self.w.get(), self.h.get()))


class CircleGenerator:
    """Generator for circle shapes"""

    def __init__(self, r):
        self.r = r

    def __iter__(self):
        return self

    def __next__(self):
        return Shape(geom.Circle(self.r.get()))


class EllipseGenerator:
    """Generator for ellipse shapes"""

    def __init__(self, rx, ry):
        self.rx = rx
        self.ry = ry

    def __iter__(self):
        return self

    def __next__(self):
        return Shape(geom.Ellipse(self.rx.get(), self.ry.get()))


class PolygonGenerator():
    """Generator for polygon shapes"""

    def __init__(self, r, corners):
        self.r = r
        self.corners = corners

    def __iter__(self):
        return self

    def __next__(self):
        count = self.corners.get()
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
        d = r.get()
        points.append(geom.Point(d * math.cos(a), d * math.sin(a)))
    return geom.Polygon(points)
