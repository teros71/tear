import pytest


from tear.model import factory, shape
from tear.geometry import geom


@pytest.mark.parametrize(
    "typename, config, expected_result",
    [("rectangle", {"w": "10:100", "h": "20:100"}, geom.Rect),
     ("circle", {"r": "10:100"}, geom.Circle),
     ("ellipse", {"rx": "10:100", "ry": "20:100"}, geom.Ellipse)
     ]
)
def test_generators(typename, config, expected_result):
    g = factory.make_generator_shape(typename, config)
    assert isinstance(g, shape.Generator)
    n = next(g)
    assert isinstance(n, shape.Shape)
    assert type(n.g) == expected_result
    n = next(g)
    assert isinstance(n, shape.Shape)
    assert type(n.g) == expected_result
