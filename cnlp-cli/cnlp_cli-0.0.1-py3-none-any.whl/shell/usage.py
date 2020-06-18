from time import ctime

from cnlp_cli.version import VERSION


def run():
    cur_time = ctime()

    text = f"""
    # cnlp-cli: CNLP Command Line Interface

    Version {VERSION} ({cur_time} +0800)
    """
    print(text)
