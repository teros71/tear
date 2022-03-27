"""
Evaluation related stuff
"""
# import usefull stuff to be used in eval
import math
from tear import goldenratio
from tear.value import points


def evaluate(exp):
    """Evaluate expression"""
    return eval(exp)


class Eval:
    """Eval object for making dynamic values"""

    def __init__(self, f):
        self.f = f
        self.i = 0
        self.last = None

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        return self.next

    @property
    def current(self):
        """current value of the evaluation"""
        return self.last

    @property
    def next(self):
        """next value"""
        self.last = evaluate(self.f.format(self.i))
        self.i += 1
        return self.last

    def reset(self):
        """reset the counter"""
        self.i = 0
