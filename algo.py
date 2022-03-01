import math
import json
import copy
import itertools
import shape
import default
import goldenratio
import tear
import random
import polygon
import value

# ===========================================================================


def applyRecursive(r, base, alg):
    if type(base) is not list:
        return alg(base)
    else:
        for s in base:
            applyRecursive(r, s, alg)
    return base

# ===========================================================================


def position(r, base):
    # set x y and scale
    s = r.get("scale", 1)
    if s != 1:
        base.scale(s)
    x = r.get("x", -1)
    y = r.get("y", -1)
    if x != -1 or y != -1:
        base.setPosition(x, y)
    return base

# ===========================================================================


def generate(r, base):
    # base must be generative shape
    count = r.get('count', 2)
    shapes = list(itertools.islice(base, count))
    return shapes

# ===========================================================================


def spread(r, base):
    # base is a list of shapes, they are spread
    rx = value.read(r, "rangeX")
    ry = value.read(r, "rangeY")

    def doIt(s):
        s.setPosition(rx.__next__(), ry.__next__())
    return applyRecursive(r, base, doIt)

# ===========================================================================


def setAppearance(r, s, colour, opacity, stroke):
    if type(s) is not list:
        s.colour = colour.__next__()
        s.opacity = opacity.__next__()
        s.stroke = stroke.__next__()
        return
    colour.reset()
    opacity.reset()
    stroke.reset()
    for ss in s:
        setAppearance(r, ss, colour, opacity, stroke)

# ===========================================================================


def appearance(r, base):
    opacity = value.read(r, 'opacity', d=1.0)
    colour = value.read(r, 'colours', d=["black"])
    stroke = value.read(r, 'stroke', d="none")
    setAppearance(r, base, colour, opacity, stroke)
    return base

# ===========================================================================


def aTear(r, base):
    # base is a list of forms, result is a list of shapes
    params = tear.Params.frommap(r.get('params'))
    shapes = []
    print("tearing shapes;count={0}".format(len(base)), end='', flush=True)
    for b in base:
        print(".", end='', flush=True)
        # take point list
        pl = b.toPolygon()
        s = tear.generateShape(pl, params)
        if s is not None:
            shapes.append(s)
    print('')
    return shapes

# ===========================================================================


def scaler(r, base):
    rf = value.read(r, "rangeF")

    def doIt(s):
        s.scale(rf.__next__())
    return applyRecursive(r, base, doIt)

# ===========================================================================


def applyAlgorithm(r, base):
    # r is mapping of parameters from json config
    # base is the base form for which we apply

    if r.get('disable', False):
        return base

    alg = r.get('algorithm', None)
    print("algorithm {0}".format(alg))

    # which one?
    if alg == 'position':
        return position(r, base)

    elif alg == 'generate':
        return generate(r, base)

    elif alg == 'spread':
        return spread(r, base)

    elif alg == 'tear':
        return aTear(r, base)

    elif alg == 'scaler':
        return scaler(r, base)

    elif alg == 'appearance':
        return appearance(r, base)

    elif alg == 'list':
        return [base]
    elif alg == 'shape':
        s = shape.Shape()
        s.points = base.toPolygon()
        s.opacity = 0.2
        return [[s]]

    elif alg == 'multiply':
        res = [base]
        xstep = r.get('x-step', 10.0)
        for i in range(r.get('count', 1)):
            nbase = copy.deepcopy(base)
            dx = i * xstep
            dy = 0
            nbase.move(dx, dy)
            res.append(nbase)
        return res
    elif alg == 'goldenRatioRectangles':
        limit = r.get('limit', 10)
        # base is a rectangle, result is a list of rectangles
        return goldenratio.spiralOfRectangles(base, limit)
    elif alg == 'goldenRatioSpiral':
        return goldenratio.toPath(base)
#    elif alg == 'line':
#        return lineUp(base)
    else:
        return base
