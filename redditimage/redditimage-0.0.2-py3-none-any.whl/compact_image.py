# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Pip
from PIL import Image, ImageDraw, ImageFont

# Local
from .utils import pil_utils
from .models.positioned_image import PositionedImage
from .models.relative_position import RelativePosition

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: CompactImage ---------------------------------------------------------- #

class CompactImage:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        distance: int,
        padding: int,
        image: Image = None,
        bg_color: (int, int, int, int) = (0, 0, 0, 0)
    ):
        self.distance = distance
        self.padding = padding
        self.bg_color = bg_color

        self.images = {}

        if image is not None:
            self.add_image(image)


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def add_image(
        self,
        image: Image,
        positioned: Optional[RelativePosition] = None,
        to_image: Image = None,
        centered: bool = False,
        extra_distance_x: int = 0,
        extra_distance_y: int = 0
    ) -> None:
        _to_image = self.images[self.__hash(to_image)] if to_image is not None else None

        if _to_image is not None:
            if positioned == RelativePosition.Right:
                x = _to_image.max_x + self.distance + extra_distance_x
                y = _to_image.y if not centered else self.__centered_val(_to_image.y, _to_image.h, image.size[1])
            else:
                # only bottom supported curreently
                x = _to_image.x if not centered else self.__centered_val(_to_image.x, _to_image.w, image.size[0])
                y = _to_image.max_y + self.distance + extra_distance_y
        else:
            x = extra_distance_x
            y = extra_distance_y

        self.images[self.__hash(image)] = PositionedImage(image, x, y)

    def render(self, width: Optional[int] = None, height: Optional[int] = None) -> Image:
        min_x = 0
        min_y = 0
        max_x = width or 0
        max_y = height or 0

        for image in self.images.values():
            if image.x < min_x:
                min_x = image.x

            if image.y < min_y:
                min_y = image.y

            if image.max_x > max_x:
                max_x = image.max_x

            if image.max_y > max_y:
                max_y = image.max_y

        lx = max_x - min_x + 2*self.padding
        ly = max_y - min_y + 2*self.padding

        width = width or lx
        height = height or ly

        multi = 1

        if lx > width:
            multi = float(width)/float(lx)

        if ly > height:
            _multi = float(height)/float(ly)

            if _multi < multi:
                multi = _multi

        img = pil_utils.image(width, height, color=self.bg_color)

        for layer in self.images.values():
            sub_img = layer.image

            if multi != 1:
                sub_img = sub_img.resize((int(float(layer.w) * multi), int(float(layer.h) * multi)), Image.ANTIALIAS)

            img.paste(sub_img, (layer.x + self.padding - min_x, layer.y + self.padding - min_y), sub_img)

        return img


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __hash(self, image: Image) -> str:
        import hashlib

        return hashlib.md5(image.tobytes()).hexdigest()
    
    def __centered_val(self, oo: int, ol: int, l: int) -> int:
        return oo + int((float(ol) - float(l)) / 2)


# ---------------------------------------------------------------------------------------------------------------------------------------- #