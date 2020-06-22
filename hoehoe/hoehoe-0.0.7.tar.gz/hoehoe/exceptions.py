class AdvertNotFoundException(Exception):
    pass


class RoxaThresholdingException(Exception):
    """
    That basically means that roksa gave us a ban and will
    respond with 403's for certain period of time.
    """
    pass


class ParsingAdException(Exception):
    """
    Something went wrong while beautifulsouping an advert.
    This might happen because Roksa probably changed their templates.
    """
    pass
