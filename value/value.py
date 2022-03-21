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
import random
import pg
import goldenratio
from colours import Colour, ColourRange


class Single:
    """Single value, always returns the same"""

    def __init__(self, value):
        self.value = value
        self.v = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.v:
            self.v = False
            return self.value
        raise StopIteration

    def get(self):
        return self.value

    def reset(self):
        self.v = True


class List:
    """List value, returns the next in the list"""

    def __init__(self, lst):
        self.lst = lst
        self.i = 0

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.lst):
            v = self.lst[self.i]
            self.i += 1
            return v
        raise StopIteration

    def __getitem__(self, item):
        return self.lst[item]

    def depth(self):
        return

    def get(self):
        if self.i >= len(self.lst):
            self.i = 0
        v = self.lst[self.i]
        self.i += 1
        return v

    def reset(self):
        self.i = 0


class Range:
    """Range value, returns next according to the step"""

    def __init__(self, min, max, step):
        self.min = min
        self.max = max
        self.step = step
        self.current = self.min

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        if self.current >= self.max:
            raise StopIteration
        return self.get()

    def get(self):
        if self.current >= self.max:
            self.current = self.min
        r = self.current
        self.current += self.step
        return r

    def reset(self):
        self.current = self.min

    @classmethod
    def fromlist(cls, lst):
        if len(lst) > 2:
            return cls(lst[0], lst[1], lst[2])
        return cls(lst[0], lst[1], 1)


class Random:
    """Random value based either on a list or a range"""

    def __init__(self, range):
        self.range = range
        self.method = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.get()

    def get(self):
        if isinstance(self.range, list):
            i = random.randint(0, len(self.range) - 1)
            return self.range[i]
        if isinstance(self.range, ColourRange):
            return self.range.random()
        if isinstance(self.range.min, float):
            return random.uniform(self.range.min, self.range.max)
        if isinstance(self.range.min, int):
            return random.randint(self.range.min, self.range.max)

    def reset(self):
        pass


class Eval:
    def __init__(self, f):
        self.f = f
        self.i = 0

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        return self.get()

    def get(self):
        v = eval(self.f.format(self.i))
        self.i += 1
        return v

    def reset(self):
        self.i = 0


class Function:
    """Function object. Get the actual callable by evaluating f"""

    def __init__(self, f, kwargs):
        self.f = eval(f)
        self.kwargs = kwargs

    def __call__(self, **kwargs):
        # get values for the arguments
        args = {key: v.get() for key, v in self.kwargs.items()}
        args.update(kwargs)
        return self.f(**args)


class Cartesian:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return self.x.get(), self.y.get()


class Polar:
    """Wrapper for polar coordinate values to cartesian"""

    def __init__(self, origo, t, r):
        self.origo = origo
        self.t = t
        self.r = r

    def get(self):
        t = self.t.get()
        r = self.r.get()
        x = r * math.cos(t)
        y = r * math.sin(t)
        return x + self.origo.x, y + self.origo.y


class Class:
    def __init__(self, s):
        self.obj = eval(s)

    def get(self):
        return self.obj()


class Series:
    def __init__(self, s):
        self.obj = eval(s)

    def get(self):
        return self.obj.get()
