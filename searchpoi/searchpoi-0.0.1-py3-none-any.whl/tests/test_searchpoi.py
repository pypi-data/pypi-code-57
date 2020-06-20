from unittest import TestCase

from ..searchpoi import SearchPoi
import pandas


class TestSearchPoi(TestCase):
    def test_clostest(self):
        s = SearchPoi('Salt Lake City')
        closest_points = s.closest(-111.876183, 40.758701, 0.1)
        self.assertTrue(isinstance(closest_points, pandas.DataFrame))
