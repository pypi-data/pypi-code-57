from datetime import datetime
from gbapi.api.base_submission import BaseSubmission

class Tutorial(BaseSubmission):
	def __init__(self, stats, sdata, ainfo):
		super(Tutorial, self).__init__(stats, sdata)
		
		"""
		{
			"_aAdditionalViewVariables": [],
			"_sViewTemplate": "?>\n<dl>\n<dt>Difficulty Level<\/dt>\n<dd class=\"DifficultyLevel\">\n<? if ($d[\"_sDifficultyLevel\"] == \"beginner\"): ?>\n<span class=\"GreenColor\">\n<? elseif ($d[\"_sDifficultyLevel\"] == \"intermediate\"): ?>\n<span class=\"BlueColor\">\n<? else: ?>\n<span class=\"RedColor\">\n<? endif ?>\n<?= ucfirst($d[\"_sDifficultyLevel\"]) ?>\n<\/span>\n<\/dd>\n<\/dl>\n<?",
			"_aCellValues": {
				"_sDifficultyLevel": "Beginner"
			}
		}
		"""
		
		self.info = ainfo['_aCellValues']
		self.difficulty = self.info['_sDifficultyLevel']