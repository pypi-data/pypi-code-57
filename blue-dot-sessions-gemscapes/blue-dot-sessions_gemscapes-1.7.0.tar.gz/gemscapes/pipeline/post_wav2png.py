import logging
import os
import typing

import PIL

from ..metadata import BDSMetaDataType

module_logger = logging.getLogger(__name__)


def c2c(
    img: PIL.Image, input_c: typing.Tuple[int], output_c: typing.Tuple[int]
) -> PIL.Image:
    """
    Convert one color to another in a PIL Image object.

    Args:
        img: PIL image object
        input_c: Input color in either RGB or RGBA tuple
        output_c: output color in either RGB or RGBA tuple

    Returns:
        modified PIL image object
    """
    if len(input_c) == 4 or len(output_c) == 4:
        module_logger.debug("c2c: converting to RGBA")
        img.convert("RGBA")

    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if all([pixdata[x, y][idx] == input_c[idx] for idx in range(len(input_c))]):
                pixdata[x, y] = output_c

    return img


def post_wav2png(
    file_path: str,
    v_wssf: float = 1.0,
    h_wssf: float = 1.0,
    track_metadata: BDSMetaDataType = None,
    dry_run: bool = False
) -> str:
    """
    This function runs after wav2png, doing any modification necessary before
    sending to primitive.

    Right now this converts the white background to transparent, and adds
    vertical and horitonal white space

    Args:
        file_path: Input .png file path
        v_wssf: "vertical white space scale factor"
            Scale the vertical axis by this much, adding
            white space. Must be greater than or equal to 1.0. If 1.0, no
            white space will be added.
        h_wssf: "horizontal white space scale factor"
            Scale the horitonal axis by this much, adding
            white space. Must be greater than or equal to 1.0. If 1.0, no
            white space will be added.
        dry_run: Run without modifying anything

    Returns:
        output file path

    """
    output_file_path = "{}.post_wav2png.png".format(os.path.splitext(file_path)[0])
    white = (255, 255, 255)
    transparent = (255, 255, 255, 0)
    # transparent = (0, 0, 0, 0)
    if not dry_run:
        img = PIL.Image.open(file_path)
        img_info = img.info
        width, height = img.size
        img.thumbnail((width, height))
        new_width = int(h_wssf * width)
        new_height = int(v_wssf * height)
        module_logger.debug(f"post_wav2png: old size=({width}, {height})")
        module_logger.debug(f"post_wav2png: new size=({new_width}, {new_height})")
        idx = (new_width - width) / 2
        idy = (new_height - height) / 2
        module_logger.debug(f"post_wav2png: pos=({idx}, {idy})")

        new_img = PIL.Image.new("RGBA", (new_width, new_height), color=white)
        new_img.paste(img, (int(idx), int(idy)))
        new_img = c2c(new_img, white, transparent)
        new_img.save(output_file_path, **img_info)

    return output_file_path
