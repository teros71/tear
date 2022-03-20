import unittest
from value import value, reader
import colours


class TestColours(unittest.TestCase):

    def test_colours(self):
        c = colours.Colour.fromstr("#4280ff")
        self.assertEqual(c.hex, "#4280ff")
        self.assertEqual(c.str(), "#4280ff")
        c = reader.read_single_colour("#c08000:#88ffff/20")
        self.assertIsInstance(c, colours.ColourRange)
        self.assertEqual(len(c.range), 20)
#        print(list(itertools.islice(c, 21)))
        c = reader.read_single_colour("?:#80ff00:#ff0080/1")
        self.assertIsInstance(c, value.Random)
        self.assertIsInstance(c.range, colours.ColourRange)
        for _ in range(20):
            print(c.get().str())
        c = reader.read_colour(tf, "colours")
        self.assertIsInstance(c, value.List)
        self.assertIsInstance(c[0], value.List)
        self.assertIsInstance(c[0][0], colours.Colour)
        self.assertIsInstance(c[1][0], colours.ColourRange)
        self.assertEqual(colours.Colour("blue"), c[0][1])

    def test_colourranges(self):
        c1 = colours.ColourRange(reader.read_single_colour("blue"),
                                 reader.read_single_colour("red"), 10)
        c2 = colours.ColourRange(reader.read_single_colour("green"),
                                 reader.read_single_colour("yellow"), 10)
        self.assertEqual(len(c1), 10)
        rr = colours.ColourRange.fromranges(c1, c2, 10)
        self.assertEqual(len(rr), 10)
        for rrr in rr:
            print("range", len(rrr))
            for c in rrr:
                print(c.str())


tf = {
    "r1": "10:100",
    "r2": "2.0:4.2",
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
