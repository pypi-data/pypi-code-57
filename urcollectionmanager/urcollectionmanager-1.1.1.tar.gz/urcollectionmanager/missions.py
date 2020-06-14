from .mission import Mission

import itertools
from urllib.parse import urlencode
from enum import Enum
from bs4 import BeautifulSoup

BASE_MISSION_URL = "https://www.urban-rivals.com/missions/missions_page.php?"


def get_mission_url(page_num: int, category: str, mission_status: str, url) -> str:
    """Returns a url for the requested parameters"""
    url = BASE_MISSION_URL if url is None else url
    category = "all" if category == "" else category
    return url + urlencode({'page': 0 if page_num is None else page_num,
                            'category': _convert_mission_category(category).value,
                            'state': _convert_mission_status(mission_status),
                            'sortby': 'date'})


def find_missions(page: BeautifulSoup):
    """Returns list of Mission based on each row in the
    given BeautifulSoup missions page"""
    return [create_mission(row) for row in page.find_all("ul")[2].find_all("li")]


def create_mission(row):
    """Creates Mission object based on BeautifulSoup list item object"""
    name = next(itertools.islice(row.stripped_strings, 0, 1))
    description = next(itertools.islice(row.stripped_strings, 1, 2))
    total_progress = next(itertools.islice(row.stripped_strings, 2, 3))
    try:
        progress, goal = str(total_progress).split("/")
    except BaseException:
        progress = 0
        goal = 0
    return Mission(name=name,
                   description=description,
                   progress=progress,
                   goal=goal
                   )


def _convert_mission_category(category: str) -> int:
    try:
        return MissionCategory[category.upper().replace(" ", "_")]
    except BaseException:
        # No matching category
        raise ValueError(f"{category} is not a supported mission category.")


def _convert_mission_status(mission_status: str) -> str:
    if "progress" in mission_status.lower():
        return "inprogress"
    elif "complete" in mission_status.lower() or \
         "done" in mission_status.lower():
        return "done"
    return 'all'


class MissionCategory(Enum):
    ALL = 0
    FIGHTS = 3
    EVOLUTION = 6
    COLLECTION = 7
    ALL_STARS = 8
    BANGERS = 9
    FANG_PI_CLANG = 10
    FREAKS = 11
    GHEIST = 12
    JUNGO = 13
    JUNKZ = 14
    LA_JUNTA = 15
    MONTANA = 16
    NIGHTMARE = 17
    PIRANAS = 18
    PUSSYCATS = 19
    RESCUE = 20
    ROOTS = 21
    SAKROHM = 22
    SENTINEL = 23
    SKEELZ = 24
    ULU_WATU = 25
    UPPERS = 26
    VORTEX = 27
    LEGENDARIES = 28
    DAMAGE = 29
    PILLZ = 30
    INTOXICATION = 31
    HEALING = 32
    TOURNAMENTS = 33
    SURVIVOR = 34
    ELO = 35
    BERZERK = 37
    FROZN = 39
    HURACAN = 41
    RIOTS = 42
    FLASH = 43
    LEADER = 44
    RAPTORS = 45
    HIVE = 47
    GHOSTOWN = 49
    TUTORIAL = 50
    DOMINION = 51
    KOMBOKA = 53
    PARADOX = 54
