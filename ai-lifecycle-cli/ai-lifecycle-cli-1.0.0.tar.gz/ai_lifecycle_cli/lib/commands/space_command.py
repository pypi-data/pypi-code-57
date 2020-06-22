#  © Copyright IBM Corporation 2020.

from ai_lifecycle_cli.lib.clients.rest_client import RESTClient
from ai_lifecycle_cli.lib.actions import manage_wml_spaces


def do_space(args):

    client = RESTClient(args.cpd_url, (args.cpd_user, args.cpd_pass))

    # 'space list' command
    if args.space == "list":

        manage_wml_spaces.list_spaces(client)

    # 'space delete' command
    if args.space == "delete":

        space_id = args.space_id

        manage_wml_spaces.delete_space(client, space_id)
