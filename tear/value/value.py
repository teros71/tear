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
from tear import pg, goldenratio
from tear.colours import Colour, ColourRange


def final(val):
    """Return the actual value
    Useful in case of hierarchical value object
    """
    if hasattr(val, 'next'):
        return final(val.next)
    return val


class Single:
    """Single value, always returns the same"""

    def __init__(self, value):
        self.value = value
        self.v = True

    def __iter__(self):
        self.v = True
        return self

    def __next__(self):
        if self.v:
            self.v = False
            return self.value
        raise StopIteration

    @property
    def current(self):
        return self.value

    @property
    def next(self):
        return self.value

    def reset(self):
        self.v = True


class List:
    """List value
    The list can be iterated in the usual fashion,
    but the next property works like a circular buffer and always returns
    a valid item.
    current is the last returned item, or if none yet, then the last item
    on the list"""

    def __init__(self, lst):
        self.lst = lst
        self.i = 0
        self.exhausted = False

    def __iter__(self):
        self.i = 0
        self.exhausted = False
        return self

    def __next__(self):
        if self.exhausted:
            raise StopIteration
        if self.i == len(self.lst) - 1:
            self.exhausted = True
        return self.next

    def __getitem__(self, item):
        return self.lst[item]

    @property
    def current(self):
        return self.lst[self.i - 1]

    @property
    def next(self):
        v = self.lst[self.i]
        self.i = (self.i + 1) % len(self.lst)
        return v

    def reset(self):
        self.i = 0


class Range:
    """Range value, returns next according to the step"""

    def __init__(self, min_v, max_v, step):
        self.min = min_v
        self.max = max_v
        self.step = step
        self._current = self.min
        self.last = self.max

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        if self.step >= 0:
            if self._current >= self.max:
                raise StopIteration
        elif self._current <= self.max:
            raise StopIteration
        return self.next

    @property
    def current(self):
        return self.last

    @property
    def next(self):
        if self.step >= 0:
            if self._current >= self.max:
                self._current = self.min
        elif self._current <= self.max:
            self._current = self.min
        self.last = self._current
        self._current += self.step
        return self.last

    def reset(self):
        self._current = self.min
        self.last = self.max

    def __repr__(self):
        return f'Range[{self.min},{self.max},{self.step},{self._current}]'

    @classmethod
    def fromlist(cls, lst):
        print("range", lst)
        if len(lst) > 2:
            return cls(lst[0], lst[1], lst[2])
        return cls(lst[0], lst[1], 1)


class Random:
    """Random value based either on a list or a range"""

    def __init__(self, range):
        self.range = range
        self.method = 0
        self.last = None

    def __iter__(self):
        return self

    def __next__(self):
        return self.next

    @property
    def current(self):
        return self.last

    @property
    def next(self):
        if isinstance(self.range, list):
            i = random.randint(0, len(self.range) - 1)
            self.last = self.range[i]
        elif isinstance(self.range, ColourRange):
            self.last = self.range.random()
        elif isinstance(self.range.min, float):
            self.last = random.uniform(self.range.min, self.range.max)
        elif isinstance(self.range.min, int):
            self.last = random.randint(self.range.min, self.range.max)
        else:
            self.last = self.range.random()
        return self.last

    def reset(self):
        pass
