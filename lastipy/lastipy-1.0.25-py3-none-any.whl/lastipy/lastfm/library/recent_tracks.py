import logging
import requests
from lastipy.lastfm.parse_lastfm_tracks import parse_artist, parse_track_name
from lastipy.track import Track
from requests import RequestException

URL = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks'
MAX_RESULTS_PER_PAGE = 200
MAX_RETRIES = 10


#TODO test
def fetch_recent_tracks(user, api_key):
    """Fetches recent tracks for the given user"""

    logging.info("Fetching recent tracks for " + user)
    all_recent_tracks = []
    page = 1
    total_pages = 1
    retries = 0
    while page <= total_pages:
        try:
            json_response = _send_request(_build_json_payload(user, api_key, page))
            logging.debug("Response: " + str(json_response))
            json_tracks = json_response['recenttracks']['track']
            recent_tracks_on_curr_page = [Track(parse_track_name(json_track), parse_artist(json_track))
                                          for json_track in json_tracks]
            all_recent_tracks = all_recent_tracks + recent_tracks_on_curr_page
            total_pages = int(json_response['recenttracks']['@attr']['totalPages'])
            page = page + 1
        except RequestException:
            # This particular endpoint has a habit of throwing back error 500, so just retry if it does
            if retries < MAX_RETRIES:
                logging.warning("Failed to fetch recent tracks page " + str(page) + ". Retrying...")
                retries = retries + 1
            else:
                logging.warning("Failed to fetch recent tracks page " + str(page) +
                                " after " + str(retries) + " retries. Giving up and moving on...")
                break

    logging.info("Fetched " + str(len(all_recent_tracks)) + " recent tracks")
    logging.debug("Fetched tracks: " + str(all_recent_tracks))
    return all_recent_tracks

def _send_request(json_payload):
    response = requests.get(URL, params=json_payload)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def _build_json_payload(user, api_key, page):
    payload = {
        'user': user,
        'format': 'json',
        'api_key': api_key,
        'limit': MAX_RESULTS_PER_PAGE,
        'page': page
    }
    return payload
