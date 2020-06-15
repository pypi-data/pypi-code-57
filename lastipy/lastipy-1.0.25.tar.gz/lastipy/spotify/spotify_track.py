from lastipy.track import Track


#TODO test
class SpotifyTrack(Track):
    """Represents a track in Spotify"""

    def __init__(self, track_name, artist, spotify_id):
        self.track_name = track_name
        self.artist = artist
        self.spotify_id = spotify_id

    def __eq__(self, other):
        return isinstance(other, SpotifyTrack) \
            and self.track_name == other.track_name \
            and self.artist == other.artist \
            and self.spotify_id == self.spotify_id

    def __repr__(self):
        return str(self.__dict__)
