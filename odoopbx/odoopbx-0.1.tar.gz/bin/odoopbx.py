import click


@click.group()
def main():
    pass


@click.group(help='Run Odoo PBX.')
def run():
    pass


main.add_command(run)


@run.command(help='Configure PBX services. Without parameters list PBX services.')
@click.option('--enable', help='Enable a service.')
def services(enable):
    click.echo('Enabled services:')
    click.echo('- Odoo')
    click.echo('- Asterisk')
    click.echo('- Agent')


if __name__ == '__main__':
    main()
