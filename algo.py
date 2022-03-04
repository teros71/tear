"""Algorithms for processing"""

import math
import copy
import itertools
import shape
import goldenratio
import tear
import value
import area
import forms
import polygon


# ===========================================================================


def apply_recursive(config, base, alg):
    """recursively apply algorithm to forms"""
    if not isinstance(base, list):
        return alg(base)
    for form in base:
        apply_recursive(config, form, alg)
    return base

# ===========================================================================


def position(config, base):
    """set x y and scale"""
    val = config.get("scale", 1)
    if val != 1:
        base.scale(val)
    x = config.get("x", -1)
    y = config.get("y", -1)
    if x != -1 or y != -1:
        base.setPosition(x, y)
    return base

# ===========================================================================


def generate(config, base):
    """base must be generative shape"""
    count = config.get('count', 2)
    shapes = list(itertools.islice(base, count))
    return shapes

# ===========================================================================


def spread(config, base):
    """base is a list of shapes, they are spread"""
    method = config.get("method", "random")
    if method == "random":
        rx = value.read(config, "rangeX")
        ry = value.read(config, "rangeY")

        def do_it(shape):
            shape.setPosition(rx.__next__(), ry.__next__())
            return shape
        return apply_recursive(config, base, do_it)
    if method == "area":
        name = config.get("area")
        shap = forms.get(name)
        if not isinstance(shap, polygon.Polygon):
            shap = polygon.Polygon(shap.toPolygon())
        a = area.RandomInArea(shap)

        def do_it2(shape):
            p = a.__next__()
            shape.setPosition(p.x, p.y)
            return shape
        return apply_recursive(config, base, do_it2)
    return base


# ===========================================================================


def set_appearance(config, shape, colour, opacity, stroke, strokew):
    """Set appearance of a shape"""
    if not isinstance(shape, list):
        shape.colour = colour.__next__()
        shape.opacity = opacity.__next__()
        shape.stroke = stroke.__next__()
        shape.stroke_width = strokew.__next__()
        return
    colour.reset()
    opacity.reset()
    stroke.reset()
    strokew.reset()
    for inner_shape in shape:
        set_appearance(config, inner_shape, colour, opacity, stroke, strokew)

# ===========================================================================


def appearance(config, base):
    """appearance algorithm"""
    opacity = value.read(config, 'opacity', d=1.0)
    colour = value.read(config, 'colours', d=["black"])
    stroke = value.read(config, 'stroke', d="none")
    strokew = value.read(config, 'strokeWidth', d=0)
    set_appearance(config, base, colour, opacity, stroke, strokew)
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
    rx = value.read(r, "rangeF")
    ry = value.read(r, "rangeFY", d=0)

    def doIt(s):
        s.scale(rx.__next__(), ry.__next__())
        return s
    return apply_recursive(r, base, doIt)

# ===========================================================================


def rotate(r, base):
    #    x = value.read(r, "cx")
    #    y = value.read(r, "cy")
    a = value.read(r, "angle")
    p = base.bBox().midPoint()
    print(p.x, p.y)
    base.rotate(p.x, p.y, (a.__next__() / 180) * math.pi)
    return base


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

    elif alg == 'rotate':
        return rotate(r, base)

    elif alg == 'list':
        return [base]

    elif alg == 'shape':
        s = shape.Shape()
        s.points = base.toPolygon()
        return s

    elif alg == 'multiply':
        res = [base]
        for i in range(r.get('count', 1)):
            nbase = copy.deepcopy(base)
            if nbase is None:
                print(base, "!!!!!!")
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
