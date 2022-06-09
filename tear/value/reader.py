"""
Handling various forms of input values

Values are read from a dictionary. The resulting value objects are generic,
and the actual value is in the 'next' property of the object.
The value can also be a value object itself.


single number, int or float, can be native or string.
42, 42.42, "42", "57.434"

string: "foobar"

number range with optional step, int or float
"42:54[:1]", "0.42:42.4[:0.1]"
can also be from bigger to smaller: "66:14/2"
note that the end value is excluded.

linear range between: "42:54/5", "43.21:32.4/9"
the range is divided and step is calculated accordingly

random int: "?:42:54"
random float: "?:42.0:54.1"
random from list: "?:1,2,3,4"

basic lists:
[1, 2, 3]
"1, 2, 3"
the real list supports any value type, the string format supports only
int, float and string

Evaluation in place:
"$(math.pi * 4)" -> results a single float value


colour: "blue" or "#0000ff"
colour range list: "blue,red,green,yellow"
colour range: "#000000:#102030/10"
- note: needs the divider to specify range
random colour: "?:#2040ff:324590"

colour lists:
["blue,red", "#ffffff", "#023345:#aabd8f/10"]
complex range:
"#ff0000:#800000/4->#ff0080:#800080/4*30",
This makes a range from each colour of the first range to the corresponding
colour of the second range with *n steps.
It can be used to make color transition for multishapes.

x = integer
x.y = float
m:n[:s] = range between m-n with step s
m:n/s = range between m-n divided into s steps
?:m:n = random between m-n integers or floats
%x%value = x percents of a value
#rrggbb:#rrggbb/n = colour range
?:#rrggbb:#rrggbb = random colour
[x, y, z] = list
x,y,z = list (only numbers or strings or colours)
?:x,y,z = random from list



f:str = function where str is evaluated with parameter x (depending no the algorithm)

"""
import logging
from tear.colours import Colour, ColourRange
from tear.value import value
from tear.value.valf import Function
from tear.value import ev
from tear import pg
from tear.value.colours import read_single_colour


log = logging.getLogger(__name__)


def read(config, name, d=None):
    """read a generic value
    Args:
        config : dictionary from where to read
        name : name of the value
        d : default if not found
    Returns:
        value object which is one of:
        Single, Range, List, Random, Eval, Function or Series
    """
    v = config.get(name, d)
    if v is None:
        # not found and no default
        return None
    obj = make(v, config)
    return obj


def read_colour(config, name):
    """read a colour value
    Args:
        config : dictionary from where to read
        name : name of the value
    Returns:
        Colour or ColourRange or List
    """
    v = config.get(name, 'black')

    def read_col(c):
        if isinstance(c, str):
            if c.startswith('?:'):
                r = read_single_colour(c[2:])
                return value.random_colour(r.begin, r.end)
            r = read_single_colour(c)
            if isinstance(r, Colour):
                return value.single(r)
            return value.lst(r.range)
        if isinstance(c, list):
            return value.lst([read_col(s) for s in c])
        raise ValueError("invalid colour")
    return read_col(v)


def convert(obj):
    match obj:
        case float() | int():
            return obj
        case list():
            return convert_list(obj)
        case dict():
            return {key: convert(v) for key, v in obj.items()}
        case str():
            return convert_str(obj)
        case _:
            log.warning(f"WARNING: unknown value type {obj}")
            raise ValueError("WARNING: unknown value type", obj)


def convert_str(s):
    if ',' in s:
        lst = convert_list(s.split(','))
        return lst
    if ':' in s:
        lst = s.split(':')
        if len(lst) == 3:
            return tuple(convert_list(lst))
        if len(lst) != 2:
            raise ValueError("WARNING: invalid range syntax", s)
        if '/' in lst[1]:
            lst2 = lst[1].split('/')
            minv = convert_value(lst[0])
            maxv = convert_value(lst2[0])
            step = (maxv - minv) / convert_value(lst2[1])
            return minv, maxv, step
        return tuple(convert_list(lst))
    return convert_value(s)


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
        lst = [convert(x) for x in lst]
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




def make_from_list(obj, js):
    """Make a list of values from a list of whatever"""
    return value.lst([make(x, js) for x in obj])


def make_from_dict(obj, js):
    return {key: make(v, js) for key, v in obj.items()}


def substitute_variables(s):
    log.debug("substituting variables;str=%s", s)
    s = s.replace("$CX", str(pg.CENTER_X))
    s = s.replace("$CY", str(pg.CENTER_Y))
    s = s.replace("$W", str(pg.WIDTH))
    s = s.replace("$H", str(pg.HEIGHT))
    s = s.replace("$GRX0", str(pg.GR_X0))
    s = s.replace("$GRY0", str(pg.GR_Y0))
    s = s.replace("$GRX1", str(pg.GR_X1))
    s = s.replace("$GRY1", str(pg.GR_Y1))
    return s


def substitute_evaluations(s):
    i = s.find('$(')
    if i == -1:
        return s
    j = s.find(')', i)
    if j == -1:
        return s
    es = s[i:j+1]
    v = ev.evaluate(es[1:])
    s = s.replace(es, str(v))
    return substitute_evaluations(s)


def make_from_str(obj, js):
    """Make a value object from string"""
    # substitute variables
    if '$' in obj:
        obj = substitute_variables(obj)
    if '(' in obj:
        obj = substitute_evaluations(obj)
    # random value
    if obj.startswith('?:'):
        val = convert_str(obj[2:])
        if isinstance(val, list):
            return value.random_seq(val)
        if isinstance(val, tuple):
            if isinstance(val[0], int):
                return value.random_irange(*val)
            return value.random_arange(*val)
        # only one value
        return value.random_seq([val])
    # function
    if obj.startswith('f:'):
        args = make_from_dict(js.get("args", {}), js)
        return Function(obj[2:], args)
    # eval TODO: fix
    if obj.startswith('e:'):
        return ev.ev_source(obj[2:])
    if obj.startswith('u:'):
        return ev.evaluate(obj[2:])
    # percent
    if obj.startswith('%'):
        return value.single(read_percent_value(obj[1:]))
#    if obj.startswith('!:'):
#        return Series(obj[2:])
    # generic string
    val = convert_str(obj)
    if isinstance(val, list):
        return value.lst(val)
    if isinstance(val, tuple):
        return value.list2range(val)
    return value.single(val)


def make(obj, js=None):
    """make a generic value object"""
    if isinstance(obj, (float, int)):
        # float or int -> single value
        return value.single(obj)
    if isinstance(obj, list):
        # list -> list of whatever values
        return make_from_list(obj, js)
    if isinstance(obj, dict):
        # dict -> make a dictionary of whatever objects
        return make_from_dict(obj, js)
    if isinstance(obj, str):
        # str -> parse value from string
        return make_from_str(obj, js)
    log.warning(f"WARNING: unknown value type {obj}")
    raise ValueError("WARNING: unknown value type", obj)
#    return obj
