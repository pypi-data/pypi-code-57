import asyncio
import re
from pathlib import Path
from typing import Optional

from cleo import Command  # type: ignore
from yaspin import yaspin  # type: ignore

from ..utils import read_file_lines, parse_telegram_post_url
from ..view import TeleboostViewer

__all__ = ("ViewCommand",)
PROXY_FILES = re.compile(r"proxies(\.txt)?$")


class ViewCommand(Command):
    """
        Adds views to а post

        view
            {url : Telegram post URL}
            {--p|proxies=?* : Proxies file(s)}
            {--c|count=? : How many views do you want to add?}
    """

    def handle(self) -> Optional[int]:
        proxies = self.option("proxies")
        proxies_files = []
        if not proxies:
            for file in Path.cwd().glob("*"):
                if not file.is_file():
                    continue
                if PROXY_FILES.fullmatch(file.name):
                    proxies_files.append(file.name)
            if not proxies_files:
                self.line("<error>Proxies files not found</error>")
                return 1

        proxies_files.extend(proxies)
        proxies_list = []
        for file in proxies_files:
            proxies_list.extend(read_file_lines(file))

        count = self.option("count")
        if count is None:
            count = len(proxies_list)
        elif count.isdecimal():
            count = int(count)
        else:
            self.line("<error>Count argument must be integer</error>")
            return 1

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.view(self.argument("url"), proxies_list, count))
        return 0

    @staticmethod
    async def view(url: str, proxies: list, count: int):
        channel, post_id = parse_telegram_post_url(url)
        viewer = TeleboostViewer(
            proxies=proxies, channel=channel, post_id=post_id, view_count=count
        )

        with yaspin(text="Adding views...").yellow.bold.dots12 as sp:
            c = 1
            async for result in viewer:
                sp.text = f"Adding views... [{c}/{count}]"
                if not result.ok:
                    sp.red.write(f"> {result.error} [{result.proxy}]")
                c += 1

            sp.green.ok("✔")
