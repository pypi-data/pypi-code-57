"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Queue
import sys
import os


def main(args, extra):

    # Create a queue object, run the command to match to an executor
    queue = Queue(config_dir=args.config_dir)

    # Pass the queue object to start a server
    try:
        from rse.app.server import start

        start(port=args.port, queue=queue, debug=args.debug)
    except:
        sys.exit(
            "You must 'pip install rse[app]' 'pip install rse[all]' to use the dashboard."
        )
