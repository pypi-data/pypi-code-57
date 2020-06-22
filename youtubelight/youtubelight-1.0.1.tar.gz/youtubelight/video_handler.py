import requests

from .core import CoreMixin


class VideoStatisticHandler(CoreMixin):

    def validate_video_list_format(self, itm):
        err_string = "Maximum number of video_id in one request no more than 50"
        if isinstance(itm, list):

            if len(itm) >= 50:
                raise Exception(err_string)
            else:
                return ','.join(itm)

        elif isinstance(itm, str):

            if len(itm.split(',')) >= 50:
                raise Exception(err_string)
            else:
                return itm

        else:
            raise Exception('Unsupported format for video_id')

    def get_video_info(self, items, default_param='snippet,contentDetails,statistics'):
        """
        Get video by video id. Support follow formats video_id: <video_id>,<video_id> or [<video_id>, <video_id>].
        """
        items = self.validate_video_list_format(items)
        url = f'{self.api_url}/videos?part={default_param}&id={items}&key={self.api_key}'
        response = requests.get(url)
        return {'status_code': response.status_code, 'content': response.json()}
