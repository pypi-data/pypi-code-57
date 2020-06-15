from time import sleep

from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import OperationalError


class RetryingQuery(BaseQuery):
    __retry_count__ = 3
    __retry_sleep_interval_sec__ = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().__iter__()
            except OperationalError as ex:
                if "server closed the connection unexpectedly" not in str(ex):
                    raise
                if attempts < self.__retry_count__:
                    print("Connection lost - sleeping for %.2f sec and will retry (attempt #%d)",
                          self.__retry_sleep_interval_sec__, attempts)
                    sleep(self.__retry_sleep_interval_sec__)
                    continue
                else:
                    raise
