import copy
import math

value = 1.618033988749895
goldenB = 0.30635


def spiralOfRectangles(rect, limit):
    global value
    # generate rectangles in golden ratio spiral side by side
    # rect is the starting point rectangle, the biggest one
    # limit is the minimum lenght of rectangle side
    # returns an array of rectangles
    rs = [rect]
    count = 1
    while rect.width > limit:
        r = copy.deepcopy(rect)
        r.scale(1 / value)
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


def spiralX(t):
    return math.cos(t) * (math.pow(math.e, (0.30635 * t)))


def spiralY(t):
    return math.sin(t) * (math.pow(math.e, (0.30635 * t)))


def toPathSingle(f):
    t = 0.0
    shapes = []
    while t < (8 * math.pi):
        s = copy.deepcopy(f)
        s.move(spiralX(t), spiralY(t))
        shapes.append(s)
        t = t + (math.pi / (1 + t))
    return shapes


def toPath(f):
    if type(f) is list:
        shapes = []
        for nf in f:
            shapes.extend(toPathSingle(nf))
        return shapes
    else:
        return toPathSingle(f)
