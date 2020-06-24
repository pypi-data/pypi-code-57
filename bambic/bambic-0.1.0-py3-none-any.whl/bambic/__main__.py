import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from math import pi, factorial

@click.version_option('0.1.0', prog_name="Calculator From CLI")
@with_plugins(iter_entry_points("click_command_tree"))
@click.group(
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="magenta",
)
def main():
    """Bambi Calculator From CLI"""
    pass

@click.group(
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="magenta"
)
def arithmetics():
    pass

def factorial1(n):
    if n < 0:
        return 0
    if n == 0:
        return 1

    f = 1
    for i in range(1, n + 1):
        f = f * i
    return f

def factorial2(n):
    if n < 0:
        return 0
    if n == 0:
        return 1

    return n * factorial2(n - 1)


# 팩토리얼 구하기
@arithmetics.command(cls=HelpColorsCommand, help_options_color="magenta")
@click.option('--method', '-m', type=int, default=1, help="Choose a number of factorial methods")
@click.argument('num', type=int)
def fact(method, num):
    """Calculate factorial value"""
    f = None
    if method == 1:
        f = factorial1(num)
    elif method == 2:
        f = factorial2(num)
    elif method == 3:
        f = factorial(num)
    else:
        click.secho("Wrong method number!", fg="red", bg="yellow")
        return
    click.secho(f"{f}", fg="blue", bg="white")


# 거듭제곱
@arithmetics.command(cls=HelpColorsCommand, help_options_color="magenta")
@click.argument('base', type=float)
@click.argument('exponent', type=float)
def pow(base, exponent):
    """Get the power of a number"""
    click.secho(f"{base**exponent}", fg="blue", bg="white")


# 도를 라디안으로 변환
@arithmetics.command(cls=HelpColorsCommand, help_options_color="magenta")
@click.argument('degree', type=float)
def dtr(degree):
    """Convert degree to radian"""
    click.secho(f"{degree*(pi/180)}", fg="blue", bg="white")
    


# 라디안을 도로 변환
@arithmetics.command(cls=HelpColorsCommand, help_options_color="magenta")
@click.argument('radian', type=float)
def rtd(radian):
    """Convert radian to degree"""
    click.secho(f"{radian*(180/pi)}", fg="blue", bg="white")


# 원통의 부피와 넓이
@arithmetics.command(cls=HelpColorsCommand, help_options_color="magenta")
@click.argument('height', type=float)
@click.argument('radian', type=float)
def vaoc(height, radian):
    """Calculate surface volume and area of a cylinder"""
    click.secho(f"Volume: {pi*radian*radian*height}", fg="blue", bg="white")
    click.secho(f"Area: {((2*pi*radian) * height) + ((pi*radian**2)*2)}", fg="blue", bg="white")


if __name__ == "__main__":
    main()