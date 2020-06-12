import logging
import requests
from lastipy.lastfm.library.scrobbled_track import ScrobbledTrack
from requests import RequestException

URL = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo'
MAX_RETRIES = 10


def fetch_playcount(track, user, api_key):
    retries = 0
    while retries <= MAX_RETRIES:
        try:
            json_response = _send_request(_build_payload(track, user, api_key))
            break
        except RequestException:
            # This endpoint throws error 500 sometimes, so retry it a few times if it does
            if retries < MAX_RETRIES:
                logging.warn("Failed to fetch playcount for track " + track + ". Retrying...")
                retries += 1
            else:
                raise Exception("Failed to fetch playcount after " + retries + " retries")
    
    if 'track' in json_response:
        playcount = int(json_response['track']['userplaycount'])
        logging.debug(user + " has played " + str(track) + " " + str(playcount) + " times")
        return playcount
    else:
        raise Exception(json_response['error'])

def _send_request(json_payload):
    response = requests.get(URL, params=json_payload)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status() 


def _build_payload(track, user, api_key):
    payload = {
        'username': user,
        'api_key': api_key,
        'format': 'json',
        'track': track.track_name,
        'artist': track.artist,
        'autocorrect': 1
    }
    return payload