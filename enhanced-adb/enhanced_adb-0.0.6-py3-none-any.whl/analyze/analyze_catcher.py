import io
import logging
import subprocess
import re

from rich.console import Console
from rich.table import Table

re_str = re.compile(r"\[\[MeeviiAnalyze\]\]:\sSendEvent:\s(\w+)\s\/\s(\w+)")
re_kv = re.compile(r"(\[\w+\:\s[\w\d\.\{\}\:]+\])")


def show_analyze(args):
    from .._utils import get_adb_exe

    logging.debug(args)

    search_re = None
    if args.search:
        search_re = re.compile(args.search)

    output = subprocess.Popen([get_adb_exe(), "logcat"], stdout=subprocess.PIPE)

    console = Console()

    for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
        s = re_str.search(line)
        if s:
            m = s.groups()
            platform = m[1]
            name = m[0]

            if search_re and not search_re.search(name):
                continue

            if args.no_adsdk is True and name.startswith("adsdk_"):
                continue

            console.rule(line[0:18], style="light_cyan3")
            console.print("[chartreuse3][u][b]{}[/u][/b]\t[gold1]{}".format(name, platform))

        kvitem = re_kv.findall(line)
        if kvitem:
            console.line()
            t = Table.grid(padding=0, pad_edge=True)
            t.add_column("c0", style='italic')
            t.add_column("c1", style="deep_sky_blue1")
            for item in kvitem:
                key, value = item[1:-1].split(": ")
                t.add_row(key + " ", value)

            console.print(t)
