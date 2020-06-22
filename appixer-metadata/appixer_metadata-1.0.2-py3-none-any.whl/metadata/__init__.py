from io import BytesIO
from mutagen.id3 import Frames
from mutagen.easyid3 import EasyID3
from PIL import Image

from .flac import FlacMeta
from .mp3 import Mp3Meta
from .music import MusicMeta

__all__ = ["MusicMeta", "FlacMeta", "Mp3Meta"]


def lyric_getter(id3, _key):
    return id3["USLT::jpn"]


def lyric_setter(id3, _key, value):
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    try:
        frame = id3["USLT::jpn"]
    except KeyError:
        id3.add(Frames["USLT"](encoding=3, lang="jpn", text=value))
    else:
        frame.encoding = 3
        frame.lang = "jpn"
        frame.text = value


def lyric_deleter(id3, _key):
    del id3["USLT::jpn"]


def cover_getter(id3, _key):
    return id3["APIC:"]


def cover_setter(id3, _key, value):
    stream = BytesIO(value)
    image = Image.open(stream)
    mime = image.get_format_mimetype()
    try:
        frame = id3["APIC:"]
    except KeyError:
        id3.add(Frames["APIC"](encoding=3, type=3, mime=mime, data=value))
    else:
        frame.encoding = 3
        frame.type = 3
        frame.mime = mime
        frame.data = value


def cover_deleter(id3, _key):
    del id3["APIC:"]


EasyID3.RegisterKey("unsyncedlyrics", lyric_getter, lyric_setter, lyric_deleter)
EasyID3.RegisterKey("cover", cover_getter, cover_setter, cover_deleter)
