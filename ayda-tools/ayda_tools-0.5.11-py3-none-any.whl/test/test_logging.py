from ayda_tools.client.resultservice import AydaLogger
from ayda_tools.client.connection import ServerConnection
from mock import MagicMock, patch
import sys

from queue import Queue
import logging

log = logging.getLogger(__name__)


def test_logging_print():
    conn = MagicMock(spec=ServerConnection)
    backup_queue = Queue()
    logger = AydaLogger("1234", conn)
    logger.lines = backup_queue
    with patch("time.sleep"):
        with logger:
            print("test")

    logged = []
    while not backup_queue.empty():
        logged.append(backup_queue.get())
    assert logged == ["test"]


def test_logging_print_stderr():
    conn = MagicMock(spec=ServerConnection)
    backup_queue = Queue()
    logger = AydaLogger("1234", conn)
    logger.lines = backup_queue
    with patch("time.sleep"):
        with logger:
            print("test", file=sys.stderr)

    logged = []
    while not backup_queue.empty():
        logged.append(backup_queue.get())
    assert logged == ["test"]


def test_logging_use_logging():
    conn = MagicMock(spec=ServerConnection)
    backup_queue = Queue()
    logger = AydaLogger("1234", conn)
    logger.lines = backup_queue
    with patch("time.sleep"):
        with logger:
            log.warning("test")

    logged = []
    while not backup_queue.empty():
        logged.append(backup_queue.get())
    assert logged == ["test"]
