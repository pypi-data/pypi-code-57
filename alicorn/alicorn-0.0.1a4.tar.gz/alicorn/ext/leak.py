#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#

import time
from alicorn.extension import Extension
from alicorn import Alicorn


class ShutdownExtension(Extension):
    """An extension to automatically shut down the server after a number of requests are served and/or after a certain
    amount of time that the server has been serving in order to prevent memory leaks.

    Configuration:
        ext.leak.max_requests (int, optional)     -   Number of requests to serve before shutting the server down
        ext.leak.max_time (int/float, optional)   -   Time the server should run for before shutting down in seconds.
        ext.leak.grace_period (int, optional)     -   The grace period the server is allowed to shut down in seconds.

    Both conditions can be specified in which case both condition must be met before the server is shutdown.

    Note: Since this only runs after request teardowns 'max_requests' actually refers to the minimum number of requests
    the server will server before terminating. Likewise the server will not automatically shut down while idle if
    'max_time' is specified, it will only be shut down after a request.
    """

    def __init__(self):
        self.app = None
        self.n_req = 0
        self.start_time = time.time()

    def register(self, app: Alicorn):
        self.n_req = 0
        self.start_time = time.time()
        self.app = app
        self.app.after_request_teardown(self.after_request_teardown)

    def after_request_teardown(self):
        self.n_req += 1
        max_req = self.app.config.get('ext.leak.max_requests')
        max_time = self.app.config.get('ext.leak.max_time')

        if not max_req and not max_time:
            return

        if max_req is not None and max_req < self.n_req:
            return

        time_since_start = time.time()

        if max_time is not None and max_time < time_since_start:
            return

        self.app.stop(self.app.config.get('ext.leak.grace_period'))
