from .models import Flag
from .util import byteToImageFile

def handleFlags(response, host):
    """Handles returning of Flag response value.

    Args:
        response (requests.Response): Request response
        host (string): Base URL of the API host.

    Returns:
        list: List of all available flags, as classes
    """
    json = response.json()
    flags = []
    for i in json:
        flag = Flag(i, json[i]['defaultAlpha'], json[i]['tooltip'], f'{host}/icon/{i}')
        flags.append(flag)
    return flags

def handleIconBytes(response):
    """Handles returning of iconBytes response value.

    Args:
        response (requests.Response): Request response

    Returns:
        bytes: Icon image in bytes
    """
    return response.content

def handleImageStatic(response, file_output):
    """Handles returning of imageStatic response value

    Args:
        response (requests.Response): Request response
        file_output (string): Optional path to save the output image

    Returns:
        bytes: Output image in bytes
    """
    if file_output is not None:
        byteToImageFile(response.content, file_output)
    return response.content

    