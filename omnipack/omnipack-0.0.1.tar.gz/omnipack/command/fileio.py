import os.path as osp
import click
import omnipack


@click.command(help='Convert tsv2csv')
@click.argument('src')
@click.argument('dst')
def tsv2csv(src, dst):
    omnipack.tsv2csv(src, dst)


@click.command(help='Convert csv2tsv')
@click.argument('src')
@click.argument('dst')
def csv2tsv(src, dst):
    omnipack.csv2tsv(src, dst)
