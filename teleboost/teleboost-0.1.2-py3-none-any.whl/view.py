import asyncio
import distutils.util
import re
from typing import List

from aiohttp import ClientSession, DummyCookieJar, ClientResponse
from aiosocksy.connector import ProxyConnector, ProxyClientRequest

from .misc import user_agent_provider, key_re
from .models import ViewResult


class TeleboostViewer:
    def __init__(self, proxies: List[str], channel: str, post_id: int, view_count: int):
        self.proxies = proxies
        self.channel = channel
        self.post_id = post_id
        self.view_count = view_count
        self.semaphore = asyncio.Semaphore(1000)

    async def add_view(self, session: ClientSession, proxy: str, user_agent: str):
        async with session.get(
            f"https://t.me/{self.channel}/{self.post_id}",
            params={"embed": 1},
            proxy=proxy,
            headers={"User-Agent": user_agent},
        ) as response:  # type: ClientResponse
            cookies = response.cookies
            embed_post = await response.text()

        res = re.search(key_re, embed_post)
        if res is None:
            return ViewResult(ok=False, proxy=proxy, error="Key not found")
        key = res.group(1)

        async with session.get(
            f"https://t.me/v/",
            params={"views": key},
            proxy=proxy,
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"https://t.me/{self.channel}/{self.post_id}?embed=1",
            },
            cookies=cookies,
        ) as response:  # type: ClientResponse
            result = await response.text()

        ok = distutils.util.strtobool(result)
        return ViewResult(
            ok=ok, proxy=proxy, error=not ok and "Invalid telegram response"
        )

    async def safe_add_view(self, session: ClientSession, proxy: str, user_agent: str):
        async with self.semaphore:
            try:
                return await self.add_view(session, proxy, user_agent)
            except Exception as ex:
                return ViewResult(ok=False, proxy=proxy, error=str(ex))

    def prepare_tasks(self, session: ClientSession, safe: bool = True):
        if safe:
            add_view = self.safe_add_view
        else:
            add_view = self.add_view

        tasks = []
        for proxy in self.proxies[: self.view_count]:
            tasks.append(
                add_view(
                    session,
                    proxy,
                    user_agent=user_agent_provider.get_random_user_agent(),
                )
            )
        return tasks

    async def __aiter__(self):
        # TODO: rework proxy
        async with ClientSession(
            cookie_jar=DummyCookieJar(),
            connector=ProxyConnector(),
            request_class=ProxyClientRequest,
        ) as session:
            tasks = self.prepare_tasks(session)
            for result in asyncio.as_completed(tasks):
                yield await result

    async def run(self):
        # TODO: rework proxy
        async with ClientSession(
            cookie_jar=DummyCookieJar(),
            connector=ProxyConnector(),
            request_class=ProxyClientRequest,
        ) as session:
            tasks = self.prepare_tasks(session)
            return await asyncio.gather(*tasks)
