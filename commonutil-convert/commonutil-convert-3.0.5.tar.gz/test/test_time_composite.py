# -*- coding: utf-8 -*-
""" Testing for time composite convert module """

import unittest
import datetime

from commonutil_convert.time_composite import to_datetime


class Test_ToDateTime(unittest.TestCase):
	def test_none(self):
		c = datetime.datetime(2018, 11, 24, 16, 39, 13)
		r = to_datetime(None, c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_string_yyyymmddhhmmss_1(self):
		c = datetime.datetime(2018, 11, 24, 16, 39, 13)
		r = to_datetime("20181124163913", c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_string_yyyymmddhhmmss_2(self):
		c = datetime.datetime(2018, 11, 24, 16, 39, 13)
		r = to_datetime("2018-11-24 16:39:13", c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_string_yyyymmddhhmm_1(self):
		c = datetime.datetime(2018, 11, 24, 16, 39, 0)
		r = to_datetime("201811241639", c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_string_yyyymmddhhmm_2(self):
		c = datetime.datetime(2018, 11, 24, 16, 39, 0)
		r = to_datetime("2018-11-24 16:39", c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_string_yyyymmdd_1(self):
		c = datetime.datetime(2018, 11, 24, 0, 0, 0)
		r = to_datetime("20181124", c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_string_yyyymmdd_2(self):
		c = datetime.datetime(2018, 11, 24, 0, 0, 0)
		r = to_datetime("2018-11-24", c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_tuple_1(self):
		c = datetime.datetime(2018, 11, 24, 16, 39, 13)
		r = to_datetime((2018, 11, 24, 16, 39, 13), c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_tuple_2(self):
		c = datetime.datetime(2018, 11, 24, 16, 39, 0)
		r = to_datetime((2018, 11, 24, 16, 39), c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_tuple_3(self):
		c = datetime.datetime(2018, 11, 24, 16, 0, 0)
		r = to_datetime((2018, 11, 24, 16), c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)

	def test_tuple_4(self):
		c = datetime.datetime(2018, 11, 24, 0, 0, 0)
		r = to_datetime((2018, 11, 24), c)
		d = r - c
		self.assertLess(abs(d.total_seconds()), 1)
