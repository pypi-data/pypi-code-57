from starlette.responses import *
from royalnet.constellation.api import *
from royalnet.utils import *
from ..tables import *


class ApiDiarioPagesStar(ApiStar):
    path = "/api/diario/pages/v1"

    parameters = {
        "get": {
            "page": "The diario page you want to get. Can be negative to get the entries in reverse order."
        }
    }

    tags = ["diario"]

    async def get(self, data: ApiData) -> JSON:
        """Get a diario page made of up to 500 diario entries."""
        page_str = data["page"]
        try:
            page = int(page_str)
        except ValueError:
            raise InvalidParameterError("'page' is not a valid int.")
        if page < 0:
            page = -page-1
            entries: typing.List[Diario] = await asyncify(
                data.session
                    .query(self.alchemy.get(Diario))
                    .order_by(self.alchemy.get(Diario).diario_id.desc()).limit(500)
                    .offset(page * 500)
                    .all
            )
        else:
            entries: typing.List[Diario] = await asyncify(
                data.session
                    .query(self.alchemy.get(Diario))
                    .order_by(self.alchemy.get(Diario).diario_id)
                    .limit(500)
                    .offset(page * 500)
                    .all
            )
        response = [entry.json() for entry in entries]
        return response
