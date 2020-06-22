#!/usr/bin/env python3

import argparse
import logging
import logging.handlers
import sys
import os

this_dir_abs_path_str = os.path.dirname(os.path.abspath(__file__))
parent_dir_abs_path_str = os.path.dirname(this_dir_abs_path_str)
# print(f"{this_dir_abs_path_str=}")
print(f"{parent_dir_abs_path_str=}")
# print(f"{sys.path=}")
# sys.path.append(this_dir_abs_path_str)
sys.path.append(parent_dir_abs_path_str)
# -this is done automatically by pycharm (run configurations), but in case we run from a script
# we need to have it here
# Pycharm docs: https://www.jetbrains.com/help/pycharm/configuring-content-roots.html
from kammanta import glob

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--testing", "-t", help="Testing (data saved in memory only)", action="store_true")
# -for info about "store_true" please search here: https://docs.python.org/3/howto/argparse.html
argument_parser.add_argument("--example", "-e", help="Example (data saved in memory only)", action="store_true")
args = argument_parser.parse_args()
glob.testing_bool = False
glob.example_bool = False
if args.testing:
    glob.testing_bool = True
    glob.copy_and_setup_testing()
if args.example:
    glob.example_bool = True
    glob.copy_and_setup_testing()

from PyQt5 import QtWidgets
import kammanta.gui.main_window


def on_about_to_quit_fired():
    logging.info("Exiting Kammanta application")


def main():
    # Logging
    # Please also see the code in the kammanta.__init__.py module for more info on how we do logging
    logger = logging.getLogger()
    # -if we set a name here for the logger the file handler will no longer work, unknown why
    logger.handlers = []  # -removing the default stream handler first
    # logger.propagate = False
    log_file_path_str = kammanta.glob.get_config_path("main.log")
    # -TODO: at the moment the config dir is used, do we want to change this to something else?

    # Logging to file
    rfile_handler = logging.handlers.RotatingFileHandler(log_file_path_str, maxBytes=8192, backupCount=2)
    rfile_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    rfile_handler.setFormatter(formatter)
    logger.addHandler(rfile_handler)

    # Logging to stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Handling of (otherwise) uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.excepthook(exc_type, exc_value, exc_traceback)

        if issubclass(exc_type, Exception):
            logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        else:
            sys.excepthook(exc_type, exc_value, exc_traceback)
        """
    sys.excepthook = handle_exception

    logging.info("Starting Kammanta application")

    application = QtWidgets.QApplication(sys.argv)
    application.aboutToQuit.connect(on_about_to_quit_fired)
    os.makedirs(kammanta.glob.get_config_path(), exist_ok=True)
    main_window = kammanta.gui.main_window.MyMainWindow()
    application.setQuitOnLastWindowClosed(False)
    main_window.show()
    application.exec_()


if __name__ == "__main__":
    main()


"""

 "QtWidgets." och lägga till ", parent=self"


-sunyata@bollingen:~/.config/kammanta/example_testing$ /home/sunyata/.local/bin/kammanta --testing
parent_dir_abs_path_str='/home/sunyata/.local/lib/python3.8/site-packages'
Traceback (most recent call last):
  File "/home/sunyata/.local/bin/kammanta", line 5, in <module>
    from kammanta.__main__ import main
  File "/home/sunyata/.local/lib/python3.8/site-packages/kammanta/__main__.py", line 30, in <module>
    my_glob.copy_and_setup_testing()
  File "/home/sunyata/.local/lib/python3.8/site-packages/kammanta/my_glob.py", line 123, in copy_and_setup_testing
    shutil.copytree(src_path_str, dst_path_str)
  File "/usr/lib/python3.8/shutil.py", line 552, in copytree
    with os.scandir(src) as itr:
FileNotFoundError: [Errno 2] No such file or directory: '/home/sunyata/.local/lib/python3.8/site-packages/testing/example'
sunyata@bollingen:~/.config/kammanta/example_testing$ 


Question: Do we want to save the settings for example and testing?


idea: dynamic nr of external tools? This works well with having a separate section in the settings
file


Still problems with the random crashes, maybe trying to fix this by adding more self-references
when creating objects/widgets


1. set support for an NA and then choosing cancel (only a problem when running live)
2. 


? PLEASE NOTE: For personal actual usage: Active tasks are moved into "projects-focus" in Kammanta


### Bugs

FnD: Dock "ä" in the file name doesn't work
however having "Å" in a dir in the path does work! Strange

processing: cannot add next action (nothing happens)

Processing: adding non-text files to reference (ex .ogg)



### User testing

#### Tasks

Using the processing system for the inbox files (after the application update)


### Refactoring

Clean up, etc. Looking for "TODO"

Potential files:
* model.py
* X gui/checklist_cw.py



#### Tasks


#### Ideas

Maybe a system for recurring actions?



### Programming (new) features

#### Tasks


#### Future tasks

error handling that is user-friendly (see wbd)

low prio: saving on application close

minor graphics bug: when deleting an inbox entry it takes some time to rebuild the list and it looks strange for a
short time


#### Ideas

[gen-ref] and [gtd-main] could be used in the file names for project links
we could even use this in the desktop links maybe?


### Other tasks (ex: Organizing, infrastructure, docs)

#### Tasks





#### Ideas

programming: standardizing the way that prefixes and suffixes are added and removed
underscore and dot (.) suffix/prefix

