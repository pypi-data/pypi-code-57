import json, platform, requests, six, urllib.parse

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

from . import VERSION
from .error import APIError

DEFAULT_BASE_URL = 'https://www.zoomconnect.com/app/'
DEFAULT_TIMEOUT = 10
PYTHON_VERSION = platform.python_version()
SYSTEM = platform.system()
ARCH = platform.machine()

class BaseClient:
    def __init__(self, base_url='', timeout=0,
                 api_token='', account_email='', valid_mobile_number_length=10):
        """
        :type base_url: str
        :type timeout: float
        :type api_token: str
        :type account_email: str
        """
        self.set_auth(api_token, account_email)
        self.set_base_url(base_url)
        self.set_timeout(timeout)

        self.valid_mobile_number_length = valid_mobile_number_length

        self.session = requests.Session()


    def set_auth(self, api_token, account_email):
        """Provides the client with an API token and account email.

        :type api_token: str
        :type account_email: str
        """
        self.api_token = api_token
        self.account_email = account_email


    def set_base_url(self, base_url):
        """Overrides the default base URL. For internal use.

        :type base_url: str
        """
        if base_url == '':
            base_url = DEFAULT_BASE_URL
        self.base_url = base_url.rstrip('/')


    def set_timeout(self, timeout):
        """Sets the timeout, in seconds, for requests made by the client.

        :type timeout: float
        """
        if timeout == 0:
            timeout = DEFAULT_TIMEOUT
        self.timeout = timeout


    def do(self, method, path, req=None, param=None, text=False):
        """Performs an API request and returns the response.

        :type method: str
        :type path: str
        :type req: dict
        :type param: dict
        :type text: bool

        :return JSON body from API endpoint
        """
        try:
            body = json.dumps(req)
        except Exception:
            body = None
        res = self.session.request(method,
                                   self.make_url(path,param),
                                   headers={
                                       "Content-Type": "application/json",
                                       "Accept": "application/json",
                                       "User-Agent": self.make_user_agent()
                                   },
                                   data=body,
                                   timeout=self.timeout)
        try:
            if text and res.status_code == 200:
                # e = res.json() str object not callable
                return True
            elif text:
                return False
            else:
                e = res.json()
            if 'error' in e and 'error_code' in e:
                raise APIError(e['error_code'], e['error'])
            return e
        except JSONDecodeError:
            raise Exception(f'zoomconnect: Response error ({res.status_code})')
        except Exception as e:
            raise Exception(f'zoomconnect: API error ({res.status_code} - {e})')


    def make_url(self, path, params):
        """
        :type path: str
        :type params: dict

        :return API endpoint URL
        """
        if params: params.update({"token":self.api_token, "email": self.account_email})
        else: params = {"token": self.api_token, "email": self.account_email}

        return f"{self.base_url}{path}?{'&'.join([f'{k}={urllib.parse.quote(v)}' for k, v in six.iteritems(params)])}"

    def make_user_agent(self):
        """
        :return: user agent string
        """
        return f"ZoomConnectPythonSDK/{VERSION} python/{PYTHON_VERSION} {SYSTEM} {ARCH}"