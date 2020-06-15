from lastipy.spotify.spotify_track import SpotifyTrack
from lastipy.spotify.playlist_track import PlaylistTrack

#TODO test
def parse_tracks(json_tracks):
    return [_parse_track(json_track) for json_track in json_tracks]


def _parse_track(json_track):
    added_at = None
    if 'added_at' in json_track:
        added_at = json_track['added_at']

    if 'track' in json_track:
        # Some endpoints do this, others don't
        json_track = json_track['track']
    track_id = json_track['id']
    name = json_track['name']
    # Just getting the first artist, even if there's multiple
    artist = json_track['artists'][0]['name']

    # TODO kinda crappy
    if added_at is None:
        return SpotifyTrack(track_name=name, artist=artist, spotify_id=track_id)
    else:
        return PlaylistTrack(track_name=name, artist=artist, spotify_id=track_id, added_at=added_at)
