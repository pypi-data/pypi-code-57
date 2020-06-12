from PIL import ImageColor


__all__ = [
    "desaturate",
    "color_from_value"
]


def desaturate(rgb, amount):
    """
        desaturate colors by amount
        amount == 0, no change
        amount == 1, grey
    """
    luminosity = sum(rgb) / 3.0
    desat = lambda color: color - amount * (color - luminosity)

    return tuple(map(int, map(desat, rgb)))


def color_from_value(value):
    """ given a value between 0 and 1, return an (r,g,b) tuple """
    return ImageColor.getrgb("hsl(%d,%d%%,%d%%)" % (int((1.0 - value) * 360), 80, 50))
