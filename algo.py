"""Algorithms for processing"""

import math
import random
import copy
import itertools
import shape
import goldenratio
import tear
from value import value, reader
import area
import forms
import geom
import voronoi


# ===========================================================================


def apply_recursive(config, base, alg):
    """Recursively apply algorithm to shapes
    Args:
        base (Shape | List): target of operation
        alg (function): function to be applied
    Returns:
        base
    """
    if not isinstance(base, shape.List):
        return alg(base)
    for form in base:
        apply_recursive(config, form, alg)
    return base


def read_point(config, name):
    """Helper to read a point from config"""
    p = config.get(name)
    if p is None:
        return None
    if not isinstance(p, list) or len(p) != 2:
        raise ValueError("invalid point")
    x = reader.make(p[0], config)
    y = reader.make(p[1], config)
    return geom.Point(x.get(), y.get())


def read_cartesian(config):
    vx = reader.read(config, 'x')
    if vx is None:
        return None
    vy = reader.read(config, 'y')
    if vy is None:
        return None
    return value.Cartesian(vx, vy)


def read_polar(config):
    origo = read_point(config, 'origo')
    if origo is None:
        return None
    t = reader.read(config, 't')
    if t is None:
        return None
    r = reader.read(config, 'r')
    if r is None:
        return None
    return value.Polar(origo, t, r)


# ===========================================================================
# The following functions have the same signature:
# Args:
#   config (dictionary): any parameters used by the algorithm.
#       This is as read from json.
#   base (shape or shape list): target of the algorithm


def position(config, base):
    """Set position of shape
    Args for cartesian:
        x (value): x coordinate
        y (value): y coordinate
    Args for polar:
        origo: (point): origo
        t (value): angle
        r (value): radius
    Args:
        leaf (bool): apply to leaf shapes rather than compounds, default true
    """

    p = read_cartesian(config)
    if p is None:
        p = read_polar(config)
    if p is None:
        raise ValueError("position: not enough data")

    def do_it(base):
        x, y = p.get()
        base.set_position(x, y)
    if config.get('leaf', True):
        apply_recursive(config, base, do_it)
    else:
        do_it(base)
    return base

# ===========================================================================


def scaler(r, base):
    """Scale shape by x and y
    Args:
        fx (value): x factor
        fy (value): y factor, if omitted, go with the same as x
    """
    # scaling is meaningful only for leafs, I suppose

    rx = reader.read(r, "fx")
    ry = reader.read(r, "fy", d=0)

    def do_it(s):
        fx = rx.get()
        fy = ry.get()
        s.scale(fx, fy)
        return s
    return apply_recursive(r, base, do_it)

# ===========================================================================


def rotate(r, base):
    """Rotate shape
    Args:
        angle (degrees): rotation angle
        around-leaf (bool): rotate around leafs rather than compound,
            default false
    """
    a = reader.read(r, "angle")
    leaf = r.get("around-leaf", False)
    bp = base.position

    def do_it(s):
        if leaf:
            p = s.position
        else:
            p = bp
        s.rotate(p.x, p.y, a.get())
    return apply_recursive(r, base, do_it)
#    base.rotate(p.x, p.y, a.get())
#    return base


def generate(config, base):
    """base must be generative shape"""
    count = config.get('count', 2)
    shapes = list(itertools.islice(base, count))
    return shape.List(shapes)

# ===========================================================================


def read_spread_s(config):
    name = config.get("area")
    if name is not None:
        shap = shape.Shape.fromstr(name)
    else:
        name = config.get("shape")
        shap = forms.get(name)
    return shap


def spread_matrix(config, base):
    rx = reader.read(config, "x")
    ry = reader.read(config, "y")
    if rx is not None:
        pos = value.List([geom.Point(x, y) for y in ry for x in rx])
    else:
        o = read_point(config, 'origo')
        rt = reader.read(config, "t")
        rr = reader.read(config, "r")
        pos = value.List(
            [geom.Point.fromtuple(geom.polar2cartesian(o.x, o.y, t, r))
                for r in rr for t in rt])

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
    count = reader.read(config, "count")
    a = shape.ShapePath(shap, count.get())

    def do_it(s):
        p = a.next()
        if p is not None:
            s.set_position(p.x, p.y)
        return s
    return apply_recursive(config, base, do_it)


