# OKLIB - the ok library !
#
#

import ok.obj, os

from ok.dbs import Db
from ok.obj import ENOCLASS, get_cls
from ok.krn import get_kernel

k = get_kernel()

def list_files(wd):
    return "|".join([x for x in os.listdir(os.path.join(wd, "store"))])

def ed(event):
    if not event.args:
        event.reply(list_files(ok.obj.workdir) or "no files yet")
        return
    cn = event.args[0]
    shorts = k.find_shorts("ok")
    if shorts:
        cn = shorts[0]
    db = Db()
    l = db.last(cn)
    if not l:
        try:
            c = get_cls(cn)
            l = c()
            event.reply("created %s" % cn)
        except ENOCLASS:
            event.reply(list_files(ok.workdir) or "no files yet")
            return
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        setter = {event.args[1]: ""}
    else:
        setter = {event.args[1]: event.args[2]}
    l.edit(setter)
    l.save()
