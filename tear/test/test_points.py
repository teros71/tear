"""Value tests"""

import math
import itertools

from tear.value import value, reader, points


data = {
    "p1": [10,20],
    "p2": "10,20",
    "p3": {"x": 10, "y": 20},
    "p4": {"origo":[10,20],"t":0.0,"r":10},
    "p5": {"origo":[30,20],"t":"$(math.pi)","r":10},
    "p6": {"origo":[20,10],"t":"$(math.pi/2)","r":10},
    "trps": "u:points.Relative(points.read([100,100]),10,10,value.lst(points.triangular_matrix(5)))",
    "cpr": {"x": "10:20:1", "y": "20:40:2"},
    "ppr": {"origo":[10,20],"t": "0.0:$(math.pi)/10", "r": "10:20:1"}
}


def test_basic():
    """test basic types"""
    for i in range(1, 4):
        p = points.read(data, f'p{i}')
#        assert isinstance(p, points.Cartesian)
        v = next(p)
        assert v.x == 10
        assert v.y == 20
    for i in range(4, 7):
        p = points.read(data, f'p{i}')
#        assert isinstance(p, points.Polar)
        v = next(p)
        assert v.x == 20
        assert v.y == 20


def test_iter():
    p = points.read(data, "cpr")
#    assert isinstance(p, points.Cartesian)
    print(list(itertools.islice(p, 10)))
    p = points.read(data, "ppr")
#    assert isinstance(p, points.Polar)
    print(list(itertools.islice(p, 10)))
    

def test_matrix():
    n = 5
    trm = points.triangular_matrix(n, 0)
    l = len(trm)
    assert l == (n * (n + 1) // 2)
    for i in range(l):
        item = i + 1 # start from 1 ->
        # y is row, which is inverse triangular of item number
        row = math.floor(math.sqrt(2 * item) + 0.5)
        prev_row = row - 1
        # x is item - triangular of previous row
        column = item - (prev_row * (prev_row + 1) // 2)
        assert trm[i].y == row - 1
        assert trm[i].x == column - 1

    trm = points.triangular_matrix(n)
    for p in trm:
        print(p)

    pp = reader.read(data, "trps")
    assert isinstance(pp, points.Relative)
    for i in range(len(pp.base)):
        print(pp.next)
