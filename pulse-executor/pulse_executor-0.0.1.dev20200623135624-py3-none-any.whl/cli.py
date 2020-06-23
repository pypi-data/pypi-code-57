import argparse
import os

from pulse_executor import executor

ROBOT_ADDRESS = os.environ.get('ROBOT_ADDRESS')

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable")
    return parser.parse_args()


def main():
    args = parse_args()
    program_name = args.executable

    if ROBOT_ADDRESS is None:
        raise EnvironmentError("ROBOT_ADDRESS is not defined")
    else:
        executor.run(program_name, ROBOT_ADDRESS)


def stop():
    executor.die()


def status():
    print(executor.read_status())


def read_error():
    print(executor.read_error())


def smart_stop():
    executor.smart_stop()
