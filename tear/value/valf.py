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
from tear import goldenratio


class Eval:
    def __init__(self, f):
        self.f = f
        self.i = 0
        self.last = None

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        return self.next

    @property
    def current(self):
        return self.last

    @property
    def next(self):
        self.last = eval(self.f.format(self.i))
        self.i += 1
        return self.last

    def reset(self):
        self.i = 0


class Function:
    """Function object. Get the actual callable by evaluating f"""

    def __init__(self, f, kwargs):
        self.f = eval(f)
        self.kwargs = kwargs

    def __call__(self, **kwargs):
        # get values for the arguments
        args = {key: v.next for key, v in self.kwargs.items()}
        args.update(kwargs)
        return self.f(**args)


class Class:
    def __init__(self, s):
        self.obj = eval(s)

    @property
    def next(self):
        return self.obj()


class Series:
    def __init__(self, s):
        self.obj = eval(s)

    @property
    def next(self):
        return self.obj.next
