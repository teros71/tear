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

    def scale(self, r):
        for p in self.points:
            p.x = p.x * r
            p.y = p.y * r

    def setPosition(self, x, y):
        bb = self.bBox()
        dx = x - (bb.width / 2)
        dy = y - (bb.height / 2)
        if dx != 0 or dy != 0:
            self.move(dx, dy)

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


class Generator():
    def __init__(self, rangeR, rangePoints):
        self.rangeR = rangeR
        self.rangePoints = rangePoints

    def __iter__(self):
        return self

    def __next__(self):
        count = self.rangePoints.__next__()
        return randomPolygon(self.rangeR.min, self.rangeR.max, count)


def randomPolygon(minR, maxR, count):
    slicea = (2 * math.pi) / count
    points = []
    for i in range(0, count):
        s = i * slicea
        a = random.uniform(s, s + slicea)
        d = random.uniform(minR, maxR)
        points.append(shape.Point(d * math.cos(a), d * math.sin(a)))
    return Polygon(points)
