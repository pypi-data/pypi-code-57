from typing import List, Optional

from .utils import first


class MusicMeta:
    COMPOSERS = "composer"
    LYRICISTS = "lyricist"
    TITLE = "title"
    ARTIST = "artist"
    LYRICS = "unsyncedlyrics"
    DISC_NUMBER = "discnumber"
    ALBUM = "album"
    ALBUM_ARTIST = "albumartist"
    GENRE = "genre"
    DATE = "date"
    TRACK_NUM = "tracknumber"

    preserve_tags = [
        COMPOSERS,
        LYRICISTS,
        TITLE,
        ARTIST,
        LYRICS,
        DISC_NUMBER,
        DATE,
        GENRE,
        TRACK_NUM,
        ALBUM_ARTIST,
        ALBUM,
    ]

    def __init__(self, file):
        self._file = file

    @property
    def title(self) -> Optional[str]:
        return self._get(self.TITLE)

    @title.setter
    def title(self, value: Optional[str]):
        self._set(self.TITLE, value)

    @property
    def artist(self) -> Optional[str]:
        return self._get(self.ARTIST)

    @artist.setter
    def artist(self, value: Optional[str]):
        self._set(self.ARTIST, value)

    @property
    def artists(self) -> List[str]:
        return self._get_list(self.ARTIST)

    @artists.setter
    def artists(self, value: List[str]):
        self._set_list(self.ARTIST, value)

    @property
    def composers(self) -> List[str]:
        return self._get_list(self.COMPOSERS)

    @composers.setter
    def composers(self, value: List[str]):
        self._set_list(self.COMPOSERS, value)

    @property
    def lyricists(self) -> List[str]:
        return self._get_list(self.LYRICISTS)

    @lyricists.setter
    def lyricists(self, value: List[str]):
        self._set_list(self.LYRICISTS, value)

    @property
    def lyrics(self) -> Optional[str]:
        return self._get(self.LYRICS)

    @lyrics.setter
    def lyrics(self, value: Optional[str]):
        self._set(self.LYRICS, value)

    @property
    def disc_num(self) -> Optional[str]:
        return self._get(self.DISC_NUMBER)

    @disc_num.setter
    def disc_num(self, value: Optional[str]):
        self._set(self.DISC_NUMBER, value)

    @property
    def album(self) -> Optional[str]:
        return self._get(self.ALBUM)

    @album.setter
    def album(self, value: Optional[str]):
        self._set(self.ALBUM, value)

    @property
    def albumartist(self) -> Optional[str]:
        return self._get(self.ALBUM_ARTIST)

    @albumartist.setter
    def albumartist(self, value: Optional[str]):
        self._set(self.ALBUM_ARTIST, value)

    @property
    def genre(self) -> Optional[str]:
        return self._get(self.GENRE)

    @genre.setter
    def genre(self, value: Optional[str]):
        self._set(self.GENRE, value)

    @property
    def date(self) -> Optional[str]:
        return self._get(self.DATE)

    @date.setter
    def date(self, value: Optional[str]):
        self._set(self.DATE, value)

    @property
    def tracknumber(self) -> Optional[str]:
        return self._get(self.TRACK_NUM)

    @tracknumber.setter
    def tracknumber(self, value: Optional[str]):
        self._set(self.TRACK_NUM, value)

    @property
    def cover(self) -> Optional[bytes]:
        raise NotImplementedError()

    @cover.setter
    def cover(self, value: Optional[bytes]):
        raise NotImplementedError()

    def clear(self):
        for tag in self._file.keys():
            if tag not in self.preserve_tags:
                self._file.pop(tag)

    def save(self):
        raise NotImplementedError()

    def _get(self, key: str) -> Optional[str]:
        return first(self._file.get(key, []))

    def _set(self, key: str, value: Optional[str]):
        if value is None:
            self._file.pop(key)
        else:
            self._file[key] = [value]

    def _get_list(self, key: str) -> List[str]:
        return self._file.get(key, [])

    def _set_list(self, key: str, value: List[str]):
        if value is None or len(value) <= 0:
            if key in self._file:
                self._file.pop(key)
        else:
            self._file[key] = value
