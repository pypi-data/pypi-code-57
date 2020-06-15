import time
import webbrowser

import requests
from yaspin import yaspin

from devyzer.auth import get_auth_token, auth

from devyzer.commands.__init__ import Command
from devyzer.constants import LINK_GITHUB_UI_ENDPOINT, AUTHORIZED_EXPIRY, AUTH_GITHUB_ENDPOINT
from devyzer.state import SessionState
from devyzer.utils import print_with_color, bcolors


class GitAccountCommand(Command):
    def name(self):
        return "ask_github_access"

    def run(self, args, sio, project_configuration):
        # open github page
        webbrowser.open(LINK_GITHUB_UI_ENDPOINT)
        import sys

        sys.stdout.isatty = lambda: False
        sys.stdout.encoding = sys.getdefaultencoding()
        t_end = time.time() + 60 * AUTHORIZED_EXPIRY
        with yaspin(text="checking your github access ...", color="green") as spinner:
            while time.time() < t_end:
                time.sleep(2)
                get_token_response = requests.get(AUTH_GITHUB_ENDPOINT(get_auth_token()),
                                                   headers={'Content-Type': 'application/json'})
                if 300 > get_token_response.status_code >= 200:
                    result = get_token_response.json()
                    if "authenticated" in result and result["authenticated"] is True:
                        spinner.ok("✔")
                        sio.emit('user_uttered',
                                 {"message": '/git_hub_access_done',
                                  "session_id": SessionState.session_id, "metadata": None})
                        return None
            spinner.fail("✘")
            print_with_color("Failed to get your github access, Timeout ", bcolors.WARNING)
            return None




class AuthCommand(Command):
    def name(self):
        return "authentication"

    def run(self, args, sio, project_configuration):
        return auth.auth(force=True)