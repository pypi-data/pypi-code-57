import unittest
from copy import copy
from gitbuilding.buildup.part import Part, PartList
from gitbuilding.buildup import ConfigSchema
from gitbuilding.buildup.buildup import Link

class PartTestCase(unittest.TestCase):

    def setUp(self):
        class MockDoc:
            def __init__(self):
                self.config = ConfigSchema().load({})
        self.doc = MockDoc()


    def test_compare_parts(self):
        link_dict = {"fullmatch": '[name](part.md){Qty: 1}',
                     "linktext": 'name',
                     "linklocation": 'part.m',
                     "alttext": '',
                     "buildup_data": 'Qty: 1'}
        link = Link(link_dict, '')
        part1 = Part(link, self.doc)
        self.assertTrue(part1.valid)
        part2 = copy(part1)
        part3 = Part(link, self.doc, indexed=True)
        part4 = copy(part1)
        part4.set_indexed(True)
        with self.assertRaises(RuntimeError):
            _ = (part1 == part2)
        self.assertEqual(part1, part3)
        self.assertEqual(part3, part4)

    def test_invalid_parts(self):
        invalid_data = ['Qtty: 1', 'Qty', 'Qty: ']
        for data in invalid_data:
            link_dict = {"fullmatch": '[name](part.md){Qty: 1}',
                         "linktext": 'name',
                         "linklocation": 'part.m',
                         "alttext": '',
                         "buildup_data": data}
            link = Link(link_dict, '')
            with self.assertLogs('BuildUp'):
                part = Part(link, self.doc)
            self.assertFalse(part.valid)

    def test_add_parts(self):
        link_dict = {"fullmatch": '[name]{Qty: 1}',
                     "linktext": 'name',
                     "linklocation": 'part.m',
                     "alttext": '',
                     "buildup_data": 'Qty: 1'}
        link1 = Link(link_dict, '')
        part1 = Part(link1, self.doc)
        link_dict["buildup_data"] = 'Qty: 2'
        link2 = Link(link_dict, '')
        part2 = Part(link2, self.doc)
        partlist = PartList(self.doc)
        partlist.count_part(part1)
        partlist.count_part(part2)
        partlist.finish_counting()
        self.assertEqual(str(partlist[0].qty_used), '3')
