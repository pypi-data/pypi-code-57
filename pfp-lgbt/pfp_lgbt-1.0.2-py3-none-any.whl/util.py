from os import path

from .models import mimes
from .error import UnsupportedMIMEError, ConvertImageError

async def byteToImageFile(byte, file):
    """Writes bytes to a file.

    Args:
        byte (bytes): The bytes to write.
        file (string): Path of the file to write to.
    """
    if isinstance(byte, (bytes, bytearray)):
        with open(file, 'wb') as f:
            f.write(byte)

async def imageToByte(image, session):
    """Attempts to auto-detect between URL link, bytes and local file path, and converts image to bytes.

    Args:
        image (string): Must be either bytes, URL link or local file path of image.

    Raises:
        ConvertImageError: Provided string is not an URL link, bytes, nor local file path to image.

    Returns:
        bytes: Bytes of the image.
    """
    if isinstance(image, (bytes, bytearray)):
        return image
    elif isUrl(image):
        if await isValidMIME(image, session):
            response = await session.get(image)
            return await response.read()
    elif path.exists(image):
        try:
            with open(image, 'rb') as img:
                return img.read()
        except:
            raise
    else:
        raise ConvertImageError('Provided image must be byte array, url or path')

def isUrl(image):
    """Checks if a string is an URL link.

    Args:
        image (string): The string to be checked.

    Returns:
        bool: True if it is a valid URL link, False if otherwise.
    """
    try:
        if image.startswith('https') or image.startswith('http'):
            return True
        return False
    except:
        return False

async def isValidMIME(image, session):
    """Checks to see whether a URL link leads to a supported image.

    Args:
        image (string): URL link to the image.

    Raises:
        UnsupportedMIMEError: Content-Type/MIME is either not present or not one of supported types.

    Returns:
        bool: True if supported, otherwise False.
    """
    response = await session.head(image)
    if 'Content-Type' in response.headers:
        if response.headers['Content-Type'] in mimes:
            return True
        raise UnsupportedMIMEError(f'Expected {mimes}, got {response.headers["Content-Type"]}')
    raise UnsupportedMIMEError(f'Content-Type not in headers.')