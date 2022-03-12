import unittest
import value
import itertools


class TestValues(unittest.TestCase):

    def test_range(self):
        r = value.read(tf, "r1")
        self.assertIsNotNone(r)
        self.assertEqual(r.min, 10)
        self.assertEqual(r.max, 100)
        r = value.read(tf, "r2")
        self.assertIsNotNone(r)
        self.assertEqual(r.min, 2.0)
        self.assertEqual(r.max, 4.2)

    def test_random(self):
        v = value.make(42)
        self.assertIsInstance(v, value.Single)
        self.assertEqual(v.get(), 42)
        v = value.make(1.2)
        self.assertIsInstance(v, value.Single)
        self.assertEqual(v.get(), 1.2)
        v = value.make("42")
        self.assertIsInstance(v, value.Single)
        v = value.make("?:2:5")
        self.assertIsInstance(v, value.Random)
        print(v.get())
        self.assertLessEqual(v.get(), 5)
        self.assertGreater(v.get(), 1)
        v = value.make([1, 2, 42])
        self.assertIsInstance(v, value.List)
        self.assertEqual(len(v.lst), 3)
        print(list(itertools.islice(v, 5)))
        print(list(itertools.islice(v, 5)))
        v = value.make(["foo1", "bar2", "42", "car"])
        self.assertIsInstance(v, value.List)
        self.assertEqual(len(v.lst), 4)
        print(list(itertools.islice(v, 5)))
        v = value.make("?:%40%$W:%60%$W")
        self.assertIsInstance(v, value.Random)
        self.assertIsInstance(v.range, value.Range)
        self.assertIsInstance(v.range.min, float)

    def test_eval(self):
        v = value.make("e:1.0@{0}*1.6")
        self.assertIsInstance(v, value.Eval)
        self.assertEqual(v.x, 1.0)
        print(list(itertools.islice(v, 5)))
        v = value.make("e:20.0@{0}+math.fabs(math.sin((math.pi/8)*{1}))*20")
        self.assertIsInstance(v, value.Eval)
        print(list(itertools.islice(v, 30)))

    def test_percent(self):
        v = value.make("%42%100")
        self.assertEqual(v.get(), 42)
        v = value.make("%50%$W")
        self.assertEqual(v.get(), 500.0)
        v = value.make("%50%$H")
        self.assertEqual(v.get(), 500.0)

    def test_colours(self):
        c = value.Colour.fromstr("#4280ff")
        self.assertEqual(c.r, 66)
        self.assertEqual(c.g, 128)
        self.assertEqual(c.b, 255)
        self.assertEqual(c.get(), "#4280ff")
        c = value.make("c:#c08000:#88ffff/20")
        self.assertIsInstance(c, value.ColourRange)
        self.assertEqual(c.count, 20)
        self.assertEqual(c.add.r, -56)
        print(list(itertools.islice(c, 21)))


tf = {
    "r1": "10:100",
    "r2": "2.0:4.2",
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
