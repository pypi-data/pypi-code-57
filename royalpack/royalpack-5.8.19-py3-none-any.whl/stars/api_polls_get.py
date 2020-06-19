from typing import *
import datetime
from royalnet.utils import *
from royalnet.constellation.api import *
from ..tables import Poll
import uuid


class ApiPollsGet(ApiStar):
    path = "/api/polls/get/v1"

    summary = "Get the poll with a specific id."

    parameters = {
        "uuid": "The UUID of the poll to get.",
    }

    requires_auth = True

    tags = ["polls"]

    async def api(self, data: ApiData) -> JSON:
        PollT = self.alchemy.get(Poll)

        try:
            pid = uuid.UUID(data["uuid"])
        except (ValueError, AttributeError, TypeError):
            raise InvalidParameterError("'uuid' is not a valid UUID.")

        poll: Poll = await asyncify(data.session.query(PollT).get, pid)
        if poll is None:
            raise NotFoundError("No such page.")

        return poll.json()
