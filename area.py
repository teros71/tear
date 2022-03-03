"""handle area related things"""

import random
import shape


class RandomInArea:
    """Random point in area"""

    def __init__(self, area):
        self.area = area
        self.bbox = area.bBox()

    def __next__(self):
        for _ in range(10):
            x = self.bbox.x + random.uniform(0.0, self.bbox.width)
            y = self.bbox.y + random.uniform(0.0, self.bbox.height)
            p = shape.Point(x, y)
            if self.area.contains(p):
                return p
        return None
