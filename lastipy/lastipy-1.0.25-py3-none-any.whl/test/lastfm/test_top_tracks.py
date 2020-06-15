
import unittest
from lastipy.lastfm.library import period
from lastipy.lastfm.library.scrobbled_track import ScrobbledTrack
from unittest.mock import patch, Mock
from requests import HTTPError
from lastipy.lastfm.library.top_tracks import fetch_top_tracks


class TopTracksFetcherTest(unittest.TestCase):
    
    @patch('requests.get')
    def test_one_page_of_results(self, mock_requests_get):
        expected_track = ScrobbledTrack(track_name="Stayin' Alive", artist="Bee Gees", playcount=2)

        mock_requests_get.ok = True

        json_track = self._build_json(expected_track)

        first_page_response = {
            'toptracks': {
                'track': [json_track]
            }
        }

        second_page_response = {
            'toptracks': {
                'track': []
            }
        }

        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = first_page_response
        mock_responses[1].json.return_value = second_page_response
        mock_requests_get.side_effect = mock_responses

        self.assertEqual(fetch_top_tracks(api_key='', user='sonofjack3', a_period=period.SEVEN_DAYS)[0], expected_track)

    @patch('requests.get')
    def test_multiple_tracks_over_multiple_pages(self, mock_requests_get):
        expected_track_1 = ScrobbledTrack(track_name="Penny Lane", artist="The Beatles", playcount=5)
        expected_track_2 = ScrobbledTrack(track_name="Won't Get Fooled Again", artist="The Who", playcount=6)
        expected_track_3 = ScrobbledTrack(track_name="Like the FBI", artist="Bob Dylan", playcount=10)
        expected_tracks = [expected_track_1, expected_track_2, expected_track_3]

        mock_requests_get.ok = True

        json_track_1 = self._build_json(expected_track_1)
        json_track_2 = self._build_json(expected_track_2)
        json_track_3 = self._build_json(expected_track_3)

        first_page_response = {
            'toptracks': {
                'track': [json_track_1, json_track_2]
            }
        }

        second_page_response = {
            'toptracks': {
                'track': [json_track_3]
            }
        }

        third_page_response = {
            'toptracks': {
                'track': []
            }
        }

        mock_responses = [Mock(), Mock(), Mock()]
        mock_responses[0].json.return_value = first_page_response
        mock_responses[1].json.return_value = second_page_response
        mock_responses[2].json.return_value = third_page_response
        mock_requests_get.side_effect = mock_responses

        fetched_tracks = fetch_top_tracks(api_key='', user="sonofjack3", a_period=period.SEVEN_DAYS)
        self.assertCountEqual(fetched_tracks, expected_tracks)
    
    @patch('requests.get')
    def test_songs_with_one_playcount_ignored(self, mock_requests_get):
        ignored_track_1 = ScrobbledTrack(track_name="Stayin' Alive", artist="Bee Gees", playcount=1)
        non_ignored_track = ScrobbledTrack(track_name="Ventura Highway", artist="America", playcount=5)
        ignored_track_2 = ScrobbledTrack(track_name="Anesthetized Lesson", artist="Gum", playcount=1)

        mock_requests_get.ok = True

        json_track_1 = self._build_json(ignored_track_1)
        json_track_2 = self._build_json(non_ignored_track)
        json_track_3 = self._build_json(ignored_track_2)

        first_page_response = {
            'toptracks': {
                'track': [json_track_1, json_track_2, json_track_3]
            }
        }

        second_page_response = {
            'toptracks': {
                'track': []
            }
        }

        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = first_page_response
        mock_responses[1].json.return_value = second_page_response
        mock_requests_get.side_effect = mock_responses

        fetched_tracks = fetch_top_tracks(api_key='', user='sonofjack3', a_period=period.SEVEN_DAYS)
        self.assertEqual(fetched_tracks.__len__(), 1)
        self.assertEqual(fetched_tracks[0], non_ignored_track)
    
    @patch('requests.get')
    def test_failure(self, mock_requests_get):
        mock_requests_get.ok = False
        mock_requests_get.side_effect = HTTPError("Mock")

        with self.assertRaises(HTTPError):
            fetch_top_tracks(api_key='', user='sonofjack3', a_period=period.SEVEN_DAYS)

    def _build_json(self, track):
        return {
            'name': track.track_name,
            'artist': {
                'name': track.artist
            },
            'playcount': track.playcount
        }
