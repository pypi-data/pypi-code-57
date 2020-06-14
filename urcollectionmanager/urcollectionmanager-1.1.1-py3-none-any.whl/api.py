from .auth import create_auth_url
from .database import init_sqlite_db, add_all, get_all
from .http import execute_http_call, convert_html_to_soup
from .history import get_history_url, find_purchases
from .missions import get_mission_url, find_missions
from .mission import Mission
from .purchase import Purchase

from requests import Session, Response
from typing import Optional, List, Dict
from bs4 import BeautifulSoup


def session_connect_to_ur(session: Session, username: str, password: str, url: Optional[str] = None) -> Response:
    """Creates an authenticated session with Urban Rivals"""
    return execute_http_call(session, create_auth_url(username, password, url))


def get_purchase_history(session: Session, num_pages: int, url: Optional[str] = None) -> List[BeautifulSoup]:
    """Returns a list of Beautiful Soup objects
    representing each Purchase History page"""
    return [convert_html_to_soup(execute_http_call(session, hist_url))
            for hist_url
            in get_history_url(num_pages, url)]


def convert_purchase_history(history_pages: List[BeautifulSoup]) -> List[List[Purchase]]:
    """Returns a list of Purchases for each
    page in a given list of Beautiful Soup
    history pages"""
    return [find_purchases(page) for page in history_pages]

# Write History to File


def connect_and_initialize_database(database_type: str, database_path: Optional[str] = None):
    """Connect and initialize db
    :param database_type:
        Type of target database. See `Supported Types` list for valid values
    :param database_path:
        URL to target database. For sqlite, this should be a str converted pathlib.Path structure
    :Supported Types:
        sqlite
    """
    if database_type.lower() == "sqlite":
        init_sqlite_db(database_path)
    else:
        raise NotImplementedError(f"{database_type} is not supported. "
                                  f"Please see docs for supported types.")


def write_history_to_database(purchases: List[Purchase], batch_size=100):
    """
    Writes a list of Purchases to database. This process uses a hash
    of id, price, level, and purchase date to avoid duplicates.
    :param purchases: List of Purchase objects to add to the database
    :param batch_size: How many Purchase objects should be persisted at one time. Default 100.
    :return: None
    """
    add_all(Purchase, purchases, batch_size)

# Get Purchases from File


def get_history_from_database(filters: Optional[Dict[str, any]] = {}) -> List[Purchase]:
    """
    Retrieves a list of Purchases from the database based on filters provided
    :param filters: A set of equality filters based on Purchase attributes.
    :return: List[Purchase]
    """
    if "purchase_date" in filters:
        filters["_purchase_date"] = filters.pop("purchase_date")
    return get_all(Purchase, filters)


def get_missions_list(session: Session, category: str, url: Optional[str] = None) -> BeautifulSoup:
    """
    Returns a BeautifulSoup object with the requested missions page data
    :param session: The authenticated session
    :param category: Category, if any, to filter missions by
    :param url: Optional URL to direct requests to
    :return: BeautifulSoup of missions page
    """
    mission_url = get_mission_url(0, category, 'all', url)
    return convert_html_to_soup(execute_http_call(session, mission_url))


def convert_missions(missions: BeautifulSoup) -> List[Mission]:
    """
    Create Mission objects based on contents of BeautifulSoup object
    :param missions: The BeautifulSoup object to parse
    :return: List of Mission objects
    """
    return find_missions(missions)


def write_missions_to_database(missions: List[Mission], batch_size=100):
    """
    Writes a list of Missions to database. This process uses a hash
    of name and description to avoid duplicates. Name changes (CR, MT)
    not supported at this time.
    :param purchases: List of Mission objects to add to the database
    :param batch_size: How many Mission objects should be persisted at one time. Default 100.
    :return: None
    """
    add_all(Mission, missions, batch_size)


def get_missions_from_database(filters: Optional[Dict[str, any]] = {}) -> List[Mission]:
    """
    Retrieves a list of Missions from the database based on filters provided
    :param filters: A set of equality filters based on Mission attributes.
    :return: List[Mission]
    """
    return get_all(Mission, filters)
# TODO: Attempt to use UR API
# TODO: Check if session token can be saved permanently
# This will skip using market scraper
