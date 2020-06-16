from .models import Flag
from .util import byteToImageFile
import asyncio

async def handleFlags(response, host):
    """Handles returning of Flag response value.

    Args:
        response (requests.Response): Request response
        host (string): Base URL of the API host.

    Returns:
        list: List of all available flags, as classes
    """
    json = await response.json()
    flags = []
    for i in json:
        print(i)
        flag = Flag(i, json[i]['defaultAlpha'], json[i]['tooltip'], f'{host}/icon/{i}')
        flags.append(flag)
    return flags

async def handleIconBytes(response):
    """Handles returning of iconBytes response value.

    Args:
        response (requests.Response): Request response

    Returns:
        bytes: Icon image in bytes
    """
    return await response.read()

async def handleImageStatic(response, file_output):
    """Handles returning of imageStatic response value

    Args:
        response (requests.Response): Request response
        file_output (string): Optional path to save the output image

    Returns:
        bytes: Output image in bytes
    """
    if file_output is not None:
        await byteToImageFile(await response.read(), file_output)
    return await response.read()

