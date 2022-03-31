"""Text for text objects"""

from tear.geometry.geom import Point


class Text:
    """Text class"""

    def __init__(self, txt, size):
        self.text = txt
        self.size = size
        self.p = Point(0, 0)

    @property
    def position(self):
        return self.p

    @position.setter
    def position(self, p):
        self.p = p

    def __repr__(self):
        return f'Text[{self.text}]'
