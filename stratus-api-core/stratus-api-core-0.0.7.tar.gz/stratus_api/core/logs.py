def get_logger():
    import logging, sys
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logger = logging.getLogger(__name__)
    return logger
