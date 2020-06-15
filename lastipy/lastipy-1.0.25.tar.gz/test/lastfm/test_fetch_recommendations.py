import unittest
from unittest.mock import patch

from lastipy.lastfm.recommendations.recommendations import fetch_recommendations
from lastipy.lastfm.library.scrobbled_track import ScrobbledTrack
from lastipy.lastfm.recommendations.recommended_track import RecommendedTrack


class RecommendationsFetcherTest(unittest.TestCase):

    @patch('lastipy.lastfm.recommendations.recommendations.fetch_recent_tracks')
    @patch('lastipy.lastfm.recommendations.recommendations.fetch_top_tracks')
    @patch('lastipy.lastfm.recommendations.recommendations.fetch_similar_tracks')
    @patch('lastipy.lastfm.recommendations.recommendations.calculate_ratings')
    def test_recent_tracks_are_filtered(self, mock_calculate_ratings, mock_similar_tracks, mock_top_tracks, mock_recent_tracks):
        recent_track_1 = ScrobbledTrack(track_name="SWALBR", artist="Cream", playcount=1)
        recent_track_2 = ScrobbledTrack(track_name="Badge", artist="Cream", playcount=1)
        recent_track_3 = ScrobbledTrack(track_name="Layla", artist="Derek & the Dominos", playcount=8)
        mock_recent_tracks.return_value = [recent_track_1, recent_track_2, recent_track_3]

        mock_top_tracks.return_value = [recent_track_3]

        new_recommendation = RecommendedTrack(track_name="Key to the Highway", artist="Derek & the Dominos", recommendation_rating=8)
        already_scrobbled_recommendation_1 = RecommendedTrack(track_name="Badge", artist="Cream", recommendation_rating=8)
        already_scrobbled_recommendation_2 = RecommendedTrack(track_name="SWALBR", artist="Cream", recommendation_rating=8)
        recommendations = [new_recommendation, already_scrobbled_recommendation_1, already_scrobbled_recommendation_2]
        mock_similar_tracks.return_value = recommendations

        mock_calculate_ratings.return_value = recommendations

        self.assertCountEqual(fetch_recommendations('test', ''), [new_recommendation])


    @patch('lastipy.lastfm.recommendations.recommendations.fetch_recent_tracks')
    @patch('lastipy.lastfm.recommendations.recommendations.fetch_top_tracks')
    @patch('lastipy.lastfm.recommendations.recommendations.fetch_similar_tracks')
    @patch('lastipy.lastfm.recommendations.recommendations.calculate_ratings')
    def test_blacklisted_artists_are_filtered(self, mock_calculate_ratings, mock_similar_tracks, mock_top_tracks, mock_recent_tracks):
        mock_recent_tracks.return_value = []
        mock_top_tracks.return_value = [ScrobbledTrack(track_name='Here Comes the Sun', artist='The Beatles', playcount=5)]

        recommendation_1 = RecommendedTrack(track_name="Badge", artist="Cream", recommendation_rating=1)
        recommendation_2 = RecommendedTrack(track_name="Penny Lane", artist="The Beatles", recommendation_rating=1)
        recommendations = [recommendation_1, recommendation_2]
        mock_similar_tracks.return_value = recommendations

        mock_calculate_ratings.return_value = recommendations

        recommendations = fetch_recommendations(user="meeee", api_key='', blacklisted_artists=['The Beatles'])

        self.assertCountEqual(recommendations, [recommendation_1])


    @patch('lastipy.lastfm.recommendations.recommendations.fetch_recent_tracks')
    @patch('lastipy.lastfm.recommendations.recommendations.fetch_top_tracks')
    @patch('lastipy.lastfm.recommendations.recommendations.fetch_similar_tracks')
    @patch('lastipy.lastfm.recommendations.recommendations.calculate_ratings')
    def test_blacklisted_artists_filtering_should_ignore_case(self, mock_calculate_ratings, mock_similar_tracks, mock_top_tracks, mock_recent_tracks):
        mock_recent_tracks.return_value = []
        mock_top_tracks.return_value = [ScrobbledTrack(track_name='everything i wanted', artist='Billie Eilish', playcount=5)]

        recommendation = RecommendedTrack(track_name="Bad Music", artist="Zayn", recommendation_rating=1)
        recommendations = [recommendation]
        mock_similar_tracks.return_value = recommendations

        mock_calculate_ratings.return_value = recommendations

        recommendations = fetch_recommendations(user="", api_key='', blacklisted_artists=['ZAYN'])

        self.assertEqual(0, len(recommendations))
