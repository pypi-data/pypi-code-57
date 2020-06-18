from textwrap import dedent
from io import StringIO
import os
import re

import click

from .parser import Converter


def get_output_stream(value, filename=None):
    """
    Возвращает поток в режиме перезаписи для указанного файла, либо None в случае ошибки.

    Если value пустое значение, то возвращает стандратный поток вывода (STDOUT).

    Если value директория, то использует аргумент filename для получения полного имени файла,
    в противном случае возвращает None.
    """
    if value is None:
        return click.get_text_stream('stdout')

    if os.path.isdir(value):
        if not filename:
            return None

        value = os.path.join(value, os.path.basename(filename))

    return click.open_file(value, 'w', lazy=True)


def pipe(required=True, mode='r'):
    """
    Allows you to use either a file stream or a standard stream as the value of the command argument.

    Arguments:
        required (bool): required argument (for write is not affected).
        mode (str): file open mode.

    Returns:
        (tuple): tuple containing:

            stream (io.IOBase): opened io stream.
            filename (str): filename, or None if using a standard stream.
    """
    def validate(ctx, param, value):
        if value is not None:
            return click.open_file(value, mode=mode, lazy=True), value

        get_stream = click.get_binary_stream if 'b' in mode else click.get_text_stream

        if 'r' not in mode:
            return get_stream('stdout'), None

        stream = get_stream('stdin')

        if not stream.isatty():
            return stream, None

        if required:
            raise click.MissingParameter(ctx=ctx, param=param)

        return None, None
    return validate


pass_converter = click.make_pass_decorator(Converter)


@click.group()
@click.version_option()
@click.option(
    '-g', '--output-syntax',
    required=True,
    type=click.Choice(Converter.get_supported_syntax()),
    help='The code generator for the target template engine.'
)
@click.option(
    '--config-file',
    envvar='JINJA_TO_ANOTHER_CONFIG',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help='The path to the configuration file. It can be set as a JINJA_TO_ANOTHER_CONFIG environment variable.'
)
@click.pass_context
def cli(ctx, config_file, output_syntax):
    """Entry point"""
    ctx.obj = Converter(output_syntax=output_syntax)

    if config_file is not None:
        ctx.obj.config.load(config_file)


@cli.command()
@click.option(
    '-o', '--output',
    type=click.Path(resolve_path=True, writable=True),
    help='The name of the file or directory into which the converted template will be saved.'
)
@click.argument(
    'template',
    type=click.Path(dir_okay=False, resolve_path=True),
    callback=pipe(),
    required=False
)
@pass_converter
def convert(converter, template, output):
    """Преобразует исходный Jinja шаблон в целевой шаблонизатор.

    Примеры вызова команды:

      adminlte convert -g django -o out/base.html base.html

      adminlte convert -g django -o out base.html

      adminlte convert -g django base.html


      JINIA_TO_ANOTHER_CONFIG=config.py adminlte convert -g django -o out base.html

      cat base.html | adminlte convert -g django -o out.html

      cat base.html | adminlte convert -g django
    """
    source_stream, filename = template
    output_stream = get_output_stream(output, filename)

    if output_stream is None:
        raise click.BadParameter('You must specify a file name to save the result.')

    converter.convert(source_stream, output_stream)

    if filename is not None:
        click.secho(f'Template "{filename}" saved to "{output_stream.name}"', err=True, fg='green')


@cli.command()
@click.argument(
    'src',
    type=click.Path(dir_okay=False, resolve_path=True),
    callback=pipe(),
    required=False
)
@click.option(
    '-o', '--output',
    type=click.Path(resolve_path=True, file_okay=False, writable=True),
    required=True,
    help='The name of the file or directory into which the converted template will be saved.'
)
@click.option('--only', type=lambda v: set(v.split(',')))
@click.option('--exclude', type=lambda v: set(v.split(',')))
@pass_converter
def macro2tags(converter, src, output, only, exclude):
    """Converts Jinja template engine macros to Django template tags."""
    source_stream, _ = src
    pattern = r'{%-?\s+macro\s+(?P<name>.+?)\((.+?)\)\s+-?%}(?P<body>.+?){%-?\s+endmacro\s+-?%}'

    for i in re.finditer(pattern, source_stream.read(), re.S):
        name = i.group('name')

        if exclude is None or name not in exclude:
            if only is None or name in only:
                body_stream = StringIO(dedent(i.group('body')).strip())
                output_stream = click.open_file(os.path.join(output, f'{name}.html'), 'w')
                converter.convert(body_stream, output_stream)
