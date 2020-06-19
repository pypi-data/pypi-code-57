# Imports go here!
from .api_bio_get import ApiBioGetStar
from .api_bio_set import ApiBioSetStar
from .api_diario_get import ApiDiarioGetStar
from .api_diario_list import ApiDiarioListStar
from .api_discord_cv import ApiDiscordCvStar
from .api_discord_play import ApiDiscordPlayStar
from .api_wiki_edit import ApiWikiEditStar
from .api_wiki_get import ApiWikiGetStar
from .api_wiki_list import ApiWikiListStar
from .api_fiorygi_get import ApiFiorygiGetStar
from .api_diario_random import ApiDiarioRandomStar
from .api_polls_create import ApiPollsCreate
from .api_polls_get import ApiPollsGet
from .api_polls_list import ApiPollsList
from .api_cvstats_latest import ApiCvstatsLatestStar
from .api_cvstats_avg import ApiCvstatsAvgStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    ApiBioGetStar,
    ApiBioSetStar,
    ApiDiarioGetStar,
    ApiDiarioListStar,
    ApiDiscordCvStar,
    ApiDiscordPlayStar,
    ApiWikiEditStar,
    ApiWikiGetStar,
    ApiWikiListStar,
    ApiFiorygiGetStar,
    ApiDiarioRandomStar,
    ApiPollsCreate,
    ApiPollsGet,
    ApiPollsList,
    ApiCvstatsLatestStar,
    ApiCvstatsAvgStar,
]

# Don't change this, it should automatically generate __all__
__all__ = [star.__name__ for star in available_page_stars]
