import os
from functools import partial
import typing
import json

from PIL import Image, ImageDraw, ImageColor
import colour
import toml

from .util import desaturate, color_from_value

__all__ = [
    "COLOR_SCHEMES",
    "DEFAULT_COLOR_SCHEME_KEY",
    "load_from_file"
]


COLOR_SCHEMES = {
    'Freesound2_norm_lum': {
        'wave_colors': [
            (0, 0, 0),  # Background color
            (51.200000000000095, 0.0, 204.8),
            (0.0, 204.8, 74.47272727272728),
            (204.8, 179.90274509803928, 0.0),
            (204.8, 56.2196078431372, 0.0)
        ],
        'spec_colors': [
            (0, 0, 0),  # Background color
            (58/4, 68/4, 65/4),
            (80/2, 100/2, 153/2),
            (90, 180, 100),
            (224, 224, 44),
            (255, 60, 30),
            (255, 255, 255)
         ]
    },
    'Freesound2': {
        'wave_colors': [
            (0, 0, 0),  # Background color
            (50, 0, 200),  # Low spectral cetroid
            (0, 220, 80),
            (255, 224, 0),
            (255, 70, 0),  # High spectral cetroid
        ],
        'spec_colors': [
            (0, 0, 0),  # Background color
            (58/4, 68/4, 65/4),
            (80/2, 100/2, 153/2),
            (90, 180, 100),
            (224, 224, 44),
            (255, 60, 30),
            (255, 255, 255)
         ]
    },
    'FreesoundBeastWhoosh': {
        'wave_colors': [
            (255, 255, 255),  # Background color
            (29, 159, 181),  # 1D9FB5, Low spectral cetroid
            (28, 174, 72),  # 1CAE48
            (255, 158, 53),  # FF9E35
            (255, 53, 70),  # FF3546, High spectral cetroid
        ],
        'spec_colors': [
            (0, 0, 0),  # Background color/Low spectral energy
            (29, 159, 181),  # 1D9FB5
            (28, 174, 72),  # 1CAE48
            (255, 158, 53),  # FF9E35
            (255, 53, 70),  # FF3546, High spectral energy
         ]
    },
    'Cyberpunk': {
        'wave_colors': [(0, 0, 0)] + [color_from_value(value/29.0) for value in range(0, 30)],
        'spec_colors': [(0, 0, 0)] + [color_from_value(value/29.0) for value in range(0, 30)],
    },
    'Rainforest': {
        'wave_colors': [(213, 217, 221)] + list(map(partial(desaturate, amount=0.1), [
                        (50, 0, 200),
                        (0, 220, 80),
                        (255, 224, 0),
                     ])),
        'spec_colors': [(213, 217, 221)] + list(map(partial(desaturate, amount=0.7), [
                        (50, 0, 200),
                        (0, 220, 80),
                        (255, 224, 0),
                     ])),
    }
}

DEFAULT_COLOR_SCHEME_KEY = 'Freesound2'


def load_palettes_from_file(file_path: str) -> dict:
    """
    Give some configuration file, either JSON or TOML, load in data.
    """
    with open(file_path, "r") as fd:
        if file_path.endswith(".toml"):
            palettes = toml.load(fd)
        elif file_path.endswith(".json"):
            palettes = json.load(fd)
        else:
            raise RuntimeError(
                ("load_palettes_from_file: Unsupported color palette"
                 f" file type: {os.path.splitext(file_path)[1]}"))
    return palettes


def standardize_palettes(palettes_obj: dict) -> typing.Dict[str, typing.Dict[str, list]]:
    """
    Given some palettes loaded from a file, standardize them so they all
    behave the same, regardless of initial structure.
    """
    def conversion_factory(type_name: str) -> callable:
        def normalize(val):
            if any([v > 1.0 for v in val]):
                val = [v / 256.0 for v in val]
            return val

        def conversion(val: typing.Union[list, str]) -> list:
            if type_name == "rgb":
                if hasattr(val, "startswith"):
                    if val.startswith("#"):
                        return colour.Color(val).rgb
                    else:
                        raise RuntimeError(
                            ("load_from_file.conversion_factory.conversion: "
                             f"Cannot load hexval {val} without beginning #"))
                else:
                    val = normalize(val)
                    return colour.Color(rgb=val).rgb
            elif type_name == "hsl":
                val = normalize(val)
                return colour.Color(hsl=val).rgb

        return conversion

    ret_palettes = {}

    for palette_name in palettes_obj:
        palette = palettes_obj[palette_name]
        background = [0.0, 0.0, 0.0]
        conversion = conversion_factory("rgb")
        if hasattr(palette, "keys"):
            type_name = "rgb"
            if "type" in palette:
                type_name = palette["type"]
            conversion = conversion_factory(type_name)

            if "background" in palette:
                background = conversion(palette["background"])
            colors = palette["palette"]
        else:
            colors = palette

        colors = [conversion(val) for val in colors]

        ret_palettes[palette_name] = {
            "background": background,
            "palette": colors
        }

    return ret_palettes


def load_from_file(file_path: str) -> typing.Dict[str, typing.Dict[str, list]]:
    """
    Load some color scheme from a file.

    File should be structured as follows:

    ```
    {
        "palette0": [
            [r, g, b]
            [r, g, b]
        ],
        "palette1": [
            "#hexcode0",
            "#hexcode1"
        ],
        "palette2": {
            "background": [h, s, l]
            "palette": [
                [h, s, l],
                ...
            ],
            type: "hsl"
        },
        "palette3": {
            "background": "#hexcode"
            "palette": [
                [r, g, b],
                ...
            ],
            type: "rgb" # not necessary, as this is implied
        }
    }
    ```

    Args:
        file_path (str): Path to file containing palettes.
            Can use either toml or json file
    Return:
        dict: Each entry is a dict with "background" and "palette" keys,
            containing rgb values ranging from 0.0 to 1.0
    """

    palettes_obj = load_palettes_from_file(file_path)
    return standardize_palettes(palettes_obj)
