class Request(object):
    """Request object.

    Args:
        endpoint (string): API endpoint for the request.
        method (string): Method for the request.
        body (string, optional): Request body. Defaults to None.
        files (dict, optional): Request files. Defaults to None.
    """
    def __init__(self, endpoint, method, body=None, files=None):
        self.endpoint = endpoint
        self.method = method
        self.body = body
        self.files = files

class Flag(object):
    """Flag object.

    Args:
        name (string): Name of the flag.
        default_alpha (int, optional): Default alpha value. Defaults to 255.
        tooltip (string, optional): Description/full name of the flag. Defaults to None.
        image (string, optional): URL Link to flag's icon. Defaults to None.
    """
    def __init__(self, name, default_alpha=255, tooltip=None, image=None):
        self.name = name
        self.default_alpha = default_alpha
        self.tooltip = tooltip
        self.image = image

types = {'circle', 'overlay', 'square', 'background'}
atypes = { 'circle', 'square' }
styles = {'solid', 'gradient'}
formats = {'png', 'jpg'}
mimes = {'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/jpg'}
