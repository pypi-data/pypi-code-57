from datetime import datetime
from gbapi.api.base_submission import BaseSubmission

class Request(BaseSubmission):
	def __init__(self, stats, sdata, ainfo):
		super(Request, self).__init__(stats, sdata)
		
		"""
		{
			"_aAdditionalViewVariables": [],
			"_sViewTemplate": "?>\n<dl>\n<dt>Resolution<\/dt>\n<dd>\n<stateLabel class=\"RequestResolution_<?= $d[\"_akResolution\"] ?>\"><?= $d[\"_sResolution\"] ?><\/stateLabel>\n<? if (!empty($d[\"_sResolutionMessage\"])): ?>\n<small><?= $d[\"_sResolutionMessage\"] ?><\/small>\n<? endif ?>\n<\/dd>\n<dt>Deadline<\/dt>\n<dd class=\"RequestResolution_<?= $d[\"_akResolution\"] ?>\">\n<? $_oDeadline = new DateTime(\"@\".$d[\"_tsDeadline\"]) ?>\n<?= $_oDeadline->format(\"M jS, Y\") ?><br\/>\n@ <?= $_oDeadline->format(\"g:i a T\") ?>\n<\/dd>\n<? if (is_array($d[\"_aAdditionalRewards\"]) && !empty($d[\"_aAdditionalRewards\"])): ?>\n<dt>Additional Rewards<\/dt>\n<dd>\n<ol>\n<? foreach ($d[\"_aAdditionalRewards\"] as $_sAdditionalReward): ?>\n<li><?= $_sAdditionalReward ?><\/li>\n<? endforeach ?>\n<\/ol>\n<a href=\"<?= \\CONF::GET(\"ADDRESS\").\"\/wikis\/1922\" ?> \">Rules regarding Additional Rewards<\/a>\n<\/dd>\n<? endif ?>\n<\/dl>\n<?",
			"_aCellValues": {
				"_tsDeadline": 1593475367,
				"_sResolution": "Open",
				"_akResolution": "open",
				"_sResolutionMessage": "",
				"_aAdditionalRewards": ""
			}
		}
		"""
		
		self.info = ainfo['_aCellValues']
		self.deadline = datetime.utcfromtimestamp(self.info['_tsDeadline'])
		self.resolution = self.info['_sResolution']
		self.resolutionMessage = self.info['_sResolutionMessage']