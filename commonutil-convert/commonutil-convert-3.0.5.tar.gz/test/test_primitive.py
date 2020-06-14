# -*- coding: utf-8 -*-
""" Testing for primitive convert module """

import unittest


from commonutil_convert.primitive import to_text

class Test_ToText(unittest.TestCase):
	def test_normal_string_1(self):
		r = to_text("normal string")
		self.assertEqual(r, "normal string")

	def test_normal_string_2(self):
		r = to_text("   normal string")
		self.assertEqual(r, "normal string")

	def test_normal_string_3(self):
		r = to_text("normal string   ")
		self.assertEqual(r, "normal string")

	def test_empty_string_1(self):
		r = to_text("")
		self.assertIsNone(r)

	def test_empty_string_2(self):
		r = to_text(None)
		self.assertIsNone(r)

	def test_empty_string_3(self):
		r = to_text(None, "-")
		self.assertEqual(r, "-")
