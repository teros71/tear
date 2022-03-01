import unittest
import value
import itertools


class TestValues(unittest.TestCase):

    def test_range(self):
        r = value.readRange(tf, "r1")
        self.assertIsNotNone(r)
        self.assertEqual(r.min, 10)
        self.assertEqual(r.max, 100)
        r = value.readRange(tf, "r2")
        self.assertIsNotNone(r)
        self.assertEqual(r.min, 2.0)
        self.assertEqual(r.max, 4.2)

    def test_random(self):
        v = value.make(42)
        self.assertIsInstance(v, value.Single)
        self.assertEqual(v.__next__(), 42)
        v = value.make(1.2)
        self.assertIsInstance(v, value.Single)
        self.assertEqual(v.__next__(), 1.2)
        v = value.make("42")
        self.assertIsInstance(v, value.Single)
        v = value.make("2-5")
        self.assertIsInstance(v, value.Random)
        print(v.__next__())
        self.assertLessEqual(v.__next__(), 5)
        self.assertGreater(v.__next__(), 1)
        v = value.make([1, 2, 42])
        self.assertIsInstance(v, value.Round)
        self.assertEqual(len(v.lst), 3)
        print(list(itertools.islice(v, 5)))
        print(list(itertools.islice(v, 5)))
        v = value.make(["foo1", "bar2", "42", "car"])
        self.assertIsInstance(v, value.Round)
        self.assertEqual(len(v.lst), 4)
        print(list(itertools.islice(v, 5)))

    def test_eval(self):
        v = value.make("1.0@{0}*1.6")
        self.assertIsInstance(v, value.Eval)
        self.assertEqual(v.x, 1.0)
        print(list(itertools.islice(v, 5)))
        v = value.make("20.0@{0}+math.fabs(math.sin((math.pi/8)*{1}))*20")
        self.assertIsInstance(v, value.Eval)
        print(list(itertools.islice(v, 30)))


tf = {
    "r1": "10-100",
    "r2": "2.0-4.2",
    "base": "rectangle",
    "recipe": [
        {
          "algorithm": "goldenRatioRectangles",
          "count": 9
        }
      ]
    }

if __name__ == '__main__':
    unittest.main()