adding a setting for the default number of days until the next tickler appears (right now it's 7)


### Arch

#### Tasks


#### Ideas

.write() or .store() function to update underlying filesystem
This would then be called at the end of functions that changes the data


### Design ######################

#### Tasks



#### Ideas

lägga till focus action in systray

idea: for next actions it's possible to just give a string as the end result, even if we have a
directory or file path. it is a good idea to let this have a field in the support dlg that is
filled in any case?

tickler: connection to remembering, wbd, matc?
recurring NAs: same (with connection)

automatically running commands at certain intervals (maybe using the tickler system or recurring action system?)
alt: allowing the user to run the commands manually, by simply "opening" the .desktop file

systray: lägga till active next action (behöver tänka på att det funkar efter update_gui). eller
kanske ett aktuellt projekt? både och?

New habits: Another section?

NA-listor med kommentarer som visas separat från todo:er? Problem: om vi har kommentarerna på nya rader så kan vi inte använda line-nr för att mappa till qlistwidget

Possible to link between different parts of the application? Relative html links will work on android (for example) and could maybe be handled programmatically for the desktop

Review mode?
Brain dump, kanske i samband med review?

"done" lists

opening url when selected in the processing text reader


-> design idea: attach the processing dlg window to the side of the application, for easier processing integration (for example with search in reference files)
another idea: allowing this to be a floating window also!

allowing .desktop files as contexts. when chosen in the combobox the link is activated


processing for any file (now possible since it accepts a search path rather than a inbox item ID)

Popup at specific time (and date), maybe each day. Maybe part of the inbox or tickler system

Considering using text files as the default instead of directories (this is based on my own experience!)
(We may need a convert function for when the user wants to expand the project she is working on)

PRIO: looking into: allowing any file/dir as a project (but maybe adding only .desktop files and dirs)
if so: for the filters: only filtering for NAs and for project-groups

maybe sending reminder to contact friends? (using tickler)

for tickled inbox items (items starting with a time) we may to have "tickling" as an easier action

Info about context in the first line of a todo list file? Maybe starting with a special character?

Date for Next Actions, plus side dock containing notifications of nr of inbox entries and
Next Actions that are (1) late, (2) to be done today, or (3) the next day

open external file explorer, together with email and calendar (in the corner widget)

considering showing a popup when a file has been saved, with the exception of checkboxes

list of projects for adding reference materials for (in the processing widiget)

help clearing out the old reference files?
the oldest files can be shown? Maybe even the ones accessed longest ago?

**********************************
**********************************
**********************************


### Unsorted ideas

*Coaching* starting with the inbox items:
* Do
* Defer (open email application)
* Next action
* Incubate
* File as PSM ref
* File as general ref

Possible places for coaching:
* Dock window
* status bar at the bottom
* another tab

GTD help, ex: PSM 80% 15% 5%


Creating a shared move operation, where files get a changed filename when moved

And adding an initial setup
* Adding a separator for "waiting for" and "someday/maybe"
* (Checking wbd to see how i handle init there)
waiting-for.txt (always create?)
someday-maybe/ (always create?)
home.txt
office.txt
errands.txt
(reading.txt)
mental contexts?

Design idea: checklists, lists (both from reference)

testing move
design thinking: implementing moving to an agenda list?

Thinking todo: what to do with files that doesn't match the pattern? logging a warning?

(Low prio and may be difficult) Programming todo: When dock is closed with the x we want to update the checkbox
in the window menu

handling cases with suffixes which aren't really suffixes
(sometimes a dot might get into a name and then it stays there)
one idea is to have a list of recognized suffixes, like
.txt, .desktop, _



### Questions

#### **Can it be a good practice to use temporary objects that are recreated when there is a change
in the underlying data storage?**

"Flyweight objects"

For example: I am working on an application where we store data in text files, and also in the
file system itself (the names of dirs and files are used). Sometimes the user might make changes
in the part of the file system that we use for our data storage (this is by design) and then we
want to update our interface to reflect these changes

#### Good practice to use a files as the backend with FSWatcher?

Can this be trusted?


### Programming notes

#### Datetime in NextCloud

Handling the dates of files:
For NextCloud it's different which times are preserved:
https://github.com/nextcloud/server/issues/15192
Conclusion: best to keep the date in the file name

#### FS watcher

asking in irc channel: Is fsw reliable enough to use as a part of the application backend? or better to call
the update_gui function ourselves after making an edit in the application?

update_item_list
step 1: clearing
step 2: using os.walk or os.listdir
step 3: adding files


### Legal

GTD copyright?
Name is copyrighted, but what about the contents themselves?

GTDNext is doing a lot with GTD, even the name: https://gtdnext.com/

Inculding a notice similar to the one on gtdnext.com?

Removing gtd_info.py?


### Design research notes

alternativeto.net: https://alternativeto.net/software/gtdnext/


#### David Allen on best software

https://gettingthingsdone.com/2019/07/david-allen-on-the-best-software-for-gtd/


#### DA Ultimate GTD application: my notes

reminder in inbox area for processing paper materials

email action for inbox items

alarm for doing shorter things

Project support structure (page 6/19)
- unprocessed notes
- how long?
- project template (for coaching)
- purpose
- successful outcome scenario
- components/sequences/priorities. ex:
  * component 1
  * comp 2 (high prio)
    * sequence step 1
    * seq step 2

recurring tickler items

weekly review/debriefing
coaching (page 19/19)

routines + reminders? --- from "areas of focus" (page 14/19) (different from areas of interest and accountability)
reference lists (see page 16/19)
checklists


#### Other software

https://www.nirvanahq.com/pro

http://www.eproductivity.com/dx/screenshots

#### Books

Getting Things Done Workbook
ebook or paperback


"""
