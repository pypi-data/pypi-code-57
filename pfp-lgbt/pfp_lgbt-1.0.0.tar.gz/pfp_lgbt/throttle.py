import time
import aiohttp
import asyncio

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
        self.session = aiohttp.ClientSession(headers=self.headers, raise_for_status=True)

    async def close(self):
        await self.session.close()

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

    async def chew(self, request):
        """Processes requests.

        Args:
            request (Request): The request to process.

        Returns:
            requests.Response: Response to our request.
        """
        if (self.__isLimited()):
            await asyncio.sleep(0.1)
            return await self.chew(request)
        else:
            self.rateRemaining -= 1
            if request.method == 'POST':
                response = await self.session.post(request.endpoint, data=request.files)
            else:
                response = await self.session.get(request.endpoint)
            self.__updateRatelimit(response.headers)
            return response
