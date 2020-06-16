import base64
import hashlib
import json
import logging
import os
import re
import sys
import socket
import threading
import uuid
from urllib.parse import urlsplit, parse_qs, urlunparse, urljoin
import furl
import requests
from flask import Flask, Blueprint, redirect, request, session
from requests.exceptions import ConnectTimeout

from dli.client.components.urls import sam_urls, identity_urls


def can_launch(port):
    current_port = port
    # if the user opens ipython in multiple windows, the first will
    # be using the 8080 socket, and then the second will not launch a
    # new server. Because we get the value using a wait/notify against
    # Listener.values global, we must use an open port, else the wrong
    # server instance's Listener.values global will be set.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # already_open = (result == 0)
        # reason = socket.errno.errorcode.get(result, "SUCCESS")
        try:
            s.bind(("localhost", current_port))
            result = True, "Bound"
        except Exception as e:
            result = False, str(e)
        finally:
            s.close()

        return result


class _Listener:

    DEFAULT_PORT = 8080
    LOCALHOST = "http://localhost"
    VALUES = {}
    _routes = None
    # _lock = threading.RLock()
    # condition = threading.Condition(_lock)

    #disable the flask startup messaging
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)


    @staticmethod
    def setup_verifiers(code):
        code_verifier = base64.urlsafe_b64encode(code).decode(
            'utf-8')
        code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode(
            'utf-8')
        code_challenge = code_challenge.replace('=', '')
        return code_challenge, code_verifier

    @staticmethod
    def register_routes(app, port):
        localhost = f"{_Listener.LOCALHOST}:{port}"
        _Listener._routes = Blueprint("auth", __name__, )

        @_Listener._routes.route('/login', methods=['GET'])
        def login():
            postbox = request.args.get("postbox")
            if not postbox:
                return """
                  <img style="max-width: 300px; height: auto; "
                    src="https://cdn.ihsmarkit.com/www2/a/p/media/images/ihsmarkit.svg" 
                    alt="IHS Logo"
                  >
                  </hr>
                  <h2 style="font-family: Arial, Helvetica, sans-serif;">
                  Forbidden. 
                  </h2>
                """, 403

            try:
                # setup the session
                rnd = os.urandom(40)
                session["catalogue"] = request.args.get("catalogue")
                session["sam_client"] = request.args.get("sam_client")
                session["sam"] = request.args.get("sam")
                session["code_challenge"], session["code_verifier"] = \
                    _Listener.setup_verifiers(rnd)
                session["postbox"] = str(postbox)

                response = requests.head(
                    urljoin(session["catalogue"], "login"),
                    timeout=10
                )
                bits = urlsplit(response.headers["Location"])
                params = parse_qs(bits.query)
                params["redirect_uri"] = [localhost]
                path = urlunparse((
                    bits.scheme, bits.netloc, bits.path, '', '', ''
                ))

                target_builder = furl.furl(path)

                target_builder.args = {
                    "state": postbox,
                    "client_id": session["sam_client"],
                    "response_type": "code",
                    "redirect_uri": localhost,
                    "scope": "openid profile saml_attributes email",
                    "code_challenge": session["code_challenge"],
                    "code_challenge_method": "S256"
                }
                redi = redirect(target_builder.url)
                return redi
            except ConnectTimeout:
                return "Could not connect - check internet connection", 400
            except Exception as e:
                return str(e), 500

        @_Listener._routes.route('/', methods=['GET', 'POST'])
        def auth_callback():

            postbox = session["postbox"]
            logging.info(f"Current postbox {postbox}")
            state = request.args.get('state', '')
            if state != postbox:
                # we have to set this, else the shell will just hang waiting
                # for a value - so they must check it and quit etc.
                _Listener.VALUES[postbox] = "invalid"
                return """
                  <img style="max-width: 300px; height: auto; "
                    src="https://cdn.ihsmarkit.com/www2/a/p/media/images/ihsmarkit.svg"
                    alt="IHS Logo"
                  >
                  </hr>
                  <h2 style="font-family: Arial, Helvetica, sans-serif;">
                  You have another SDK session open.
                  </h2>
                """, 403

            code = request.args.get('code')
            client_id = request.args.get('client_id')

            # exchange this code for a token
            tokens = requests.post(
                urljoin(session["sam"], sam_urls.sam_token),
                data={
                    "grant_type": "authorization_code",
                    "client_id": client_id,
                    "redirect_uri": localhost,
                    "code": code,
                    "code_verifier": session["code_verifier"]
                },
                allow_redirects=False
            )

            if tokens.status_code != 200:
                return tokens.text, tokens.status_code


            token = tokens.json()["id_token"]
            # ok now we wanna exchange this token with catalogue
            catalogue_response = requests.post(
                urljoin(session["catalogue"],
                        identity_urls.identity_token),
                data={
                    "client_id": client_id,
                    "subject_token": token,
                    "origin": "SDK"

                },
                allow_redirects=False
            )


            if catalogue_response.status_code != 200:
                return catalogue_response.text, catalogue_response.status_code

            jwt = catalogue_response.json()["access_token"]
            # with _Listener.condition:
            # logging.info(f"We are setting the postbox {postbox}")
            _Listener.VALUES[postbox] = jwt
            # _Listener.condition.notify_all()

            logging.info("Acquired Catalogue JWT")
            return """
              <img style="max-width: 300px; height: auto; "
                src="https://cdn.ihsmarkit.com/www2/a/p/media/images/ihsmarkit.svg" 
                alt="IHS Logo"
              >
              </hr>
              <h2 style="font-family: Arial, Helvetica, sans-serif;">
              You're now logged in. Please close this window.
              </h2>
            """

        @_Listener._routes.route('/shutdown', methods=['GET', 'POST'])
        def shutdown():
            try:
                pass
            finally:
                return 'Server shutting down...'

        @_Listener._routes.route('/get/<query_postbox>')
        def get(query_postbox):
            if _Listener.VALUES.get(query_postbox, False):
                return json.dumps({
                    "jwt": _Listener.VALUES.get(query_postbox, "")
                }), 200

            return json.dumps({"jwt": "None"}), 404


        app.register_blueprint(_Listener._routes)

    @staticmethod
    def run(port=DEFAULT_PORT, debug=False):
        postbox = base64.urlsafe_b64encode(uuid.uuid4().bytes)\
            .decode('utf-8').replace('=', '')

        app = Flask(__name__)
        app.logger.disabled = True
        app.secret_key = os.urandom(20)
        if debug:
            _Listener.app = app

        _Listener.register_routes(app, port)

        # check whether we need to launch the listener server
        if not debug:
            result, reason = can_launch(_Listener.DEFAULT_PORT)
            if result:
                try:
                    t = threading.Thread(
                        target=lambda: app.run(port=port)
                    )
                    t.daemon = True
                    t.start()
                except OSError:
                    print("Already running")

        return str(postbox)
