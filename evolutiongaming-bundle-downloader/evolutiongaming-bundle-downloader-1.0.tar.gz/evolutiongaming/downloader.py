#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = "Ozgur Vatansever"
__version__ = "1.0"

import argparse
import itertools
import json
import logging
import tempfile
import requests
import os
import sys

try:
    from urlparse import urlparse, parse_qsl
except:
    from urllib.parse import urlparse, parse_qsl

class Downloader(object):

    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, token):
            self.token = token

        def __call__(self, response):
            response.headers["Authorization"] = "Bearer %s" % self.token
            return response

    def __init__(self, username, password, client_id):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.redirect_uri = "https://bundle-repo.evo-games.com/auth"

    @property
    def authentication_token_payload(self):
        return {
            "username": self.username,
            "password": self.password,
            "relayState": self.redirect_uri
        }

    @property
    def masked_password(self):
        return self.password[:1] + ((len(self.password) - 2)*"*") + self.password[-2:-1]

    def authentication_token(self):
        logging.info(
            "Retrieving authentication token: {}/{}".format(self.username, self.masked_password)
        )
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        result = requests.post(
            "https://evolutiongaming.okta-emea.com/api/v1/authn",
            headers=headers,
            data=json.dumps(self.authentication_token_payload)
        )
        result.raise_for_status()
        authentication_token = result.json().get("sessionToken")
        logging.info(
            "Retrieved authentication token: {}".format(authentication_token)
        )
        return authentication_token

    def authorization_token(self, authentication_token):
        logging.info(
            "Retrieving authorization token: {}".format(authentication_token)
        )
        params = {
            "client_id": self.client_id,
            "nonce": "staticNonce",
            "redirect_uri": self.redirect_uri,
            "response_type": "id_token",
            "scope": "openid profile email",
            "sessionToken": authentication_token,
            "state": "ci-user-staticState"
        }
        result = requests.get(
            "https://evolutiongaming.okta-emea.com/oauth2/v1/authorize",
            params=params
        )
        locations = (h.headers["Location"] for h in result.history)
        fragments = (urlparse(loc).fragment for loc in locations)
        tokens = itertools.chain.from_iterable((parse_qsl(f) for f in fragments))
        authorization_token = dict(tokens).get("id_token")
        logging.info(
            "Retrieved authorization token: {}".format(authorization_token)
        )
        return authorization_token

    def download_files(self, authorization_token):
        host = "https://bundle-repo.evo-games.com/api/list_files"
        logging.info(
            "Retrieving list of available games: {}".format(host)
        )
        bearer = Downloader.BearerAuth(authorization_token)
        result = requests.get(host, auth=bearer)
        result.raise_for_status()

        files = result.json().get("files", [])
        downloads = [(name, file["DownloadLink"]) for name, file in files.items()]
        logging.info(
            "Retrieved:\n{}".format("\n".join(" * %s" % d[0] for d in downloads))
        )
        return downloads

    def download_file(self, name, url, authorization_token, directory, timeout):
        path = os.path.join(directory, name)
        logging.info(
            "Downloading {} into {}".format(url, path)
        )
        bearer = Downloader.BearerAuth(authorization_token)
        result = requests.get(url, auth=bearer, stream=True, timeout=timeout)

        with open(path, "wb") as f:
            for chunk in result.iter_content(chunk_size=10 * 1024 * 1024):
                if chunk:
                    f.write(chunk)
                    logging.debug("Written {} bytes into {}".format(len(chunk), path))

        logging.info("Download finished: {}".format(path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--client-id", type=str)
    parser.add_argument("-o", "--output-directory", type=str, default=tempfile.gettempdir())
    parser.add_argument("-p", "--password", type=str)
    parser.add_argument("-t", "--timeout", help="timeout when downloading games", type=int, default=30)
    parser.add_argument("-u", "--username", type=str)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    downloader = Downloader(username=args.username, password=args.password, client_id=args.client_id)
    token = downloader.authentication_token()
    secret = downloader.authorization_token(token)

    for name, url in downloader.download_files(secret):
        downloader.download_file(name, url, secret, args.output_directory, args.timeout)
