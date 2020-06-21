import sys
import logging
import socket
from typing import List

import telegram_log.handler

from yad_uploader.arguments import Arguments


def configure_logger(logger: logging.Logger, tg_token: str, tg_chat_ids: List[str]):
    logger.setLevel(logging.DEBUG)
    host_name = socket.gethostname()
    log_format = '%(asctime)s [%(levelname)s] [{0} %(name)s:%(lineno)s] %(message)s'.format(host_name)
    formatter = logging.Formatter(log_format)
    if tg_token and tg_chat_ids:
        tg_handler = telegram_log.handler.TelegramHandler(token=tg_token, chat_ids=tg_chat_ids, err_log_name='')
        tg_handler.setLevel(logging.ERROR)
        tg_handler.setFormatter(formatter)
        logger.addHandler(tg_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def set_exception_hook(logger: logging.Logger):
    def excepthook(exctype, value, traceback):
        logger.exception('', exc_info=(exctype, value, traceback))

    sys.excepthook = excepthook


def setup(options: Arguments):
    assert options.tg_token
    assert options.tg_chats_id
    _logger = logging.getLogger(__name__)
    configure_logger(_logger, options.tg_token, options.tg_chats_id)
    set_exception_hook(_logger)
