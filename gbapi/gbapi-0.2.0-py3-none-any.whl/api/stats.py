"""module containing Stats class"""

from datetime import datetime

"""
{
    "_aAdditionalViewVariables": [],
    "_sViewTemplate": "?>\n<ul>\n<? if (isset($d[\"_nLikesCount\"])): ?>\n<li class=\"LikesCount CountStat\" title=\"Likes\">\n<spriteIcon class=\"MiscIcon LikeIcon\"><\/spriteIcon>\n<itemCount><?= short_number_format($d[\"_nLikesCount\"]) ?><\/itemCount>\n<\/li>\n<? endif ?>\n\n<? if (isset($d[\"_nViewCount\"]) && $d[\"_nViewCount\"] > 0): ?>\n<li class=\"ViewCount CountStat\" title=\"Views: <?= number_format($d[\"_nViewCount\"]) ?>\">\n<spriteIcon class=\"MiscIcon SubscribeIcon\"><\/spriteIcon>\n<itemCount><?= short_number_format($d[\"_nViewCount\"]) ?><\/itemCount>\n<\/li>\n<? endif ?>\n<? if (isset($d[\"_nPostCount\"]) && $d[\"_nPostCount\"] > 0): ?>\n<li class=\"PostCount CountStat\" title=\"Posts\">\n<spriteIcon class=\"SubmissionTypeSmall Post\"><\/spriteIcon>\n<itemCount><?= number_format($d[\"_nPostCount\"]) ?><\/itemCount>\n<\/li>\n<? endif ?>\n<li class=\"DateAdded TimeStat\" title=\"Submitted\">\n<spriteIcon class=\"SubnavigatorIcon HistoryIcon\"><\/spriteIcon>\n<? \\gamebanana\\eColoredDate($d[\"_tsDateAdded\"]) ?>\n<\/li>\n<? if ($d[\"_tsDateModified\"] > $d[\"_tsDateAdded\"]): ?>\n<li class=\"DateModified TimeStat\" title=\"Modified\">\n<spriteIcon class=\"SubnavigatorIcon HistoryIcon\"><\/spriteIcon>\n<? \\gamebanana\\eColoredDate($d[\"_tsDateModified\"]) ?>\n<\/li>\n<? endif ?>\n\n<\/ul>\n<?",
    "_aCellValues": {
        "_nLikesCount": 0,
        "_nViewCount": 88,
        "_nPostCount": 0,
        "_tsDateAdded": 1591660967,
        "_tsDateModified": 1591660967
    }
}
"""

class Stats:
	"""
		Internal Stats class.
		Represents stats of a submission on GameBanana.
	"""
	def __init__(self, src):
		if not isinstance(src, dict):
			raise TypeError(
				f"from Stats: "
				f"src must be `dict`, not {type(raw)}!"
			)
		src = src['_aCellValues']
			
		self.likes = src.get('_nLikesCount', None)
		self.views = src['_nViewCount']
		self.posts = src['_nPostCount']
		
		self.added = datetime.utcfromtimestamp(src['_tsDateAdded'])
		self.modified = datetime.utcfromtimestamp(src['_tsDateModified'])