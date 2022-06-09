"""Value tests"""

import unittest
import math
import itertools

from tear.value import value, reader
from tear import goldenratio


data = {
    "iv1": 42,
    "iv2": "42",
    "fv1": 42.42,
    "fv2": "42.42",
    "sv1": "foo",
    "sv2": "bar",
    "r1": "10:100",
    "r2": "10:100:10",
    "r3": "10:100/10",
    "r4": "2.0:4.2:0.2",
    "r5": "42:2/4",
    "ran1": "?:2:5",
    "ran2": "?:1,2,42",
    "ran3": "?:0.1:0.9",
    "list1": "foo,bar,42,car",
    "per1": "$(0.1*42):$(0.5*42)"
}

def test_basic():
    """test basic types"""
    # ints
    v1 = reader.read(data, "iv1")
    assert isinstance(next(v1), int)
    assert next(v1) == 42
    assert next(v1) == 42
    v2 = reader.read(data, "iv2")
    assert isinstance(next(v2), int)
    assert next(v1) == next(v2)
    # floats
    v1 = reader.read(data, "fv1")
    assert isinstance(next(v1), float)
    assert next(v1) == 42.42
    assert next(v1) == 42.42
    v2 = reader.read(data, "fv2")
    assert isinstance(next(v2), float)
    assert next(v1) == next(v2)

    v1 = reader.read(data, "sv1")
    assert isinstance(next(v1), str)
    assert next(v1) == "foo"
    assert next(v1) != next(reader.read(data, "sv2"))


def test_range():
    r = reader.read(data, "r1")
#    assert isinstance(r, value.Range)
#    assert r.min == 10
#    assert r.max == 100
#    assert r.step == 1
    assert next(r) == 10
#    assert r.current == 10
    assert next(r) == 11
    for _ in range(88):
        print(next(r))
#    assert r.current == 99
    assert next(r) == 10
    r = reader.read(data, "r2")
#    assert isinstance(r, value.Range)
#    assert r.min == 10
#    assert r.max == 100
#    assert r.step == 10
    assert next(r) == 10
    assert next(r) == 20
    for _ in range(7):
        print(next(r))
#    assert r.current == 90
    assert next(r) == 10
    r = reader.read(data, "r3")
#    assert isinstance(r, value.Range)
#    assert r.min == 10
#    assert r.max == 100
#    assert r.step == 9
    assert next(r) == 10
    r = reader.read(data, "r4")
#    assert isinstance(r, value.Range)
#    assert r.min == 2.0
#    assert r.max == 4.2
#    assert r.step == 0.2
    assert next(r) == 2.0
    assert next(r) == 2.2
    r = reader.read(data, "r5")
#    assert isinstance(r, value.Range)
#    assert r.min == 42
#    assert r.max == 2
#    assert r.step == -10
    assert next(r) == 42
    assert next(r) == 32


def test_random():
    v = reader.read(data, "ran1")
#    assert isinstance(v, value.Random)
    for _ in range(10):
        a = next(v)
        assert a <= 5
        assert a >= 2
#        assert v.current >= 2
    v = reader.read(data, "ran2")
    for _ in range(10):
        a = next(v)
        assert isinstance(a, int)
        assert a == 1 or a == 2 or a == 42
    v = reader.read(data, "ran3")
    for _ in range(10):
        a = next(v)
        assert a >= 0.1
        assert isinstance(a, float)
        assert a <= 0.9


def test_list():
    v = reader.read(data, "list1")
#    assert isinstance(v, value.List)
#    assert len(v) == 4
    assert next(v) == "foo"
    assert next(v) == "bar"
    assert next(v) == 42 # int!
    assert next(v) == "car"
    assert next(v) == "foo"


def test_percent():
    v = reader.read(data, "per1")
#    assert isinstance(v, value.Range)
#    assert v.min == 4.2
#    assert v.max == 21.0
#    assert v.step == 1.0
    assert next(v) == 4.2
    assert next(v) == 5.2


def test_simples():
    v = value.single(42)
    print(next(v))
    print(next(v))
    print(list(itertools.islice(v, 10)))
    v = value.lst([3, 2, 42, 64, 18])
    print(list(itertools.islice(v, 10)))
    print(next(v))
    print(next(v))
    print(next(v))
    v = value.irange(24, 42, 3)
    print(list(itertools.islice(v, 20)))
    v = value.irange(42, 24, -3)
    print(list(itertools.islice(v, 20)))
    v = value.arange(2.3, 4.2, 0.4)
    print(list(itertools.islice(v, 10)))
    v = value.arange(4.3, 1.2, -0.4)
    print(list(itertools.islice(v, 10)))
    v = value.arange(1, 10, 1)
    assert next(v) == 1
    assert next(v) != 1
    assert next(v) == 3
    v = value.arange(10, 1, -1)
    assert next(v) == 10
    assert next(v) != 10
    assert next(v) == 8

    v = value.random_seq(["foo", "bar", "yew", "blaa"])
    print(list(itertools.islice(v, 10)))
    v = value.random_irange(0, 42, 2)
    print(list(itertools.islice(v, 10)))
    v = value.random_arange(1.34, 2.3)
    print(list(itertools.islice(v, 10)))

    def my_value(a, b):
        return a + b

    v = value.value_source(my_value, value.single(42), value.lst([1, 2, 3]))
    assert next(v) == 43
    assert next(v) == 44
    assert next(v) == 45
    assert next(v) == 43


class TestValues(unittest.TestCase):
    """Test various value types"""

    def test_eval(self):
        v = reader.make("e:{0}*1.6")
#        self.assertIsInstance(v, Eval)
        print(list(itertools.islice(v, 5)))
        v = reader.make("e:{0}+math.fabs(math.sin((math.pi/8)*{0}))*20")
#        self.assertIsInstance(v, Eval)
        print(list(itertools.islice(v, 30)))

    def test_series(self):
        v = reader.make("u:goldenratio.Fibonacci()")
        #self.assertIsInstance(v, Series)
        self.assertIsInstance(v, goldenratio.Fibonacci)
        for _ in range(20):
            print(v.next)

    def test_evals(self):
        v = reader.make("42$(math.pi * 4)")
        self.assertEqual(next(v), 4200 + math.pi * 4)


if __name__ == '__main__':
    unittest.main()
