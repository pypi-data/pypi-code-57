import shutil


def truncatestring(string: str, width=30, placeholder="...") -> str:
    # https://stackoverflow.com/questions/2872512/python-truncate-a-long-string/39017530
    width -= len(placeholder)
    assert width > 0
    return (string[:width] + placeholder) if len(string) > width else string


def get_tty_width(default=80) -> int:
    return shutil.get_terminal_size((default, 20)).columns
