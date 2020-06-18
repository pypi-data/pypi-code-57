import os
import time
import turtle

from ybc_kit.session import Session, FunctionCall

from ybc_commons.oss.path import url_of
from ybc_exception import InternalError
from ybc_exception import ParameterTypeError
from ybc_exception import ParameterValueError

session = Session()


def _wrap(method_name, cache=True):

    def wrapped(*args, **kwargs):
        session.append(FunctionCall('python.turtle.' + method_name,
                                    args + tuple(kwargs.values()), {}))
        if not cache:
            response = session.start()
            session.clear()
            return response

    return wrapped


def _dummy_wrap(method_name):
    def wrapped(*args, **kwargs):
        pass

    return wrapped


def _colorstr(color):
    """Return color string corresponding to args.

    Argument may be a string or a tuple of three
    numbers corresponding to actual colormode,
    i.e. in the range 0<=n<=colormode.

    If the argument doesn't represent a color,
    an error is raised.
    """
    if not isinstance(color, (str, tuple)):
        raise ParameterTypeError('_colorstr', "'color'")

    if len(color) == 1:
        color = color[0]
    if isinstance(color, str):
        return color

    try:
        r, g, b = color
    except (TypeError, ValueError):
        raise ParameterTypeError('_colorstr', "'color'")

    if (r < 1) and (g < 1) and (b < 1):
        r, g, b = [round(255.0 * x) for x in (r, g, b)]

    if not ((0 <= r <= 255) and (0 <= g <= 255) and (0 <= b <= 255)):
        raise ParameterValueError('_colorstr', "'color'")

    return "#%02x%02x%02x" % (r, g, b)


def forward(distance):
    _wrap("forward")(distance=distance)


def back(distance):
    _wrap("back")(distance=distance)


def right(angle):
    _wrap("right")(angle=angle)


def left(angle):
    _wrap("left")(angle=angle)


def goto(x, y=None):
    _wrap("goto")(x=x, y=y)


def home():
    _wrap("home")()


def setx(x):
    _wrap("setx")(x=x)


def sety(y):
    _wrap("sety")(y=y)


def setheading(to_angle):
    _wrap("setheading")(to_angle=to_angle)


def circle(radius, extent=None, steps=None):
    _wrap("circle")(radius=radius, extent=extent, steps=steps)


def pensize(width=None):
    _wrap("pensize")(width=width)


def penup():
    _wrap("penup")()


def pendown():
    _wrap("pendown")()


def speed(speed=None):
    _wrap("speed")(speed=speed)


def color(*args):
    if args:
        _args_count = len(args)
        if _args_count == 1:
            _pencolor = _fillcolor = args[0]
        elif _args_count == 2:
            _pencolor, _fillcolor = args
        elif _args_count == 3:
            _pencolor = _fillcolor = args
        _pencolor = _colorstr(_pencolor)
        _fillcolor = _colorstr(_fillcolor)
        _wrap("color")(_pencolor, _fillcolor)
    else:
        _wrap("color", cache=False)()


def pencolor(*args):
    _color = _colorstr(args)
    _wrap("pencolor")(_color)


def fillcolor(*args):
    _color = _colorstr(args)
    _wrap("fillcolor")(_color)


def showturtle():
    _wrap("showturtle")()


def hideturtle():
    _wrap("hideturtle")()


def begin_fill():
    _wrap("begin_fill")()


def end_fill():
    _wrap("end_fill")()


def screensize(canvwidth=None, canvheight=None, bg=None):
    _wrap("screensize")(canvwidth=canvwidth, canvheight=canvheight, bg=bg)


def bgcolor(*args):
    _color = _colorstr(args)
    _wrap("bgcolor")(_color)


def reset():
    _wrap("reset")()


def done():
    _wrap("done", cache=False)()


def save(filename=None):
    try:
        if filename:
            file_path = './' + filename
        else:
            file_path = './' + 'snapshot-' + str(int(time.time())) + '.png'

        file_key = _wrap("save", cache=False)()
        if filename:
            os.replace(file_key, file_path)
            return filename
        else:
            return file_key
    except Exception as e:
        raise InternalError(e, 'turtle_wrapper')


