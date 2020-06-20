from typing import *
from royalnet.utils import *
from royalnet.constellation.api import *
from ..tables import Poll
import uuid


class ApiPollsList(ApiStar):
    path = "/api/polls/list/v1"

    summary = "Get a list of all polls."

    requires_auth = True

    tags = ["polls"]

    async def api(self, data: ApiData) -> JSON:
        PollT = self.alchemy.get(Poll)

        polls: List[Poll] = await asyncify(data.session.query(PollT).all)

        return list(map(lambda p: {
            "id": p.id,
            "question": p.question,
            "creator": p.creator.json(),
            "expires": p.expires.isoformat(),
            "created": p.created.isoformat(),
        }, polls))
