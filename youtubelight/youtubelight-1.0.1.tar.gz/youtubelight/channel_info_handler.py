# https://developers.google.com/youtube/v3/docs
import requests

from .core import CoreMixin


class СhannelInfoHandler(CoreMixin):

    def get_channel_info_by_name(self, channel_name, default_param='snippet,contentDetails,statistics'):
        """Get channel information by channel name."""
        url = f'{self.api_url}/channels?part={default_param}&forUsername={channel_name}&key={self.api_key}'
        response = requests.get(url)
        return {'status_code': response.status_code, 'content': response.json()}

    def get_channel_info_by_id(self, channel_id, default_param='snippet,contentDetails,statistics'):
        """Get channel information by channel id."""
        url = f'{self.api_url}/channels?part={default_param}&id={channel_id}&key={self.api_key}'
        response = requests.get(url)
        return {'status_code': response.status_code, 'content': response.json()}

    def get_channel_sections(self, channel_id, default_param='snippet,contentDetails'):
        """
        A channelSection resource contains information about a
        set of videos that a channel has chosen to feature.
        """
        url = f'{self.api_url}/channelSections?part={default_param}&channelId={channel_id}&key={self.api_key}'
        response = requests.get(url)
        return {'status_code': response.status_code, 'content': response.json()}
