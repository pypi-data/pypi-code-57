from gbapi.api.base_submission import BaseSubmission

class Project(BaseSubmission):
	def __init__(self, stats, sdata, ainfo):
		super(Project, self).__init__(stats, sdata)
		
		"""
		{
			"_aAdditionalViewVariables": [],
			"_sViewTemplate": "?>\n<dl>\n<dt>Completion<\/dt>\n<dd class=\"Completion\">\n<itemCount><?= $d[\"_iCompletionPercentage\"] ?>%<\/itemCount>\n<\/dd>\n<dt>Development State<\/dt>\n<dd class=\"DevelopmentState\"><?= $d[\"_sDevelopmentState\"] ?><\/dd>\n<? if (!empty($d[\"_sFinishedProjectSubmissionUrl\"])): ?>\n<dt>Finished Project<\/dt>\n<dd class=\"FinishedProject\">\n<a href=\"<?= $d[\"_sFinishedProjectSubmissionUrl\"] ?>\">Project<\/a>\n<\/dd>\n<? endif ?>\n<\/dl>\n<?",
			"_aCellValues": {
				"_iCompletionPercentage": 64,
				"_sDevelopmentState": "In Development",
				"_sFinishedProjectSubmissionUrl": "",
				"_sWipCount": 0,
				"_sFileCount": 0
			}
		}
		"""
		
		self.info = ainfo['_aCellValues']
		self.completion = self.info['_iCompletionPercentage']
		self.dev_state = self.info['_sDevelopmentState']
		self.finished_url = self.info['_sFinishedProjectSubmissionUrl']
		self.wip_count = self.info['_sWipCount']
		self.file_count = self.info['_sFileCount']