import unittest

from .boundary_box import BoundaryBox


class TestBoundaryBox(unittest.TestCase):
    def test_create_boundary_box(self):
        box = BoundaryBox(0, 0, 1, 1)
        self.assertIsNotNone(box)

    def test_scale_coordinates(self):
        box = BoundaryBox(0, 0, 1, 1)
        box.scale_coordinates(700, 600)
        self.assertEqual([{'x': 0, 'y': 0}, {'x': 700, 'y': 600}], box.data)

if __name__ == '__main__':
    unittest.main()
