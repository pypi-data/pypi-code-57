from typing import *
from royalnet.utils import *
from royalnet.backpack.tables import *
from royalnet.constellation.api import *
from ..tables import Fiorygi


class ApiFiorygiStar(ApiStar):
    path = "/api/fiorygi/v2"

    parameters = {
        "get": {
            "uid": "The user to get the fiorygi of."
        }
    }

    tags = ["fiorygi"]

    async def get(self, data: ApiData) -> JSON:
        """Get fiorygi information about a specific user."""
        user = await User.find(self.alchemy, data.session, data.int("uid"))
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
