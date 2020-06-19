import math

from PIL import Image, ImageDraw

from ..color import (interpolate_colors_rgb,
                     COLOR_SCHEMES,
                     DEFAULT_COLOR_SCHEME_KEY)


__all__ = [
    "WaveformImage"
]


class WaveformImage(object):
    """
    Given peaks and spectral centroids from the AudioProcessor, this class will construct
    a wavefile image which can be saved as PNG.
    """
    def __init__(self, image_width, image_height, palette, background_color: tuple = None):
        if image_height % 2 == 0:
            print("WARNING: Height is not uneven, images look much better at uneven height")

        if background_color is None:
            background_color = (0, 0, 0)
        # if color_scheme not in COLOR_SCHEMES:
        #     background_color = (0, 0, 0)
        #     colors = getattr(cc, color_scheme)
        # else:
        #     waveform_colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES[DEFAULT_COLOR_SCHEME_KEY])['wave_colors']
        #     background_color = waveform_colors[0]
        #     colors = waveform_colors[1:]
        #
        # self.palette = interpolate_colors_rgb(colors)
        self.palette = palette
        if len(self.palette) < 256:
            raise RuntimeError("palette has to be at least 256 elements in size")

        self.image = Image.new("RGB", (image_width, image_height), background_color)

        self.image_width = image_width
        self.image_height = image_height

        self.draw = ImageDraw.Draw(self.image)
        self.previous_x, self.previous_y = None, None

        self.pix = self.image.load()

    def draw_peaks(self, x, peaks, spectral_centroid, peak_width=1, transform_fn=None):
        """ draw 2 peaks at x using the spectral_centroid for color """
        if transform_fn is None:
            def transform_fn(spectral_centroid):
                return spectral_centroid
        # module_logger.debug(f"WaveformImage.draw_peaks: x={x}, peaks={peaks}, spectral_centroid={spectral_centroid}")
        y1 = self.image_height * 0.5 - peaks[0] * (self.image_height - 4) * 0.5
        y2 = self.image_height * 0.5 - peaks[1] * (self.image_height - 4) * 0.5

        # line_color = self.palette[min(int((spectral_centroid-.02)*355.0), 255)]
        line_color = self.palette[min(int(transform_fn(spectral_centroid)*255.0), 255)]

        if peak_width == 1:
            if self.previous_y != None:
                self.draw.line([self.previous_x, self.previous_y, x, y1, x, y2], line_color, width=peak_width)
            else:
                self.draw.line([x, y1, x, y2], line_color, width=peak_width)
            self.previous_x, self.previous_y = x, y2
            self.draw_anti_aliased_pixels(x, y1, y2, line_color)
        else:
            x *= peak_width
            self.draw.rectangle([
                (x, y2), (x + peak_width, y1)
            ], fill=line_color, width=0)


    def draw_anti_aliased_pixels(self, x, y1, y2, color):
        """ vertical anti-aliasing at y1 and y2 """

        y_max = max(y1, y2)
        y_max_int = int(y_max)
        alpha = y_max - y_max_int

        if alpha > 0.0 and alpha < 1.0 and y_max_int + 1 < self.image_height:
            current_pix = self.pix[x, y_max_int + 1]

            r = int((1-alpha)*current_pix[0] + alpha*color[0])
            g = int((1-alpha)*current_pix[1] + alpha*color[1])
            b = int((1-alpha)*current_pix[2] + alpha*color[2])

            self.pix[x, y_max_int + 1] = (r,g,b)

        y_min = min(y1, y2)
        y_min_int = int(y_min)
        alpha = 1.0 - (y_min - y_min_int)

        if alpha > 0.0 and alpha < 1.0 and y_min_int - 1 >= 0:
            current_pix = self.pix[x, y_min_int - 1]

            r = int((1-alpha)*current_pix[0] + alpha*color[0])
            g = int((1-alpha)*current_pix[1] + alpha*color[1])
            b = int((1-alpha)*current_pix[2] + alpha*color[2])

            self.pix[x, y_min_int - 1] = (r,g,b)

    def save(self, filename):
        # draw a zero "zero" line
        a = 25
        for x in range(self.image_width):
            self.pix[x, self.image_height/2] = tuple(
                map(lambda p: p+a, self.pix[x, self.image_height/2]))

        self.image.save(filename)
