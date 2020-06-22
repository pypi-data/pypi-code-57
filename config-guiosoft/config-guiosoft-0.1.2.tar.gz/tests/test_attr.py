import unittest

from tests.mocks.attr_mock import AttrMock


class TestAttr(unittest.TestCase):

    def test_attr(self):
        attr = AttrMock()
        self.assertEqual(attr.ATTR, 'abcd')
        setattr(attr, 'ATTR', '1234')
        self.assertEqual(attr.ATTR, '1234')
