import spotipy
from lastipy.spotify.parse_spotify_tracks import parse_tracks
from datetime import datetime
import logging
from lastipy.track import Track


#TODO test
def fetch_new_tracks(spotify, as_of_date=datetime.today().date()):
    """Fetches new tracks (as of the given date) released by the current Spotify user's followed artists"""

    logging.info("Fetching new tracks for " + spotify.current_user()['id'] + " as of " + str(as_of_date))

    followed_artist_ids = _get_followed_artists(spotify)

    all_albums = []
    for artist_id in followed_artist_ids:
        artist_albums = _get_releases(spotify, artist_id)
        all_albums += artist_albums

    new_albums = _filter_new_releases(all_albums, as_of_date)

    all_tracks = []
    for album in new_albums:
        all_tracks += _get_album_tracks(spotify, album)

    new_tracks = parse_tracks(all_tracks)
    
    new_tracks = _remove_duplicates(new_tracks)
    logging.info("Fetched " + str(len(new_tracks)) + " new tracks " + str(new_tracks))
    return new_tracks


def _get_followed_artists(spotify):
    followed_artists = []

    curr_response = spotify.current_user_followed_artists(limit=50)

    while len(curr_response['artists']['items']) > 0:
        curr_response = spotify.current_user_followed_artists(limit=50, after=curr_response['artists']['items'][len(curr_response) - 1]['id'])
        followed_artists += curr_response['artists']['items']

    # The above Spotipy function doesn't really seem to function properly and results in duplicates, 
    # so we remove them here by converting the list to just the IDs (not doing so results in
    # an unhashable error), then converting to a set and back to a list 
    followed_artists = [artist['id'] for artist in followed_artists]
    followed_artist_ids = list(set(followed_artists))
    return followed_artist_ids


def _filter_new_releases(all_albums, as_of_date):
    new_albums = []
    for album in all_albums:
        if album['release_date_precision'] == 'day':
            if datetime.strptime(album['release_date'], "%Y-%m-%d").date() >= as_of_date:
                new_albums.append(album)
        elif album['release_date_precision'] == 'month':
            release_date = datetime.strptime(album['release_date'], "%Y-%m")
            if release_date.year > as_of_date.year or (release_date.year == as_of_date.year and release_date.month >= as_of_date.month):
                   new_albums.append(album)
        elif album['release_date_precision'] == 'year':
            if datetime.strptime(album['release_date'], '%Y').year >= as_of_date.year:
                new_albums.append(album)
    return new_albums


def _get_releases(spotify, artist_id):
    # Albums
    curr_response = spotify.artist_albums(artist_id, album_type='album', limit=50)
    artist_albums = curr_response['items']
    while len(curr_response['items']) > 0:
        curr_response = spotify.artist_albums(artist_id, album_type='album', limit=50, offset=len(artist_albums))
        artist_albums += curr_response['items']
    # Singles
    curr_response = spotify.artist_albums(artist_id, album_type='single', limit=50)
    artist_singles = curr_response['items']
    while len(curr_response['items']) > 0:
        curr_response = spotify.artist_albums(artist_id, album_type='single', limit=50, offset=len(artist_singles))
        artist_singles += curr_response['items']
    return artist_albums + artist_singles


def _get_album_tracks(spotify, album):
    curr_response = spotify.album_tracks(album['id'], limit=50)
    album_tracks = curr_response['items']
    while len(curr_response['items']) > 0:
        curr_response = spotify.album_tracks(album['id'], limit=50, offset=len(album_tracks))
        album_tracks += curr_response['items']
    return album_tracks


def _remove_duplicates(tracks):
    """Removes duplicate tracks (ie: tracks that have identical name and artist; see Track.are_equivalent)"""
    logging.debug("New tracks before removing duplicates: " + str(tracks))
    tracks_without_duplicates = []
    # We remove duplicates with a list comprehension rather than the traditional hack of using a set, since that
    # requires the object to be hashable; plus we only want to compare the track name/artist of each track, not
    # any of the other fields (eg: Spotify ID) which might in fact differ
    [tracks_without_duplicates.append(track_x) 
        for track_x in tracks 
        if not any(Track.are_equivalent(track_x, track_y) 
                   for track_y in tracks_without_duplicates)]
    logging.debug("New tracks after removing duplicates: " + str(tracks_without_duplicates))
    return tracks_without_duplicates