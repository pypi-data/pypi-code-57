__all__ = ['store_redirect', 'retrieve_redirect', 'verify']

import os
from flask import Flask, redirect, url_for, request, session
import requests
import json


def store_redirect():
    redirectURL = request.values.get('redirect')
    if redirectURL:
        session['FLASK_REDIRECT'] = redirectURL


def retrieve_redirect():
    redirectURL = session.get('FLASK_REDIRECT', url_for('index'))
    if 'FLASK_REDIRECT' in session:
        session.pop('FLASK_REDIRECT')
    return redirectURL


def verify(token):
    url = os.getenv('SPYC_LOGIN_URL') + "/verify"
    response = requests.get(url, params={'token': token}).text
    identity = json.loads(response)
    return identity
