import math
import random
import json
import copy
import value


class Point:
    # Point at x,y
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def randomize(self, maxR):
        nd = random.uniform(0.0, maxR)
        na = random.uniform(0, 2 * math.pi)
        self.x = self.x + nd * math.cos(na)
        self.y = self.y + nd * math.sin(na)

    def output(self):
        print(self.x, self.y)


def halfWayPoint(p1, p2):
    return Point(p1.x + (p2.x - p1.x) / 2, p1.y + (p2.y - p1.y) / 2)


def distance(p1, p2):
    return math.sqrt(math.pow(p2.y - p1.y, 2) + math.pow(p2.x - p1.x, 2))


def angle(p1, p2):
    return math.atan2(p2.y - p1.y, p2.x - p1.x)


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    def scale(self, dr):
        self.width = self.width * dr
        self.height = self.height * dr

    def setPosition(self, x, y):
        self.x = x - (self.width / 2)
        self.y = y - (self.height / 2)

    def bBox(self):
        return Rect(self.x, self.y, self.width, self.height)

    def toPolygon(self):
        return [Point(self.x, self.y), Point(self.x + self.width, self.y), Point(self.x + self.width, self.y + self.height), Point(self.x, self.y + self.height)]


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    def scale(self, r):
        self.x = self.x * r
        self.y = self.y * r
        self.r = self.r * r

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def bBox(self):
        return Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def copy(self, x, y):
        return Circle(x, y, self.r)

    def toPolygon(self):
        points = []
        t = 0.0
        while t < math.pi * 2:
            points.append(Point(self.x + self.r * math.cos(t),
                                self.y + self.r * math.sin(t)))
            t = t + math.pi / 8
        return points


class RectGenerator:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __iter__(self):
        return self

    def __next__(self):
        return Rect(0, 0, self.w.__next__(), self.h.__next__())


class CircleGenerator:
    def __init__(self, r):
        self.r = r

    def __iter__(self):
        return self

    def __next__(self):
        return Circle(0, 0, self.r.__next__())


class Shape:
    def __init__(self):
        self.points = []
        self.colour = 'black'
        self.opacity = 1
        self.stroke = 'none'

    def move(self, dx, dy):
        for p in self.points:
            p.x = p.x + dx
            p.y = p.y + dy

    def scale(self, r):
        for p in self.points:
            p.x = p.x * r
            p.y = p.y * r


class OutputParams:
    def __init__(self):
        self.count = 1
        self.opacity = 0.2
        self.colours = ["black"]
        self.dx = 0.0
        self.dy = 0.0


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


def readFromFile(fname):
    defaults = Shape()
    shapes = []
    f = open(fname, 'r')
    # json to dictionary
    data = json.load(f)
    t = data.get('defaults')
    if t != None:
        defaults.tear.iterations = t.get('iterations', 1)
        defaults.tear.minDistance = t.get('minDistance', 2.0)
        defaults.tear.angleVar = t.get('angleVar', 2)
        defaults.output.count = t.get('count', 1)
        defaults.output.opacity = t.get('opacity', 2.0)
    for shap in data['shapes']:
        #        print(shap)
        p = Shape()
        typ = shap.get('type')
        if typ == 'polygon':
            g = shap['geometry']
            x = math.fabs(g.get('x', 0.0))
            y = math.fabs(g.get('y', 0.0))
            g = g['points']
            if len(g) % 2 != 0:
                raise ValueError("invalid polygon geometry")
            for i in range(0, len(g), 2):
                p.points.append(
                    Point(math.fabs(g[i]) + x, math.fabs(g[i+1]) + y))
        elif typ == 'rectangle':
            g = shap['geometry']
            x = math.fabs(g.get('x', 0.0))
            y = math.fabs(g.get('y', 0.0))
            w = math.fabs(g['width'])
            h = math.fabs(g['height'])
            p.points.append(Point(x, y))
            p.points.append(Point(x + w, y))
            p.points.append(Point(x + w, y + h))
            p.points.append(Point(x, y + h))
        else:
            raise ValueError("invalid shape type", typ)

        t = shap.get('tear')
        if t is not None:
            p.tear.iterations = t.get('iterations', defaults.tear.iterations)
            p.tear.minDistance = t.get(
                'minDistance', defaults.tear.minDistance)
            p.tear.angleVar = math.pi / \
                t.get('angleVar', defaults.tear.angleVar)
        t = shap.get('output')
        if t is not None:
            p.output.count = t.get('count', defaults.output.count)
            p.output.opacity = t.get('opacity', defaults.output.opacity)
            p.output.colours = t.get('colours', ['black'])
            p.output.dx = t.get('dx', 0.0)
            p.output.dy = t.get('dy', 0.0)
#        shapes.append(p)
        t = shap.get('production')
        if t is not None:
            count = t.get('count', 1)
            rects = goldenRects2(Rect(200, 150, 600, 600), 10)
            for r in rects:
                np = copy.deepcopy(p)
                np.points = r.points()
                shapes.append(np)
    f.close()
    return shapes
