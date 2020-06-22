#  © Copyright IBM Corporation 2020.

import time
import datetime
import string
import textwrap

from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler
from ai_lifecycle_cli.lib.utils import print_utils
from ai_lifecycle_cli.lib.actions import preparation


logger = LoggingHandler()


def list_spaces(client):

    print("Listing spaces...\n")

    get_spaces_url = "/v4/spaces"

    get_spaces_res = client.make_request('get', path=get_spaces_url)
    if not get_spaces_res.ok:
        raise Exception("Couldn't retrieve spaces - reason: {}".format(get_spaces_res.text))

    resources = {}
    resources['spaces'] = []
    for space in get_spaces_res.json()['resources']:
        resources['spaces'].append(
            dict(
                id=space['metadata']['id'],
                name=space['entity'].get('name', '<no name provided>')
            )
        )

    print_utils.print_resource_lists(["spaces"], ["ID", "Name"], resources)


def delete_space(client, space_id):

    print("Deleting space...\n")

    delete_space_url = "/v4/spaces/{}".format(space_id)

    delete_space_res = client.make_request('delete', path=delete_space_url)
    if not delete_space_res.ok:
        raise Exception("Couldn't delete space - reason: {}".format(delete_space_res.text))

    print("Space with ID {} has been deleted".format(space_id))
