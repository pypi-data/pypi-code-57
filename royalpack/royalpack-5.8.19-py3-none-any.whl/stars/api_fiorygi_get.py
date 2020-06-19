from typing import *
from royalnet.utils import *
from royalnet.backpack.tables import *
from royalnet.constellation.api import *
from ..utils import find_user_api
from ..tables import Fiorygi, FiorygiTransaction


class ApiFiorygiGetStar(ApiStar):
    path = "/api/user/fiorygi/get/v1"

    summary = "Get the fiorygi of a Royalnet user."

    parameters = {
        "id": "The user to get the fiorygi of."
    }

    tags = ["user"]

    async def api(self, data: ApiData) -> JSON:
        user: User = await find_user_api(data["id"], self.alchemy, data.session)
        if user.fiorygi is None:
            return {
                "fiorygi": 0,
                "transactions": [],
                "warning": "No associated fiorygi table"
            }
        fiorygi: Fiorygi = user.fiorygi
        transactions: JSON = sorted(fiorygi.transactions, key=lambda t: -t.id)
        return {
            "fiorygi": fiorygi.fiorygi,
            "transactions": list(map(lambda t: {
                "id": t.id,
                "change": t.change,
                "reason": t.reason,
                "timestamp": t.timestamp.isoformat() if t.timestamp else None
            }, transactions))
        }
