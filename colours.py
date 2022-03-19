"""Handling of colours, using colour library"""
import random
import colour


class Colour(colour.Color):
    """Colour that reads rgb hex or named colour"""

    @classmethod
    def fromstr(cls, s):
        """read from string #rrggbb"""
        return cls(s)

    def get(self):
        """get string value"""
        return self.hex_l

    def add(self, c):
        """add another colour to this"""
        return Colour(rgb=(self.red + c.red, self.green + c.green, self.blue + c.blue))

    def substract(self, c):
        """substract another colour from this"""
        return Colour(rgb=(self.red - c.red, self.green - c.green, self.blue - c.blue))

    def copy(self):
        """return copy of this"""
        return Colour(self)

    def reset(self):
        pass


class ColourRange:
    def __init__(self, begin, end, count):
        self.begin = begin
        self.end = end
        self.range = None
        self.count = count
        if count > 0:
            self.range = [Colour(c) for c in begin.range_to(end, count)]
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.get()

    def get(self):
        if self.i >= self.count:
            self.i = 0
        r = self.range[self.i]
        self.i += 1
        return r.get()

    def random(self):

        def rnd(m, n):
            vmin = min(m, n)
            vmax = max(m, n)
            return random.uniform(vmin, vmax)

        r = rnd(self.begin.red, self.end.red)
        g = rnd(self.begin.green, self.end.green)
        b = rnd(self.begin.blue, self.end.blue)
        return Colour(rgb=(r, g, b))

    def reset(self):
        self.i = 0
