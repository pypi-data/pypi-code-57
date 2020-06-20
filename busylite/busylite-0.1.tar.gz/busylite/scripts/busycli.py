#!/usr/bin/env python
#
#
import os
import click
import logging
import logging.config
import busylite
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

# Setup logger
logger = logging.getLogger(__name__)
_log_filename = os.path.expanduser('~/busylite.log')

def configure_logging(verbose, logfn):
    """
    Function to handle setting up logger
    """

    # TODO: just use the integer value and pass that to the config.
    if verbose == 0:
        log_lvl = 'ERROR'
    elif verbose == 1:
        log_lvl = 'WARNING'
    elif verbose == 2:
        log_lvl = 'INFO'
    elif verbose > 2:
        log_lvl = 'DEBUG'

    # Just keep it here for simplicity
    config = {
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}},
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': log_lvl,
                'stream': 'ext://sys.stdout'},
            'file_handler': {
                'backupCount': 20,
                'class': 'logging.handlers.RotatingFileHandler',
                'encoding': 'utf8',
                'filename': logfn,
                'formatter': 'simple',
                'level': 'DEBUG',
                'maxBytes': 10485760}},
        'loggers': {
            'blobcli': {
                'handlers': ['console', 'file_handler'],
                'level': log_lvl,
                'propagate': False}},
        'root': {
            'handlers': ['console', 'file_handler'],
            'level': log_lvl},
        'version': 1}

    logging.config.dictConfig(config)
    logging.captureWarnings(True)

@click.group()
@click.option('-l','--logfn', help='log file path', default=_log_filename,
              type=click.Path())
@click.option('-v', '--verbose', help="SHOW ME WHAT YOU GOT!", count=True)
def cli(logfn, verbose):
    configure_logging(verbose, logfn)

@cli.command()
@click.option('-b','--blink', type=float, default=1)
def test(blink):
    """
    CLI tool to write to busylite 
    """
    busylite.crazy_lights(wait_time=blink)

@cli.command()
@click.option('-w','--wait', type=float, default=1)
@click.option('-s','--steps', type=int, default=100)
def rainbow(wait, steps):
    """
    CLI tool to write to busylite 
    """
    busylite.smooth_rainbow(wait_time=wait, steps=steps)

@cli.command()
def clear():
    """
    CLI tool to write to busylite an "empty" buffer, removes all light/sound. 
    """
    busylite.clear_bl()

@cli.command()
@click.option('-r','--red', type=int, default=0)
@click.option('-g','--green', type=int, default=0)
@click.option('-b','--blue', type=int, default=0)
@click.option('--blink', type=int, default=0)
def show(red, green, blue, blink):
    """
    CLI tool to write sigle color to busylite.
    """

    bl = busylite.busylite(red=red, green=green, blue=blue, blink=blink)
    bl.write()

@cli.command()
@click.option('-t','--tone', default='openoffice')
@click.option('--vol',type=int, default=3)
def say(tone, vol):
    """
    CLI tool to write signal sounds to busylite. Tone options:

    \b
        * openoffice (default)
        * funky
        * fairytale
        * kuandotrain
        * telephonenordic
        * telephoneoriginal
        * telephonepickmeup
        * buzz
    """

    bl = busylite.busylite(tone=tone, vol=vol)
    bl.write()

@cli.command()
@click.argument('host', type=str)
@click.argument('port', type=int)
@click.option('-u', '--user',type=str, default='busylite')
@click.option('-p', '--password',type=str, default='busylite')
def serve(host, port, user, password):
    """
    Start server and listen for commands
    """

    #
    # Flask Related things
    #
    app = Flask(__name__)
    auth = HTTPBasicAuth()

    @auth.get_password
    def get_password(username):
        if username == user:
            return password
        return None

    @app.route('/send/<command>', methods=['POST'])
    @auth.login_required
    def index(command):

        if command == 'done':
            busylite.crazy_lights(wait_time=0.1)
        elif command == 'clear':
            busylite.clear_bl()
        else:
            abort(404)

        return jsonify({'command': command}), 201
    
    # Run the app
    app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    cli()