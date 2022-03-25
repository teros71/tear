import unittest
import form
import forms
import shape
from geometry import geom


class TestForms(unittest.TestCase):

    def test_generate(self):
        form.generate_form(tf)
        s = forms.get("gr-rect")
        self.assertIsInstance(s, shape.Shape)
        self.assertIsInstance(s.base, geom.Rect)
        self.assertEqual(s.base.width, 2800)
        self.assertEqual(s.base.height, 400)
        p = s.position
        self.assertEqual(p.x, 1400)
        self.assertEqual(p.y, 900)
        bb = s.bbox()
        self.assertEqual(bb.x0, 0.0)
        self.assertEqual(bb.x1, 2800.0)
        self.assertEqual(bb.y0, 700.0)
        self.assertEqual(bb.y1, 1100.0)
        sl = shape.List([s])
        bb = sl.bbox()
        self.assertEqual(bb.x0, 0.0)
        self.assertEqual(bb.x1, 2800.0)
        self.assertEqual(bb.y0, 700.0)
        self.assertEqual(bb.y1, 1100.0)
        ns = shape.Shape(geom.Polygon(s.get_points()))
        self.assertEqual(len(ns.base.points), 4)
        self.assertEqual(ns.base.points[0].x, -1400.0)
        self.assertEqual(ns.base.points[0].y, -200.0)
        self.assertEqual(ns.base.points[1].x, -1400.0)
        self.assertEqual(ns.base.points[1].y, 200.0)
        self.assertEqual(ns.base.points[2].x, 1400.0)
        self.assertEqual(ns.base.points[2].y, 200.0)
        self.assertEqual(ns.base.points[3].x, 1400.0)
        self.assertEqual(ns.base.points[3].y, -200.0)
        ns.inherit(s)
        p = ns.position
        self.assertEqual(p.x, 1400)
        self.assertEqual(p.y, 900)
        bb = ns.bbox()
        self.assertEqual(bb.x0, 0.0)
        self.assertEqual(bb.x1, 2800.0)
        self.assertEqual(bb.y0, 700.0)
        self.assertEqual(bb.y1, 1100.0)


tf = {
    "name": "gr-rect",
    "base": "new",
    "type": "rectangle",
    "h": 400,
    "w": 2800,
    "recipe": [
        {
            "algorithm": "position",
            "x": 1400,
            "y": 900
        }
      ]
    }

if __name__ == '__main__':
    form.initFormTable()
    print("initialized form table")
    unittest.main()
