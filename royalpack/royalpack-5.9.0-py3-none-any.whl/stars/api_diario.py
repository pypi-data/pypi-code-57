from royalnet.constellation.api import *
from royalnet.utils import *
from ..tables import *


class ApiDiarioGetStar(ApiStar):
    path = "/api/diario/v2"

    parameters = {
        "get": {
            "id": "The id of the diario entry to get."
        }
    }

    tags = ["diario"]

    async def get(self, data: ApiData) -> JSON:
        """Get a specific diario entry."""
        diario_id = data.int("id")
        entry: Diario = await asyncify(data.session.query(self.alchemy.get(Diario)).get, diario_id)
        if entry is None:
            raise NotFoundError("No such diario entry.")
        return entry.json()
