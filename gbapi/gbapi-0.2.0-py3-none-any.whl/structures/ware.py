from gbapi.api.stats import Stats
from gbapi.api.base_submission import BaseSubmission

class Ware(BaseSubmission):
	def __init__(self, stats, sdata, ainfo):
		super(Ware, self).__init__(stats, sdata)
		
		self.info = ainfo['_aCellValues']
		self.ware_type = self.info['_sType']