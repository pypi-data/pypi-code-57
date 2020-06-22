from .resources import CONFIG
from .exceptions import UndefinedError, InvalidAuthorization, \
    NotFound, InternalError, InvalidJson, InvalidServerPayload,\
    ServerNotRunning, NoHistoricalData


class AWR:
    def __init__(self, route, **kwargs):
        self.route = route
        self.kwargs = kwargs

    async def _raise_exception(self, resp):
        error_details = await resp.json()
        error_details = error_details["error_details"]

        if error_details["code"] == 1000 or error_details["code"] == 1004:
            raise InvalidAuthorization(error_details["message"])
        elif error_details["code"] == 2012:
            raise InvalidServerPayload(error_details["message"])
        elif error_details["code"] == 2001:
            raise ServerNotRunning(error_details["message"])
        elif error_details["code"] == 2003:
            raise NoHistoricalData(error_details["message"])
        elif error_details["code"] == 1001:
            raise NotFound(error_details["message"])
        elif error_details["code"] == 1002:
            raise InternalError(error_details["message"])
        elif error_details["code"] == 1003:
            raise InvalidJson(error_details["message"])
        else:
            raise UndefinedError(error_details["message"])

    async def _check(self, resp):
        if resp.status == 200:
            return await resp.json()
        else:
            await self._raise_exception(resp)

    async def get(self):
        async with CONFIG.session.get(
            self.route,
            headers=CONFIG.api_key,
            **self.kwargs
        ) as resp:
            return await self._check(resp)

    async def delete(self, json=True):
        async with CONFIG.session.delete(
            self.route,
            headers=CONFIG.api_key,
            **self.kwargs
        ) as resp:
            if json:
                return await self._check(resp)

    async def put(self, json=True):
        async with CONFIG.session.put(
            self.route,
            headers=CONFIG.api_key,
            **self.kwargs
        ) as resp:
            if json:
                return await self._check(resp)

    async def post(self, json=True):
        async with CONFIG.session.post(
            self.route,
            headers=CONFIG.api_key,
            **self.kwargs
        ) as resp:
            if json:
                return await self._check(resp)
