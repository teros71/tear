import shape
import polygon
import value
import algo
import forms


def make_generator_form(config):
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
        return polygon.Generator(rar, rap)


def make_new_form(r):
    t = r.get('type', 'rectangle')
    x = r.get("x", 0.0)
    y = r.get("y", 0.0)
    if t == 'rectangle':
        return shape.Rect(x, y, r.get("width", 10.0), r.get("height", 10.0))
    if t == 'circle':
        return shape.Circle(x, y, r.get("r", 10.0))
    if t == 'polygon':
        p = polygon.Polygon.fromstr(
            r.get("points", "0.0 0.0, 10.0 5.0, 5.0 10.0"))
        return p


def apply_recipe(recipe, base):
    for r in recipe:
        base = algo.applyAlgorithm(r, base)
    return base


def generate_form(config):
    name = config.get('name')
    base_name = config['base']
    base = None
    if base_name == 'generator':
        base = make_generator_form(config)
    elif base_name == 'new':
        base = make_new_form(config)
    else:
        print("generating form {0} from {1}".format(name, base_name))
        base = forms.get(base_name)
    new_form = apply_recipe(config.get('recipe', None), base)
    forms.add(name, new_form)
