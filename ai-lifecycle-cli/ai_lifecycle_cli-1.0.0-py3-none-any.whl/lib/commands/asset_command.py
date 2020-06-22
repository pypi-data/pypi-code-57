#  © Copyright IBM Corporation 2020.

from ai_lifecycle_cli.lib.clients.rest_client import RESTClient
from ai_lifecycle_cli.lib.actions import manage_wml_assets


def do_asset(args):

    client = RESTClient(args.cpd_url, (args.cpd_user, args.cpd_pass))

    # 'asset list' command
    if args.asset == "list":

        space_id = args.space_id
        asset_types = args.asset_type
        asset_ids = args.asset_id
        asset_names = args.asset_name

        manage_wml_assets.list_assets(client=client, space_id=space_id, asset_types=asset_types, ids=asset_ids, names=asset_names)
