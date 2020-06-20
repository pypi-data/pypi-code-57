#!/usr/bin/env python3

import argparse
import sys
from pprint import pprint
from sheetgear.bridge.gauth import authorize

def main(argv=sys.argv):
  parser = argparse.ArgumentParser(prog='python3 -m sheetgear')
  subparsers = parser.add_subparsers(help='Sub-commands', dest='sub_command')

  # create the parser for the "authen" command
  parser_authen = subparsers.add_parser('authen', help='Google sheets API authentication')
  parser_authen.add_argument("credentials_file", type=str,
      help="Path to a credentials file")

  parser_authen.add_argument("client_secrets_file", type=str,
      help="Path to a client_secrets file")

  args = parser.parse_args(args=argv[1:])

  if args.sub_command == 'authen':
    creds = authorize(credentials_file=args.credentials_file,
        client_secrets_file=args.client_secrets_file,
        use_prompt=True)

    pprint({
      'client_id': creds.client_id,
      'client_secret': '********',
      'id_token': creds.id_token,
      'refresh_token': '********',
      'token_uri': creds.token_uri,
      'valid': creds.valid,
      'expired': creds.expired,
      'scopes': creds.scopes,
    })

    return 0

  parser.print_help()
  return -1

if __name__ == "__main__":
  sys.exit(main(sys.argv))
