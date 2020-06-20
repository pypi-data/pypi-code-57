import royalnet.constellation.api as rca
import royalnet.utils as ru
import royalnet.backpack.tables as rbt
from .api_user_get_ryg import ApiUserGetRygStar


class ApiUserFindRygStar(ApiUserGetRygStar):
    summary = "Ottieni le informazioni su un utente della Royal Games."

    description = ""

    methods = ["GET"]

    path = "/api/user/find/ryg/v1"

    requires_auth = False

    parameters = {"alias": "L'alias dell'utente di cui vuoi vedere le informazioni."}

    tags = ["user"]

    async def get_user(self, data: rca.ApiData):
        user = await rbt.User.find(self.alchemy, data.session, data["alias"])
        if user is None:
            raise rca.NotFoundError("No such user.")
        return user

    async def api(self, data: rca.ApiData) -> dict:
        user = await self.get_user(data)
        result = {
            **user.json(),
            "bio": user.bio.json() if user.bio is not None else None,
            "fiorygi": user.fiorygi.fiorygi if user.fiorygi is not None else None,
            "steam": [steam.json() for steam in user.steam],
            "leagueoflegends": [leagueoflegends.json() for leagueoflegends in user.leagueoflegends],
            "trivia": user.trivia_score.json() if user.trivia_score is not None else None
        }
        return result
