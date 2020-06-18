from gbapi.api.base_submission import BaseSubmission

class Tool(BaseSubmission):
	def __init__(self, stats, sdata, ainfo):
		super(Tool, self).__init__(stats, sdata)
		
		self.info = ainfo['_aCellValues']
		self.download = self.info['_sDownloadUrl']
		self.homepage = self.info['_sHomepageUrl']