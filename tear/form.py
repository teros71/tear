"""Handle new shape generation according the instructions"""

import logging
from tear import algo
from tear.value import reader, points
from tear.model import store, shape
from tear.geometry import geom, path

log = logging.getLogger(__name__)


def generate_form(config):
    """Generate a new shape according to the config"""
    if config.get('disable', False):
        return
    name = config.get('name')
    shap = create_shape(config)
    store.add_shape(name, shap)


def create_shape(config):
    """Create a new shape based on config"""
    base = get_base_shape(config)
    if base is None:
        raise ValueError("no base for shape")
    recipe = config.get('recipe')
    if recipe is not None:
        new_form = apply_recipe(recipe, base)
    else:
        new_form = base
    if isinstance(new_form, list):
        new_form = shape.List(new_form)
    return new_form


def get_base_shape(config):
    """Get base shape for a new shape"""
    base_name = config.get('base')
    if base_name is not None:
        log.info("base shape;name=%s", base_name)
        return store.get_shape(base_name)
    base_name = config.get('generator')
    if base_name is not None:
        log.info("generator shape;type=%s", base_name)
        return make_generator_shape(base_name, config)
    base_name = config.get('new')
    if base_name is not None:
        log.info("new shape;type=%s", base_name)
        return make_new_shape(base_name, config)
    base_name = config.get('template')
    if base_name is not None:
        log.info("from template;name=%s", base_name)
        conf = config.get('params')
        return create_shape(store.get_template(base_name, conf))
    return None


def make_generator_shape(t, config):
    """Make a new generator shape"""
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


def make_new_shape(t, r):
    """Make a new shape"""
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