def spread_f(config, base):
    o = read_point(config, 'origo')
    fx = reader.read(config, "f")
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
    vals = {key: reader.read(config, key) for key in params}
    fx = reader.read(config, "f")

    def do_it(s):
        args = {key: v.get() for key, v in vals.items()}
        p = fx(s, **args)
        s.set_position(p.x + o.x, p.y + o.y)
        return s
    return apply_recursive(config, base, do_it)


def spread_polar(config, base):
    """base is a list of shapes, they are spread"""
    o = read_point(config, 'origo')
    rr = reader.read(config, "r")
    rt = reader.read(config, "t")
#    r = rr.get()
#    t = rt.get()
#    x = r * math.cos(t)
#    y = r * math.sin(t)

    def do_it(shap):
        r = rr.get()
        t = rt.get()
        x = r * math.cos(t)
        y = r * math.sin(t)
        print("polar", rr)
        if isinstance(shap, shape.List):
            for s in shap:
                apply_recursive(config, s, do_it)
            return
        shap.set_position(x + o.x, y + o.y)
        return shap

#    recur(base)
    apply_recursive(config, base, do_it)
    return base


def spread(config, base):
    """base is a list of shapes, they are spread"""
    rx = reader.read(config, "x")
    ry = reader.read(config, "y")
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

def set_appearance_colour(config, shap, colour):
    if isinstance(shap, shape.Shape):
        c = colour.get().str()
        shap.appearance.colour = c
    else:
        for s in shap.shapes:
            if isinstance(colour, value.List):
                c = colour.get()
            else:
                c = colour
            set_appearance_colour(config, s, c)
        c.reset()


def set_appearance(config, shap, opacity, stroke, strokew, shad, blur):
    """Set appearance of a shape"""
    if isinstance(shap, shape.List):
        opacity.reset()
        stroke.reset()
        strokew.reset()
        for inner_shape in shap.shapes:
            set_appearance(config, inner_shape,
                           opacity, stroke, strokew, shad, blur)
        return
    shap.appearance.set(opacity.get(),
                        stroke.get(), strokew.get(), shad, blur)

# ===========================================================================


def appearance(config, base):
    """appearance algorithm"""
    opacity = reader.read(config, 'opacity', d=1.0)
    colour = reader.read_colour(config, 'colours')
    stroke = reader.read(config, 'stroke', d="none")
    strokew = reader.read(config, 'strokeWidth', d=0)
    shad = config.get('shadow', False)
    blur = config.get('blur', False)

    def pit(col):
        if isinstance(col, value.List):
            for c in col:
                pit(c)
            return
        print(col)
#    pit(colour)
    set_appearance_colour(config, base, colour)
    set_appearance(config, base, opacity, stroke, strokew, shad, blur)
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
        return tear.generate_shape(base, params)
    print(f"tearing shapes;count={len(base.shapes)}", end='', flush=True)
    shapes = []
    for b in base.shapes:
        print(".", end='', flush=True)
        s = tear.generate_shape(b, params)
        if s is not None:
            shapes.append(s)
    print('')
    return shape.List(shapes)

# ===========================================================================


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
        a = math.degrees(ang)
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


def clip(r, base):
    path = r.get('shape')
    clipid = forms.add_clip(path)

    def do_it(s):
        if isinstance(s, shape.List):
            if isinstance(s.shapes[0], shape.List):
                for ss in s:
                    do_it(ss)
            else:
                s.appearance.clip = clipid
        else:
            s.appearance.clip = clipid
    do_it(base)
    return base
#    return apply_recursive(r, base, do_it)


algorithms = {
    "position": position,
    "generate": generate,
    "spread": spread,
    "spread-area": spread_area,
    "spread-path": spread_path,
    "spread-polar": spread_polar,
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
    "voronoi-b": b_voronoi,
    "clip": clip
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
