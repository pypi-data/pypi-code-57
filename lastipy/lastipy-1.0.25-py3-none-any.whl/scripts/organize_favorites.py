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
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import iso8601

NEW_FAVORITES_PLAYLIST = 'New Favorites'
OLD_FAVORITES_PLAYLIST = 'Old Favorites'
NEGLECTED_PLAYLIST = 'Neglected'


def organize_favorites():
    """Organizes a user's Spotify library. Saved tracks with more than 3 plays are moved to a "New Favorites" playlist. Tracks
       in the "New Favorites" playlist are moved to an "Old Favorites" playlist after 6 months (if they still only have 3
       plays at that point, they're completely removed from the library)."""

    setup_logging('organize_favorites.log')
    args = _extract_args()
    spotify = Spotify(auth=token.get_token(args.spotify_user, args.spotify_client_id_key, args.spotify_client_secret_key))

    logging.info("Organizing " + args.spotify_user + "'s favorites")
    move_saved_tracks(spotify, args)
    move_new_favorites(spotify, args)
    logging.info("Done!")


def move_new_favorites(spotify, args):
    new_favorites_tracks = playlist.get_tracks_in_playlist(spotify, playlist_name=NEW_FAVORITES_PLAYLIST)
    tracks_to_move = []
    neglected_tracks = []
    for track in new_favorites_tracks:
        added_at = iso8601.parse_date(track.added_at)
        new_favorites_time_limit = added_at + relativedelta(days=int(args.new_favorites_time_limit))
        if datetime.now(timezone.utc) >= new_favorites_time_limit:
            try:
                playcount = track_info.fetch_playcount(track, args.lastfm_user, args.lastfm_api_key)
                if playcount <= int(args.new_favorites_playcount_limit):
                    neglected_tracks.append(track)
                else:
                    tracks_to_move.append(track)
            except:
                logging.warn("Couldn't get playcount for track " + str(track))
       

    logging.info("Moving " + str(len(tracks_to_move)) + " tracks from " + NEW_FAVORITES_PLAYLIST + " to " + OLD_FAVORITES_PLAYLIST)
    playlist.remove_tracks_from_playlist(spotify, NEW_FAVORITES_PLAYLIST, tracks_to_move)
    playlist.add_tracks_to_playlist(spotify, OLD_FAVORITES_PLAYLIST, tracks_to_move)

    logging.info("Moving " + str(len(neglected_tracks)) + " neglected tracks to " + NEGLECTED_PLAYLIST)
    playlist.remove_tracks_from_playlist(spotify, NEW_FAVORITES_PLAYLIST, neglected_tracks)
    playlist.add_tracks_to_playlist(spotify, NEGLECTED_PLAYLIST, neglected_tracks)

def move_saved_tracks(spotify, args):
    saved_tracks = library.get_saved_tracks(spotify)
    tracks_to_move = []
    for track in saved_tracks:
        try:
            playcount = track_info.fetch_playcount(track, args.lastfm_user, args.lastfm_api_key)
            if playcount >= int(args.saved_songs_playcount_limit):
                tracks_to_move.append(track)
        except:
            logging.warn("Couldn't get playcount for track " + str(track))

    logging.info("Moving " + str(len(tracks_to_move)) + " tracks from library to " + NEW_FAVORITES_PLAYLIST)
    library.remove_tracks_from_library(spotify, tracks_to_move)
    playlist.add_tracks_to_playlist(spotify, NEW_FAVORITES_PLAYLIST, tracks_to_move)


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
    args.saved_songs_playcount_limit = config_parser[section]['SavedSongsPlaycountLimit']
    args.new_favorites_time_limit = config_parser[section]['NewFavoritesTimeLimit']
    args.new_favorites_playcount_limit = config_parser[section]['NewFavoritesPlaycountLimit']
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