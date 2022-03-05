import math
import random
import shape
import default
import geom


class Params:
    def __init__(self):
        self.iterations = default.TEAR_ITERATIONS
        self.minDistance = default.TEAR_MINDISTANCE
        self.minDistanceFactor = 0
        self.angleVar = math.pi / default.TEAR_ANGLEVAR
        self.randomizeBase = True
        self.count = 1

    @classmethod
    def frommap(cls, p):
        pr = cls()
        pr.iterations = p.get('iterations', default.TEAR_ITERATIONS)
        pr.minDistance = p.get(
            'minDistance', default.TEAR_MINDISTANCE)
        pr.minDistanceFactor = p.get(
            'minDistanceFactor', default.TEAR_MINDISTANCEFACTOR)
        pr.angleVar = math.pi / \
            p.get('angleVar', default.TEAR_ANGLEVAR)
        pr.randomizeBase = p.get('randomizeBase', default.TEAR_RANDOMIZEBASE)
        pr.count = p.get('count', default.TEAR_COUNT)
        pr.opacity = p.get('opacity', default.TEAR_OPACITY)
        pr.colours = p.get('colours', default.TEAR_COLOURS)
        return pr


def generatePoint(p1, p2, params):
    d = geom.distance(p1, p2)
    a = geom.angle(p1, p2)
#    print("d a", d, a)
    if d < params.minDistance:
        return None
    md = max(d * params.minDistanceFactor, params.minDistance)
    nd = random.uniform(md, d)
    na = random.uniform(a - params.angleVar, a + params.angleVar)
#    print("angle", a, na)
#    print("new da", nd, na)
    x = p1.x + nd * math.cos(na)
    y = p1.y + nd * math.sin(na)
    return geom.Point(x, y)


def randomizePoints(points, params):
    newPoints = []
    mp = points[len(points) - 1]
    for p in points:
        np = generatePoint(mp, p, params)
        if np is not None:
            newPoints.append(np)
        else:
            newPoints.append(p)
        mp = p
    return newPoints


def generatePoints(points, params, moveEndPoint):
    i = 1
    newPoints = []
    p1 = points[0]
    while i < len(points):
        p2 = points[i]
        newPoints.append(p1)
        np = generatePoint(p1, p2, params)
        if np is not None:
            newPoints.append(np)
            # also randomize the second point
            if moveEndPoint:
                np = generatePoint(np, p2, params)
                if np is not None:
                    p2 = np
        p1 = p2
        i = i + 1
    newPoints.append(p2)
    np = generatePoint(p2, points[0], params)
    if np is not None:
        newPoints.append(np)
    return newPoints


def generate(points, params):
    # 1st round: randomize existing points also
    newps = None
    if params.randomizeBase:
        newps = randomizePoints(points, params)
    else:
        newps = points
    for i in range(params.iterations):
        newps = generatePoints(newps, params, False)
    return newps


def generateShape(base, params):
    shapes = []
    for i in range(params.count):
        s = shape.Shape(geom.Polygon(generate(base.get_points(), params)))
        s.inherit(base)
        print(base, s)
        shapes.append(s)
    return shapes
