import unittest
from unittest.mock import patch

from lastipy.lastfm.library.scrobbled_artist import ScrobbledArtist
from lastipy.lastfm.library.scrobbled_track import ScrobbledTrack
from lastipy.lastfm.recommendations.rating_calculator import calculate_ratings 
from lastipy.lastfm.recommendations.recommended_track import RecommendedTrack


class RatingCalculatorTest(unittest.TestCase):

    @patch('lastipy.lastfm.recommendations.rating_calculator.fetch_recent_artists')
    def test_rating_with_one_top_track_one_recommendation(self, mock_recent_artists):
        mock_recent_artists.return_value = []
        top_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever', recommendation_rating=1)
        top_tracks_to_recommendations = {
            top_track: [recommended_track_1]
        }
        recommendations = calculate_ratings('test', '', top_tracks_to_recommendations)
        self.assertEqual(10, recommendations[0].recommendation_rating)

    @patch('lastipy.lastfm.recommendations.rating_calculator.fetch_recent_artists')
    def test_rating_with_one_top_track_multiple_recommendations(self, mock_recent_artists):
        mock_recent_artists.return_value = []
        top_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever', recommendation_rating=1)
        recommended_track_2 = RecommendedTrack(artist="The Beatles", track_name='Baby You\'re a Rich Man', recommendation_rating=1)
        recommended_track_3 = RecommendedTrack(artist="The Beatles", track_name="Blue Jay Way", recommendation_rating=1)
        top_tracks_to_recommendations = {
            top_track: [recommended_track_1, recommended_track_2, recommended_track_3]
        }
        recommendations = calculate_ratings('test', '', top_tracks_to_recommendations)
        self.assertEqual(10, recommendations[0].recommendation_rating)
        self.assertEqual(10, recommendations[1].recommendation_rating)
        self.assertEqual(10, recommendations[2].recommendation_rating)

    @patch('lastipy.lastfm.recommendations.rating_calculator.fetch_recent_artists')
    def test_rating_with_multiple_top_tracks_multiple_recommendations(self, mock_recent_artists):
        mock_recent_artists.return_value = []
        top_track_1 = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever', recommendation_rating=1)
        recommended_track_2 = RecommendedTrack(artist="The Beatles", track_name='Baby You\'re a Rich Man', recommendation_rating=1)
        recommended_track_3 = RecommendedTrack(artist="The Beatles", track_name="Blue Jay Way", recommendation_rating=1)
        top_track_2 = ScrobbledTrack(artist='The Rolling Stones', track_name='Satisfaction', playcount=20)
        recommended_track_4 = RecommendedTrack(artist='The Rolling Stones', track_name='Ruby Tuesday', recommendation_rating=1)
        recommended_track_5 = RecommendedTrack(artist="The Beatles", track_name='Get Off Of My Cloud', recommendation_rating=1)
        top_tracks_to_recommendations = {
            top_track_1: [recommended_track_1, recommended_track_2, recommended_track_3],
            top_track_2: [recommended_track_4, recommended_track_5]
        }
        recommendations = calculate_ratings('test', '', top_tracks_to_recommendations)
        self.assertEqual(10, recommendations[0].recommendation_rating)
        self.assertEqual(10, recommendations[1].recommendation_rating)
        self.assertEqual(10, recommendations[2].recommendation_rating)
        self.assertEqual(20, recommendations[3].recommendation_rating)
        self.assertEqual(20, recommendations[4].recommendation_rating)

    @patch('lastipy.lastfm.recommendations.rating_calculator.fetch_recent_artists')
    def test_rating_is_reduced_based_on_artist_playcount(self, mock_recent_artists):
        mock_recent_artists.return_value = [ScrobbledArtist(artist_name='The Beatles', playcount=9)]
        top_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=5)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever', recommendation_rating=1)
        recommended_track_2 = RecommendedTrack(artist='The Beatles', track_name='Blue Jay Way', recommendation_rating=1)
        top_tracks_to_recommendations = {
            top_track: [recommended_track_1, recommended_track_2]
        }
        recommendations = calculate_ratings('test', '', top_tracks_to_recommendations)
        self.assertEqual(0.1, recommendations[0].recommendation_rating)
        self.assertEqual(0.1, recommendations[1].recommendation_rating)

    @patch('lastipy.lastfm.recommendations.rating_calculator.fetch_recent_artists')
    def test_multiple_recommendations_and_multiple_recent_artists(self, mock_recent_artists):
        mock_recent_artists.return_value = [ScrobbledArtist(artist_name='The Beatles', playcount=9),
                                            ScrobbledArtist(artist_name='The Rolling Stones', playcount=19)]    
        top_track_1 = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=5)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever', recommendation_rating=1)
        top_track_2 = ScrobbledTrack(artist='The Rolling Stones', track_name='Satisfaction', playcount=10)
        recommended_track_2 = RecommendedTrack(artist='The Kinks', track_name='You Really Got Me', recommendation_rating=1)
        recommended_track_3 = RecommendedTrack(artist='The Rolling Stones', track_name='Ruby Tuesday', recommendation_rating=1)
        top_tracks_to_recommendations = {
            top_track_1: [recommended_track_1],
            top_track_2: [recommended_track_2, recommended_track_3]
        }
        recommendations = calculate_ratings('test', '', top_tracks_to_recommendations)
        self.assertEqual(0.1, recommendations[0].recommendation_rating)
        self.assertEqual(10, recommendations[1].recommendation_rating)
        self.assertEqual(0.1, recommendations[2].recommendation_rating)

    @patch('lastipy.lastfm.recommendations.rating_calculator.fetch_recent_artists')
    def test_recommendations_where_artist_has_one_playcount_should_get_rating_halved(self, mock_recent_artists):
        mock_recent_artists.return_value = [ScrobbledArtist(artist_name='The Beatles', playcount=1)]
        top_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever', recommendation_rating=1)
        top_tracks_to_recommendations = {
            top_track: [recommended_track_1]
        }
        recommendations = calculate_ratings('test', '', top_tracks_to_recommendations)
        self.assertEqual(1, recommendations[0].recommendation_rating)

    @patch('lastipy.lastfm.recommendations.rating_calculator.fetch_recent_artists')
    def test_reducing_based_on_recent_artists_ignores_case(self, mock_recent_artists):
        mock_recent_artists.return_value = [ScrobbledArtist(artist_name='LANY', playcount=3)]
        top_track = ScrobbledTrack(artist='LANY', track_name='Some Whiny Crap', playcount=2)
        recommended_track = RecommendedTrack(artist='Lany', track_name='Some Other Whiny Crap', recommendation_rating=1)
        top_tracks_to_recommendations = {
            top_track: [recommended_track]
        }
        recommendations = calculate_ratings('test', '', top_tracks_to_recommendations)
        self.assertEqual(0.1, recommendations[0].recommendation_rating)