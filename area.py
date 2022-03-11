"""handle area related things"""

import random
import geom


class RandomInArea:
    """Random point in area"""

    def __init__(self, area, out):
        self.area = area
        if out:
            self.bbox = None
        else:
            self.bbox = area.bbox()
        self.out = out

    def get(self):
        for _ in range(15):
            if self.out:
                x = random.uniform(0.0, 2800)
                y = random.uniform(0.0, 1800)
                p = geom.Point(x, y)
                if not self.area.contains(p):
                    return p
            else:
                x = self.bbox.x0 + random.uniform(0.0, self.bbox.x1)
                y = self.bbox.y0 + random.uniform(0.0, self.bbox.y1)
                p = geom.Point(x, y)
                if self.area.contains(p):
                    return p
        return None
