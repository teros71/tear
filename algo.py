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
import geom


# ===========================================================================


def apply_recursive(config, base, alg):
    """recursively apply algorithm to forms"""
    if not isinstance(base, shape.List):
        return alg(base)
    for form in base.shapes:
        apply_recursive(config, form, alg)
    return base

# ===========================================================================


def position(config, base):
    """set x y and scale"""
    val = config.get("scale", 1)

    def do_it(base):
        base.scale(val)
    if val != 1:
        apply_recursive(config, base, do_it)
    x = config.get("x", -1)
    y = config.get("y", -1)

    def do_it2(base):
        base.set_position(x, y)
    if x != -1 or y != -1:
        apply_recursive(config, base, do_it2)
    return base

# ===========================================================================


def generate(config, base):
    """base must be generative shape"""
    count = config.get('count', 2)
    shapes = list(itertools.islice(base, count))
    return shape.List(shapes)

# ===========================================================================


def spread(config, base):
    """base is a list of shapes, they are spread"""
    method = config.get("method", "random")
    if method == "random":
        rx = value.read(config, "rangeX")
        ry = value.read(config, "rangeY")

        def do_it(shape):
            shape.set_position(rx.__next__(), ry.__next__())
            return shape
        return apply_recursive(config, base, do_it)
    if method == "area":
        name = config.get("area")
        shap = forms.get(name)
        a = area.RandomInArea(geom.Polygon(shap.get_rendering_points()))

        def do_it2(s):
            p = a.__next__()
            s.set_position(p.x, p.y)
            return s
        return apply_recursive(config, base, do_it2)
    return base


# ===========================================================================


def set_appearance(config, shap, colour, opacity, stroke, strokew):
    """Set appearance of a shape"""
    if isinstance(shap, shape.List):
        colour.reset()
        opacity.reset()
        stroke.reset()
        strokew.reset()
        for inner_shape in shap.shapes:
            set_appearance(config, inner_shape, colour,
                           opacity, stroke, strokew)
        return
    shap.appearance.set(colour.__next__(), opacity.__next__(),
                        stroke.__next__(), strokew.__next__())

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


def xinherit_shape(shap, base):
    """inherit position and appearance"""
    if not isinstance(shap, list):
        print(shap)
        shap.position = copy.deepcopy(base.position)
        shap.appearance = copy.deepcopy(base.appearance)
        return
    print(len(shap))
    for s in shap:
        xinherit_shape(s, base)


def a_tear(r, base):
    """tear a shape"""
    params = tear.Params.frommap(r.get('params'))
    if not isinstance(base, shape.List):
        print("tearing shapes;count=1")
        return tear.generateShape(base, params)
    print(f"tearing shapes;count={len(base.shapes)}", end='', flush=True)
    shapes = []
    for b in base.shapes:
        print(".", end='', flush=True)
        s = tear.generateShape(b, params)
        if s is not None:
            shapes.append(s)
    print('')
    return shape.List(shapes)

# ===========================================================================


def scaler(r, base):
    """scale x and y"""
    rx = value.read(r, "rangeF")
    ry = value.read(r, "rangeFY", d=0)

    def do_it(s):
        s.scale(rx.__next__(), ry.__next__())
        return s
    return apply_recursive(r, base, do_it)

# ===========================================================================


def rotate(r, base):
    #    x = value.read(r, "cx")
    #    y = value.read(r, "cy")
    a = value.read(r, "angle")
    p = base.position
    print(p.x, p.y)
    base.rotate(p.x, p.y, (a.__next__() / 180) * math.pi)
    return base


def multiply(r, base):
    res = [base]
    for i in range(r.get('count', 1)):
        nbase = copy.deepcopy(base)
        if nbase is None:
            print(base, "!!!!!!")
        res.append(nbase)
    return shape.List(res)


algorithms = {
    "position": position,
    "generate": generate,
    "spread": spread,
    "tear": a_tear,
    "scaler": scaler,
    "appearance": appearance,
    "rotate": rotate,
    "multiply": multiply
}


def apply_algorithm(r, base):
    """Apply algorithm
       r is mapping of parameters from json config
       base is the base form for which we apply"""

    alg = r.get('algorithm', None)
    if r.get('disable', False):
        print(f"disabled algorithm {alg}")
        return base
    print(f"algorithm {alg}")

    af = algorithms.get(alg)
    if af is not None:
        return af(r, base)

    # which one?
    if alg == 'goldenRatioRectangles':
        limit = r.get('limit', 10)
        # base is a rectangle, result is a list of rectangles
        return goldenratio.spiralOfRectangles(base, limit)
    if alg == 'goldenRatioSpiral':
        return goldenratio.toPath(base)
#    elif alg == 'line':
#        return lineUp(base)
    print(f"WARNING: unknown algorithm {alg}")
    return base
