from PIL import Image, ImageDraw, ImageFont
from filehandling import join_path
from omnitools import color_value, textbox
import os


__ALL__ = ["TextToPng"]


class TextToPng(object):
    def __init__(self, font_file: str, font_size: int,
                 background_color: color_value = (0, 0, 0),
                 text_color: color_value = (255, 255, 255),
                 save_dir: str = os.environ["TEMP"]) -> None:
        self.font_file = font_file
        self.font_size = font_size
        self.background_color = background_color
        self.text_color = text_color
        self.save_dir = save_dir

    def create(self, text: str, padding: int = -1, filename: str = None) -> str:
        if filename is None:
            filename = "__tmp.png"
        font = ImageFont.truetype(self.font_file, self.font_size)
        shape, pos = textbox(font, text, padding)
        img = Image.new("RGB", shape, color=self.background_color)
        brush = ImageDraw.Draw(img)
        brush.text(pos, text, font=font, fill=self.text_color)
        save_path = join_path(self.save_dir, filename)
        img.save(save_path)
        return save_path


