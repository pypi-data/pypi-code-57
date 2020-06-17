"""
Module to test the class parser
"""

import unittest
import os.path as opth
import sys

DOXYXML_ROOT = opth.join(opth.dirname(__file__), "..")
DOXYXML = opth.join(DOXYXML_ROOT, "DoxyXML")

sys.path.insert(0, DOXYXML_ROOT)

from DoxyXML.class_obj import Class


str_truth = """Class Geometry::Rectangle
Generalization:
  class_geometry_1_1_shape
Aggregations:
Composition:
  class_my_float
Attributes:
    private MyFloat m_width
    private float m_height
Operations:
    public void Rectangle()
    public void Rectangle(float w,  float h)
    public void ~Rectangle()
    public float area()
    public void setWidth(const float w)
    public void setHeight(const float h)
    public float height()
    public float width()
"""


class TestClassParser(unittest.TestCase):

    def test_parse_class_file(self):
        class_file = opth.join(DOXYXML_ROOT, "example_res", "Doxygen", "xml", "class_geometry_1_1_rectangle.xml")
        print(opth.abspath(class_file))
        self.assertTrue(opth.exists(class_file))

        obj = Class.from_xml(class_file)

        self.assertEqual("class_geometry_1_1_rectangle", obj.refid)
        self.assertEqual(str_truth, obj.__str__())


if __name__ == '__main__':
    unittest.main()