def write(arg, move=False, align="left", font=("Arial", 8, "normal")):
    error_flag = 1
    error_msg = ""
    # 参数类型错误检测
    if not isinstance(move, bool):
        error_flag = -1
        error_msg = "'move'"
    if not isinstance(align, str):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'left'"
    if not isinstance(font, tuple):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'font'"
    if error_flag == -1:
        raise ParameterTypeError('write', error_msg)

    font_name, font_size, font_type = font
    if font_type not in ["normal", "bold", "italic"]:
        font_type = "normal"

    css_font = "%s %dpx \"%s\"" % (font_type, font_size, font_name)
    _wrap("write")(arg=arg, move=move, align=align, font=css_font)


def dot(size=None, *color):
    """
    Draw a dot with diameter size, using color.

    Optional arguments:
    size -- an integer >= 1 (if given)
    color -- a color string or a numeric color tuple

    Draw a circular dot with diameter size, using color.
    If size is not given, the maximum of pensize+4 and 2*pensize is used.
    """
    # _size = size
    _color = color
    if not color:
        if isinstance(size, (str, tuple)):
            _color = _colorstr(size)
            # _size = None
        else:
            _color = None
    elif len(color) > 0:
        _color = _colorstr(color)
    else:
        _color = None
    _wrap("dot")(size, _color)


def sleep(seconds=0):
    done()
    time.sleep(seconds)


def reset_coordinate():
    _wrap("reset_coordinate")()


def is_wrapper():
    return True


def bgpic(filename: str):
    if filename == 'nopic' or filename is None:
        filename = ''
    else:
        filename = url_of(filename)
    _wrap('bgpic')(filename)


_all_turtle_methods = []
# Get all public methods in turtle module
for method_name in dir(turtle):
    if callable(getattr(turtle, method_name)) and not method_name.startswith('_'):
        _all_turtle_methods.append(method_name)

# Wrap all public methods in turtle module into dummy method to ignore them
for method_name in _all_turtle_methods:
    setattr(turtle, method_name, _dummy_wrap(method_name))

setattr(turtle, "forward", forward)
setattr(turtle, "back", back)
setattr(turtle, "right", right)
setattr(turtle, "left", left)
setattr(turtle, "goto", goto)
setattr(turtle, "home", home)
setattr(turtle, "setx", setx)
setattr(turtle, "sety", sety)
setattr(turtle, "setheading", setheading)
setattr(turtle, "circle", circle)
setattr(turtle, "fd", forward)
setattr(turtle, "bk", back)
setattr(turtle, "backward", back)
setattr(turtle, "rt", right)
setattr(turtle, "lt", left)
setattr(turtle, "setpos", goto)
setattr(turtle, "setposition", goto)
setattr(turtle, "seth", setheading)
setattr(turtle, "pensize", pensize)
setattr(turtle, "penup", penup)
setattr(turtle, "pendown", pendown)
setattr(turtle, "speed", speed)
setattr(turtle, "color", color)
setattr(turtle, "pencolor", pencolor)
setattr(turtle, "fillcolor", fillcolor)
setattr(turtle, "showturtle", showturtle)
setattr(turtle, "hideturtle", hideturtle)
setattr(turtle, "width", pensize)
setattr(turtle, "up", penup)
setattr(turtle, "pu", penup)
setattr(turtle, "pd", pendown)
setattr(turtle, "down", pendown)
setattr(turtle, "st", showturtle)
setattr(turtle, "ht", hideturtle)
setattr(turtle, "begin_fill", begin_fill)
setattr(turtle, "end_fill", end_fill)
setattr(turtle, "screensize", screensize)
setattr(turtle, "bgcolor", bgcolor)
setattr(turtle, "reset", reset)
setattr(turtle, "done", done)
setattr(turtle, "write", write)
setattr(turtle, "dot", dot)
setattr(turtle, "sleep", sleep)
setattr(turtle, "reset_coordinate", reset_coordinate)
setattr(turtle, "is_wrapper", is_wrapper)
setattr(turtle, "bgpic", bgpic)
