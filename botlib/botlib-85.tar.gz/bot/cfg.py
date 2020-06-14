# BOTLIB - the bot library !
#
#

from .irc import Cfg

def cfg(event):
    c = Cfg()
    c.last()
    try:
        c.server, c.channel, c.nick = event.args
        c.save()
    except:
        event.reply(c)
        return
    event.reply("ok")
