import re
from logging import getLogger
from typing import Optional
import requests
from bs4 import BeautifulSoup, Tag, ResultSet

from .result import Result


requests.adapters.DEFAULT_RETRIES = 100
logger = getLogger(__name__)


def _select_from(title: str, artist: str, results: ResultSet) -> Optional[str]:
    choice = -3

    url = None

    while choice >= len(results) or choice < -2:
        print(f"{title} / {artist}")
        for i, result in enumerate(results):
            print(f"{i}: {result.text}")
        print("-1: Others")
        print("-2: Skip")
        try:
            choice = int(input("Enter your choice:"))
        except ValueError:
            pass

    if choice == -1:
        path = input("Enter (artist/lyrics):")
        url = f"http://j-lyric.net/artist/{path}.html"

    if choice != -2:
        url = results[choice]["href"]

    return url


def _search_page(
    title: str, artist: str, url: str, first: bool, request: dict
) -> Optional[str]:
    params = {
        "ct": 2,
        "kt": title,
        "ca": 2,
        "ka": artist,
        "cl": 2,
        "kl": "",
    }
    response = requests.get(url, params=params, **request)
    if not response.ok:
        return None
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.select("#mnb > div.bdy > p.mid > a")
    if len(results) == 0:
        return None

    if len(results) == 1 or first:
        return results[0]["href"]

    # Title exact match
    exact = [r for r in results if r.text == title]
    if len(exact) == 1:
        return exact[0]["href"]

    return _select_from(title=title, artist=artist, results=results)


def search(
    title: str,
    artist: str,
    url: str = "http://search.j-lyric.net/index.php",
    first: bool = False,
    request: Optional[dict] = None,
) -> Optional[Result]:
    if request is None:
        request = {}
    result_url = _search_page(
        title=title, artist=artist, url=url, first=first, request=request
    )
    if result_url is None:
        logger.error("Fail to search for %s, %s", title, artist)
        return None

    response = requests.get(url, timeout=60, **request)
    if not response.ok:
        logger.error("Fail to load %s", url)
        return None
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    result = Result()

    mnb = soup.select_one("#mnb")
    lyric_tag = soup.select_one("#Lyric")
    for br in lyric_tag.find_all("br"):
        br.replace_with("\r\n")
    result.lyric = lyric_tag.text
    for sm1 in mnb.select(".lbdy > .sml"):  # type: Tag
        text = sm1.get_text()
        match = re.search("作曲：(.*)", text, re.IGNORECASE)
        if match is not None:
            text = match.group(1)
            if text != "":
                result.composers.extend(text.split("/"))
            continue
        match = re.search("作詞：(.*)", text, re.IGNORECASE)
        if match is not None:
            text = match.group(1)
            if text != "":
                result.lyricists.extend(text.split("/"))
            continue
    if len(result.composers) <= 0:
        logger.warning("No composers for %s/%s (%s)", title, artist, url)
    if len(result.lyricists) <= 0:
        logger.warning("No lyricists for %s/%s (%s)", title, artist, url)

    return result
