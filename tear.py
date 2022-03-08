import math
import random
import shape
import default
import geom
import value


class Params:
    def __init__(self, it, md, mdf, av, rb, c):
        self.iterations = it
        self.minDistance = md
        self.minDistanceFactor = mdf
        self.angleVar = av
        self.randomizeBase = rb
        self.count = c

    @classmethod
    def frommap(cls, p):
        it = value.read(p, 'iterations', d=default.TEAR_ITERATIONS)
        md = value.read(p, 'minDistance', d=default.TEAR_MINDISTANCE)
        mdf = value.read(p, 'minDistanceFactor',
                         d=default.TEAR_MINDISTANCEFACTOR)
        av = value.read(p, 'angleVar', d=default.TEAR_ANGLEVAR)
        rb = value.read(p, 'randomizeBase', d=default.TEAR_RANDOMIZEBASE)
        c = value.read(p, 'count', d=default.TEAR_COUNT)
        return cls(it, md, mdf, av, rb, c)


def generatePoint(p1, p2, min_d, min_df, av):
    d = geom.distance(p1, p2)
    a = geom.angle(p1, p2)
#    print("d a", d, a)
    if d < min_d:
        return None
    md = max(d * min_df, min_d)
    nd = random.uniform(md, d)
    na = random.uniform(a - av, a + av)
#    print("angle", a, na)
#    print("new da", nd, na)
    x = p1.x + nd * math.cos(na)
    y = p1.y + nd * math.sin(na)
    return geom.Point(x, y)


def randomizePoints(points, min_d, min_df, av):
    newPoints = []
    mp = points[len(points) - 1]
    for p in points:
        np = generatePoint(mp, p, min_d, min_df, av)
        if np is not None:
            newPoints.append(np)
        else:
            newPoints.append(p)
        mp = p
    return newPoints


def generatePoints(points, min_d, min_df, av):
    i = 1
    newPoints = []
    p1 = points[0]

    while i < len(points):
        p2 = points[i]
        newPoints.append(p1)
        np = generatePoint(p1, p2, min_d, min_df, av)
        if np is not None:
            newPoints.append(np)
            # also randomize the second point
        p1 = p2
        i = i + 1
    newPoints.append(p2)
    np = generatePoint(p2, points[0], min_d, min_df, av)
    if np is not None:
        newPoints.append(np)
    return newPoints


def generate(points, it, min_d, min_df, av, rb):
    # 1st round: randomize existing points also
    newps = None

    if rb:
        newps = randomizePoints(points, min_d, min_df, av)
    else:
        newps = points
    for _ in range(it):
        newps = generatePoints(newps, min_d, min_df, av)
    return newps


def generateShape(base, params):
    shapes = []
    it = params.iterations.get()
    min_d = params.minDistance.get()
    min_df = params.minDistanceFactor.get()
    av = params.angleVar.get()
    rb = params.randomizeBase.get()
    for _ in range(params.count.get()):
        points = generate(base.get_points(), it, min_d, min_df, av, rb)
        s = shape.Shape(geom.Polygon(points))
        s.inherit(base)
        shapes.append(s)
    sl = shape.List(shapes)
    return sl
