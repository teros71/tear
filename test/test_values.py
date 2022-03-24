import unittest
from value import value, reader
from value.valf import Series, Eval
import colours
import itertools
import goldenratio


class TestValues(unittest.TestCase):

    def test_range(self):
        r = reader.read(tf, "r1")
        self.assertIsNotNone(r)
        self.assertEqual(r.min, 10)
        self.assertEqual(r.max, 100)
        r = reader.read(tf, "r2")
        self.assertIsNotNone(r)
        self.assertEqual(r.min, 2.0)
        self.assertEqual(r.max, 4.2)
        r = reader.read(tf, "r3")
        self.assertIsNotNone(r)
        self.assertEqual(r.next, 42)
        self.assertEqual(r.current, 42)
        self.assertEqual(r.next, 32)
        self.assertEqual(r.current, 32)
        r = reader.read(tf, "r4")
        self.assertEqual(r.next, 42)
        self.assertEqual(r.current, 42)
        self.assertEqual(r.next, 44)
        self.assertEqual(r.next, 46)
        self.assertEqual(r.next, 42)
        self.assertEqual(r.current, 42)
        self.assertIsNotNone(r)

    def test_random(self):
        v = reader.make(42)
        self.assertIsInstance(v, value.Single)
        self.assertEqual(v.get(), 42)
        v = reader.make(1.2)
        self.assertIsInstance(v, value.Single)
        self.assertEqual(v.get(), 1.2)
        v = reader.make("42")
        self.assertIsInstance(v, value.Single)
        v = reader.make("?:2:5")
        self.assertIsInstance(v, value.Random)
        self.assertLessEqual(v.get(), 5)
        self.assertGreater(v.get(), 1)
        v = reader.make([1, 2, 42])
        self.assertIsInstance(v, value.List)
        self.assertEqual(len(v.lst), 3)
        print(list(itertools.islice(v, 5)))
        print(list(itertools.islice(v, 5)))
        v = reader.make(["foo1", "bar2", "42", "car"])
        self.assertIsInstance(v, value.List)
        self.assertEqual(len(v.lst), 4)
        print(list(itertools.islice(v, 5)))
        v = reader.make("?:%40%$W:%60%$W")
        self.assertIsInstance(v, value.Random)
        self.assertIsInstance(v.range, value.Range)
        self.assertIsInstance(v.range.min, float)

    def test_eval(self):
        v = reader.make("e:{0}*1.6")
        self.assertIsInstance(v, Eval)
        print(list(itertools.islice(v, 5)))
        v = reader.make("e:{0}+math.fabs(math.sin((math.pi/8)*{0}))*20")
        self.assertIsInstance(v, Eval)
        print(list(itertools.islice(v, 30)))

    def test_percent(self):
        v = reader.make("%42%100")
        self.assertEqual(v.next, 42)
        v = reader.make("%50%$W")
        self.assertEqual(v.next, 500.0)
        v = reader.make("%50%$H")
        self.assertEqual(v.next, 500.0)

    def test_series(self):
        v = reader.make("!:goldenratio.Fibonacci()")
        self.assertIsInstance(v, Series)
        self.assertIsInstance(v.obj, goldenratio.Fibonacci)
        for _ in range(20):
            print(v.next)


tf = {
    "r1": "10:100",
    "r2": "2.0:4.2",
    "r3": "42:2/4",
    "r4": "42:48:2",
    "base": "rectangle",
    "colours": [["red", "blue"], ["#0011ff:#ff0000"]],
    "recipe": [
        {
          "algorithm": "goldenRatioRectangles",
          "count": 9
        }
      ]
    }

if __name__ == '__main__':
    unittest.main()
