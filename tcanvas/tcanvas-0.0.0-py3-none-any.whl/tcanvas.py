"""Text-based canvases.

Colours
-------

Colours can be specified as a single character string, or as a tuple of RGB
values. Tuples of floats are assumed to be in the 0.0-1.0 range, tuples of ints
in the 0-255 range. Strings map to the default terminal colours like this:

====== ====================
String Colour
====== ====================
0      Default fg/bg colour
k      black
r      red
g      green
y      yellow
b      blue
m      magenta
c      cyan
w      white
K      bright black
R      bright red
G      bright green
Y      bright yellow
B      bright blue
M      bright magenta
C      bright cyan
W      bright white

"""

import click


class Texel(object):
    """One character on the screen.

    Parameters
    ----------

    character : str
        The character to be displayed
    fg_color, bg_color : str or tuple
        Forground and background colours.
    bold, underline, cross, blink : bool
        Set special text effects

    """

    def __init__(
        self,
        character="",
        fg_color="0",
        bg_color="0",
        bold=False,
        faint=False,
        italic=False,
        underline=False,
        cross=False,
        blink=False,
        inverse=False,
        overline=False,
    ):
        self.character = character
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.bold = bold
        self.faint = faint
        self.italic = italic
        self.underline = underline
        self.blink = blink
        self.inverse = inverse
        self.cross = cross
        self.overline = overline

    @staticmethod
    def ansi_color_code(color, bg=False):
        """Return the ANSI colour code for the given colour."""

        # String to default terminal colours
        subs = {
            "k": 30,
            "r": 31,
            "g": 32,
            "y": 33,
            "b": 34,
            "m": 35,
            "c": 36,
            "w": 37,
            "0": 39,  # Reset to default
            "K": 90,
            "R": 91,
            "G": 92,
            "Y": 93,
            "B": 94,
            "M": 95,
            "C": 96,
            "W": 97,
        }
        if color in subs:
            if bg:
                return "%d;" % (subs[color] + 10,)
            else:
                return "%d;" % (subs[color],)

        # Other wise this probably a tuple of rgb values
        if isinstance(color[0], float):
            # Translate 0.0-1.0 floats to 0-255 ints
            color = tuple(int(x * 255) for x in color)
        if bg:
            return "48;2;%d;%d;%d;" % color
        else:
            return "38;2;%d;%d;%d;" % color

    def render(self):
        """Return the ANSI sequence representing the Texel."""

        ansi = "\033["
        ansi += self.ansi_color_code(self.fg_color, bg=False)
        ansi += self.ansi_color_code(self.bg_color, bg=True)
        if self.bold:
            ansi += "1;"
        if self.faint:
            ansi += "2;"
        if self.italic:
            ansi += "3;"
        if self.underline:
            ansi += "4;"
        if self.blink:
            ansi += "5;"
        if self.inverse:
            ansi += "7;"
        if self.cross:
            ansi += "9;"
        if self.overline:
            ansi += "53;"
        ansi = ansi[:-1]  # Remove last ";"
        ansi += "m"
        if len(self.character) > 0:
            ansi += self.character  # The actual character to print
        else:
            ansi += " "
        # Finally reset everything
        ansi += "\033[0m"

        return ansi


class TCanvas(object):
    """A basic canvas.

    Parameters
    ----------

    columns, rows : int or None
        The size of the canvas. Defaults to current terminal size.
    **kwargs : optional
        Properties of the Texels to initialise the canvas.
    """

    def __init__(self, columns=None, rows=None, **kwargs):
        term_width, term_height = click.get_terminal_size()
        if columns is None:
            self._columns = term_width
        else:
            self._columns = columns
        if rows is None:
            self._rows = term_height
        else:
            self._rows = rows

        self.clear(**kwargs)

        self._transformations = {}

    @property
    def size(self):
        """Return the number of columns and rows."""
        return self._columns, self._rows

    def clear(self, **kwargs):
        """Clear the canvas.

        Parameters
        ----------

        **kwargs : optional
            Initialise the Texels with these settings.

        """
        self._buffer = []
        ncol, nrow = self.size
        for row in range(nrow):
            self._buffer.append([])
            for column in range(ncol):
                self._buffer[-1].append(Texel(**kwargs))

    @property
    def buffer(self):
        """Return the buffer of the canvas."""
        return self._buffer

    @property
    def transformations(self):
        """Return the named transformation functions."""
        return self._transformations

    def transform_position(self, pos, transformation=None):
        """Transform a floating point position to a texel index.

        Returns
        -------

        col, row : int

        """

        # No transformation:
        # x = columns from the left
        # y = rows from the top
        if transformation is None:
            return tuple(int(round(x)) for x in pos)

        # Look up transformation
        return self._transformations[transformation](pos)

    def render(self):
        """Render the canvas as a string."""
        string = ""
        for line in self.buffer:
            for texel in line:
                string += texel.render()
            string += "\n"
        # Remove last newline
        return string[:-1]

    def show(self):
        """Print the canvas to the screen.

        This does not print a final newline.

        """

        click.echo(self.render())

    def set(self, pos, transformation=None, **kwargs):
        """Set texel properties at the given position.

        Parameters
        ----------

        pos : (int, int) or (float, float)
            The position of the manipulated texel
        transformation : str, optional
            The transformation to be used to translate between the position
            coordinates and text rows and columns
        **kwargs : optional
            The properties of the Texel to be set

        """

        col, row = self.transform_position(pos, transformation)
        ncol, nrow = self.size
        if 0 <= col < ncol and 0 <= row < nrow:
            for attr, val in kwargs.items():
                setattr(self._buffer[row][col], attr, val)

    def line(self, pos0, pos1, transformation=None, **kwargs):
        """Draw a line between the two positions."""

        px0, py0 = pos0
        px1, py1 = pos1
        x0, y0 = self.transform_position(pos0, transformation)
        x1, y1 = self.transform_position(pos1, transformation)

        Dx = abs(x1 - x0)
        Dy = abs(y1 - y0)
        steps = max(Dx, Dy)

        if steps == 0:
            self.set(pos0, transformation, **kwargs)
        else:
            dpx = (px1 - px0) / steps
            dpy = (py1 - py0) / steps
            x = px0
            y = py0
            self.set((x, y), transformation, **kwargs)

            for i in range(steps):
                x += dpx
                y += dpy
                self.set((x, y), transformation, **kwargs)

    def text(self, pos, text, transformation=None, **kwargs):
        """Write some text at the specified position."""

        x0, y0 = self.transform_position(pos, transformation)
        x, y = x0, y0
        for char in text:
            if char == "\n":
                y += 1
                x = x0
            else:
                self.set((x, y), transformation=None, character=char, **kwargs)
                x += 1
