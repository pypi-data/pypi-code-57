from typing import *
import datetime
import uuid
from royalnet.utils import *
from royalnet.constellation.api import *
from ..tables import Poll


class ApiPollStar(ApiStar):
    path = "/api/poll/v2"

    parameters = {
        "get": {
            "uuid": "The UUID of the poll to get.",
        },
        "post": {
            "question": "The question to ask in the poll.",
            "description": "A longer Markdown-formatted description.",
            "expires": "A ISO timestamp of the expiration date for the poll.",
        }
    }

    auth = {
        "get": False,
        "post": True
    }

    methods = ["GET", "POST"]

    tags = ["poll"]

    async def get(self, data: ApiData) -> JSON:
        """Get a specific poll."""
        PollT = self.alchemy.get(Poll)

        try:
            pid = uuid.UUID(data["uuid"])
        except (ValueError, AttributeError, TypeError):
            raise InvalidParameterError("'uuid' is not a valid UUID.")

        poll: Poll = await asyncify(data.session.query(PollT).get, pid)
        if poll is None:
            raise NotFoundError("No such page.")

        return poll.json()

    async def post(self, data: ApiData) -> JSON:
        """Create a new poll."""
        PollT = self.alchemy.get(Poll)

        poll = PollT(
            id=uuid.uuid4(),
            creator=await data.user(),
            created=datetime.datetime.now(),
            expires=datetime.datetime.fromisoformat(data["expires"]) if "expires" in data else None,
            question=data["question"],
            description=data.get("description"),
        )

        data.session.add(poll)
        await data.session_commit()

        return poll.json()
