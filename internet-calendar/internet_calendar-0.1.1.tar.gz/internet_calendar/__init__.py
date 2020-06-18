import pendulum
import json
from bs4 import BeautifulSoup
import re
from requests_cache import CachedSession
from datetime import timedelta
"""
the web url matching regex used by markdown
http://daringfireball.net/2010/07/improved_regex_for_matching_urls
https://gist.github.com/gruber/8891611
"""
URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""


class Forekast:

    expire_after = timedelta(hours=1)
    session = CachedSession(backend='memory', expire_after=expire_after)

    def __init__(self, lazy=False, load_all=False):
        self.url = "https://forekast.com"
        self._parsed = False
        self._events = {}
        self._just_added = []
        self._trending = []
        self._page = 0
        if not lazy:
            self._parse()
            if load_all:
                self.load_more(999999)

    def _parse(self):
        html = self.session.get(self.url+"?page={n}".format(n=self._page)).text
        soup = BeautifulSoup(html, 'html.parser')

        # parse highlights
        just_added = []
        trending = []
        for s in soup.find_all("preview-event"):
            _event = json.loads(s.attrs[":event"])
            descript = _event["description"]
            urls = None
            if descript:
                descript = descript.replace("</br>", "\n")
                urls = re.findall(URL_REGEX, descript)
                descript = re.sub(URL_REGEX, "", descript)\
                    .replace("\r\n", "").strip()
            date = pendulum.parse(_event["started_at"]).date()
            event = {"name": _event["name"],
                    # "is_all_day": _event["is_all_day"],
                     "country": _event["country"],
                     "event_type": _event["subkast"],
                     "image": _event["image"],
                     "description": descript,
                     "urls": urls,
                     "date": date}
            if s.attrs["title"] == "Trending":
                trending.append(event)
            if s.attrs["title"] == "Just Added":
                just_added.append(event)
            if event["name"] not in self.events:
                self._events[event["name"]] = event

        self._just_added = just_added
        self._trending = trending

        # parse events
        for s in soup.find_all("event-thumb"):
            _event = json.loads(s.attrs[":event"])
            descript = _event["description"]
            urls = None
            if descript:
                descript = descript.replace("</br>", "\n")
                urls = re.findall(URL_REGEX, descript)
                descript = re.sub(URL_REGEX, "", descript) \
                    .replace("\r\n", "").strip()
            date = pendulum.parse(_event["started_at"]).date()

            event = {"name": _event["name"],
                   #  "is_all_day": _event["is_all_day"],
                     "country": _event["country"],
                     "event_type": _event["subkast"],
                     "image": _event["image"],
                     "description": descript,
                     "urls": urls,
                     "date": date}
            if event["name"] not in self.events:
                self._events[event["name"]] = event

        self._page += 1

    @property
    def event_types(self):
        e_types = []
        for e in self.events:
            e = self.events[e]
            if e["event_type"] not in e_types:
                e_types.append(e["event_type"])
        return e_types

    @property
    def events(self):
        return self._events

    def trending(self):
        if not self._parsed:
            self._parse()
        return self._trending

    def just_added(self):
        if not self._parsed:
            self._parse()
        return self._just_added

    def yesterday(self):
        # TODO recent events uses js
        raise NotImplemented
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["date"] == pendulum.yesterday().date():
                events.append(event)
        return events

    def today(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["date"] == pendulum.today().date():
                events.append(event)
        return events

    def tomorrow(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["date"] == pendulum.tomorrow().date():
                events.append(event)
        return events

    def sports_events(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["event_type"] == "sports":
                events.append(event)
        return events

    def tv_events(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["event_type"] == "tv":
                events.append(event)
        return events

    def music_events(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["event_type"] == "music":
                events.append(event)
        return events

    def gaming_events(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["event_type"] == "tv":
                events.append(event)
        return events

    def holidays(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["event_type"] == "holidays":
                events.append(event)
        return events

    def space_events(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["event_type"] == "space":
                events.append(event)
        return events

    def art_events(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["event_type"] == "arts":
                events.append(event)
        return events

    def other_events(self):
        if not self._parsed:
            self._parse()
        events = []
        for event_name in self.events:
            event = self.events[event_name]
            if event["event_type"] == "other":
                events.append(event)
        return events

    def load_more(self, pages=1):
        total = len(self.events)
        for i in range(pages):
            self._parse()
            if len(self.events) == total:
                return
            total = len(self.events)

