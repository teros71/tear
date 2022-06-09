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

import math
from tear.value import ev


class Function:
    """Function object. Get the actual callable by evaluating f"""

    def __init__(self, f, kwargs):
        self.f = ev.evaluate(f)
        self.kwargs = kwargs

    def __call__(self, **kwargs):
        # get values for the arguments
        args = {key: v.next for key, v in self.kwargs.items()}
        args.update(kwargs)
        return self.f(**args)


def triangular():
    n = 0
    while True:
        n += 1
        yield n * (n + 1) / 2


def inverse_triangular():
    n = 0
    while True:
        n += 1
        yield math.floor(math.sqrt(2 * n) + 0.5)


class Class:
    def __init__(self, s):
        self.obj = eval(s)

    @property
    def next(self):
        return self.obj()
