from lastipy.spotify import library
from spotipy import Spotify
from lastipy.spotify import token



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
from lastipy.track import Track
from numpy.random import choice
from spotipy import Spotify
from lastipy.spotify import token
from lastipy.util.setup_logging import setup_logging
import logging
from lastipy.util.parse_api_keys import ApiKeysParser
from lastipy.spotify import library, search, playlist
from lastipy.lastfm.library import track_info

#TODO parameterize these?
library_playcount_limit = 3
playlist_a = 'New Favorites'
playlist_a_playcount_limit = 7
playlist_b = 'Old Favorites'


def organize_favorites():
    """Organizes a user's Spotify library by placing more-listened-to tracks in other playlists"""

    setup_logging('organize_favorites.log')
    args = _extract_args()
    spotify = Spotify(auth=token.get_token(args.spotify_user, args.spotify_client_id_key, args.spotify_client_secret_key))

    logging.info("Organizing " + args.spotify_user + "'s favorites")

    saved_tracks = library.get_saved_tracks(spotify)
    saved_tracks_to_move = []
    for saved_track in saved_tracks:
        try:
            playcount = track_info.fetch_playcount(saved_track, args.lastfm_user, args.lastfm_api_key)
            if playcount >= library_playcount_limit:
                saved_tracks_to_move.append(saved_track)
        except:
            logging.warn("Couldn't get playcount for track " + str(saved_track))

    logging.info("Moving " + str(len(saved_tracks_to_move)) + " tracks from library to " + playlist_a)
    library.remove_tracks_from_library(spotify, saved_tracks_to_move)
    playlist.add_tracks_to_playlist(spotify, playlist_a, saved_tracks_to_move)

    tracks_in_playlist = playlist.get_tracks_in_playlist(spotify, playlist_name=playlist_a)
    playlist_tracks_to_move = []
    for playlist_track in tracks_in_playlist:
        try:
            playcount = track_info.fetch_playcount(playlist_track, args.lastfm_user, args.lastfm_api_key)
            if playcount >= playlist_a_playcount_limit:
                playlist_tracks_to_move.append(playlist_track)
        except:
            logging.warn("Couldn't get playcount for track " + str(playlist_track))
    
    logging.info("Moving " + str(len(playlist_tracks_to_move)) + " tracks from " + playlist_a + " to " + playlist_b)
    playlist.remove_tracks_from_playlist(spotify, playlist_a, playlist_tracks_to_move)
    playlist.add_tracks_to_playlist(spotify, playlist_b, playlist_tracks_to_move)

    logging.info("Done!")


def _extract_args():
    args_parser = _setup_args_parser()
    args = args_parser.parse_args()
    args = _extract_user_configs(args)
    args = _extract_api_keys(args)
    return args


def _setup_args_parser():
    parser = argparse.ArgumentParser(description="Organize Spotify saved tracks by removing tracks with a certain playcount from liked tracks and moving them to other playlists")
    parser.add_argument('user_configs_file', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('api_keys_file', type=argparse.FileType('r', encoding='UTF-8'))
    return parser


def _extract_user_configs(args):
    config_parser = ConfigParser()
    config_parser.read(args.user_configs_file.name)
    section = 'Config'
    args.lastfm_user = config_parser[section]['LastFMUser']
    args.spotify_user = config_parser[section]['SpotifyUser']
    return args


def _str_to_bool(to_convert):
    return to_convert == "True"


def _extract_api_keys(args):
    keys_parser = ApiKeysParser(args.api_keys_file)
    args.lastfm_api_key = keys_parser.lastfm_api_key
    args.spotify_client_id_key = keys_parser.spotify_client_id_key
    args.spotify_client_secret_key = keys_parser.spotify_client_secret_key
    return args


if __name__ == "__main__":
    organize_favorites()