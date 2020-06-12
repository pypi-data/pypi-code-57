# -*- coding: utf-8 -*-

# Copyright 2016-2020 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://downloads.khinsider.com/"""

from .common import Extractor, Message, AsynchronousMixin
from .. import text, exception


class KhinsiderSoundtrackExtractor(AsynchronousMixin, Extractor):
    """Extractor for soundtracks from khinsider.com"""
    category = "khinsider"
    subcategory = "soundtrack"
    directory_fmt = ("{category}", "{album[name]}")
    archive_fmt = "{filename}.{extension}"
    pattern = (r"(?:https?://)?downloads\.khinsider\.com"
               r"/game-soundtracks/album/([^/?&#]+)")
    root = "https://downloads.khinsider.com"
    test = (("https://downloads.khinsider.com"
             "/game-soundtracks/album/horizon-riders-wii"), {
        "pattern": r"https?://vgmdownloads.com/soundtracks/horizon-riders-wii/"
                   r"[^/]+/Horizon%20Riders%20Wii%20-%20Full%20Soundtrack.mp3",
        "keyword": "5b2c35cce638c326cab2a4f7a79f245d008d62ff",
    })

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.album = match.group(1)

    def items(self):
        url = self.root + "/game-soundtracks/album/" + self.album
        page = self.request(url, encoding="utf-8").text
        if "Download all songs at once:" not in page:
            raise exception.NotFoundError("soundtrack")

        data = self.metadata(page)
        yield Message.Version, 1
        yield Message.Directory, data
        for track in self.tracks(page):
            track.update(data)
            yield Message.Url, track["url"], track

    def metadata(self, page):
        extr = text.extract_from(page)
        return {"album": {
            "name" : text.unescape(extr("Album name: <b>", "<")),
            "count": text.parse_int(extr("Number of Files: <b>", "<")),
            "size" : text.parse_bytes(extr("Total Filesize: <b>", "<")[:-1]),
            "date" : extr("Date added: <b>", "<"),
            "type" : extr("Album type: <b>", "<"),
        }}

    def tracks(self, page):
        page = text.extract(page, '<table id="songlist">', '</table>')[0]

        for num, url in enumerate(text.extract_iter(
                page, '<td class="clickable-row"><a href="', '"'), 1):
            url = text.urljoin(self.root, url)
            page = self.request(url, encoding="utf-8").text

            url = text.extract(page, 'style="color: #21363f;" href="', '"')[0]
            yield text.nameext_from_url(url, {"num": num, "url": url})
