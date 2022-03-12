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
    """set x and y"""

    vx = value.read(config, 'x')
    vy = value.read(config, 'y')

    def do_it(base):
        base.set_position(vx.get(), vy.get())
    apply_recursive(config, base, do_it)
    return base

# ===========================================================================


def generate(config, base):
    """base must be generative shape"""
    count = config.get('count', 2)
    shapes = list(itertools.islice(base, count))
    return shape.List(shapes)

# ===========================================================================

# TODO: add different spreading schemes:
# - paths, fill, polar coordinates...


def read_point(s):
    print(s)
    x = value.make(s[0])
    y = value.make(s[1])
    return geom.Point(x.get(), y.get())


def read_spread_s(config):
    name = config.get("area")
    if name is not None:
        shap = shape.Shape.fromstr(name)
    else:
        name = config.get("shape")
        shap = forms.get(name)
    return shap


def spread_matrix(config, base):
    rx = value.read(config, "x")
    ry = value.read(config, "y")
    pos = value.List([geom.Point(x, y) for y in ry for x in rx])

    def do_it(shape):
        p = pos.get()
        shape.set_position(p.x, p.y)
        return shape
    return apply_recursive(config, base, do_it)


def spread_area(config, base):
    shap = read_spread_s(config)
    if shap is None:
        return None
    out = config.get("out", False)
    a = area.RandomInArea(geom.Polygon(shap.get_rendering_points()), out)

    def do_it(s):
        p = a.get()
        if p is not None:
            s.set_position(p.x, p.y)
        return s
    return apply_recursive(config, base, do_it)


def spread_path(config, base):
    shap = read_spread_s(config)
    if shap is None:
        return None
    count = value.read(config, "count")
    a = shape.ShapePath(shap, count.get())

    def do_it(s):
        p = a.next()
        if p is not None:
            s.set_position(p.x, p.y)
        return s
    return apply_recursive(config, base, do_it)


def spread_f(config, base):
    origo = config.get('origo', [0, 0])
    o = read_point(origo)
    rx = value.read(config, "x")
    fx = value.read(config, "f")

    def do_it(s):
        x = rx.get()
        p = fx(x)
        s.set_position(p.x + o.x, p.y + o.y)
        return s
    return apply_recursive(config, base, do_it)


def spread(config, base):
    """base is a list of shapes, they are spread"""
    rx = value.read(config, "x")
    ry = value.read(config, "y")
    x = rx.get()
    y = ry.get()

    def do_it(shape):
        shape.set_position(x, y)
        return shape
    for s in base.shapes:
        apply_recursive(config, s, do_it)
        x = rx.get()
        y = ry.get()
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
    c = colour.get()
    if not isinstance(c, str):
        c = c.get()
    shap.appearance.set(c, opacity.get(),
                        stroke.get(), strokew.get())

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
    rx = value.read(r, "fx")
    ry = value.read(r, "fy", d=0)

    def do_it(s):
        fx = rx.get()
        fy = ry.get()
        s.scale(fx, fy)
        return s
    return apply_recursive(r, base, do_it)

# ===========================================================================


def rotate(r, base):
    #    x = value.read(r, "cx")
    #    y = value.read(r, "cy")
    a = value.read(r, "angle")
    p = base.position
    base.rotate(p.x, p.y, a)
    return base


def multiply(r, base):
    res = [base]
    for i in range(r.get('count', 1)):
        nbase = copy.deepcopy(base)
        if nbase is None:
            print(base, "!!!!!!")
        res.append(nbase)
    return shape.List(res)


def mirror(r, base):
    base.mirror()
    return base


algorithms = {
    "position": position,
    "generate": generate,
    "spread": spread,
    "spread-area": spread_area,
    "spread-path": spread_path,
    "spread-matrix": spread_matrix,
    "spread-f": spread_f,
    "tear": a_tear,
    "scaler": scaler,
    "appearance": appearance,
    "rotate": rotate,
    "multiply": multiply,
    "mirror": mirror
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
