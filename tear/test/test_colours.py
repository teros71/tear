import unittest
from tear.value import value, reader
from tear.colours import Colour, ColourRange, NoColour, multirange
from tear.value.colours import read_single_colour

def test_basic():
    c = Colour.fromstr("transparent")
    assert isinstance(c, NoColour)
    c = Colour.fromstr("none")
    assert isinstance(c, NoColour)
    c = Colour.fromstr("lime")
    assert isinstance(c, Colour)
    assert c == Colour.fromstr("#00ff00")


def test_colours():
    c = Colour.fromstr("#4280ff")
    assert c.hex == "#4280ff"
    assert c.str() == "#4280ff"
    c = read_single_colour("#c08000:#88ffff/20")
    assert isinstance(c, ColourRange)
    assert len(c.range) == 20

#        print(list(itertools.islice(c, 21)))
#        c = read_single_colour("?:#80ff00:#ff0080/1")
#        self.assertIsInstance(c, value.Random)
#        self.assertIsInstance(c.range, colours.ColourRange)
 #       for _ in range(20):
  #          print(next(c).str())
    c = reader.read_colour(tf, "colours")
    v1 = next(c)
    assert Colour("red") == v1
    v2 = next(c)
    assert Colour("blue") == v2
    v2 = next(c)
    assert isinstance(v2, Colour)
#        self.assertIsInstance(c, value.List)
#        self.assertIsInstance(c[0], value.List)
#        self.assertIsInstance(c[0][0], colours.Colour)
#        self.assertIsInstance(c[1][0], colours.ColourRange)
#        self.assertEqual(colours.Colour("blue"), c[0][1])


def test_colourranges():
    red = Colour.fromstr("red")
    green = Colour.fromstr("green")
    blue = Colour.fromstr("blue")
    c0 = ColourRange.fromlist([red, green, blue], 4)
    assert len(c0.range) == 7
    assert c0.range[0] == red
    assert c0.range[3] == green
    assert c0.range[6] == blue
    for c in c0:
        print(c.str())

    yellow = Colour.fromstr("yellow")
    c1 = ColourRange.fromcolours(blue, red, 10)
    c2 = ColourRange.fromcolours(green, yellow, 10)
    assert len(c1) == 10
    assert c1.range[0] == Colour("blue")
    assert c1.range[1] != Colour("red")
    rr = multirange(c1, c2, 10)
    assert len(rr) == 10
    for rrr in rr:
        print("range", len(rrr))
        for c in rrr:
            print(c.str())


tf = {
    "colours": ["red", "blue", "#0011ff:#ff0000"]
}

if __name__ == '__main__':
    unittest.main()
