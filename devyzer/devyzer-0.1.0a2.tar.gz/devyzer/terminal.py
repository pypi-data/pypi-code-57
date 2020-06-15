# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import threading
import time
from typing import List
from os import _exit




import socketio
from halo import Halo
from yaspin import yaspin

import devyzer
from devyzer.auth import get_auth_token, auth
from devyzer.cli import Cli
from devyzer.command_executor import CommandExecutor
from devyzer.config import Config
from devyzer.constants import EXIT, BOT_SOCKET_IO_ENDPOINT, CONNECTING_TIMEOUT
from devyzer.state import SessionState
from devyzer.utils import print_devyzer
from devyzer.utils.cli import wrap_with_color, bcolors, print_with_color
from devyzer.utils.console import print_bot_output
from devyzer.utils.logger import TerminalLogger
from devyzer.utils.command import is_command


class DevyzerTerminal(object):
    """Encapsulates the Devyzer Terminal.
    """

    ev = threading.Event()
    is_authenticated = False

    def __init__(self, token, commands_package):
        """Inits DevyzerTerminal.

        Returns:
            None.
        """

        self.status_watcher = None
        self.token = token
        self.commands_package = commands_package
        self.logger = TerminalLogger(__name__,
                                     devyzer.config[Config.MAIN][Config.LOG_FILE],
                                     devyzer.config[Config.MAIN][Config.LOG_LEVEL]).logger

        self.cli = Cli(self.logger)
        self._sio = None
        self._connected = False
        self._connecting_event = threading.Event()
        self._input_paused = False
        self._command_executor = None
        self._active_project = None
        self.session_state = SessionState()

    def auto_select_project(self):
        if self.session_state.current_configurations and self.session_state.current_configurations['slug']:
            print(f'{wrap_with_color("Devyzer project config file exists in current folder. ", bcolors.UNDERLINE)}'
                  f'{wrap_with_color(f"will auto select your project", bcolors.UNDERLINE)}  ')
            msg = f"/select_project{{\"project_name\": \"{self.session_state.current_configurations['slug']}\"}}"
            self.send_message(msg, metadata=self.session_state.current_configurations)

    def run(self):
        self.init_sio()

        if not self._connected:
            return

        # run events after connected
        # todo: make this runs as events subscriptions or something similar
        self.auto_select_project()

        print(f'{wrap_with_color("Devyzer Bot loaded. Type a message and press enter ", bcolors.OKGREEN)}'
              f'{wrap_with_color(f"(type {{{EXIT}}} to exit): ", bcolors.WARNING)}  ')
        print("\n")
        while self._connected:
            while not self._input_paused:
                try:
                    text = self.cli.prompt()
                except KeyboardInterrupt:
                    self._sio.disconnect()
                    _exit(0)
                    break
                else:
                    if text.lower() == EXIT.lower():
                        self._sio.disconnect()
                        _exit(0)
                        break

                    if text:
                        if self.cli.handle_cd(text):
                            self.auto_select_project()
                        else:
                            if is_command(text):
                                self.pause_user_input()
                                os.system(text)
                                self.resume_user_input()
                            else:
                                self.send_message(text)

    def init_sio(self):
        self._sio = socketio.Client(reconnection=True, reconnection_attempts=10)
        self._sio.on('connect', self.handle_connect)
        self._sio.on('session_confirm', self.handle_session_confirm)
        self._sio.on('bot_uttered', self.handle_bot_uttered)
        self._sio.on('disconnect', self.handle_disconnect)

        # Connecting to the bot
        with yaspin(text="Connecting ...", color="green") as spinner:
            try:
                self._connected = False
                self._sio.connect(BOT_SOCKET_IO_ENDPOINT)
                self._connecting_event.wait(timeout=CONNECTING_TIMEOUT)
                if self._connected:
                    spinner.ok("✔")
                else:
                    spinner.fail("✘")
                    return False
            except:
                spinner.fail("✘")
                self._connecting_event.set()

        if not self._connected:
            return False

        # Signing and Authentication the session
        if self.authenticate(self.token):
            self._command_executor = CommandExecutor(self._sio, self.logger)
            self._command_executor.register_package(self.commands_package)
        else:
            self._sio.disconnect()
            return False

        return True

    def authenticate(self, token):
        with yaspin(text="Authenticating session ...", color="green") as spinner:
            self._sio.emit('session_request', {"id_token": token, 'session_id': SessionState.session_id})
            self.ev.wait(timeout=CONNECTING_TIMEOUT)
            if self.is_authenticated:
                spinner.ok("✔")
            else:
                spinner.fail("✘")
        return self.is_authenticated

    def handle_session_confirm(self, data, **kwargs):
        self.is_authenticated = True
        self.ev.set()  # unblock the call

    def handle_connect(self):
        self._connected = True
        self._connecting_event.set()

    def handle_disconnect(self):
        self._connected = False
        print_with_color('Disconnected!', bcolors.FAIL)

    def handle_bot_uttered(self, data, **kwargs):
        # todo: enhance this call here and the way that the session state variables gotten!
        print_bot_output(data)

        commands = data.get("commands")
        if commands:
            self.pause_user_input()
            for command in commands:
                self._command_executor.run(command)
            self.resume_user_input()

        if "status" in data:
            self.session_state.status = data.get("status", None)
            if self.session_state.status == "waiting_process":
                self.pause_user_input()
                if self.status_watcher is None or not self.status_watcher.isAlive():
                    self.start_status_watcher()

        if "activeProject" in data:
            self.session_state.active_project = data.get("activeProject", None)

    def status_watcher_handler(self):
        # sleep a bit to prevent printing other messages comes from bot after the spinner in same line
        time.sleep(1)
        spinner = Halo(text='Loading', text_color='cyan', color='cyan', spinner='dots')
        spinner.start()
        while True:
            if self.session_state.status != "waiting_process":
                spinner.stop()
                print('')
                self.resume_user_input()
                break
            time.sleep(1)

    def start_status_watcher(self):
        self.status_watcher = threading.Thread(target=self.status_watcher_handler)
        self.status_watcher.daemon = True
        self.status_watcher.start()

    def resume_user_input(self):
        self._input_paused = False

    def pause_user_input(self):
        self._input_paused = True

    def send_message(self, msg, metadata=None):
        self._sio.emit('user_uttered', {"message": msg, 'session_id': SessionState.session_id, 'metadata': metadata})


# noinspection PyProtectedMember
def subparser(
        subparsers: argparse._SubParsersAction, parents: List[argparse.ArgumentParser]
):
    run_parser = subparsers.add_parser(
        "run",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Starts the terminal.",
    )
    run_parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    """Creates and calls DevyzerTerminal.

    Args:
        * None.

    Returns:
        None.
    """
    try:

        import os

        os.system('cls')  # For Windows
        os.system('clear')  # For Linux/OS X

        print_devyzer()

        if auth() is False:
            return

        terminal = DevyzerTerminal(get_auth_token(), "devyzer.commands")
        terminal.run()

    except EOFError:
        terminal.config_obj.write()
