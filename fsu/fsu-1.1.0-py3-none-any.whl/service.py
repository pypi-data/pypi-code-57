from uuid import uuid4

from fastapi import FastAPI, Request

_sym = str(uuid4())

async def create(app : FastAPI, name : str, fn):
    if not hasattr(app.state, _sym):
        setattr(app.state, _sym, {})

    srvs = getattr(app.state, _sym)
    srv  = await fn()

    srvs[name] = srv

async def destroy(app : FastAPI, name : str, fn):
    srvs = getattr(app.state, _sym, {})

    if name in srvs:
        srv = srvs[name]
        await fn(srv)

        del srvs[name]


def get_from_app(app : FastAPI, name : str):
    srvs = getattr(app.state, _sym, {})

    return srvs.get(name)


def get(name : str):
    def get_(request : Request):
        return get_from_app(request.app, name)

    return get_
