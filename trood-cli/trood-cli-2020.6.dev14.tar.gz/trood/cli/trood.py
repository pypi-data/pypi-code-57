import click
import requests

from pyfiglet import Figlet
from trood.cli import utils

from .spaces import space


@click.group()
@click.option('-t', '--token')
@click.option('-f', '--force', is_flag=True, flag_value=True)
@click.pass_context
def trood(ctx, token: str, force: bool):
    ctx.ensure_object(dict)
    ctx.obj['TOKEN'] = token
    ctx.obj['FORCE'] = force
    pass

@trood.command()
def info():
    f = Figlet(font='slant')
    click.echo(f.renderText('TROOD'), nl=False)
    click.echo('Welcome to Trood sdk! Use `trood --help` to view all commands.')
    click.echo()


@trood.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(username: str, password: str):
    result = requests.post(
        'https://tcp.trood.com/auth/api/v1.0/login',
        json={'login': username.strip(), 'password': password.strip()}
    )

    if result.status_code == 200:
        data = result.json()
        utils.save_token(data["data"]["token"])

        click.echo(f'Successfully logged in as {username}')
    elif result.status_code == 403:

        click.echo(f'Login failed. Wrong login or password')
    else:

        click.echo(f'Cant login. Login server response: {result.json()}')


@trood.command()
def logout():
    click.confirm('Do you want to logout ?', abort=True)

    requests.post('https://tcp.trood.com/auth/api/v1.0/logout', headers={"Authorization": utils.get_token()})

    utils.clean_token()

@trood.command()
def token():
    click.echo(utils.get_token())

trood.add_command(space)
