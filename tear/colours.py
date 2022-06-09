"""Handling of colours, using colour library"""
import random
import colour


class NoColour:
    def __init__(self, s):
        self.col = s

    def str(self):
        return self.col


class Colour(colour.Color):
    """Colour that reads rgb hex or named colour"""

    @classmethod
    def fromstr(cls, s):
        """read from string #rrggbb"""
        if s == 'none' or s == 'transparent':
            return NoColour(s)
        return cls(s)

    def __next__(self):
        return self.next

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


class ColourRange:
    def __init__(self, lst: list):
        self.range = lst

    def extend(self, r: "ColourRange"):
        if self.range[-1] == r.range[0]:
            self.range.extend(r.range[1:])
        else:
            self.range.extend(r.range)

    @property
    def begin(self):
        return self.range[0]

    @property
    def end(self):
        return self.range[-1]

    @classmethod
    def fromcolours(cls, begin: Colour, end: Colour, count: int) -> "ColourRange":
        if count > 0:
            return cls([Colour(c) for c in begin.range_to(end, count)])
        else:
            return cls([begin, end])

    @classmethod
    def fromlist(cls, lst: list, count: int) -> "ColourRange":
        if len(lst) == 1:
            return cls(lst)
        r = ColourRange.fromcolours(lst[0], lst[1], count)
        i = 2
        while i < len(lst):
            r.extend(ColourRange.fromcolours(lst[i - 1], lst[i], count))
            i += 1
        return r

    def __len__(self):
        return len(self.range)

    def __getitem__(self, item):
        return self.range[item]

    def __iter__(self):
        return iter(self.range)


def multirange(begin: ColourRange, end: ColourRange, count: int):
    ranges = []
    i = 0
    for c1 in begin:
        if i < len(end):
            c2 = end[i]
            i += 1
        ranges.append(ColourRange.fromcolours(c1, c2, count))
    nr = []
    for i in range(count):
        nr.append(ColourRange([r[i] for r in ranges]))
    return nr


def lst2colours(lst):
    return [Colour.fromstr(c) for c in lst]


def random_from_range(r):
    return random.choice(r.range)


def random_between(start, end):
    def rnd(m, n):
        vmin = min(m, n)
        vmax = max(m, n)
        return random.uniform(vmin, vmax)

    r = rnd(start.red, end.red)
    g = rnd(start.green, end.green)
    b = rnd(start.blue, end.blue)
    return Colour(rgb=(r, g, b))
