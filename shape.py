import math
import random
import json
import copy
import geom


class RectGenerator:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __iter__(self):
        return self

    def __next__(self):
        return Shape(geom.Rect(self.w.get(), self.h.get()))


class CircleGenerator:
    def __init__(self, r):
        self.r = r

    def __iter__(self):
        return self

    def __next__(self):
        return Shape(geom.Circle(self.r.get()))


class PolygonGenerator():
    """Generator for shapes"""

    def __init__(self, range_r, range_points):
        self.range_r = range_r
        self.range_points = range_points

    def __iter__(self):
        return self

    def __next__(self):
        count = self.range_points.get()
        return Shape(random_polygon(self.range_r.min, self.range_r.max, count))


def random_polygon(minR, maxR, count):
    slicea = (2 * math.pi) / count
    points = []
    for i in range(0, count):
        s = i * slicea
        a = random.uniform(s, s + slicea)
        d = random.uniform(minR, maxR)
        points.append(geom.Point(d * math.cos(a), d * math.sin(a)))
    return geom.Polygon(points)


class Shape:
    def __init__(self, base):
        self.base = base
        self.position = geom.Point(0, 0)
        self.appearance = Appearence()

    def move(self, dx, dy):
        """move shape by dx, dy"""
        self.position.x += dx
        self.position.y += dy

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def scale(self, rx, ry=0):
        if ry == 0:
            ry = rx
        if isinstance(self.base, list):
            for b in self.base:
                b.scale(rx, ry)
            return
        self.base.scale(rx, ry)

    def rotate(self, x, y, a):
        self.base.rotate(x, y, math.radians(a.get()))

    def bbox(self):
        if isinstance(self.base, geom.Rect):
            tlx = self.position.x - self.base.width / 2
            tly = self.position.y - self.base.height / 2
            return geom.BBox(tlx, tly, tlx + self.base.width,
                             tly + self.base.height)
        if isinstance(self.base, geom.Circle):
            return geom.BBox(self.position.x - self.base.r,
                             self.position.y - self.base.r,
                             self.position.x + self.base.r,
                             self.position.y + self.base.r)
        if isinstance(self.base, geom.Polygon):
            bb = self.base.bbox()
            bb.x0 += self.position.x
            bb.x1 += self.position.x
            bb.y0 += self.position.y
            bb.y1 += self.position.y
            return bb

    def get_points(self):
        return self.base.get_points(0, 0)

    def get_rendering_points(self):
        return self.base.get_points(self.position.x, self.position.y)

    def inherit(self, s):
        self.appearance = copy.deepcopy(s.appearance)
        self.position = copy.deepcopy(s.position)


class List:
    def __init__(self, ls):
        self.shapes = ls
        bb = self.bbox()
        self.position = geom.Point(bb.x0 + (bb.x1 - bb.x0) / 2,
                                   bb.y0 + (bb.y1 - bb.y0) / 2)
#        self.base = base
        self.appearance = Appearence()

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

    def scale(self, rx, ry=0):
        if ry == 0:
            ry = rx
        for b in self.shapes:
            b.scale(rx, ry)

    def rotate(self, x, y, a):
        for b in self.shapes:
            b.rotate(x, y, a)

    def bbox(self):
        bb = None
        for b in self.shapes:
            if bb is None:
                bb = b.bbox()
            else:
                bb.join(b.bbox())
        return bb

#    def inherit(self, s):
#        for b in self.shapes:
#            b.inherit(s)


class Appearence:
    def __init__(self):
        self.colour = 'black'
        self.opacity = 1
        self.stroke = 'none'
        self.stroke_width = 0

    def set(self, c, o, s, sw):
        self.colour = c
        self.opacity = o
        self.stroke = s
        self.stroke_width = sw


def goldenRects2(rect, limit):
    rs = [rect]
    count = 1
    while rect.width > limit:
        r = copy.deepcopy(rect)
        r.ratio(1 / 1.618)
        if count % 4 == 1:
            r.move(rect.width, 0)
        elif count % 4 == 2:
            r.move(rect.width - r.width, rect.height)
        elif count % 4 == 3:
            r.move(-r.width, rect.height - r.height)
        else:
            r.move(0, -r.height)
        count = count + 1
        rs.append(r)
        rect = r
    return rs
