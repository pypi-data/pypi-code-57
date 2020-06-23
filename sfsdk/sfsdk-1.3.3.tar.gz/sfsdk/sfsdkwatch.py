#!/usr/bin/env python2

# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import json
import time
import os
import sys
from threading import Lock
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

modified_files = []
lock = Lock()
folder_to_monitor = None

def on_any_event(event):

    global folder_to_monitor

    path_to_add = event.src_path
    if path_to_add == folder_to_monitor:
        return

    # Cut the path to have just the piece just after the / 
    # of the folder to monitor
    path_to_add = os.path.sep.join(
        path_to_add.split(os.path.sep)[0:folder_to_monitor.count('/')+2]
    )

    # Add the trailing slash if it's a folder
    if os.path.isdir(path_to_add):
        path_to_add = os.path.join(path_to_add, '')

    lock.acquire()
    if not path_to_add in modified_files:


        modified_files.append(path_to_add)

        with open(status_json, 'w') as outfile:
            json.dump(modified_files, outfile, indent=2)

    lock.release()

if __name__ == "__main__":

    global folder_to_monitor

    if len(sys.argv) != 3:
        print('Usage: sfsdkwatch.py <folder> <output file>')
        sys.exit(1)

    folder_to_monitor = sys.argv[1].rstrip('/') # No ending slash
    status_json = sys.argv[2]

    event_handler = PatternMatchingEventHandler(
            ignore_patterns=[
                "/home/sf/.Xauthority*",
                "/home/sf/.xorgxrdp.*",
                "/home/sf/.xsession-errors",
                "/home/sf/.dbus/**",
                "/home/sf/.dbus",
                "/home/sf/.cache/**",
                "/home/sf/.cache",
                "/home/sf/thinclient_drives/**",
                "/home/sf/thinclient_drives",
                "/home/sf/.ICEauthority*",
                "/home/sf/.gvfs/**",
                "/home/sf/.gvfs",
                "/home/sf/exercise/app/**",
                "/home/sf/exercise/app",
                "/home/sf/exercise/.sf/**",
                "/home/sf/exercise/.sf",
                ],
            ignore_directories=False,
            case_sensitive=True
            )
    event_handler.on_any_event = on_any_event

    observer = Observer()
    observer.schedule(event_handler, folder_to_monitor, recursive=True)
    observer.start()

    # Create an empty json when ready
    with open(status_json, 'w') as outfile:
        json.dump([], outfile)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
                observer.stop()
    observer.join()
