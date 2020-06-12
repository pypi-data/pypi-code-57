from guillotina import configure
from guillotina.response import HTTPOk

import json


@configure.service(
    name="@respond",
    method="POST",
    requestBody={
        "required": False,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {"exception": {"type": "boolean", "default": False}},
                }
            }
        },
    },
    validate=True,
)
async def respond(context, request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        data = {}

    if data.get("exception", False):
        raise Exception("foobar")
    return HTTPOk(content={"foo": "bar"})
