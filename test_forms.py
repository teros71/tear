import unittest
import form


class TestForms(unittest.TestCase):

    def test_generate(self):
        form.generateForm(tf)
        nf = form.formTable.get('gr-rect', None)
        self.assertFalse(nf == None)


tf = {
    "name": "gr-rect",
    "base": "rectangle",
    "recipe": [
        {
          "algorithm": "goldenRatioRectangles",
          "count": 9
        }
      ]
    }

if __name__ == '__main__':
    form.initFormTable()
    print("initialized form table")
    unittest.main()
