import re

REGEX = "(-?[0-9]+(?:.[0-9]+)?) *([A-Za-z_]*)?"


def parse_input(input: str):
    m = re.match(REGEX, input)
    return m.groups() if m is not None else ()
