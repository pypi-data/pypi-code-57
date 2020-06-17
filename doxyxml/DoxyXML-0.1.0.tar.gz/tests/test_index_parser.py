"""
Module to test the index parser
"""

import unittest
import os.path as opth
import sys

DOXYXML_ROOT = opth.join(opth.dirname(__file__), "..")

sys.path.insert(0, DOXYXML_ROOT)

from DoxyXML.index_parser import IndexParser  # noqa: E402


str_truth = """Class MyFloat
Generalization:
Aggregations:
Composition:
Attributes:
    public float m_f
Operations:
    public void MyFloat(float f)

Class Geometry::Rectangle
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

abstract Class Geometry::Shape
Generalization:
Aggregations:
Composition:
Attributes:
Operations:
    public void Shape()
    public float area()

"""


class TestClassParser(unittest.TestCase):
    """
    Class to test index.xml parser class
    """

    def test_parse_class_file(self):
        index_file = opth.join(DOXYXML_ROOT, "example_res", "Doxygen", "xml", "index.xml")
        self.assertTrue(opth.exists(index_file))

        parser = IndexParser(index_file)

        self.assertEqual(3, len(parser.classes))
        self.assertEqual(1, len(parser.namespaces))

        clss_str = ""

        for c in parser.classes:
            clss_str += c.__str__() + "\n"

        self.assertEqual(str_truth, clss_str)


if __name__ == '__main__':
    unittest.main()
