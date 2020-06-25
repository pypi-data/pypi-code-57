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
    assert name == 'sql'
    engine = sa.create_engine(dsn)
    manifest = Manifest()
    dataset = Dataset('datasets/gov/data')
    resource = Resource('sqlite', dataset)
    sql.inspect(manifest, resource, engine)
    print(ascii.render(manifest))
