import math

from PIL import Image

from ..color import (interpolate_colors_rgb,
                     COLOR_SCHEMES,
                     DEFAULT_COLOR_SCHEME_KEY)

__all__ = [
    "SpectrogramImage"
]


class SpectrogramImage(object):
    """
    Given spectra from the AudioProcessor, this class will construct a wavefile image which
    can be saved as PNG.
    """
    def __init__(self, image_width, image_height, fft_size, palette):
        self.image_width = image_width
        self.image_height = image_height
        self.fft_size = fft_size

        self.image = Image.new("RGB", (image_height, image_width))
        # self.palette = interpolate_colors_rgb(COLOR_SCHEMES.get(color_scheme,
        #                                                     COLOR_SCHEMES[DEFAULT_COLOR_SCHEME_KEY])['spec_colors'])
        self.palette = palette
        if len(self.palette) < 256:
            raise RuntimeError("palette has to be at least 256 elements in size")
        # generate the lookup which translates y-coordinate to fft-bin
        self.y_to_bin = []
        f_min = 100.0
        f_max = 22050.0
        y_min = math.log10(f_min)
        y_max = math.log10(f_max)
        for y in range(self.image_height):
            freq = math.pow(10.0, y_min + y / (image_height - 1.0) *(y_max - y_min))
            bin = freq / 22050.0 * (self.fft_size/2 + 1)

            if bin < self.fft_size/2:
                alpha = bin - int(bin)

                self.y_to_bin.append((int(bin), alpha * 255))

        # this is a bit strange, but using image.load()[x,y] = ... is
        # a lot slower than using image.putadata and then rotating the image
        # so we store all the pixels in an array and then create the image when saving
        self.pixels = []

    def draw_spectrum(self, x, spectrum, peak_width=1):
        # for all frequencies, draw the pixels
        for idx in range(peak_width):
            for (index, alpha) in self.y_to_bin:
                self.pixels.append(
                    self.palette[int((255.0-alpha) * spectrum[index] + alpha * spectrum[index + 1])])

        # if the FFT is too small to fill up the image, fill with black to the top
        # for idx in range(peak_width):
            for y in range(len(self.y_to_bin), self.image_height):
                self.pixels.append(self.palette[0])

    def save(self, filename, quality=80):
        # assert filename.lower().endswith(".jpg")
        self.image.putdata(self.pixels)
        self.image.transpose(Image.ROTATE_90).save(filename, quality=quality)
