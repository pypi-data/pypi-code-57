"""This is a Docstring"""
import typer
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from enum import Enum
import filetype
import os


app = typer.Typer()

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version("imagetitle")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


class TitlePosition(str, Enum):
    """ What position of the image do we want to position the title? """

    bottom = "bottom"
    top = "top"
    left = "left"
    right = "right"


def version_callback(value: bool):
    """ Check that we have a version response for this application. """
    if value:
        typer.echo(f"Version: {__version__}")
        raise typer.Exit()


def font_callback(value: bool):
    """ Does this font exist on this operating system? """
    try:
        font = ImageFont.truetype(value)  # noqa: F841
    except OSError:
        raise typer.BadParameter(f"'{value}' font not found.")
    return value


def input_callback(value: Path):
    """ Check that the file exists and check that it is an image. """
    if not value.is_file():
        raise typer.BadParameter(f"Input file {value} not found.")
    else:
        kind = filetype.guess(
            os.path.abspath(str(value)),
        )  # filetype cannot deal with Path objects yet.
        if kind.MIME not in [
            "image/jpeg",
            "image/jpx",
            "image/png",
            "image/gif",
            "image/webp",
            "image/tiff",
            "image/bmp",
        ]:
            raise typer.BadParameter(f"Input file {value} not a suitable image file.")
    return value


@app.command()
def main(
    input: Path = typer.Option(
        "input.png",
        "-i",
        "--input",
        help="Image file name.",
        show_default=True,
        callback=input_callback,
    ),
    output: Path = typer.Option(
        "output.png", "-o", "--output", help="Output file name.", show_default=True,
    ),
    position: TitlePosition = typer.Option(
        "bottom",
        "-p",
        "--position",
        help="Where to position the tile.",
        show_default=True,
    ),
    title_text: str = typer.Option(
        "Some text.", "-t", "--title", help="Text for title.", show_default=False,
    ),
    font_name: str = typer.Option(
        "Ubuntu-C.ttf",
        "-f",
        "--font",
        help="Font name or path.",
        show_default=False,
        callback=font_callback,
    ),
    fraction: float = typer.Option(
        "0.75",
        "-r",
        "--fraction",
        help="What fraction, 0 to 1, of the image edge should be covered by the title?",
        show_default=True,
        min=0,
        max=1,
    ),
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    """ Overlay a title over the edge of the image. """

    source_img = Image.open(input)
    image_format = source_img.format
    source_img = source_img.convert("RGBA")
    width, hight = source_img.size

    fontsize = 1  # starting font size
    font = ImageFont.truetype(font_name, fontsize)
    breakpoint = fraction * source_img.size[0]
    jumpsize = 75
    while True:
        if font.getsize(title_text)[0] < breakpoint:
            fontsize += jumpsize
        else:
            jumpsize = int(jumpsize / 2)
            fontsize -= jumpsize
        font = ImageFont.truetype(font_name, fontsize)
        if jumpsize <= 1:
            break

    # get text size
    text_size = font.getsize(title_text)

    # set button size + 10px margins
    button_size = (text_size[0] + 20, text_size[1] + 20)

    # create image with correct size and black background
    button_img = Image.new("RGBA", button_size, "grey")

    # put text on button with 10px margins
    button_draw = ImageDraw.Draw(button_img)
    button_draw.text((10, 10), title_text, font=font)

    # put button on source image in position (0, 0)
    if position == "bottom":
        source_img.paste(button_img, (0, hight - button_size[1]))
    elif position == "top":
        source_img.paste(button_img, (0, 0))
    elif position == "right":
        transposed_img = button_img.transpose(Image.ROTATE_270)
        source_img.paste(transposed_img, (width - button_size[1], 0))
    elif position == "left":
        transposed_img = button_img.transpose(Image.ROTATE_90)
        source_img.paste(transposed_img, (0, hight - button_size[0]))

    # save in new file
    source_img.convert("RGB").save(output, image_format)
    return
