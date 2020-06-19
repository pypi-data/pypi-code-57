import royalnet.utils as ru
from royalnet.backpack.tables import *
from royalnet.constellation.api import *
from ..tables import Cvstats


class ApiCvstatsLatestStar(ApiStar):
    path = "/api/cvstats/latest/v1"

    methods = ["GET"]

    summary = "Get the latest 500 cvstats."

    tags = ["cvstats"]

    async def api(self, data: ApiData) -> ru.JSON:
        CvstatsT = self.alchemy.get(Cvstats)

        cvstats = data.session.query(CvstatsT).order_by(CvstatsT.timestamp.desc()).limit(500).all()

        return list(map(lambda c: c.json(), cvstats))
