from io import BytesIO
from pathlib import Path
from typing import Optional

from PIL import Image
from mutagen.flac import FLAC, Picture

from .music import MusicMeta
from .utils import first


class FlacMeta(MusicMeta):
    def __init__(self, path: Path):
        super().__init__(FLAC(path))

    @property
    def cover(self) -> Optional[bytes]:
        return first(self._file.pictures())

    @cover.setter
    def cover(self, value: Optional[bytes]):
        self._file.clear_pictures()
        if value is None:
            return

        stream = BytesIO(value)
        image = Image.open(stream)
        mime = image.get_format_mimetype()

        picture = Picture()
        picture.type = 3
        picture.mime = mime
        picture.data = value
        self._file.add_picture(picture)

    def save(self):
        self._file.save()
