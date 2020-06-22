from unittest import TestCase, skip
from mock import MagicMock, patch, PropertyMock

from tests.context import analysis
from analysis.shared.clustering.scipypatch import ScipyPatch

IVL = [2, 5, 3, 4, 7, 1, 8, 6]
REVERSED_IVL = list(reversed(IVL))
FLAT_CLUSTERS = [7, 6, 3, 8, 1, 4, 2, 5]

class TestScipyPatch(TestCase):
    @patch.object(ScipyPatch, 'make_dendrogram', return_value={'leaves':[1, 2, 0]})
    def test_reorder_matrix(self, mock_make_dendrogram):
        clusters = MagicMock()
        reordered_matrix = MagicMock()
        matrix = MagicMock()
        matrix.sub_matrix = MagicMock(return_value=reordered_matrix)
        matrix.get_file_names = MagicMock(return_value=['a', 'b', 'c'])

        result = ScipyPatch.reorder_matrix(clusters, matrix)

        self.assertIs(result, reordered_matrix)
        matrix.get_file_names.assert_called_once()
        mock_make_dendrogram.assert_called_once_with(clusters, matrix)
        self.assertEqual(list(matrix.sub_matrix.call_args[0][0]), ['a', 'c', 'b'])

    @patch.object(ScipyPatch, 'make_dendrogram', return_value={'ivl':IVL})
    @patch.object(ScipyPatch, '_obtain_order', return_value=REVERSED_IVL)
    def test_rename_clusters(self, _obtain_order, make_dendrogram):
        matrix = MagicMock()
        remap_clusters = MagicMock()
        clusters = MagicMock()
        count = PropertyMock(return_value=8)
        type(clusters).count = count
        clusters.make_flat_clusters = MagicMock(return_value=FLAT_CLUSTERS)
        clusters.remap_clusters_ids = MagicMock(return_value=remap_clusters)

        result = ScipyPatch.rename_clusters(clusters, matrix)

        self.assertIs(result, remap_clusters)
        make_dendrogram.assert_called_with(clusters, matrix)
        self.assertEqual(list(_obtain_order.call_args[0][0]), REVERSED_IVL)
        count.assert_called()
        clusters.make_flat_clusters.assert_called_with(matrix)
        clusters.remap_clusters_ids.assert_called_with([4, 1, 6, 2, 3, 5, 8, 7], matrix)

    @patch.object(ScipyPatch, '_compute_color_threshold')
    @patch('scipy.cluster.hierarchy.dendrogram')
    def test_make_dendrogram(self, mock_dendrogram, mock_compute_color_threshold):
        clusters = MagicMock()
        matrix = MagicMock()

        ScipyPatch._compute_color_threshold(clusters)

        ScipyPatch.make_dendrogram(clusters, matrix)

        mock_compute_color_threshold.assert_called_with(clusters)

    @skip("Not Implemented")
    def test_compute_color_threshold(self):
        self.fail("Not Implemented")

    @skip("Not Implemented")
    def test_obtain_order(self):
        self.fail("Not Implemented")
