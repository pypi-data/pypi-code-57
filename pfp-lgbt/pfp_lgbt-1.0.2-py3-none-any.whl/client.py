from .throttle import RequestThrottle
from .models import Request, types, atypes, styles, formats
from .handlers import handleFlags, handleIconBytes, handleImageStatic
from .util import imageToByte

import asyncio

class Client(object):
    """Object for the API Wrapper client.

    Args:
        host (str, optional): Base URL of the API Host. Defaults to 'https://api.pfp.lgbt/v3'.
        user_agent (str, optional): User-Agent to send the requests with. Defaults to 'pfp_lgbt.py/0.1.0'.
        key (string, optional): API Key, not yet used - serving just as a placeholder. Defaults to None.
    """
    def __init__(self, host='https://api.pfp.lgbt/v3', user_agent='pfp_lgbt.py/0.1.0', key=None):
        self.host = host
        self.key = key

        self.throttle = RequestThrottle(user_agent)

    async def close(self):
        """Closes the aiohttp Client Session. Asynchronous.
        """
        await self.throttle.close()

    async def flags(self):
        """Retrieve all available flags. Asynchronous.

        Returns:
            list: List of all available flags, as classes

        """
        endpoint = f'{self.host}/flags'
        response = await self.throttle.chew(Request(endpoint, 'GET'))
        return await handleFlags(response, self.host)

    def icon(self, flag):
        """Retrieves icon for a specific Flag.

        Args:
            flag (Flag): The Flag to retrieve the icon for.

        Returns:
            string: The icon URL.
        """
        endpoint = f'{self.host}/icon/{flag.name}'
        return endpoint

    async def iconBytes(self, flag):
        """Retrieves the icon for a specific Flag in bytes. Asynchronous.

        Args:
            flag (Flag): The Flag to retrieve the icon for.

        Returns:
            bytes: Flag icon in bytes.
        """
        endpoint = f'{self.host}/icon/{flag.name}'
        response = await self.throttle.chew(Request(endpoint, 'GET'))
        return await handleIconBytes(response)

    async def imageStatic(self, image, itype, istyle, flag, iformat='png', output_file=None):
        """Generates a static pride image from the API. Asynchronous.

        Args:
            image (string): The bytes, URL link or path of the input image.
            itype (string): The output image type. Can be 'circle', 'overlay', 'square' or 'background'.
            istyle (string): The output image style. Can be either 'solid' or 'gradient'.
            flag (Flag): The Flag to create the image with.
            iformat (str, optional): The output image format. Can be either 'png' or 'jpg'. Defaults to 'png'.
            output_file (string, optional): If not None, the output image will also be created under this path. Defaults to None.

        Raises:
            ValueError: Wrong values inserted for 'itype', 'istyle' or 'iformat'.

        Returns:
            bytes: The output image in bytes.
        """
        endpoint = f'{self.host}/image/static/{itype}/{istyle}/{flag.name}.{iformat}'
        if itype not in types:
            raise ValueError(f'imageStatic: itype must be one of {types}')
        if istyle not in styles:
            raise ValueError(f'imageStatic: istyle must be one of {styles}')
        if iformat not in formats:
            raise ValueError(f'imageStatic: iformat must be one of {formats}')
        files = {
            'file' : await imageToByte(image, self.throttle.session)
        }
        response = await self.throttle.chew(Request(endpoint, 'POST', None, files))
        return await handleImageStatic(response, output_file)

    async def imageAnimated(self, image, itype, flag, output_file=None):
        """Generates an animated pride image from the API. Asynchronous.

        Args:
            image (string): The bytes, URL link or path of the input image.
            itype (string): The output image type. Can be either 'circle' or 'square'.
            flag (Flag): The Flag to create the image with.
            output_file (string, optional): If not None, the output image will also be created under this path. Defaults to None.

        Raises:
            ValueError: Wrong value inserted for 'itype'.

        Returns:
            bytes: The output image in bytes.
        """
        endpoint = f'{self.host}/image/animated/{itype}/{flag.name}'
        if itype not in atypes:
            raise ValueError(f'imageAnimated: itype must be one of {atypes}')
        files = {
            'file' : imageToByte(image, self.throttle.session)
        }
        response = await self.throttle.chew(Request(endpoint, 'POST', None, files))
        return await handleImageStatic(response, output_file)