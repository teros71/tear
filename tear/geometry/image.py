"""Image for bitmap objects"""

from tear.geometry.geom import Point


class Image:
    """Image class"""

    def __init__(self, fname, width, height):
        self.fname = fname
        self.p = Point(0, 0)
        self.width = width
        self.height = height

    @property
    def path(self):
        return self.fname

    @property
    def position(self):
        return self.p

    @position.setter
    def position(self, p):
        self.p = p
