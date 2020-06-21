import requests
import configparser
from rich.console import Console
from blc.handlers.exceptions import ApiError
config = configparser.ConfigParser()
config.read('config.ini')
console = Console()


class Call():
    """Shortcut for the requests"""

    def __init__(self):
        self.token = config['default']['api_key']
        self.base = config['default']['base_url']

    def do(self, extra='tasks/', pay=None, method='GET'):
        """Calls the api."""
        headers = {'authorization': f'Token {self.token}'}
        resp = requests.request(method, self.base+extra, data=pay, headers=headers)
        if not resp.ok:
            console.print('Host could not be contacted!\n', style='bold red')
            console.print('Please make sure base url and api key are properly configured', style='bold yellow')
            raise ApiError
        return resp
