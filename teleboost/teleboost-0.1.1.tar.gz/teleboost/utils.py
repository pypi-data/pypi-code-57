import re
from pathlib import Path
from typing import List, Tuple, Union
from yarl import URL

from .misc import post_url_re


__all__ = ("parse_telegram_post_url", "read_file_lines")
ALLOWED_PROXY_SCHEME = ("http", "socks5", "socks4", "socks4a")


def parse_telegram_post_url(url: str) -> Tuple[str, int]:
    res = re.search(post_url_re, url)
    if res is None:
        raise Exception("Invalid url")
    channel, post_id = res.groups()
    return channel, int(post_id)


def read_file_lines(path: Union[str, Path]) -> List[str]:
    lines = []

    with open(path) as file:
        for line in file.read().splitlines():
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue

            proxy_url = URL(line)
            if not proxy_url.is_absolute():
                # TODO: logger.warn(...)
                proxy_url = URL(f"http://{line}")
            if proxy_url.scheme not in ALLOWED_PROXY_SCHEME:
                # TODO: logger.warn(...)
                continue
            lines.append(line)

    return lines
