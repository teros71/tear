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
import random
from tear.colours import random_between


def final(val):
    """Return the actual value
    Useful in case of hierarchical value object
    """
    if hasattr(val, 'next'):
        return final(val.next)
    return val


def single(value):
    while True:
        yield value


def lst(values):
    while True:
        for v in values:
            msg = yield v
            if msg:
                yield
                break


def irange(minv, maxv, step):
    while True:
        for v in range(minv, maxv, step):
            msg = yield v
            if msg:
                yield
                break


def arange(minv, maxv, step):
    current = minv
    while True:
        if step >= 0:
            if current >= maxv:
                current = minv
        elif current <= maxv:
            current = minv
        msg = yield current
        if msg:
            current = minv
            yield
        else:
            current += step


def list2range(lst):
    if len(lst) > 2:
        return arange(lst[0], lst[1], lst[2])
    return arange(lst[0], lst[1], 1)


def random_seq(seq):
    while True:
        yield random.choice(seq)


def random_irange(minv, maxv, step=1):
    while True:
        yield random.randrange(minv, maxv, step)


def random_arange(minv, maxv):
    while True:
        yield random.uniform(minv, maxv)


def random_colour(begin, end):
    while True:
        yield random_between(begin, end)


def value_source(func, *args):
    while True:
        nargs = tuple(next(a) for a in args)
        msg = yield func(*nargs)
        if msg:
            for a in args:
                a.send('reset')


def xreset(val):
    try:
        val.send(True)
    except TypeError:
        pass

