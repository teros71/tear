import unittest
import form
import forms
import shape
import geom


class TestForms(unittest.TestCase):

    def test_generate(self):
        form.generate_form(tf)
        s = forms.get("gr-rect")
        self.assertIsInstance(s, shape.Shape)
        p = s.position
        print(s.base.width, s.base.height)
        print(p.x, p.y)
        bb = s.bbox()
        print(bb.x0, bb.y0, bb.x1, bb.y1)
        sl = shape.List([s])
        p = s.position
        print(p.x, p.y)
        bb = sl.bbox()
        print(bb.x0, bb.y0, bb.x1, bb.y1)
        ns = shape.Shape(geom.Polygon(s.get_points()))
        for pp in ns.base.points:
            print("  ", pp.x, pp.y)
        bb = ns.base.bbox()
        print("poly", bb.x0, bb.y0, bb.x1, bb.y1)
        ns.inherit(s)
        p = ns.position
        print(p.x, p.y)
        bb = ns.bbox()
        print(bb.x0, bb.y0, bb.x1, bb.y1)


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
