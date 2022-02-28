unitSize = 1000.0
tear_iterations = 18
tear_minDistance = 2.0
tear_minDistanceFactor = 0.0
tear_angleVar = 4
tear_randomizeBase = True
tear_count = 6
tear_opacity = 0.2
tear_colours = '[black]'


def read(d):
    global unitSize
    global tear_iterations
    global tear_minDistance
    global tear_minDistanceFactor
    global tear_angleVar
    global tear_randomizeBase
    global tear_count
    global tear_opacity
    global tear_colours
    unitSize = d.get('unitSize', unitSize)
    print(unitSize)
    t = d.get('tear', None)
    if t is not None:
        tear_iterations = t.get('iterations', tear_iterations)
        tear_minDistance = t.get('minDistance', tear_minDistance)
        tear_minDistanceFactor = t.get(
            'minDistanceFactor', tear_minDistanceFactor)
        tear_angleVar = t.get('angleVar', tear_angleVar)
        tear_randomizeBase = t.get('randomizeBase', tear_randomizeBase)
    t = d.get('multitear', None)
    if t is not None:
        tear_count = t.get('count', tear_count)
        tear_opacity = t.get('opacity', tear_opacity)
        tear_colours = t.get('colours', tear_colours)
