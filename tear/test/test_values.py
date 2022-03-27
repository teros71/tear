"""Value tests"""

import unittest
import math
import itertools

from tear.value import value, reader
from tear.value.ev import Eval
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
    assert isinstance(v1, value.Single)
    assert isinstance(v1.next, int)
    assert v1.next == 42
    assert v1.next == 42
    v2 = reader.read(data, "iv2")
    assert isinstance(v2, value.Single)
    assert v1.next == v2.next
    # floats
    v1 = reader.read(data, "fv1")
    assert isinstance(v1, value.Single)
    assert isinstance(v1.next, float)
    assert v1.next == 42.42
    assert v1.next == 42.42
    v2 = reader.read(data, "fv2")
    assert isinstance(v2, value.Single)
    assert v1.next == v2.next

    v1 = reader.read(data, "sv1")
    assert isinstance(v1, value.Single)
    assert isinstance(v1.next, str)
    assert v1.next == "foo"
    assert v1.next != reader.read(data, "sv2").next


def test_range():
    r = reader.read(data, "r1")
    assert isinstance(r, value.Range)
    assert r.min == 10
    assert r.max == 100
    assert r.step == 1
    assert r.next == 10
    assert r.current == 10
    assert r.next == 11
    for _ in range(88):
        print(r.next)
    assert r.current == 99
    assert r.next == 10
    r = reader.read(data, "r2")
    assert isinstance(r, value.Range)
    assert r.min == 10
    assert r.max == 100
    assert r.step == 10
    assert r.next == 10
    assert r.next == 20
    for _ in range(7):
        print(r.next)
    assert r.current == 90
    assert r.next == 10
    r = reader.read(data, "r3")
    assert isinstance(r, value.Range)
    assert r.min == 10
    assert r.max == 100
    assert r.step == 9
    assert r.next == 10
    r = reader.read(data, "r4")
    assert isinstance(r, value.Range)
    assert r.min == 2.0
    assert r.max == 4.2
    assert r.step == 0.2
    assert r.next == 2.0
    assert r.next == 2.2
    r = reader.read(data, "r5")
    assert isinstance(r, value.Range)
    assert r.min == 42
    assert r.max == 2
    assert r.step == -10
    assert r.next == 42
    assert r.next == 32


def test_random():
    v = reader.read(data, "ran1")
    assert isinstance(v, value.Random)
    for _ in range(10):
        assert v.next <= 5
        assert v.current >= 2
    v = reader.read(data, "ran2")
    for _ in range(10):
        a = v.next
        assert isinstance(a, int)
        assert a == 1 or a == 2 or a == 42
    v = reader.read(data, "ran3")
    for _ in range(10):
        assert v.next >= 0.1
        assert isinstance(v.current, float)
        assert v.current <= 0.9


def test_list():
    v = reader.read(data, "list1")
    assert isinstance(v, value.List)
    assert len(v) == 4
    assert v.next == "foo"
    assert v.next == "bar"
    assert v.next == 42 # int!
    assert v.next == "car"
    assert v.next == "foo"


def test_percent():
    v = reader.read(data, "per1")
    assert isinstance(v, value.Range)
    assert v.min == 4.2
    assert v.max == 21.0
    assert v.step == 1.0
    assert v.next == 4.2
    assert v.next == 5.2


class TestValues(unittest.TestCase):
    """Test various value types"""

    def test_eval(self):
        v = reader.make("e:{0}*1.6")
        self.assertIsInstance(v, Eval)
        print(list(itertools.islice(v, 5)))
        v = reader.make("e:{0}+math.fabs(math.sin((math.pi/8)*{0}))*20")
        self.assertIsInstance(v, Eval)
        print(list(itertools.islice(v, 30)))

    def test_series(self):
        v = reader.make("u:goldenratio.Fibonacci()")
        #self.assertIsInstance(v, Series)
        self.assertIsInstance(v, goldenratio.Fibonacci)
        for _ in range(20):
            print(v.next)

    def test_evals(self):
        v = reader.make("42$(math.pi * 4)")
        self.assertEqual(v.next, 4200 + math.pi * 4)


if __name__ == '__main__':
    unittest.main()
