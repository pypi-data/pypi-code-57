# OKBOT - the ok bot !
#
#

import re, time, urllib

from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode, urlunparse
from urllib.request import Request, urlopen

from ok.obj import Cfg, Default, Object
from ok.clk import Repeater
from ok.dbs import Db
from ok.krn import get_kernel
from ok.thr import launch
from ok.tms import to_time, day

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

def __dir__():
    return ("Cfg,", "Feed", "Rss", "Seen", "Fetcher", "delete", "display", "feed", "fetch", "init", "rss")

debug = False

k = get_kernel()

def init(kernel):
    fetcher = Fetcher()
    fetcher.start()
    return fetcher

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.display_list = "title,link"
        self.dosave = True
        self.tinyurl = False

class Feed(Default):

    pass

class Rss(Object):

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(Object):

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(Object):

    cfg = Cfg()
    seen = Seen()

    def __init__(self):
        super().__init__()
        self._thrs = []

    def display(self, o):
        result = ""
        dl = []
        try:
            dl = o.display_list.split(",")
        except AttributeError:
            pass
        if not dl:
            dl = self.cfg.display_list.split(",")
        if not dl or not dl[0]:
            dl = ["title", "link"]
        for key in dl:
            if not key:
                continue
            data = o.get(key, None)
            if key == "link" and self.cfg.tinyurl:
                datatmp = get_tinyurl(data)
                if datatmp:
                    data = datatmp[0]
            if data:
                data = data.replace("\n", " ")
                data = strip_html(data.rstrip())
                data = unescape(data)
                result += data.rstrip()
                result += " - "
        return result[:-2].rstrip()

    def fetch(self, obj):
        counter = 0
        objs = []
        if not obj.rss:
            return 0
        for o in reversed(list(get_feed(obj.rss))):
            if not o:
                continue
            feed = Feed()
            feed.update(obj)
            feed.update(o)
            u = urllib.parse.urlparse(feed.link)
            if u.path and not u.path == "/":
                url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
            else:
                url = feed.link
            if url in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(url)
            counter += 1
            objs.append(feed)
            if self.cfg.dosave:
                feed.save()
        if objs:
            Fetcher.seen.save()
        for o in objs:
            k.fleet.announce(self.display(o))
        return counter

    def run(self):
        thrs = []
        db = Db()
        for o in db.all("bot.rss.Rss"):
            thrs.append(launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        Fetcher.cfg.last()
        Fetcher.seen.last()
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()
            return repeater

    def stop(self):
        Fetcher.seen.save()

def file_time(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp)).replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def get_feed(url):
    if debug:
        return [Object(), Object()]
    try:
        result = get_url(url)
    except Exception as ex:
        return [Object(), Object()]
    if gotparser:
        res = feedparser.parse(result.data)
        if "entries" in res:
            for entry in res["entries"]:
                yield entry
    else:
        print("feedparser is missing")
        return [Object(), Object()]

def get_tinyurl(url):
    postarray = [
        ('submit', 'submit'),
        ('url', url),
        ]
    postdata = urlencode(postarray, quote_via=quote_plus)
    req = Request('http://tinyurl.com/create.php', data=bytes(postdata, "UTF-8"))
    req.add_header('User-agent', useragent())
    for txt in urlopen(req).readlines():
        line = txt.decode("UTF-8").strip()
        i = re.search('data-clipboard-text="(.*?)"', line, re.M)
        if i:
            return i.groups()

def get_url(url):
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent())
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response

def strip_html(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def unescape(text):
    import html
    import html.parser
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)

def useragent():
    return 'Mozilla/5.0 (X11; Linux x86_64) OKBOT +http://git@bitbucket.org/bthate/ok)'

def delete(event):
    if not event.args:
        event.reply("delete <match>")
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    db = Db()
    for rss in db.find("bot.rss.Rss", selector):
        nr += 1
        rss._deleted = True
        got.append(rss)
    for rss in got:
        rss.save()
    event.reply("ok")

def display(event):
    if len(event.args) < 2:
        event.reply("display <feed> key1,key2,etc.")
        return
    nr = 0
    setter = {"display_list": event.args[1]}
    db = Db()
    for o in db.find("bot.rss.Rss", {"rss": event.args[0]}):
        nr += 1
        o.edit(setter)
        o.save()
    event.reply("ok")

def feed(event):
    if not event.args:
        event.reply("feed <match>")
        return
    match = event.args[0]
    nr = 0
    diff = time.time() - to_time(day())
    db = Db()
    res = list(db.find("bot.rss.Feed", {"link": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s - %s" % (nr, o.title, o.summary, o.updated or o.published or "nodate", o.link))
        nr += 1
    if nr:
        return
    res = list(db.find("bot.rss.Feed", {"title": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1
    res = list(db.find("bot.rss.Feed", {"summary": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1
    if not nr:
        event.reply("no results found")
 
def fetch(event):
    res = []
    thrs = []
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    event.reply("fetched %s" % ",".join([str(x) for x in res]))

def rss(event):
    db = Db()
    if not event.args or "http" not in event.args[0]:
        nr = 0
        for o in db.find("bot.rss.Rss", {"rss": ""}):
            event.reply("%s %s" % (nr, o.rss))
            nr += 1
        if not nr:
            event.reply("rss <url>")
        return
    url = event.args[0]
    res = list(db.find("bot.rss.Rss", {"rss": url}))
    if res:
        event.reply("feed is already known.")
        return
    o = Rss()
    o.rss = event.args[0]
    o.save()
    event.reply("ok")
