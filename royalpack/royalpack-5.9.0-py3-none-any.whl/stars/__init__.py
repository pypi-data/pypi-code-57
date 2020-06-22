# Imports go here!
from .api_bio import ApiBioSetStar
from .api_diario import ApiDiarioGetStar
from .api_diario_list import ApiDiarioPagesStar
from .api_discord_cv import ApiDiscordCvStar
from .api_discord_play import ApiDiscordPlayStar
from .api_fiorygi import ApiFiorygiStar
from .api_diario_random import ApiDiarioRandomStar
from .api_poll import ApiPollStar
from .api_poll_list import ApiPollsListStar
from .api_cvstats_latest import ApiCvstatsLatestStar
from .api_cvstats_avg import ApiCvstatsAvgStar
from .api_user_ryg import ApiUserRygStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    ApiBioSetStar,
    ApiDiarioGetStar,
    ApiDiarioPagesStar,
    ApiDiscordCvStar,
    ApiDiscordPlayStar,
    ApiFiorygiStar,
    ApiDiarioRandomStar,
    ApiPollStar,
    ApiPollsListStar,
    ApiCvstatsLatestStar,
    ApiCvstatsAvgStar,
    ApiUserRygStar,
]

# Don't change this, it should automatically generate __all__
__all__ = [star.__name__ for star in available_page_stars]
