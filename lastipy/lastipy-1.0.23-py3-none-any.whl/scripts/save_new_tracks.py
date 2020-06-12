#!/usr/bin/env python3.7

from configparser import ConfigParser
import argparse
import os
from lastipy import definitions
from lastipy.lastfm.library.top_tracks import fetch_top_tracks
from lastipy.lastfm.recommendations.similar_tracks import fetch_similar_tracks
from lastipy.lastfm.recommendations.recommendations import fetch_recommendations
from lastipy.lastfm.library.recent_tracks import fetch_recent_tracks
from lastipy.lastfm.library.recent_artists import fetch_recent_artists
from lastipy.lastfm.library import period
from lastipy.spotify import playlist, search, library
from lastipy.track import Track
from numpy.random import choice
from spotipy import Spotify
from lastipy.spotify import token
from lastipy.util.setup_logging import setup_logging
import logging
from lastipy.spotify import new_releases
from datetime import datetime
from lastipy.util.parse_api_keys import ApiKeysParser


def save_new_tracks():
    """Saves new tracks (as of the current date) from the specified Spotify user's followed artists to their library"""

    setup_logging("new_releases.log")
    args = _extract_args()
    spotify = Spotify(auth=token.get_token(args.spotify_user, args.spotify_client_id_key, args.spotify_client_secret_key))

    new_tracks = new_releases.fetch_new_tracks(spotify)

    if len(new_tracks) > 0:
        # Only process further if we actually fetched any new tracks; otherwise there's no point

        # Filter out new tracks that are already saved in the library
        tracks_to_save = _filter_out_already_saved_tracks(spotify, new_tracks)

        library.add_tracks_to_library(spotify, tracks_to_save)
    else:
        logging.info("No new tracks to add!")

    logging.info("Done!")

def _filter_out_already_saved_tracks(spotify, new_tracks):
    saved_tracks = library.get_saved_tracks(spotify)
    logging.info("Filtering out already saved tracks from new tracks")
    tracks_to_save = [new_track for new_track in new_tracks 
                        if not any(new_track == saved_track for saved_track in saved_tracks)]
    return tracks_to_save

def _extract_args():
    args = _parse_args()

    # Parse API keys file
    keys_parser = ApiKeysParser(args.api_keys_file)
    args.spotify_client_id_key = keys_parser.spotify_client_id_key
    args.spotify_client_secret_key = keys_parser.spotify_client_secret_key
    
    return args

def _parse_args():
    args_parser = argparse.ArgumentParser(description="Adds new tracks from followed artists to a Spotify playlist")
    args_parser.add_argument('spotify_user', type=str)
    args_parser.add_argument('api_keys_file', type=argparse.FileType('r', encoding='UTF-8'))
    return args_parser.parse_args()

if __name__ == "__main__":
    save_new_tracks()