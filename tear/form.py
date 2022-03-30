"""Handle new shape generation according the instructions"""

import logging
from tear import algo
from tear.value import reader, points
from tear.model import store, shape
from tear.geometry import geom, path

log = logging.getLogger(__name__)


def make_generator_shape(config):
    """Make a new generator shape"""
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
        sp = points.read(config, "start")
        ep = points.read(config, "end")
        count = config.get("count")
        av = config.get("av")
        typ = config.get("curve")
        return shape.PathGenerator(typ, sp, ep, count, av)
    raise ValueError("unkown generator type", t)


def make_new_shape(r):
    """Make a new shape"""
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
        sp = points.read(r, "start")
        ep = points.read(r, "end")
        count = r.get("count")
        av = r.get("av")
        typ = r.get("curve")
        if typ == "cubic":
            base = path.random_path_quadratic(sp.next, ep.next, count, av, 2.0)
        else:
            base = path.random_path_cubic(sp.next, ep.next, count, av, 2.0)
    else:
        raise ValueError("new shape: unknown type")
    s = shape.Shape(base)
    s.set_position(x, y)
    log.info(f"new shape;type={t};x={x};y={y}")
    log.debug(f"shape={s}")
    return s


def apply_recipe(recipe, base):
    """Apply shape recipe"""
    for r in recipe:
        base = algo.apply_algorithm(r, base)
    return base


def generate_form(config):
    """Generate a new shape according to the config"""
    if config.get('disable', False):
        return
    name = config.get('name')
    create_shape(name, config)


def create_shape(name, config):
    """Create a new shape with the given name and config"""
    base_name = config.get('base')
    if base_name is None:
        base_name = config.get('template')
        if base_name is None:
            raise ValueError("no base for shape")
        conf = config.get('params')
        create_shape(name, store.get_template(base_name, conf))
        return
    base = None
    if base_name == 'generator':
        base = make_generator_shape(config)
    elif base_name == 'new':
        base = make_new_shape(config)
    else:
        log.info(f"\ngenerating form {name} from {base_name}")
        base = store.get_shape(base_name)
    new_form = apply_recipe(config.get('recipe', None), base)
    if isinstance(new_form, list):
        new_form = shape.List(new_form)
    store.add_shape(name, new_form)
