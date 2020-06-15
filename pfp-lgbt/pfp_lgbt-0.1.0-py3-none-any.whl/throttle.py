import time
import requests

class RequestThrottle(object):
    """Request throttling to abide to rate limit.

    Args:
        user_agent (string): User-Agent to use for requests.
    """
    def __init__(self, user_agent):
        self.rateLimit = 2
        self.rateRemaining = 2
        self.rateReset = 0
        self.headers = {
            'User-Agent': user_agent,
            'Accept': '*/*'
        }

    def __updateRatelimit(self, headers):
        """Updates the current state of the rate limit.

        Args:
            headers (dict): The latest response headers.
        """
        if (('X-Ratelimit-Limit' in headers) and ('X-Ratelimit-Remaining' in headers) and ('X-Ratelimit-Reset' in headers)):
            self.rateLimit = int(headers['X-Ratelimit-Limit'])
            self.rateRemaining = int(headers['X-Ratelimit-Remaining'])
            self.rateReset = int(headers['X-Ratelimit-Reset'])

    def __isLimited(self):
        """Checks if we are currently being rate limited.

        Returns:
            bool: True if we are being rate limited, otherwise False
        """
        if ((time.time() - self.rateReset) > 0):
            self.rateRemaining = self.rateLimit
        if (self.rateRemaining > 0):
            return False
        return True

    def chew(self, request):
        """Processes requests.

        Args:
            request (Request): The request to process.

        Returns:
            requests.Response: Response to our request.
        """
        if (self.__isLimited()):
            time.sleep(0.1)
            return self.chew(request)
        else:
            response = requests.request(request.method, headers=self.headers, url=request.endpoint, data=request.body, files=request.files)
            self.__updateRatelimit(response.headers)
            if response.status_code != 200:
                response.raise_for_status()
            return response
