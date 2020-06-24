# This file is part of openreviewio-py.
#
# openreviewio-py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# openreviewio-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with openreviewio-py.  If not, see <https://www.gnu.org/licenses/>

from pathlib import Path
import toml
from typing import Union


class TextComment:
    body: str

    def __init__(self, body: str):
        """Text comment related to the whole media.

        :param body: Comment message
        :type body: str
        """
        self.body = body


class Image:

    __mime__ = {"jpeg", "jpg", "png"}
    path_to_image: Union[Path, str]

    def __init__(self, path_to_image: Union[Path, str]):
        """Image related to the whole media.

        :param path_to_image: Path to image file
        """
        self.path_to_image = Path(path_to_image)

        # Check mime for file extension
        if path_to_image:
            file = Path(self.path_to_image)
            if file.suffix.replace(".", "") not in self.__mime__:
                raise TypeError(
                    f"Image file '{file.suffix}' extension format is not valid. "
                    f"Please select either: {', '.join(sorted(self.__mime__))}."
                )


class ImageAnnotation(Image):
    frame: int
    duration: int
    reference_image: Union[Path, str, Image]

    def __init__(
        self,
        path_to_image: Union[Path, str],
        frame: int,
        duration: int,
        reference_image: Union[Path, str, Image] = "",
    ):
        """Image related to a frame and a duration of the media.

        :param path_to_image: Path to annotation image
        :param frame: Starting frame
        :type frame: int
        :param duration: Frames duration
        :type duration: int
        :param reference_image: Keep an image path as reference for the drawing
        """
        super(ImageAnnotation, self).__init__(path_to_image)

        self.frame = frame
        self.duration = duration

        self.reference_image = reference_image

    # reference image getter setter
    @property
    def reference_image(self):
        return self._reference_image.path_to_image

    @reference_image.setter
    def reference_image(self, value):
        # Sentinel for reference image
        if value and value.__class__ is not Image:
            self._reference_image = Image(value)
