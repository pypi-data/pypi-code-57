class UnsupportedMIMEError(Exception):
    """Exception raised when Content-Type/MIME is not supported."""
    pass

class ConvertImageError(Exception):
    """Exception raised when an issue prevents the image being converted into bytes."""
    pass