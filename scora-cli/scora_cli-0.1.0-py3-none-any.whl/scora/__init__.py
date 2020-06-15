# -*- coding: utf-8 -*-

"""Top-level package for CLI App"""

import click
from pkgver import package_version
from scora import commands


__author__ = """Oncase"""
__email__ = 'contato@oncase.com.br'
__version__ = package_version


@click.group()
def cli():
    pass


# Add commands
cli.add_command(commands.blocks)
