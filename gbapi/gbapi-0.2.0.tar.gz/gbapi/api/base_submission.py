"""module containing BaseSubmission class"""

from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class BaseSubmission(StructuredData, Stats):
	"""
		Internal BaseSubmission class.
		Implements basic stats and structured data.
	"""
	def __init__(self, stats, sdata):
		StructuredData.__init__(self,sdata)
		Stats.__init__(self,stats)