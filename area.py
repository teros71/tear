"""handle area related things"""

import random
from geometry import geom
import pg


class RandomInArea:
    """Random point in area"""

    def __init__(self, area, out):
        self.area = area
        self.bbox = area.bbox()
        self.out = out

    @property
    def next(self):
        if self.out:
            for _ in range(15):
                x = random.uniform(0.0, pg.WIDTH)
                y = random.uniform(0.0, pg.HEIGHT)
                p = geom.Point(x, y)
                if not self.area.is_inside(p):
                    return p
            p.x = self.bbox.x0 - 0.1
            return p
        for _ in range(15):
            x = self.bbox.x0 + random.uniform(0.0, self.bbox.x1)
            y = self.bbox.y0 + random.uniform(0.0, self.bbox.y1)
            p = geom.Point(x, y)
            if self.area.is_inside(p):
                return p
        return geom.Point(self.area.position.x, self.area.position.y)
