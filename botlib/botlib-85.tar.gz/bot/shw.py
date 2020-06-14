# OKLIB - the ok library !
#
#

from ok.obj import get_type
from ok.krn import get_kernel

k = get_kernel()

def cmds(event):
    bot = k.fleet.by_orig(event.orig)
    if not bot:
        bot = k
    event.reply("|".join(sorted(bot.cmds)))

def fleet(event):
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet])
