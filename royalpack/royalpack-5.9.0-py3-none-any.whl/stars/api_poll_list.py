from typing import *
from royalnet.utils import *
from royalnet.constellation.api import *
from ..tables import Poll
import uuid


class ApiPollsListStar(ApiStar):
    path = "/api/poll/list/v2"

    tags = ["poll"]

    async def get(self, data: ApiData) -> JSON:
        """Get a list of all polls."""
        PollT = self.alchemy.get(Poll)

        polls: List[Poll] = await asyncify(data.session.query(PollT).all)

        return list(map(lambda p: {
            "id": p.id,
            "question": p.question,
            "creator": p.creator.json(),
            "expires": p.expires.isoformat(),
            "created": p.created.isoformat(),
        }, polls))
