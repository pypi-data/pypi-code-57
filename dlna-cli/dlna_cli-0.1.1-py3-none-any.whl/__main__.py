from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar, Optional

import click
import termcolor

from dlna_cli.api import DLNAApi, MediaDevice, MediaContainer, MediaItem
from dlna_cli.api_factory import (
    ScanDevicesDiscoverer,
    CacheKeepDeviceIDXDiscoverer,
    DEFAULT_SCAN_TIMEOUT,
    DEFAULT_CACHE_FILE,
    create_api_from_discoverer,
)

T = TypeVar('T')


@dataclass
class App:
    api: DLNAApi


@click.group()
@click.option('--scan-timeout', type=float, default=DEFAULT_SCAN_TIMEOUT / 2)
@click.option('--disable-cache', type=bool, default=False)
@click.option('--cache-file', type=Path, default=DEFAULT_CACHE_FILE)
@click.pass_context
def cli(ctx: click.Context, scan_timeout: int, disable_cache: bool, cache_file: Path):
    discoverer = ScanDevicesDiscoverer(scan_timeout)
    if not disable_cache:
        discoverer = CacheKeepDeviceIDXDiscoverer(discoverer, cache_file)

    api = create_api_from_discoverer(discoverer)

    app = App(api)
    ctx.obj = app


@click.pass_context
@cli.resultcallback
def shutdown(ctx):
    pass


@cli.command()
@click.option(
    '--format', type=str, default='{pos} {c.name}\t{c.description}\t{c.location}'
)
@click.pass_obj
def list_servers(app: App, format: str):
    click.echo('Available servers list:')

    header_entity = MediaDevice(
        udn='UDN',
        name='Name',
        description='Description',
        location='Location',
        icon_url='Icon URL',
        presentation_url='Presentation URL',
    )
    click.echo(f'\t{format.format(c=header_entity, pos=" ")}')

    for idx, container in enumerate(app.api.list_servers()):
        click.echo('\t' + format.format(c=container, pos=idx))


@cli.command()
@click.argument('server-idx', type=int)
@click.argument('parent', type=str, required=False, default=None)
@click.pass_obj
def list_items(app: App, server_idx: int, parent: str = None):
    click.echo('Server content:')

    for idx, child in enumerate(
        app.api.list_server_items(served_identificator=server_idx, parent=parent)
    ):
        name_color: Optional[str] = None
        append_text: str = ''
        if isinstance(child, MediaItem):
            name_color = 'magenta'
            for sink_idx, sink in enumerate(child.sinks):
                append_text += f'\n\t\tsink #{sink_idx}:\n'
                append_text += f'\t\t\turl={sink.url}\n'
                append_text += '\n'.join(
                    f'\t\t\t{key}={value!r}' for key, value in sink.meta.items()
                )
        elif isinstance(child, MediaContainer):
            append_text = f'\t{child.child_count}'
            name_color = 'blue'

        name_colored: str
        if name_color is not None:
            name_colored = termcolor.colored(child.name, name_color)
        else:
            name_colored = child.name

        click.echo(f'{idx}\t{name_colored}{append_text}', nl=False)
        click.echo()


cli()
