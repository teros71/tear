import math
import random
import shape
import default


class Params:
    def __init__(self):
        self.iterations = default.tear_iterations
        self.minDistance = default.tear_minDistance
        self.minDistanceFactor = 0
        self.angleVar = math.pi / default.tear_angleVar
        self.randomizeBase = True
        self.count = 1
        self.opacity = 1.0
        self.colours = '[black]'

    @classmethod
    def frommap(cls, p):
        pr = cls()
        pr.iterations = p.get('iterations', default.tear_iterations)
        pr.minDistance = p.get(
            'minDistance', default.tear_minDistance)
        pr.minDistanceFactor = p.get(
            'minDistanceFactor', default.tear_minDistanceFactor)
        pr.angleVar = math.pi / \
            p.get('angleVar', default.tear_angleVar)
        pr.randomizeBase = p.get('randomizeBase', default.tear_randomizeBase)
        pr.count = p.get('count', default.tear_count)
        pr.opacity = p.get('opacity', default.tear_opacity)
        pr.colours = p.get('colours', default.tear_colours)
        return pr


def generatePoint(p1, p2, params):
    d = shape.distance(p1, p2)
    a = shape.angle(p1, p2)
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
    return shape.Point(x, y)


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


def generateShape(points, params):
    shapes = []
#    print("variation", params.angleVar)
    for i in range(params.count):
        s = shape.Shape()
        s.points = generate(points, params)
#        s.colour = params.colours[i % len(params.colours)]
#        s.opacity = params.opacity
        shapes.append(s)
    return shapes
