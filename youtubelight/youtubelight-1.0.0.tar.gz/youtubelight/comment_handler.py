import requests

from .core import CoreMixin


class CommentHandler(CoreMixin):

    video_id = ''
    next_page_token = ''
    default_param = ''

    def filter_comment(self, items, filter_by_word=''):
        """Filter comment by textOriginal field."""
        filtered_list = []
        if filter_by_word:
            for itm in items.get('items'):
                comment = itm['snippet']['topLevelComment']['snippet']['textOriginal'].lower().split(' ')
                res = [x for x in comment if x in filter_by_word.lower().split(' ')]
                if not res:
                    continue
                else:
                    filtered_list.append(itm)
        return filtered_list

    def comments_next_page(self):
        if not self.video_id:
            raise Exception('Cannot get the following page: video_id - None')
        return self.get_video_comment(self.video_id, page_token=self.next_page_token,
                                      default_param=self.default_param)

    def _create_url(self, video_id, page_token, default_param):
        if page_token:
            url = f'{self.api_url}/commentThreads?part={default_param}&videoId={video_id}&key={self.api_key}&' \
                  f'pageToken={page_token}'
        else:
            url = f'{self.api_url}/commentThreads?part={default_param}&videoId={video_id}&key={self.api_key}'
        return url

    def get_video_comment(self, video_id, page_token='', default_param='snippet,replies'):
        url = self._create_url(video_id, page_token, default_param)
        response = requests.get(url)
        if response.status_code == 200:
            self.next_page_token = response.json().get('nextPageToken')
            self.video_id = video_id
            self.default_param = default_param
        return {'status_code': response.status_code, 'content': response.json()}
