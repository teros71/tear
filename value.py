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


class Range:
    # Range of values, between min - max
    def __init__(self, min, max):
        self.min = min
        self.max = max

    @classmethod
    def fromlist(cls, lst):
        return cls(lst[0], lst[1])


class Random:
    def __init__(self, range):
        self.range = range
        self.method = 0

    def __iter__(self):
        return self

    def __next__(self):
        if isinstance(self.range.min, int):
            return random.randint(self.range.min, self.range.max)
        else:
            return random.uniform(self.range.min, self.range.max)

    def reset(self):
        pass


class Single:
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return self

    def __next__(self):
        return self.value

    def reset(self):
        pass


class Round:
    def __init__(self, lst):
        self.lst = lst
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
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
        return self

    def __next__(self):
        v = self.current
        self.i += 1
        self.current = eval(self.f.format(self.current, self.i))
        return v

    def reset(self):
        self.current = self.x
        self.i = 0


def str2Eval(s):
    lst = s.split('@')
    if len(lst) == 2:
        return Eval(float(lst[0]), lst[1])
    return None


def readRange(js, name, d="0.0-1"):
    r = js.get(name, d)
    if isinstance(r, list):
        if isint(r[0]) and isint(r[1]):
            return Range(int(r[0]), int(r[1]))
        else:
            return Range(float(r[0]), float(r[1]))
    if isinstance(r, str):
        rr = str2Range(r)
        if rr is not None:
            return rr
    return Range(0.0, 1.0)


def str2Range(s):
    lst = s.split('-')
    if len(lst) == 2:
        if isint(lst[0]) and isint(lst[1]):
            return Range(int(lst[0]), int(lst[1]))
        else:
            return Range(float(lst[0]), float(lst[1]))
    return None


def read(js, name, d=42):
    v = js.get(name, d)
    return make(v)


def make(obj):
    if isinstance(obj, int) or isinstance(obj, float):
        return Single(obj)
    if isinstance(obj, list):
        return Round(obj)
    if isinstance(obj, str):
        rr = str2Range(obj)
        if rr is not None:
            return Random(rr)
        rr = str2Eval(obj)
        if rr is not None:
            return rr
        return Single(obj)
    return obj
