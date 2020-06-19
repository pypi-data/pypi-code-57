from typing import *
import datetime
import uuid
from royalnet.utils import *
from royalnet.constellation.api import *
from ..tables import Poll


class ApiPollsCreate(ApiStar):
    path = "/api/polls/create/v1"

    summary = "Create a new poll."

    parameters = {
        "question": "The question to ask in the poll.",
        "description": "A longer Markdown-formatted description.",
        "expires": "A ISO timestamp of the expiration date for the poll.",
    }

    requires_auth = True

    methods = ["POST"]

    tags = ["polls"]

    async def api(self, data: ApiData) -> JSON:
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
