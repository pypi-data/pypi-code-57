from royalnet.constellation.api import *
from royalnet.utils import *
from ..tables import *


class ApiDiarioGetStar(ApiStar):
    path = "/api/diario/get/v1"

    summary = "Get the diario entry with a specific id."

    parameters = {
        "id": "The id of the diario entry to get."
    }

    tags = ["diario"]

    async def api(self, data: ApiData) -> dict:
        try:
            diario_id = int(data["id"])
        except ValueError:
            raise InvalidParameterError("'id' is not a valid int.")
        entry: Diario = await asyncify(data.session.query(self.alchemy.get(Diario)).get, diario_id)
        if entry is None:
            raise NotFoundError("No such diario entry.")
        return entry.json()
