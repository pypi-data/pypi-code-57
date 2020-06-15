from lastipy.track import Track


class RecommendedTrack(Track):
    """Represents a track recommended from Last.fm"""

    def __init__(self, track_name, artist, recommendation_rating=0):
        super().__init__(track_name, artist)
        self.recommendation_rating = recommendation_rating

    def __eq__(self, other):
        return isinstance(other, RecommendedTrack) \
            and self.track_name == other.track_name \
            and self.artist == other.artist \
            and self.recommendation_rating == other.recommendation_rating

    def __hash__(self):
        return hash((self.track_name, self.artist, self.recommendation_rating))

    def __repr__(self):
        return str(self.__dict__)
