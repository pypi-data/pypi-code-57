import io
import os

from rich.style import Style
from rich.table import Table
from rich import box
from datetime import datetime

from rich.theme import Theme

from .inspect_result import InspectResult
from .. import _utils


def rich_text(ir: InspectResult, args):
    from rich.console import Console

    theme = Theme({
        "pr.normal": "",
        "pr.warning": "yellow",
        "pr.danger": "bold red"
    })
    console = Console(file=io.StringIO(), force_terminal=True, theme=theme)

    from rich.panel import Panel
    console.print(Panel("[yellow]{} {}({})".format(ir.label, ir.version, ir.version_code)),
                  justify="center")
    console.line()

    # foundations
    foundation_table = Table.grid(padding=1, pad_edge=True)
    foundation_table.add_column("c0", style="repr.tag_name")
    foundation_table.add_column("c1", style="repr.tag_contents")

    stat = os.stat(ir.path)
    dt = datetime.utcfromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    foundation_table.add_row("hash", ir.file_hash.upper())
    foundation_table.add_row("package", ir.package)
    foundation_table.add_row("size", _utils.sizeof_fmt(stat.st_size))
    foundation_table.add_row("create_date", str(dt))
    foundation_table.add_row("target_sdk_version", ir.compile_config['targetSdkVersion'])
    foundation_table.add_row("sdk_version", ir.compile_config['sdkVersion'])
    foundation_table.add_row("compile_sdk_version", ir.compile_config['compileSdkVersion'])

    console.print(foundation_table)
    console.line()

    permission_table = Table(show_header=False, show_lines=True, box=box.SIMPLE)
    permission_table.add_column("name", justify="left", overflow="fold")
    permission_table.add_column("description", overflow="fold")

    level_style = {
        '0': "pr.normal",
        '1': "pr.warning",
        '2': "pr.danger"
    }

    count = [0, 0, 0, 0]

    for p in ir.permissions:
        count[0] += 1

        if p.level == '0':
            count[1] += 1
        elif p.level == '1':
            count[2] += 1
        elif p.level == '2':
            count[3] += 1

        style = level_style.get(p.level, 'pr.normal')
        permission_table.add_row("[{}]{}".format(style, p.name), "[{}]{}".format(style, p.description))

    permission_table.title = "(total)/(normal)/(warning)/(danger): {}/{}/{}/{}".format(*count)

    console.print(permission_table)

    console.line()

    if args.manifest:
        from .manifest_parser import ManifestWrapper
        mw = ManifestWrapper(ir.manifest)
        app = mw.application

        activities = app.activities

        for a in activities:
            if a.is_launch_activity:
                console.print("(ACTIVITY) '{}' #Launch".format(a.name))
            else:
                console.print("(ACTIVITY) '{}'".format(a.name))

        console.line()

        services = app.services

        for s in services:
            console.print("(SERVICE) '{}'".format(s.name))

        receivers = app.receivers

        console.line()
        for r in receivers:
            console.print("(RECEIVER) '{}'".format(r.name))

        providers = app.providers

        console.line()
        for p in providers:
            console.print("Provider '{}'".format(p.name))

        metas = app.metas

        console.line()
        for m in metas:
            console.print("Meta '{}'={}".format(m.name, m.value))

    if args.properties:
        console.print(ir.properties)

    # console.rule("summary")
    print(console.file.getvalue())  # type: ignore
