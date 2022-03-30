"""
Geometry related value types

Returning points:
cartesian : x, y
polar : origo, t, r
coordinate matrix : cart: y * x polar: (origo, r) * t
positional matrix : y * x
function : n => x,y
relative: origo, fx, fy applied to base

triangular: n*(n+1)/2
to make pyramid, base:
n => x: n, y: floor(sqrt(2n) + 1/2)
inverse of triangular number: floor(sqrt(2n) + 1/2)
+
positional with moving origo...

Relative with Cartesian with x: e:{0}+1  y: u:InverseTriangular()

field matrix: x: "1:n" y: "10"

x = n - m*(m+1)/2
where m = floor(sqrt(2n) + 1/2) - 1
i.e. x = n - triangular(inverseTriangular(n)-1)

"""
from tear.geometry import geom
from tear.value import value, reader
from tear.model import store
from tear.model.shape import Path


class Cartesian:
    """Cartesian points, defined by x and y"""

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
    """Polar points defined by origo, t and r"""

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


class Relative:
    """Relative points defined by origo and factors xf and yf
    applied to base points
    """

    def __init__(self, origo, fx, fy, base):
        self.origo = origo
        self.fx = fx
        self.fy = fy
        self.base = base

    @property
    def next(self):
        p = self.base.next
        o = self.origo.next
        return geom.Point(o.x + (p.x * self.fx), o.y + (p.y * self.fy))


def triangular_matrix(n, add=-0.5):
    """Simple list of triangular positions"""
    return value.List([geom.Point(x+(y-1)*add, y-1) for y in range(n+1) for x in range(y)])


# functions to read points from dict

def read_point_data(p):
    if isinstance(p, str):
        p = p.split(',')
    if not isinstance(p, list) or len(p) != 2:
        raise ValueError("invalid point")
    x = reader.make(p[0])
    y = reader.make(p[1])
    return Cartesian(x, y)


def read_cartesian(config, name=None):
    if name is not None:
        config = config.get(name)
    if config is None:
        return None
    if isinstance(config, dict):
        vx = reader.read(config, 'x')
        if vx is None:
            return None
        vy = reader.read(config, 'y')
        if vy is None:
            return None
        return Cartesian(vx, vy)
    return read_point_data(config)


def read_polar(config):
    origo = read_cartesian(config, 'origo')
    if origo is None:
        return None
    t = reader.read(config, 't')
    if t is None:
        return None
    r = reader.read(config, 'r')
    if r is None:
        return None
    return Polar(origo, t, r)


def read_path(config):
    name = config.get("path")
    if name is None:
        return None
    count = config.get("count", 1)
    shap = store.get_shape(name)
    return Path.fromshape(shap, float(count))


def read(config, name=None):
    """read point value
    Args:
        config : dictionary
        name : optional name of a dictionary containing the value data

    If name is omitted, data is read from the given config directly.
    Data is either for cartesian coordinates:
        "x": value
        "y": value
        or
        [x, y]
        or
        "x, y"
    or for polar coordinates:
        "origo": <cartesian point as dictionary or data>
        "t": value for angle
        "r": value for distance
    or for path:
        "path": <shape name>
        "count": how many steps on path

    Returns:
        Cartesian or Polar value object
    """
    if name is not None:
        config = config.get(name)
    if config is None:
        return None
    p = read_cartesian(config, None)
    if p is None:
        p = read_polar(config)
    if p is None:
        p = read_path(config)
    if p is None:
        raise ValueError("invalid point")
    return p
