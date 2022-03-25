"""Handling of colours, using colour library"""
import random
import colour


class NoColour:
    def __init__(self, s):
        self.col = s

    @property
    def next(self):
        return self

    def str(self):
        return self.col

    def reset(self):
        pass

class Colour(colour.Color):
    """Colour that reads rgb hex or named colour"""

    @classmethod
    def fromstr(cls, s):
        """read from string #rrggbb"""
        if s == 'none' or s == 'transparent':
            return NoColour(s)
        return cls(s)

    @property
    def next(self):
        return self

    def str(self):
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
        if count > 0:
            self.count = count
            self.range = [Colour(c) for c in begin.range_to(end, count)]
        else:
            self.range = [begin, end]
            self.count = 2
        self.i = 0

    @classmethod
    def fromlist(cls, lst):
        r = cls(None, None, 0)
        r.range = lst
        r.count = len(lst)
        return r

    @classmethod
    def fromranges(cls, begin, end, count):
        ranges = []
        i = 0
        for c1 in begin:
            if i < len(end):
                c2 = end[i]
                i += 1
            ranges.append(ColourRange(c1, c2, count))
        nr = []
        for i in range(count):
            nr.append(ColourRange.fromlist([range[i] for range in ranges]))
        return nr

    def __len__(self):
        return self.count

    def __getitem__(self, item):
        return self.range[item]

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.count:
            r = self.range[self.i]
            self.i += 1
            return r
        raise StopIteration

    @property
    def next(self):
        if self.i >= self.count:
            self.i = 0
        r = self.range[self.i]
        self.i += 1
        return r

    def random(self):

        def rnd(m, n):
            vmin = min(m, n)
            vmax = max(m, n)
            return random.uniform(vmin, vmax)

        start = self.range[0]
        end = self.range[-1]
        r = rnd(start.red, end.red)
        g = rnd(start.green, end.green)
        b = rnd(start.blue, end.blue)
        return Colour(rgb=(r, g, b))

    def reset(self):
        self.i = 0
