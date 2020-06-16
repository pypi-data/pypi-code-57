import collections

CATEGORIES = ['security', 'recommended', 'optional', 'feature', 'document', 'yast']
SEVERITIES = ['critical', 'important', 'moderate', 'low', 'unspecified']


Patch = collections.namedtuple('Patch', 'category severity')
Product = collections.namedtuple('Product', 'name eol')
