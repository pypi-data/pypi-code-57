# OKLIB - the ok library !.
#
#

import ok.obj, os, time

from ok.krn import get_kernel
from ok.obj import cdir
from ok.dbs import Db

def __dir__():
    return ("find",)

k = get_kernel()

def find(event):
    if not event.args:
        wd = os.path.join(ok.obj.workdir, "store", "")
        cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0] for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    db = Db()
    target = db.all
    otype = event.args[0]
    try:
       match = event.args[1]
       target = db.find_value
    except:
       match = None
    try:
        args = event.args[2:]
    except ValueError:
        args = None
    nr = -1
    for o in target(otype, match):
        nr += 1
        event.display(o, str(nr), args or o.keys())
    if nr == -1:
        event.reply("no %s found." % otype)
