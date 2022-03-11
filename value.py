"""
Handling various forms of input values
single number (int or float): 42 or 42.42
string: "foobar"
number range with optional step, int or float: "42:54[:1]", "0.42:42.4[:0.1]"
linear range between: "42:54/5"

random int: "?:42:54"
random float: "?:42.0:54.1"
random from list: "?:1,2,3,4"

colour: "blue" or "#0000ff"
colour range: "c:#000000:#102030"

tuple: [1, 2, 3]
range, tuple: [1, 2, 3]:[4, 4, 4]
random: "e:math.uniform(1.0, 42.3)"
random: "f:math.uniform(1.0, 42.3)"
"""
import random
import math


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def isint(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


class Simple:
    def __init__(self, val):
        self.val = val

    def value(self):
        return self.val


class Colour:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def fromstr(cls, s):
        return cls(int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))

    def get(self):
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}'

    def add(self, c):
        return Colour(self.r + c.r, self.g + c.g, self.b + c.b)

    def substract(self, c):
        return Colour(self.r - c.r, self.g - c.g, self.b - c.b)

    def copy(self):
        return Colour(self.r, self.g, self.b)


class ColourRange:
    def __init__(self, begin, end, count):
        self.begin = begin
        self.end = end
        self.add = end.substract(begin)
        self.count = count
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.get()

    def get(self):

        def add(v, n, m):
            r = int(float(v) * (float(n) / float(m)))
            return r

        if self.i > self.count:
            self.i = 0
        c = self.begin
        r = Colour(c.r + add(self.add.r, self.i, self.count),
                   c.g + add(self.add.g, self.i, self.count),
                   c.b + add(self.add.b, self.i, self.count))
        self.i += 1
        return r.get()

    def reset(self):
        self.i = 0


class Range:
    # Range of values, between min - max
    def __init__(self, min, max, step):
        self.min = min
        self.max = max
        self.step = step
        self.current = self.min

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        if self.current >= self.max:
            raise StopIteration
        return self.get()

    def get(self):
        if self.current >= self.max:
            self.current = self.min
        r = self.current
        self.current += self.step
        return r

    def reset(self):
        self.current = self.min

    @classmethod
    def fromlist(cls, lst):
        if len(lst) > 2:
            return cls(lst[0], lst[1], lst[2])
        return cls(lst[0], lst[1], 1)


class Random:
    def __init__(self, range):
        self.range = range
        self.method = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.get()

    def get(self):
        if isinstance(self.range, list):
            i = random.randint(0, len(self.range) - 1)
            return self.range[i]
        if isinstance(self.range.min, int):
            return random.randint(self.range.min, self.range.max)
        return random.uniform(self.range.min, self.range.max)

    def reset(self):
        pass


class Single:
    def __init__(self, value):
        self.value = value
        self.v = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.v:
            self.v = False
            return self.value
        raise StopIteration

    def get(self):
        return self.value

    def reset(self):
        self.v = True


class List:
    def __init__(self, lst):
        self.lst = lst
        self.i = 0

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.lst):
            v = self.lst[self.i]
            self.i += 1
            return v
        raise StopIteration

    def get(self):
        v = self.lst[self.i]
        self.i = (self.i + 1) % len(self.lst)
        return v

    def reset(self):
        self.i = 0


class Eval:
    def __init__(self, x, f):
        self.x = x
        self.current = x
        self.f = f
        self.i = 0

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        return self.get()

    def get(self):
        self.i += 1
        self.current = eval(self.f.format(self.current, self.i))
        return self.current

    def reset(self):
        self.current = self.x
        self.i = 0


def str2Eval(s):
    lst = s.split('@')
    if len(lst) == 2:
        return Eval(float(lst[0]), lst[1])
    return None


#def readRange(js, name, d="0.0-1"):
#    r = js.get(name, d)
#    if isinstance(r, list):
#        if isint(r[0]) and isint(r[1]):
#            return Range(int(r[0]), int(r[1]))
#        else:
#            return Range(float(r[0]), float(r[1]))
#    if isinstance(r, str):
#        rr = str2Range(r)
#        if rr is not None:
#            return rr
#    return Range(0.0, 1.0)


#def str2Range(s):
#    lst = s.split(':')
#    if len(lst) == 2:
#        if isint(lst[0]) and isint(lst[1]):
#            return Range(int(lst[0]), int(lst[1]))
#        else:
#            return Range(float(lst[0]), float(lst[1]))
#    return None


def convert_list(lst):
    if isint(lst[0]):
        lst = [int(x) for x in lst]
    elif isfloat(lst[0]):
        lst = [float(x) for x in lst]
    return lst


def convert_value(val):
    if isint(val):
        return int(val)
    if isfloat(val):
        return float(val)
    return val


def read_str_value(s):
    if ',' in s:
        lst = convert_list(s.split(','))
        return List(lst)
    if ':' in s:
        lst = s.split(':')
        if len(lst) == 3:
            return Range.fromlist(convert_list(lst))
        if len(lst) != 2:
            print("WARNING: invalid range syntax", s)
        if '/' in lst[1]:
            lst2 = lst[1].split('/')
            minv = convert_value(lst[0])
            maxv = convert_value(lst2[0])
            step = (maxv - minv) / convert_value(lst2[1])
            return Range(minv, maxv, step)
        return Range.fromlist(convert_list(lst))
    return Single(convert_value(s))


def read_colour(s):
    if s[0] != '#':
        return s
    lst = s.split(':')
    if len(lst) != 2:
        print("ERROR: invalid colour", s)
        return None
    lst2 = lst[1].split('/')
    return ColourRange(Colour.fromstr(lst[0]), Colour.fromstr(lst2[0]), int(lst2[1]))


def read(js, name, d=42):
    v = js.get(name, d)
    obj = make(v)
    return obj


def make(obj):
    if isinstance(obj, int) or isinstance(obj, float):
        return Single(obj)
    if isinstance(obj, list):
        if isinstance(obj[0], str) and obj[0].startswith('c:'):
            cl = [read_colour(c[2:]) for c in obj]
            return List(cl)
        return List(obj)
    if isinstance(obj, str):
        # colour range?
        if obj.startswith('c:'):
            return read_colour(obj[2:])
        if obj.startswith('?:'):
            val = read_str_value(obj[2:])
            if isinstance(val, List):
                return Random(val.lst)
            if isinstance(val, Range):
                return Random(val)
            return Random([val.value])

        if obj.startswith('e:'):
            return str2Eval(obj[2:])
        return read_str_value(obj)
    print("WARNING: unknown value type", obj)
    return obj
