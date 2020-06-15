import logging, requests
from lastipy.lastfm.library import period
from lastipy.lastfm.parse_lastfm_tracks import parse_track_name, parse_artist
from lastipy.lastfm.library.scrobbled_track import ScrobbledTrack

URL = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks'


def fetch_top_tracks(user, api_key, a_period=period.OVERALL):
    """Fetches the top tracks for the given user over the given period"""

    page = 1
    all_top_tracks = []
    keep_fetching = True
    logging.info("Fetching top tracks for user " + user + " over period " + a_period)
    while keep_fetching:
        json_response = _send_request(_build_json_payload(user, api_key, a_period, page))
        json_tracks = json_response['toptracks']['track']
        top_tracks = [ScrobbledTrack(parse_track_name(json_track), parse_artist(json_track), int(json_track['playcount']))
                      for json_track in json_tracks]
        
        # Filter out tracks with a playcount of 1, since those shouldn't be considered "top"
        top_tracks = [track for track in top_tracks if track.playcount > 1]
        
        logging.debug("Fetched " + str(top_tracks))
        
        all_top_tracks = all_top_tracks + top_tracks
        page = page + 1
        if not top_tracks:
            keep_fetching = False

    logging.info("Fetched " + str(len(all_top_tracks)) + " top tracks")
    logging.debug("Fetched tracks: " + str(all_top_tracks))
    return all_top_tracks

def _send_request(json_payload):
    response = requests.get(URL, params=json_payload)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def _build_json_payload(user, api_key, period, page):
    payload = {
        'user': user,
        'api_key': api_key,
        'format': 'json',
        'period': period,
        'page': page
    }
    return payload

