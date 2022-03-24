import unittest
import math

from geometry import geom


class TestGeom(unittest.TestCase):

    def test_rect(self):
        r = geom.Rect(10.0, 20.0)
        self.assertEqual(r.width, 10.0)
        self.assertEqual(r.height, 20.0)
        r.scale(2.0, 1.0)
        self.assertEqual(r.width, r.height)
        ps = r.get_points(geom.Point(5.0, 4.0))
        self.assertEqual(len(ps), 4)
        self.assertEqual(ps[2].x, 15.0)
        self.assertEqual(ps[2].y, 14.0)
        self.assertEqual(r.length(), 80.0)
        p = r.point_at(50.0 / 80.0)
        self.assertEqual(p.x, 10.0)
        self.assertEqual(p.y, 0.0)
        p = r.point_at(61.0 / r.length())
        self.assertEqual(p.x, 9.0)
        self.assertEqual(p.y, -10.0)

    def test_circle(self):
        c = geom.Circle(10.0)
        self.assertEqual(c.r, 10.0)
        c.scale(2.0)
        self.assertEqual(c.r, 20.0)
        ps = c.get_points(geom.Point(5.0, 4.0))
        self.assertEqual(len(ps), 16)
        self.assertEqual(c.length(), 2 * math.pi * c.r)
        p = c.point_at(math.pi * c.r / c.length())
        self.assertEqual(p.x, -20.0)
        self.assertEqual(round(p.y, 4), 0.0)
        p = c.point_at(0)
        self.assertEqual(p.x, 20.0)
        self.assertEqual(p.y, 0.0)

    def test_polygon(self):
        r = geom.Rect(10.0, 20.0)
        pol = geom.Polygon.fromrect(r)
        self.assertEqual(len(pol.points), 4)
        ps = pol.get_points(geom.Point(10.0, 20.0))
        self.assertEqual(ps[0].x, 5.0)
        pol.scale(2.0, 1.0)
        self.assertEqual(pol.length(), 80.0)
        p = pol.point_at(50.0 / 80.0)
        self.assertEqual(p.x, 10.0)
        self.assertEqual(p.y, 0.0)
        p = pol.point_at(61.0 / 80.0)
        self.assertEqual(p.x, 9.0)
        self.assertEqual(p.y, -10.0)


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
