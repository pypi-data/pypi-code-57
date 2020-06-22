from unittest import TestCase, skip
from mock import patch, MagicMock
from hypothesis import given
from hypothesis import strategies as st
import tempfile, os
from tests.context import analysis
from analysis.annotate.report.composers.composer import Composer, LegendMaker, ScatterPlot, PieChartsBuilder, PieCharts, PieChart, Slices, Slice

class TestComposer(TestCase):
    def test_run(self):
        with self.assertRaises(NotImplementedError):
            Composer().run(None, None, None)

    @patch('os.remove')
    @patch('os.close')
    def test_tmp_name(self, close, remove):
        mkstemp_fd = MagicMock()
        mkstemp_temp_path = MagicMock(spec=str)

        with patch('tempfile.mkstemp', return_value=(mkstemp_fd, mkstemp_temp_path)) as mkstemp:
            temp_path = Composer().tmp_name()
            mkstemp.assert_called()

        close.assert_called_with(mkstemp_fd)
        remove.assert_called_with(temp_path)
        self.assertIs(temp_path, mkstemp_temp_path)

class TestLegendMaker(TestCase):
    @given(st.lists(st.text()))
    def test_create_colors_dict_property(self, labels):
        LegendMaker.create_colors_dict(labels)

    @skip("Not Implemented")
    def test_create_patches(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_limit_chars(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_make_composed_tags(self):
        self.fail("Not Implemented")

class TestScatterPlot(TestCase):
    @skip("Not Implemented")
    def test_make_tags_sp(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_make_clusters_sp(self):
        self.fail("Not Implemented")

class TestPieChartsBuilder(TestCase):
    @skip("Not Implemented")
    def test_build(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_make_labels_for_tags(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_list_size_for_composed_tags(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_set_annotation(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_set_category_name(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_set_max_nb_tags(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_set_show_nb_tags(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_set_max_chars(self):
        self.fail("Not Implemented")

class TestPieCharts(TestCase):
    @skip("Not Implemented")
    def test_get_percents_for_cluster(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_get_colors_for_cluster(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_get_category_name(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_get_handles(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_get_title_for_cluster(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_make_piecharts(self):
        self.fail("Not Implemented")

class TestPieChart(TestCase):
    @skip("Not Implemented")
    def test_get_percents(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_get_title(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_get_colors(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_make_piechart(self):
        self.fail("Not Implemented")

class TestSlices(TestCase):
    @skip("Not Implemented")
    def test_get_percents(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_get_total(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_get_colors(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_make_slices(self):
        self.fail("Not Implemented")

class TestSlice(TestCase):
    @skip("Not Implemented")
    def test_make_slice(self):
        self.fail("Not Implemented")
