"""
Evaluation related stuff
"""
# import usefull stuff to be used in eval
import math
from tear import goldenratio
from tear.value import points, value


def evaluate(exp):
    """Evaluate expression"""
    return eval(exp)



def ev_source(expr):
    i = 0
    while True:
        yield evaluate(expr.format(i))
        i += 1
