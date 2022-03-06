import shape
import value
import algo
import forms
import geom


def make_generator_shape(config):
    t = config.get('type', 'rectangle')
    if t == 'rectangle':
        rw = value.read(config, "rangeW")
        rh = value.read(config, "rangeH")
        return shape.RectGenerator(rw, rh)
    if t == 'circle':
        rr = value.read(config, "rangeR")
        return shape.CircleGenerator(rr)
    if t == 'polygon':
        rar = value.readRange(config, "rangeR")
        rap = value.read(config, "rangePoints")
        return shape.PolygonGenerator(rar, rap)


def make_new_shape(r):
    t = r.get('type', 'rectangle')
    x = r.get("x", 0.0)
    y = r.get("y", 0.0)
    base = None
    if t == 'rectangle':
        base = geom.Rect(r.get("width", 10.0), r.get("height", 10.0))
    if t == 'circle':
        base = geom.Circle(r.get("r", 10.0))
    if t == 'polygon':
        base = geom.Polygon.fromstr(
            r.get("points", "0.0 0.0, 10.0 5.0, 5.0 10.0"))
    s = shape.Shape(base)
    s.set_position(x, y)
    return s


def apply_recipe(recipe, base):
    for r in recipe:
        base = algo.apply_algorithm(r, base)
    return base


def generate_form(config):
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
