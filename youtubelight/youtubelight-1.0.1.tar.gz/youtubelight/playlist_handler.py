import requests
import dateutil.parser

from .core import CoreMixin


class PlaylistHandler(CoreMixin):

    next_page_token = ''
    channel_id = ''
    itm_result = ''
    default_param = ''

    @staticmethod
    def filter_playlist(items, title='', description='', date='', date_lt='',
                        date_lte='', date_gt='', date_gte=''):

        filtered_list = []
        for itm in items:
            # filter by title
            if title:
                _title = itm['snippet']['title'].lower().split(' ')
                res = [x for x in _title if x in title.lower().split(' ')]
                if not res:
                    continue
            # filter by description
            if description:
                _desc = itm['snippet']['description'].lower().split(' ')
                res = [x for x in _desc if x in description.lower().split(' ')]
                if not res:
                    continue
            # filter by date
            datetime_object = dateutil.parser.parse(itm.get('snippet').get('publishedAt'))
            if date:
                if datetime_object != date:
                    continue
            elif date_lt:
                if datetime_object > date_lt:
                    continue
            elif date_gt:
                if datetime_object < date_gt:
                    continue
            elif date_lte:
                if datetime_object >= date_lte:
                    continue
            elif date_gte:
                if datetime_object <= date_gte:
                    continue

            filtered_list.append(itm)
        return filtered_list

    def playlist_next_page(self):
        """Get the next page for the playlist."""
        if not self.channel_id:
            raise Exception('Cannot get the following page: channel_id - None')
        return self.get_play_list(self.channel_id, itm_result=self.itm_result,
                                  page_token=self.next_page_token, default_param=self.default_param)

    def _create_url(self, channel_id, itm_result, page_token, default_param):
        if page_token:
            url = f'{self.api_url}/playlists?part={default_param}&channelId={channel_id}' \
                  f'&maxResults={itm_result}&key={self.api_key}&pageToken={page_token}'
        else:
            url = f'{self.api_url}/playlists?part={default_param}&channelId={channel_id}' \
                    f'&maxResults={itm_result}&key={self.api_key}'
        return url

    def get_play_list(self, channel_id, itm_result=50, page_token='', default_param='snippet,contentDetails'):
        """A playlist resource represents a YouTube playlist."""
        url = self._create_url(channel_id, itm_result, page_token, default_param)
        response = requests.get(url)
        if response.status_code == 200:
            self.next_page_token = response.json().get('nextPageToken')
            self.channel_id = channel_id
            self.itm_result = itm_result
            self.default_param = default_param
        return {'status_code': response.status_code, 'content': response.json()}

    def get_all_playlists(self, channel_id, default_param='snippet,contentDetails'):
        """Get all playlists for a channel."""
        result = {}
        page_token = ''
        while True:
            url = self._create_url(channel_id, 50, page_token, default_param)
            response = requests.get(url)
            if response.status_code == 200:
                response = response.json()

                page_token = response.get('nextPageToken')

                if not result:
                    result = response
                else:
                    result['items'].append(response.get('items'))

                if not response.get('nextPageToken'):
                    break

            else:
                raise Exception(f'Unable to retrieve entire playlist for channel: {response.json()}')

        return result


class PlaylistItemHandler(PlaylistHandler):

    def list_itm_next_page(self):
        res = super().playlist_next_page()
        return res

    def _create_url(self, channel_id, itm_result, page_token, default_param):
        if page_token:
            url = f'{self.api_url}/playlistItems?part={default_param}&playlistId={channel_id}' \
                  f'&maxResults={itm_result}&key={self.api_key}&pageToken={page_token}'
        else:
            url = f'{self.api_url}/playlistItems?part={default_param}&playlistId={channel_id}' \
                    f'&maxResults={itm_result}&key={self.api_key}'
        return url

    def get_play_list_itm(self, channel_id, itm_result=50, page_token='', default_param='snippet,contentDetails'):
        res = super().get_play_list(channel_id, itm_result, page_token, default_param)
        return res

    def get_all_playlist_itm(self, channel_id, default_param='snippet,contentDetails'):
        res = super().get_all_playlists(channel_id, default_param)
        return res

    @staticmethod
    def filter_playlist_itm(items, title='', description='', date='', date_lt='',
                        date_lte='', date_gt='', date_gte=''):
        res = super().self.filter_playlist(items, title, description, date, date_lt, date_lte, date_gt, date_gte)
        return res
