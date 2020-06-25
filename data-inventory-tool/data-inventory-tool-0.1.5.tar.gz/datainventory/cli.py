import click
import sqlalchemy as sa

from datainventory.core import Dataset
from datainventory.core import Manifest
from datainventory.core import Resource
from datainventory.formats import ascii
from datainventory.sources import sql


@click.group()
def main():
    pass


@main.command()
@click.argument('name')
@click.argument('dsn')
def inspect(name, dsn):
    if name != 'sql':
        raise click.ClickException(f"Unknown data source type {name!r}.")
    try:
        engine = sa.create_engine(dsn)
    except ModuleNotFoundError as e:
        raise click.ClickException(
            f"Database driver not found: {e}.\n"
            "See: https://docs.sqlalchemy.org/en/13/dialects/index.html"
        )
    manifest = Manifest()
    dataset = Dataset('datasets/gov/data')
    resource = Resource('sqlite', dataset)
    sql.inspect(manifest, resource, engine)
    print(ascii.render(manifest))
