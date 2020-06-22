#  © Copyright IBM Corporation 2020.

import time
import datetime
import string
import textwrap

from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler
from ai_lifecycle_cli.lib.utils import print_utils
from ai_lifecycle_cli.lib.actions import preparation


logger = LoggingHandler()


def create_deployment(client, space_id, asset_id, asset_name=None, deploy_name="default", deploy_type="online", hardware_spec_name=None, hardware_spec_num_nodes=0, params={}):

    print("Creating deployment...\n")

    post_deployment_url = "/v4/deployments"

    deploy_types = {
        "online": dict(online={}),
        "batch": dict(batch={})
    }

    # Retrieve asset ID by name
    if asset_name is not None:
        query = "asset.asset_name:{}".format(asset_name)
        search_res = preparation.search_asset(client, query, "space", space_id)
        if len(search_res) == 0:
            print("Asset with name {} is not available for deployment".format(asset_name))
            return
        if len(search_res) > 1:
            print("There are multiple assets with given name.")
            for res in search_res:
                print("{} -> {}".format(res['asset_name'], res['asset_id']))
            return
        asset_id = search_res[0]['asset_id']

    # Create deployment

    deployment_props = dict()
    deployment_props.update(name=deploy_name)
    deployment_props.update(space_id=space_id)
    deployment_props.update(asset=dict(id=asset_id))
    deployment_props.update(deploy_types.get(deploy_type, dict(online={})))
    if hardware_spec_name is not None:
        deployment_props.update(hardware_spec=
                                dict(
                                    name=hardware_spec_name,
                                    num_nodes=hardware_spec_num_nodes
                                ))
    deployment_props.update(params)

    post_deploy_res = client.make_request('post', path=post_deployment_url, body=deployment_props)
    if not post_deploy_res.ok:
        raise Exception("Couldn't create new deployment - reason: {}".format(post_deploy_res.text))

    deploy_guid = post_deploy_res.json()['metadata']['guid']
    print("Deployment created with ID: {}".format(deploy_guid))
    if deploy_type == "online":
        scoring_url = client.host + "/v4/deployments/" + deploy_guid + "/predictions"
        print("Predictions URL: {}".format(scoring_url))


def delete_deployment(client, space_id, deployment_id, deployment_name=None):

    print("Deleting deployment...\n")

    # Get deployment ID by its name
    if deployment_name is not None:
        get_deployments_url = "/v4/deployments?space_id={}".format(space_id)

        get_deploy_res = client.make_request('get', path=get_deployments_url)
        if not get_deploy_res.ok:
            raise Exception("Couldn't retrieve deployment ID by its name - reason: {}".format(get_deploy_res.text))

        available_deployments = list(filter(lambda x: deployment_name == x['metadata']['name'], get_deploy_res.json()['resources']))
        if len(available_deployments) == 0:
            print("Deployment with name {} is not available".format(deployment_name))
            return
        if len(available_deployments) > 1:
            print("There are multiple deployments with given name.")
            for res in available_deployments:
                print("{} -> {}".format(res['metadata']['name'], res['metadata']['id']))
            return
        deployment_id = available_deployments[0]['metadata']['id']

    # Check if deployment exists in space
    get_deployment_url = "/v4/deployments/{}".format(deployment_id)

    get_deploy_res = client.make_request('get', path=get_deployment_url)
    if not get_deploy_res.ok:
        raise Exception("Couldn't check if deployment exists in space - reason: {}".format(get_deploy_res.text))

    if 'metadata' not in get_deploy_res.json():
        print("Deployment does not exist.")
        return
    if get_deploy_res.json()['metadata']['space_id'] != space_id:
        print("Deployment does not exists in given space.")
        print("Given space ID: {}".format(space_id))
        print("Deployment's space ID: {}".format(get_deploy_res.json()['metadata']['space_id']))
        return

    # Delete deployment
    delete_deployment_url = "/v4/deployments/{}".format(deployment_id)

    delete_deploy_res = client.make_request('delete', path=delete_deployment_url)
    if not delete_deploy_res.ok:
        raise Exception("Couldn't delete deployment - reason: {}".format(delete_deploy_res.text))

    print("Deployment with ID {} has been deleted".format(deployment_id))


def list_deployments(client, space_id, deployment_type):

    print("Listing deployments...\n")

    deployment_types = ['batch', 'online'] if deployment_type is None else sorted(deployment_type.split(','))

    get_deployments_url = "/v4/deployments?space_id={}".format(space_id)

    get_deploy_res = client.make_request('get', path=get_deployments_url)
    if not get_deploy_res.ok:
        raise Exception("Couldn't retrieve deployments - reason: {}".format(get_deploy_res.text))

    resources = {}
    deployments = get_deploy_res.json()['resources']
    for deploy_type in deployment_types:
        resources[deploy_type] = []
        for deploy in deployments:
            if deploy_type in deploy['entity']:
                resources[deploy_type].append(
                    dict(
                        id=deploy['metadata']['id'],
                        name=deploy['metadata'].get('name', '<no name provided>')
                    ))

    print_utils.print_resource_lists(deployment_types, ["ID", "Name"], resources)
