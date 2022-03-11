import unittest
import math

import form
import forms
import shape
import geom


class TestForms(unittest.TestCase):

    def test_rect(self):
        r = geom.Rect(10.0, 20.0)
        self.assertEqual(r.width, 10.0)
        self.assertEqual(r.height, 20.0)
        r.scale(2.0, 1.0)
        self.assertEqual(r.width, r.height)
        ps = r.get_points(5.0, 4.0)
        self.assertEqual(len(ps), 4)
        self.assertEqual(ps[2].x, 15.0)
        self.assertEqual(ps[2].y, 14.0)
        self.assertEqual(r.length(), 80.0)
        p = r.point_at(10.0, 20.0, 50.0)
        self.assertEqual(p.x, 20.0)
        self.assertEqual(p.y, 20.0)
        p = r.point_at(10.0, 20.0, r.length() + 61.0)
        self.assertEqual(p.x, 19.0)
        self.assertEqual(p.y, 10.0)

    def test_circle(self):
        c = geom.Circle(10.0)
        self.assertEqual(c.r, 10.0)
        c.scale(2.0, 4.0)
        self.assertEqual(c.r, 20.0)
        ps = c.get_points(5.0, 4.0)
        self.assertEqual(len(ps), 16)
        self.assertEqual(c.length(), 2 * math.pi * c.r)
        p = c.point_at(10.0, 20.0, math.pi * c.r)
        self.assertEqual(p.x, -10.0)
        self.assertEqual(round(p.y, 4), 20.0)
        p = c.point_at(50.0, 50.0, 0)
        self.assertEqual(p.x, 70.0)
        self.assertEqual(p.y, 50.0)

    def test_polygon(self):
        r = geom.Rect(10.0, 20.0)
        pol = geom.Polygon.fromrect(r)
        self.assertEqual(len(pol.points), 4)
        ps = pol.get_points(10.0, 20.0)
        self.assertEqual(ps[0].x, 5.0)
        pol.scale(2.0, 1.0)
        self.assertEqual(pol.length(), 80.0)
        p = pol.point_at(10.0, 20.0, 50.0)
        self.assertEqual(p.x, 20.0)
        self.assertEqual(p.y, 20.0)
        p = pol.point_at(10.0, 20.0, pol.length() + 61.0)
        self.assertEqual(p.x, 19.0)
        self.assertEqual(p.y, 10.0)


if __name__ == '__main__':
    unittest.main()
