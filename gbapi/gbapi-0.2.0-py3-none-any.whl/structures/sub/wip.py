class WorkOnGB:
	def __init__(self, src):
		self.src = src
		
		self.name = src['_sName']
		self.profile = src['_sProfileUrl']

class FinishedWork:
	def __init__(self, src):
		self.src = src
		
		"""
		(from wip.py)
		"_aFinishedWork": {
			"_aFinishedWorksOnGameBanana": [
				{
					"_sName": "Global Warfare AK47 Animations",
					"_sProfileUrl": "https:\/\/gamebanana.com\/skins\/178007",
					"_sSubFeedPreviewHtml": "<img class=\"PreviewImage lazy\" alt=\"Global Warfare AK47 Animations\" data-src=\"https:\/\/screenshots.gamebanana.com\/img\/ss\/srends\/220-90_5ee0806e42eea.jpg\"\/>"
				}
			],
			"_aRemoteFinishedWorkUrls": []
		}
		"""
		
		self.on_gamebanana = [
			WorkOnGB(w) for w in self.src['_aFinishedWorksOnGameBanana']
		]
		self.remote = self.src['_aRemoteFinishedWorkUrls']