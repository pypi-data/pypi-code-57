from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from royalnet.backpack.tables import *
from ..tables import *
from royalnet.constellation.api import *


class ApiWikiListStar(ApiStar):
    path = "/api/wiki/list/v1"

    summary = "Get a list of available wiki pages."

    tags = ["wiki"]

    async def api(self, data: ApiData) -> JSON:
        pages: typing.List[WikiPage] = await asyncify(data.session.query(self.alchemy.get(WikiPage)).all)
        return [page.json_list() for page in sorted(pages, key=lambda p: p.title)]
