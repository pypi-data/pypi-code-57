from datetime import datetime
from gbapi.api.base_submission import BaseSubmission
from gbapi.structures.sub.wip import FinishedWork

class WiP(BaseSubmission):
	def __init__(self, stats, sdata, ainfo):
		super(WiP, self).__init__(stats, sdata)
		
		self.info = ainfo['_aCellValues']
		self.dev_state = self.state = self.info['_sDevelopmentState']
		# self.completion = self.progress = self.info['_iCompletionProgress']
		self.is_private = self.info['_sbIsPrivate']
		self.finished_work = FinishedWork(self.info['_aFinishedWork'])
		self.added = datetime.utcfromtimestamp(self.info['_tsDateAdded'])