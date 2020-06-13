#  Copyright 2020 Parakoopa
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
from typing import List, Tuple

try:
    from PIL import Image, ImageOps
except ImportError:
    from pil import Image, ImageOps
from skytemple_rust.pmd_wan import WanImage, MetaFrameGroup, MetaFrame, Animation


class MetaFramePositioningSpecs:
    def __init__(self, img: Image, width: int, height: int, x_offset: int, y_offset: int):
        self.img = img
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset
        # This will be filled and contain the offset on the image specs generated by process.
        self.final_relative_x = None
        self.final_relative_y = None

    @classmethod
    def process(cls, items: List['MetaFramePositioningSpecs']) -> Tuple[int, int, int, int]:
        """
        Returns the full image dimensions and the image's center point and set's
        the final_relative_x/y attributes of all entries

        -> (width, height, center x, center y)
        """
        if len(items) < 1:
            return 0, 0, 0, 0
        smallest_x = 9999999
        smallest_y = 9999999
        biggest_x = -9999999
        biggest_y = -9999999

        for frame in items:
            smallest_x = min(smallest_x, frame.x_offset)
            smallest_y = min(smallest_y, frame.y_offset)
            biggest_x = max(biggest_x, frame.x_offset + frame.width)
            biggest_y = max(biggest_y, frame.y_offset + frame.height)

        for frame in items:
            frame.final_relative_x = frame.x_offset - smallest_x
            frame.final_relative_y = frame.y_offset - smallest_y

        return (biggest_x - smallest_x), (biggest_y - smallest_y), abs(smallest_x), abs(smallest_y)


class Wan:
    def __init__(self, data):
        self.model: WanImage = WanImage(data)

    @property
    def frame_groups(self):
        return self.model.meta_frame_store.meta_frame_groups

    @property
    def anim_groups(self):
        return self.model.anim_store.anim_groups

    @property
    def animations(self):
        return self.model.anim_store.animations

    def get_animations_for_group(self, anim_group: Tuple[int, int]) -> List[Animation]:
        return self.model.anim_store.animations[anim_group[0]:anim_group[0]+anim_group[1]]

    def render_frame_group(self, frame_group: MetaFrameGroup) -> Tuple[Image.Image, Tuple[int, int]]:
        """Returns the frame group as an image and it's center position as a tuple."""
        specs: List[MetaFramePositioningSpecs] = []

        for mf_i, meta_frame_id in enumerate(frame_group.meta_frames_id):
            meta_frame: MetaFrame = self.model.meta_frame_store.meta_frames[meta_frame_id]
            meta_frame_img = self.model.image_store.images[meta_frame.image_index]

            im = Image.frombuffer('RGBA',
                                  (meta_frame_img.width, meta_frame_img.height),
                                  bytearray(meta_frame_img.img),
                                  'raw', 'RGBA', 0, 1)
            if meta_frame.h_flip:
                im = ImageOps.mirror(im)
            if meta_frame.v_flip:
                im = ImageOps.flip(im)

            specs.append(MetaFramePositioningSpecs(im, meta_frame_img.width, meta_frame_img.height,
                                                   meta_frame.offset_x, meta_frame.offset_y))

        w, h, cx, cy = MetaFramePositioningSpecs.process(specs)

        final_img = Image.new('RGBA', (w, h), (255, 0, 0, 0))
        for frame in specs:
            final_img.paste(
                frame.img,
                (frame.final_relative_x, frame.final_relative_y,
                 frame.final_relative_x + frame.width, frame.final_relative_y + frame.height),
                frame.img
            )

        return final_img, (cx, cy)
