"""
Handling various forms of input values
single number (int or float): 42 or 42.42
string: "foobar"
number range with optional step, int or float: "42:54[:1]", "0.42:42.4[:0.1]"
linear range between: "42:54/5"

random int: "?:42:54"
random float: "?:42.0:54.1"
random from list: "?:1,2,3,4"

colour: "blue" or "#0000ff"
colour range: "c:#000000:#102030/10"

x = integer
x.y = float
?:m:n = random between m-n integers or floats
m:n:s = range between m-n with step s
m:n/s = range between m-n divided into s steps
%x%value = x percents of a value
c:#rrggbb:#rrggbb/n = colour range
[x, y, z] = list
f:str = function where str is evaluated with parameter x (depending no the algorithm)

"""
from geometry import geom
import pg
import goldenratio
from colours import Colour, ColourRange
from value.value import Single, Range, Random, List
from value.valg import Polar, Cartesian
from value.valf import Function, Eval, Series


def isfloat(num):
    """can convert to float?"""
    try:
        float(num)
        return True
    except ValueError:
        return False


def isint(num):
    """can convert to int?"""
    try:
        int(num)
        return True
    except ValueError:
        return False


def convert_list(lst):
    """convert a list of values"""
    if isint(lst[0]):
        lst = [int(x) for x in lst]
    elif isfloat(lst[0]):
        lst = [float(x) for x in lst]
    else:
        lst = [convert_value(x) for x in lst]
    return lst


def convert_value(val):
    """convert value"""
    if isint(val):
        return int(val)
    if isfloat(val):
        return float(val)
    if isinstance(val, str) and val.startswith('%'):
        return read_percent_value(val[1:])
    return val


def read_percent_value(s):
    """read percentual value, assumes float"""
    ls = s.split('%')
    v = convert_value(ls[1])
    return (float(ls[0]) / 100) * v


def read_str_value(s):
    if ',' in s:
        lst = convert_list(s.split(','))
        return List(lst)
    if ':' in s:
        lst = s.split(':')
        if len(lst) == 3:
            return Range.fromlist(convert_list(lst))
        if len(lst) != 2:
            raise ValueError("WARNING: invalid range syntax", s)
        if '/' in lst[1]:
            lst2 = lst[1].split('/')
            minv = convert_value(lst[0])
            maxv = convert_value(lst2[0])
            step = (maxv - minv) / convert_value(lst2[1])
            return Range(minv, maxv, step)
        return Range.fromlist(convert_list(lst))
    return Single(convert_value(s))


def read_colour_transition(s):
    ran = s.split('->')
    rc = ran[1].split('*')
    from_c = read_single_colour(ran[0])
    to_c = read_single_colour(rc[0])
    count = int(rc[1])
    return List(ColourRange.fromranges(from_c, to_c, count))


def read_single_colour(s):
    if '->' in s:
        return read_colour_transition(s)
    if s.startswith('?:'):
        return Random(read_single_colour(s[2:]))
    if ',' in s:
        lst = s.split(',')
        return ColourRange.fromlist([Colour.fromstr(c) for c in lst])
    if ':' in s:
        lst = s.split(':')
        if len(lst) != 2:
            raise ValueError("invalid colour")
        if '/' in lst[1]:
            lst2 = lst[1].split('/')
            return ColourRange(Colour.fromstr(lst[0]), Colour.fromstr(lst2[0]), int(lst2[1]))
        return ColourRange(Colour(lst[0]), Colour(lst[1]), 0)
    return Colour.fromstr(s)


def read_colour(js, name):
    v = js.get(name, 'black')

    def read_col(c):
        if isinstance(c, str):
            return read_single_colour(c)
        if isinstance(c, list):
            return List([read_col(s) for s in c])
        raise ValueError("invalid colour")
    return read_col(v)


def read(js, name, d=None):
    v = js.get(name, d)
    obj = make(v, js)
    return obj


def make_from_list(obj, js):
    return List([make(x, js) for x in obj])


def make_from_dict(obj, js):
    return {key: make(v, js) for key, v in obj.items()}


def substitute_variables(s):
    s = s.replace("$CX", str(pg.CENTER_X))
    s = s.replace("$CY", str(pg.CENTER_Y))
    s = s.replace("$W", str(pg.WIDTH))
    s = s.replace("$H", str(pg.HEIGHT))
    s = s.replace("$GRX0", str(pg.GR_X0))
    s = s.replace("$GRY0", str(pg.GR_Y0))
    s = s.replace("$GRX1", str(pg.GR_X1))
    s = s.replace("$GRY1", str(pg.GR_Y1))
    return s


def make_from_str(obj, js):
    # substitute variables
    if '$' in obj:
        obj = substitute_variables(obj)
    # random value
    if obj.startswith('?:'):
        val = read_str_value(obj[2:])
        if isinstance(val, List):
            return Random(val.lst)
        if isinstance(val, Range):
            return Random(val)
        return Random([val.value])
    # function
    if obj.startswith('f:'):
        args = make_from_dict(js.get("args", {}), js)
        return Function(obj[2:], args)
    # eval TODO: fix
    if obj.startswith('e:'):
        return Eval(obj[2:])
    if obj.startswith('u:'):
        return eval(obj[2:])
    # percent
    if obj.startswith('%'):
        return Single(read_percent_value(obj[1:]))
    if obj.startswith('!:'):
        return Series(obj[2:])
    # generic string
    return read_str_value(obj)


def make(obj, js=None):
    """make a generic value object"""
    if isinstance(obj, (float, int)):
        return Single(obj)
    if isinstance(obj, list):
        return make_from_list(obj, js)
    if isinstance(obj, str):
        return make_from_str(obj, js)
    if isinstance(obj, dict):
        return make_from_dict(obj, js)
    print("WARNING: unknown value type", obj)
    return obj


# read geometrical data


def read_point_data(p):
    if isinstance(p, str):
        p = p.split(',')
    if not isinstance(p, list) or len(p) != 2:
        raise ValueError("invalid point")
    x = make(p[0])
    y = make(p[1])
    return Cartesian(x, y)


def read_cartesian(config, name=None):
    if name is not None:
        config = config.get(name)
    if config is None:
        return None
    if isinstance(config, dict):
        vx = read(config, 'x')
        if vx is None:
            return None
        vy = read(config, 'y')
        if vy is None:
            return None
        return Cartesian(vx, vy)
    return read_point_data(config)


def read_polar(config):
    origo = read_cartesian(config, 'origo')
    if origo is None:
        return None
    t = read(config, 't')
    if t is None:
        return None
    r = read(config, 'r')
    if r is None:
        return None
    return Polar(origo, t, r)


def read_point(config, name=None):
    if name is not None:
        config = config.get(name)
    if config is None:
        return None
    p = read_cartesian(config, None)
    if p is None:
        p = read_polar(config)
    if p is None:
        raise ValueError("invalid point")
    return p
