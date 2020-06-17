from PIL import Image, ImageDraw, ImageFont


class ImageAnnotator(object):

    def __init__(self,
                 img_path: str,
                 font: str = None,
                 font_size: int = 5):
        assert isinstance(img_path, str)
        self._img = Image.open(img_path).convert('RGBA')
        self._img_draw = ImageDraw.Draw(self._img)

        if font is None:
            self._font = None
        else:
            assert isinstance(font, str)
            self._font = ImageFont.truetype(font, font_size)

    def image(self):
        return self._img.convert('RGB')

    def save(self, img_path):
        self._img.convert('RGB').save(img_path)

    def draw_line(self,
                  points: list,
                  fill: str = None,
                  width: int = 1):
        """
        Draw a line on image
        """
        assert isinstance(points, (list, tuple)) and len(points) == 2
        for pair in points:
            assert isinstance(pair, tuple) and len(pair) == 2
        self._img_draw.line(points, fill, width)

    def draw_rectangle(self,
                       points: list,
                       outline: str = None,
                       width: int = 1,
                       text: str = None,
                       text_fill: str = None):
        """
        Draw detection bounding box with text
        """
        assert isinstance(points, (list, tuple))
        assert len(points) == 2 or len(points) == 4
        for pair in points:
            assert len(pair) == 2

        if len(points) == 4:
            points = [points[0], points[2]]

        self._img_draw.rectangle(points, outline=outline, width=width)

        if text is not None:
            assert isinstance(text, str)
            text_points = (points[0][0], points[1][1])
            self.draw_text(points=text_points,
                           text=text,
                           fill=text_fill)

    def draw_polygon(self,
                     points: list,
                     outline: str = None,
                     width: int = 1,
                     text: str = None,
                     text_fill: str = None):
        """
        Draw polygon with text
        """
        assert isinstance(points, (tuple, list)) and len(points) > 2
        for pair in points:
            assert isinstance(pair, tuple) and len(pair) == 2

        for i in range(len(points)):
            line_pts = (points[i], points[(i+1) % len(points)])
            self.draw_line(points=line_pts,
                           fill=outline,
                           width=width
                           )

        if text is not None:
            assert isinstance(text, str)
            self.draw_text(points=points[0],
                           text=text,
                           fill=text_fill)

    def draw_text(self,
                  points: tuple,
                  text: str,
                  fill: str = None,
                  ):
        """
        Draw text on image
        """
        assert isinstance(points, tuple) and len(points) == 2
        self._img_draw.text(points, text, font=self._font, fill=fill)
