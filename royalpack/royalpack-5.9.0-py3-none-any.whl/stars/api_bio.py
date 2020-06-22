import royalnet.utils as ru
from royalnet.backpack.tables import *
from royalnet.constellation.api import *
from ..tables import Bio


class ApiBioSetStar(ApiStar):
    path = "/api/bio/v2"

    methods = ["GET", "PUT"]

    parameters = {
        "get": {
            "uid": "The id of the user to get the bio of."
        },
        "put": {
            "contents": "The contents of the bio."
        }
    }

    auth = {
        "get": False,
        "put": True,
    }

    tags = ["bio"]

    async def get(self, data: ApiData) -> ru.JSON:
        """Get the bio of a specific user."""
        user = await User.find(self.alchemy, data.session, data.int("uid"))
        return user.bio.json() if user.bio else None

    async def put(self, data: ApiData) -> ru.JSON:
        """Set the bio of current user."""
        contents = data["contents"]
        BioT = self.alchemy.get(Bio)
        user = await data.user()
        bio = user.bio
        if bio is None:
            bio = BioT(user=user, contents=contents)
            data.session.add(bio)
        else:
            bio.contents = contents
        await data.session_commit()
        return bio.json()
