import shape
from value import reader
import algo
import forms
from geometry import geom, path


def make_generator_shape(config):
    t = config.get('type', 'rectangle')
    if t == 'rectangle':
        rw = reader.read(config, "w")
        rh = reader.read(config, "h")
        return shape.RectGenerator(rw, rh)
    if t == 'circle':
        rr = reader.read(config, "r")
        return shape.CircleGenerator(rr)
    if t == 'ellipse':
        rx = reader.read(config, "rx")
        ry = reader.read(config, "ry")
        return shape.EllipseGenerator(rx, ry)
    if t == 'polygon':
        rar = reader.read(config, "r")
        rap = reader.read(config, "c")
        return shape.PolygonGenerator(rar, rap)
    if t == 'path':
        sp = reader.read_point(config, "start")
        ep = reader.read_point(config, "end")
        count = config.get("count")
        av = config.get("av")
        return shape.PathGenerator(sp, ep, count, av)


def make_new_shape(r):
    t = r.get('type', 'rectangle')
    x = r.get("x", 0.0)
    y = r.get("y", 0.0)
    base = None
    if t == 'rectangle':
        base = geom.Rect(r.get("w", 10.0), r.get("h", 10.0))
    elif t == 'circle':
        base = geom.Circle(r.get("r", 10.0))
    elif t == 'ellipse':
        base = geom.Ellipse(r.get("rx", 20.0), r.get("ry", 10.0))
    elif t == 'polygon':
        base = geom.Polygon.fromstr(
            r.get("points", "0.0 0.0, 10.0 5.0, 5.0 10.0"))
    elif t == 'path':
        #        segs = r.get("segments")
        sp = reader.read_point(r, "start")
        ep = reader.read_point(r, "end")
        count = r.get("count")
        av = r.get("av")
        base = path.random_path(sp.next, ep.next, count, av, 2.0)
    else:
        raise ValueError("new shape: unknown type")
    s = shape.Shape(base)
    s.set_position(x, y)
    return s


def apply_recipe(recipe, base):
    for r in recipe:
        base = algo.apply_algorithm(r, base)
    return base


def generate_form(config):
    if config.get('disable', False):
        return
    name = config.get('name')
    base_name = config['base']
    base = None
    if base_name == 'generator':
        base = make_generator_shape(config)
    elif base_name == 'new':
        base = make_new_shape(config)
    else:
        print("\ngenerating form {0} from {1}".format(name, base_name))
        base = forms.get(base_name)
    new_form = apply_recipe(config.get('recipe', None), base)
    if isinstance(new_form, list):
        new_form = shape.List(new_form)
    forms.add(name, new_form)
