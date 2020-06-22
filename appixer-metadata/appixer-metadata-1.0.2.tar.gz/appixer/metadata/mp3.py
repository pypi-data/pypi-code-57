from pathlib import Path
from typing import Optional
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

from .music import MusicMeta


class Mp3Meta(MusicMeta):
    preserve_tags = [
        "TCOM",
        "TEXT",
        "TIT2",
        "TPE1",
        "USLT::jpn",
        "TPOS",
        "TDRC",
        "TCON",
        "TRCK",
        "TPE2",
        "TALB",
        "APIC:",
    ]
    COVER = "cover"

    def __init__(self, path: Path):
        self._path = path
        try:
            file = EasyID3(path)
        except ID3NoHeaderError:
            file = EasyID3()
        super().__init__(file)

    @property
    def lyrics(self) -> Optional[str]:
        return self._file.get(self.LYRICS)

    @lyrics.setter
    def lyrics(self, value: Optional[str]):
        self._file[self.LYRICS] = value

    @property
    def cover(self) -> Optional[bytes]:
        return self._file.get(self.COVER)

    @cover.setter
    def cover(self, value: Optional[bytes]):
        self._file[self.COVER] = value

    def clear(self):
        # pylint: disable=protected-access
        id3 = self._file._EasyID3__id3
        tags = [t for t in id3.keys() if t not in self.preserve_tags]
        for tag in tags:
            id3.pop(tag)

    def save(self):
        self._file.save(self._path, v2_version=3, v23_sep=None)
