import unittest

from tests.context import analysis
from analysis.shared.util.string_builder import StringBuilder

TEMPLATE_1 = 'GeEC-annotate, k=%(nb_clusters) clusters'
TEMPLATE_2 = '%(nb_clusters)%(nb_clusters)%(nb_clusters)%(nb_clusters)'
TEMPLATE_3 = '%(first)%(second)%(third)'

class TestStringBuilder(unittest.TestCase):
    def test_build(self):
        sb1 = StringBuilder(TEMPLATE_1)
        sb1.set('nb_clusters', 3)
        self.assertEqual(sb1.build(), 'GeEC-annotate, k=3 clusters')

        sb2 = StringBuilder(TEMPLATE_2)
        sb2.set('nb_clusters', 50)
        self.assertEqual(sb2.build(), '50505050')

        sb3 = StringBuilder(TEMPLATE_3)
        sb3.set('first', 'Manners ')
        sb3.set('second', 'maketh ')
        sb3.set('third', 'man.')
        self.assertEqual(sb3.build(), 'Manners maketh man.')

        sb4 = StringBuilder(TEMPLATE_1)
        sb4.set('potato', 'gun')
        self.assertEqual(sb4.build(), 'GeEC-annotate, k=None clusters')

        sb5 = StringBuilder(TEMPLATE_1)
        self.assertEqual(sb5.build(), 'GeEC-annotate, k=None clusters')
