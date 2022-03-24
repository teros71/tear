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


class Cartesian:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last = geom.Point(x.current, y.current)

    @property
    def current(self):
        return self.last

    @property
    def next(self):
        self.last = geom.Point(self.x.next, self.y.next)
        return self.last

    def __repr__(self):
        return f'Cartesian[{self.x}, {self.y}]'


class Polar:
    """Wrapper for polar coordinate values to cartesian"""

    def __init__(self, origo, t, r):
        self.origo = origo
        self.t = t
        self.r = r
        o = origo.current
        self.last = geom.Point.fromtuple(
            geom.polar2cartesian(t.current, r.current, o.x, o.y))

    @property
    def current(self):
        return self.last

    @property
    def next(self):
        o = self.origo.next
        self.last = geom.Point.fromtuple(
            geom.polar2cartesian(self.t.next, self.r.next, o.x, o.y))
        return self.last
