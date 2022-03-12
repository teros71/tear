"""default config values"""

TEAR_ITERATIONS = 18
TEAR_MINDISTANCE = 2.0
TEAR_MINDISTANCEFACTOR = 0.0
TEAR_ANGLEVAR = 0.1
TEAR_RANDOMIZEBASE = True
TEAR_COUNT = 6
TEAR_OPACITY = 0.2
TEAR_COLOURS = '[black]'


def read(config):
    """read defaults"""
    global TEAR_ITERATIONS
    global TEAR_MINDISTANCE
    global TEAR_MINDISTANCEFACTOR
    global TEAR_ANGLEVAR
    global TEAR_RANDOMIZEBASE
    global TEAR_COUNT
    global TEAR_OPACITY
    global TEAR_COLOURS
    t = config.get('tear', None)
    if t is not None:
        TEAR_ITERATIONS = t.get('iterations', TEAR_ITERATIONS)
        TEAR_MINDISTANCE = t.get('minDistance', TEAR_MINDISTANCE)
        TEAR_MINDISTANCEFACTOR = t.get(
            'minDistanceFactor', TEAR_MINDISTANCEFACTOR)
        TEAR_ANGLEVAR = t.get('angleVar', TEAR_ANGLEVAR)
        TEAR_RANDOMIZEBASE = t.get('randomizeBase', TEAR_RANDOMIZEBASE)
