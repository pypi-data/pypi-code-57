from lastipy.spotify.parse_spotify_tracks import parse_tracks
from lastipy.spotify.playlist import get_tracks_in_playlist
import spotipy
import logging

MAX_ITEMS_PER_REQUEST = 50


def get_saved_tracks(spotify):
    """Returns the currently-logged-in users's saved tracks"""

    logging.info("Fetching " + spotify.current_user()['id'] + "'s saved tracks")

    saved_tracks = []
    keep_fetching = True
    while keep_fetching:
        json_response = spotify.current_user_saved_tracks(offset=len(saved_tracks))
        if json_response['items']:
            saved_tracks = saved_tracks + parse_tracks(json_response['items'])
        else:
            keep_fetching = False

    logging.info("Fetched " + str(len(saved_tracks)) + " saved tracks")
    logging.debug("Fetched tracks: " + str(saved_tracks))

    return saved_tracks


def add_tracks_to_library(spotify, tracks):
    logging.info("Adding " + str(len(tracks)) + " to " + spotify.current_user()['id'] + "'s library")
    logging.debug("Adding tracks: " + str(tracks))
    track_chunks = _chunk(tracks, MAX_ITEMS_PER_REQUEST) 
    for chunk in track_chunks:
        spotify.current_user_saved_tracks_add([track.spotify_id for track in chunk])
    logging.info("Finished adding tracks")


def remove_tracks_from_library(spotify, tracks):
    logging.info("Removing " + str(len(tracks)) + " from " + spotify.current_user()['id'] + "'s library")
    logging.debug("Removing tracks: " + str(tracks))
    track_chunks = _chunk(tracks, MAX_ITEMS_PER_REQUEST)
    for chunk in track_chunks:
        spotify.current_user_saved_tracks_delete([track.spotify_id for track in chunk])
    logging.info("Finished removing tracks")


def _chunk(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)] 