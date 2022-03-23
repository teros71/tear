import unittest
import math

from geometry import geom


class TestGeom(unittest.TestCase):
    def test_line_seg_intersect(self):
        inters = geom.intersect(geom.Point(0, 0), geom.Point(5, 5),
                                geom.Point(0, 5), geom.Point(5, 0))

        self.assertIsNotNone(inters)
        self.assertTrue(inters.is_equal(geom.Point(2.5, 2.5)))

    def test_line_seg_no_intersect(self):
        inters = geom.intersect(geom.Point(3, 0), geom.Point(3, 4),
                                geom.Point(0, 5), geom.Point(5, 5))
        self.assertIsNone(inters)

    def test_line_seg_overlap(self):
        inters = geom.intersect(geom.Point(0, 0), geom.Point(2, 0),
                                geom.Point(1, 0), geom.Point(3, 0))
        self.assertIsNone(inters)
#    Assert.IsTrue(actual);
#    Assert.AreEqual(double.NaN, intersection.X);
#    Assert.AreEqual(double.NaN, intersection.Y);


if __name__ == '__main__':
    unittest.main()
