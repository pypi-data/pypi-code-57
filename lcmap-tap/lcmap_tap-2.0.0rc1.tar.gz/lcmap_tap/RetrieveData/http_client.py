"""
http_client - provide common http request functions.
"""
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def setup_session(retry_count=3, backoff=1):
    """
    Configures a requests session with retries and backoff.
    Args: retry_count: int num times to retry request.
          backoff: int sleep (seconds) in between retries.
    Returns: The requests session object.
    """
    session = requests.Session()
    retries = Retry(
        total=retry_count, backoff_factor=backoff, status_forcelist=[502, 503, 504]
    )
    session.mount("http://", HTTPAdapter(max_retries=retries))
    return session


def try_download(session, obj_key, timeout_secs=5, params=None):
    """
    A common object downloader wrapped in a try.
    Gets the object and decodes it.
    Args:
        session: A requests session object.
        key: The full path to the object key.
        timeout_secs: An integer of the timeout in seconds.
        params: Any query paramaters to send to endpoint.
    Returns: The requests response object or an empty list if errors.
    """
    try:
        result = decode(get_object(session, obj_key, timeout_secs, params))
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL) as e:
        print("-> Error downloading object!", e)
        return []
    return result


def get_object(session, key, timeout_secs=5, params=None):
    """
    Download an object via a session.
    Args:
        session: A requests session object.
        key: The full path to the object key.
        timeout_secs: An integer of the timeout in seconds.
        params: Any query paramaters to send to endpoint.
    Returns The requests response object.
    """
    return session.get(key, timeout=timeout_secs, params=params)


def decode(result):
    """
    Decodes a request/session object into json.
    Args: result: The object returned from a session or request get.
    Returns: The json loaded content.
    """
    if result.status_code == 200:
        return json.loads(result.content)
    return []
