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


def build_recommendations_playlist():
    """Adds recommendations to the given Spotify user's playlist based on the given Last.fm user's recommendations"""

    setup_logging('recommendations.log')
    args = _extract_args()
    spotify = Spotify(auth=token.get_token(args.spotify_user, args.spotify_client_id_key, args.spotify_client_secret_key))

    recommendations = fetch_recommendations(user=args.lastfm_user,
                                            api_key=args.lastfm_api_key,
                                            recommendation_period=args.recommendation_period,
                                            max_similar_tracks_per_top_track=args.max_recommendations_per_top_track,
                                            blacklisted_artists=args.blacklisted_artists,
                                            prefer_unheard_artists=args.prefer_unheard_artists)
    
    library_saved_tracks = library.get_saved_tracks(spotify)
    library_playlist_tracks = playlist.get_tracks_in_playlists(spotify)

    logging.info("Searching for recommendations in Spotify")
    tracks_for_playlist = []
    while len(tracks_for_playlist) < args.playlist_size and len(recommendations) > 0:
        recommendation = choice(recommendations, p=_calculate_rating_weights(recommendations))
        recommendations.remove(recommendation)

        search_results = search.search_for_tracks(spotify=spotify,
                                                  query=recommendation.artist + " " + recommendation.track_name)
        # Always use the first result, which we can assume is the closest match
        first_result = search_results[0] if search_results else None

        if first_result is not None \
           and Track.are_equivalent(first_result, recommendation) \
           and not any(Track.are_equivalent(first_result, track) for track in tracks_for_playlist) \
           and not any(Track.are_equivalent(first_result, playlist_track) for playlist_track in library_playlist_tracks) \
           and not any(Track.are_equivalent(first_result, saved_track) for saved_track in library_saved_tracks) \
           and not any(first_result.artist == item.artist for item in tracks_for_playlist):
            logging.debug("Adding " + str(first_result))
            tracks_for_playlist.append(first_result)

    playlist.replace_tracks_in_playlist(spotify, args.playlist_name, tracks_for_playlist)

    logging.info("Done!")

def _extract_args():
    args_parser = _setup_args_parser()
    args = args_parser.parse_args()
    args = _extract_user_configs(args)
    args = _extract_api_keys(args)
    return args


def _setup_args_parser():
    parser = argparse.ArgumentParser(description="Create a Spotify playlist based off recommendations from Last.fm")
    parser.add_argument('user_configs_file', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('api_keys_file', type=argparse.FileType('r', encoding='UTF-8'))
    return parser


def _extract_user_configs(args):
    config_parser = ConfigParser()
    config_parser.read(args.user_configs_file.name)
    section = 'Config'
    args.lastfm_user = config_parser[section]['LastFMUser']
    args.spotify_user = config_parser[section]['SpotifyUser']
    args.recommendation_period = config_parser[section]['RecommendationPeriod']
    args.max_recommendations_per_top_track = int(config_parser[section]['MaxRecommendationsPerTopTrack'])
    args.playlist_size = int(config_parser[section]['PlaylistSize'])
    args.playlist_name = config_parser[section]['PlaylistName']
    args.blacklisted_artists = config_parser[section]['BlacklistedArtists'].split(",")
    args.prefer_unheard_artists = _str_to_bool(config_parser[section]['PreferUnheardArtists'])
    return args


def _str_to_bool(to_convert):
    return to_convert == "True"


def _extract_api_keys(args):
    keys_parser = ApiKeysParser(args.api_keys_file)
    args.lastfm_api_key = keys_parser.lastfm_api_key
    args.spotify_client_id_key = keys_parser.spotify_client_id_key
    args.spotify_client_secret_key = keys_parser.spotify_client_secret_key
    return args


def _calculate_rating_weights(recommendations):
    total_ratings = 0
    for recommendation in recommendations:
        total_ratings += recommendation.recommendation_rating

    rating_weights = []
    for recommendation in recommendations:
        rating_weights.append(recommendation.recommendation_rating / total_ratings)
    return rating_weights

if __name__ == "__main__":
    build_recommendations_playlist()