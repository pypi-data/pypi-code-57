import functools
import os
import sys

import click
from loguru import logger
import serial

from lx16a.servo import Protocol, Servo

logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"))


@click.group()
@click.pass_context
def cli(ctx):
    click.echo(ctx.get_help())


def common_servo_params(func):
    @click.option("--id", type=int, help="Servo ID")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@click.group()
@click.pass_context
def servo(ctx):
    click.echo(ctx.get_help())


cli.add_command(servo)


@click.command(help="Get or set the current position.")
@common_servo_params
@click.argument("new_position", type=int, required=False, default=None)
def position(id, new_position):
    print(new_position)
    print("AAAAAAAAAAAAAAAA")
    ser = serial.Serial("/dev/cu.usbserial-1420", 115200, timeout=1, xonxoff=True)
    p = Protocol(serial=ser)
    servo = Servo(protocol=p, servo_id=id)
    if not new_position:
        print("GETTING POSITION")
        click.echo(servo.get_position())
    else:
        print("setting position")
        servo.set_position(new_position)


servo.add_command(position)


if __name__ == "__main__":
    cli()
