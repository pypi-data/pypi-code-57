import logging
import requests
from lastipy.lastfm.recommendations.recommended_track import RecommendedTrack
from lastipy.lastfm.parse_lastfm_tracks import parse_track_name, parse_artist

URL = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar'


def fetch_similar_tracks(api_key, track, limit):
    """Fetches tracks similar to the given track"""

    logging.info("Fetching up to " + str(limit) + " tracks similar to " + str(track))
    json_response = _send_request(_build_json_payload(api_key, track, limit))
    if 'similartracks' in json_response:
        json_tracks = json_response['similartracks']['track']
        # Initialize the track's recommendation rating to the "match" attribute from Last.fm, which is sort of an index of
        # how similar a track is to another
        similar_tracks = [RecommendedTrack(parse_track_name(json_track), parse_artist(json_track), float(json_track['match'])) 
                          for json_track in json_tracks]
        logging.info("Fetched " + str(len(similar_tracks)) + " similar tracks")
        logging.debug("Fetched tracks: " + str(similar_tracks))
        return similar_tracks
    elif 'errors' in json_response:
        raise Exception("Error occurred while fetching similar tracks " + json_response['errors'])

def _send_request(json_payload):
    response = requests.get(URL, params=json_payload)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def _build_json_payload(api_key, track, limit):
    payload = {
        'track': track.track_name,
        'artist': track.artist,
        'format': 'json',
        'api_key': api_key,
        'limit': limit
    }
    return payload
