
_ansi_colors = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "reset": 39,
    "bright_black": 90,
    "bright_red": 91,
    "bright_green": 92,
    "bright_yellow": 93,
    "bright_blue": 94,
    "bright_magenta": 95,
    "bright_cyan": 96,
    "bright_white": 97,
}
_ansi_reset_all = "\033[0m"



# A list of known text names of colors
known_colors = ["black",        # (might be a gray)
                "red",
                "green",
                "yellow",       # (might be an orange)
                "blue",
                "magenta",
                "cyan",
                "white",        # (might be light gray)
                "bright_black",
                "bright_red",
                "bright_green",
                "bright_yellow",
                "bright_blue",
                "bright_magenta",
                "bright_cyan",
                "bright_white",
                "reset"]


def style(
    text,
    fg=None,
    bg=None,
    bold=None,
    dim=None,
    underline=None,
    blink=None,
    reverse=None,
    reset=True,
):
    """Styles a text with ANSI styles and returns the new string.  By
    default the styling is self contained which means that at the end
    of the string a reset code is issued.  This can be prevented by
    passing ``reset=False``.
    Examples::
        click.echo(click.style('Hello World!', fg='green'))
        click.echo(click.style('ATTENTION!', blink=True))
        click.echo(click.style('Some things', reverse=True, fg='cyan'))
    Supported color names:
    * ``black`` (might be a gray)
    * ``red``
    * ``green``
    * ``yellow`` (might be an orange)
    * ``blue``
    * ``magenta``
    * ``cyan``
    * ``white`` (might be light gray)
    * ``bright_black``
    * ``bright_red``
    * ``bright_green``
    * ``bright_yellow``
    * ``bright_blue``
    * ``bright_magenta``
    * ``bright_cyan``
    * ``bright_white``
    * ``reset`` (reset the color code only)
    .. versionadded:: 2.0
    .. versionadded:: 7.0
       Added support for bright colors.
    :param text: the string to style with ansi codes.
    :param fg: if provided this will become the foreground color.
    :param bg: if provided this will become the background color.
    :param bold: if provided this will enable or disable bold mode.
    :param dim: if provided this will enable or disable dim mode.  This is
                badly supported.
    :param underline: if provided this will enable or disable underline.
    :param blink: if provided this will enable or disable blinking.
    :param reverse: if provided this will enable or disable inverse
                    rendering (foreground becomes background and the
                    other way round).
    :param reset: by default a reset-all code is added at the end of the
                  string which means that styles do not carry over.  This
                  can be disabled to compose styles.
    """
    bits = []
    if fg:
        try:
            bits.append(f"\033[{_ansi_colors[fg]}m")
        except KeyError:
            raise TypeError(f"Unknown color {fg!r}")
    if bg:
        try:
            bits.append(f"\033[{_ansi_colors[bg] + 10}m")
        except KeyError:
            raise TypeError(f"Unknown color {bg!r}")
    if bold is not None:
        bits.append(f"\033[{1 if bold else 22}m")
    if dim is not None:
        bits.append(f"\033[{2 if dim else 22}m")
    if underline is not None:
        bits.append(f"\033[{4 if underline else 24}m")
    if blink is not None:
        bits.append(f"\033[{5 if blink else 25}m")
    if reverse is not None:
        bits.append(f"\033[{7 if reverse else 27}m")
    bits.append(text)
    if reset:
        bits.append(_ansi_reset_all)
    return "".join(bits)


# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from HTMLParser import HTMLParser
except:
    from html.parser import HTMLParser


class ColorMarkupClickPrinter(HTMLParser, object):

    def error(self, message):
        pass

    is_bold = False       # the next printed text will be bold
    is_underline = False  # the next printed text will be underlined
    color = ""            # color of the next printed text

    def handle_starttag(self, tag, attrs):

        # make in case independent
        tag = tag.lower()

        # do we know this tag?
        if tag == 'b':
            self.is_bold = True
        elif tag == 'u':
            self.is_underline = True
        elif tag in known_colors:
            self.color = tag
        else:
            print(style('<{}>'.format(tag), fg=self.color, bold=self.is_bold, underline=self.is_underline), end="")


    def handle_endtag(self, tag):
        # make in case independent
        tag = tag.lower()

        # do we know this tag?
        if tag == 'b':
            self.is_bold = False
        elif tag == 'u':
            self.is_underline = False
        elif tag in known_colors:
            self.color = "reset"
        else:
            print(style('<{}>'.format(tag), fg=self.color, bold=self.is_bold, underline=self.is_underline), end="")

    def handle_data(self, data):
        print(style(data, fg=self.color, bold=self.is_bold, underline=self.is_underline), end="")


def markup_print(text, *args, **kwargs):
    """markdown print
    <red> </red>
    <green> <green>
    <blue><blue>
    """
    if args or kwargs:
        text = text.format(*args, **kwargs)
    parser = ColorMarkupClickPrinter()
    parser.feed(text)
    print("")     # new line in the end


if __name__ == "__main__":
    markup_print("One two <b> df <red> my red red red </red> </b>")