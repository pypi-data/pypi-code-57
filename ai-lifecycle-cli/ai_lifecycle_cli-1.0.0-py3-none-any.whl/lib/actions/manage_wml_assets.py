#  © Copyright IBM Corporation 2020.

import time
import datetime
import string
import textwrap

from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler
from ai_lifecycle_cli.lib.utils import print_utils
from ai_lifecycle_cli.lib.actions import preparation


logger = LoggingHandler()


def list_assets(client, space_id, asset_types, ids, names):

    print("Retrieving assets...\n")
    types = asset_types if asset_types is None else asset_types.split(',')
    assets = preparation.get_all_assets(client, types, "space", space_id, full_metadata=True)

    if types is None:
        available_types = sorted(list(set(map(lambda x: x['asset_type'], assets))))
    else:
        available_types = sorted(types)

    resources = {}
    for available_type in available_types:
        if len(list(filter(lambda x: x['asset_type'] == available_type, assets))) > 0:
            resources[available_type] = list()

            for asset in assets:
                type_filter = asset['asset_type'] == available_type
                no_filter = ids is None and names is None
                id_filter = ids is not None and asset['asset_id'] in ids.split(',')
                name_filter = names is not None and asset['name'] in names.split(',')

                if type_filter and (no_filter or id_filter or name_filter):
                    resources[available_type].append(
                        dict(
                            id=asset['asset_id'],
                            name=asset['name']
                        ))
    print_utils.print_resource_lists(available_types, ["ID", "Name"], resources)
    return resources
