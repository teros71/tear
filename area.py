"""handle area related things"""

import random
import geom


class RandomInArea:
    """Random point in area"""

    def __init__(self, area):
        self.area = area
        self.bbox = area.bbox()

    def __next__(self):
        for _ in range(10):
            x = self.bbox.x0 + random.uniform(0.0, self.bbox.x1)
            y = self.bbox.y0 + random.uniform(0.0, self.bbox.y1)
            p = geom.Point(x, y)
            if self.area.contains(p):
                return p
        return None
