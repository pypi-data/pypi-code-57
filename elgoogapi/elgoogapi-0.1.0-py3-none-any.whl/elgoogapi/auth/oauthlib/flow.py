#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, re-authenticate by deleting the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authorize(credentials_file, client_secrets_file, credentials_info=None, client_secrets_info=None, use_prompt=False, scopes=SCOPES):
  if isinstance(credentials_info, dict):
    _creds = Credentials(**credentials_info)
    if _creds and _creds.valid and not _creds.expired:
      return _creds
  creds = None
  # The file [credentials_file] stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first time.
  if os.path.exists(credentials_file):
    with open(credentials_file, 'rb') as creds_file:
      creds = pickle.load(creds_file)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      if client_secrets_info is not None:
        flow = InstalledAppFlow.from_client_config(client_secrets_info, scopes)
      else:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
      if use_prompt:
        creds = flow.run_console()
      else:
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(credentials_file, 'wb') as creds_file:
      pickle.dump(creds, creds_file)
  return creds
