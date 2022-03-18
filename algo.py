"""Algorithms for processing"""

import math
import random
import copy
import itertools
import shape
import goldenratio
import tear
import value
import area
import forms
import geom
import voronoi


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


def read_point(s, config):
    print(s)
    x = value.make(s[0], config)
    y = value.make(s[1], config)
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
    a = area.RandomInArea(shap, out)

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
    o = read_point(origo, config)
    fx = value.read(config, "f")
    shape_arg = config.get("shape-arg", False)

    def do_it(s):
        if shape_arg:
            p = fx(s)
        else:
            p = fx()
        s.set_position(p.x + o.x, p.y + o.y)
        return s
    return apply_recursive(config, base, do_it)


def x_spread_s(config, base):
    origo = config.get('origo', [0, 0])
    o = read_point(origo, config)
    params = config.get('params', [])
    vals = {key: value.read(config, key) for key in params}
    fx = value.read(config, "f")

    def do_it(s):
        args = {key: v.get() for key, v in vals.items()}
        p = fx(s, **args)
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


def set_appearance(config, shap, colour, opacity, stroke, strokew, shad, blur):
    """Set appearance of a shape"""
    if isinstance(shap, shape.List):
        colour.reset()
        opacity.reset()
        stroke.reset()
        strokew.reset()
        for inner_shape in shap.shapes:
            set_appearance(config, inner_shape, colour,
                           opacity, stroke, strokew, shad, blur)
        return
    c = colour.get()
    if not isinstance(c, str):
        c = c.get()
    shap.appearance.set(c, opacity.get(),
                        stroke.get(), strokew.get(), shad, blur)

# ===========================================================================


def appearance(config, base):
    """appearance algorithm"""
    opacity = value.read(config, 'opacity', d=1.0)
    colour = value.read(config, 'colours', d=["black"])
    stroke = value.read(config, 'stroke', d="none")
    strokew = value.read(config, 'strokeWidth', d=0)
    shad = config.get('shadow', False)
    blur = config.get('blur', False)
    set_appearance(config, base, colour, opacity, stroke, strokew, shad, blur)
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


def vectorfield(r, base):
    fields = r.get("fields")

    def do_it(s):
        ox = s.position.x
        oy = s.position.y
        fi = 0
        fj = 0
        for f in fields:
            x = ox - f[0]
            y = oy - f[1]
            i, j = eval(f[2])
            print("eval", i, j)
            fi += i
            fj += j
        ang = geom.angle(geom.Point(0, 0), geom.Point(fi, fj))
        print(x, y, fi, fj, math.degrees(ang))
        a = value.Single(math.degrees(ang))
        s.rotate(0, 0, a)
        return s
    return apply_recursive(r, base, do_it)


def shadow(r, base):

    def do_it(s):
        s.appearance.shadow = True
    return apply_recursive(r, base, do_it)


def a_voronoi(r, base):
    infinite = r.get("infinite", False)
    ps = []
    for s in base.shapes:
        ps.extend(s.get_points())
    if infinite:
        return shape.List([shape.Shape(p) for p in voronoi.all_polygons(ps)])
    return shape.List([shape.Shape(p) for p in voronoi.finite_polygons(ps)])


def b_voronoi(r, base):
    count = r.get("count", 1)
    res = None
    for s in base.shapes:
        ps = []
        bb = s.bbox()
        for _ in range(count):
            i = 15
            while i > 0:
                p = geom.Point(random.randint(int(bb.x0), int(bb.x1)),
                               random.randint(int(bb.y0), int(bb.y1)))
                if s.is_inside(p):
                    ps.append(p)
                    i = 1
                i -= 1
        print(count, len(ps))
        ns = voronoi.all_polygons(ps)
        for pol in ns:
            pol.shrink_to_inside(s.base)

        shaps = [shape.Shape(p) for p in ns]
        if res is None:
            res = shape.List(shaps)
        else:
            res.shapes.extend(shaps)
    return res


algorithms = {
    "position": position,
    "generate": generate,
    "spread": spread,
    "spread-area": spread_area,
    "spread-path": spread_path,
    "spread-matrix": spread_matrix,
    "spread-f": spread_f,
    "x-spread-s": x_spread_s,
    "tear": a_tear,
    "scaler": scaler,
    "appearance": appearance,
    "rotate": rotate,
    "multiply": multiply,
    "mirror": mirror,
    "vectorfield": vectorfield,
    "shadow": shadow,
    "voronoi": a_voronoi,
    "voronoi-b": b_voronoi
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
