#  © Copyright IBM Corporation 2020.
import json
from ai_lifecycle_cli.lib.clients.rest_client import RESTClient
from ai_lifecycle_cli.lib.actions import manage_wml_deployments


def do_deployment(args):

    client = RESTClient(args.cpd_url, (args.cpd_user, args.cpd_pass))

    # 'deployment create' command
    if args.deployment == "create":

        space_id = args.space_id
        asset_id = args.asset_id
        asset_name = args.asset_name
        deployment_name = args.deployment_name
        deployment_type = args.deployment_type
        hardware_spec_name = args.hardware_spec_name
        hardware_spec_num_nodes = args.hardware_spec_num_nodes
        params = {} if args.params is None else json.loads(args.params)

        manage_wml_deployments.create_deployment(
            client=client,
            space_id=space_id,
            asset_id=asset_id,
            asset_name=asset_name,
            deploy_name=deployment_name,
            deploy_type=deployment_type,
            hardware_spec_name=hardware_spec_name,
            hardware_spec_num_nodes=hardware_spec_num_nodes,
            params=params
        )

    # 'deployment delete' command
    if args.deployment == "delete":

        space_id = args.space_id
        deployment_id = args.deployment_id

        manage_wml_deployments.delete_deployment(
            client=client,
            space_id=space_id,
            deployment_id=deployment_id
        )

    # 'deployment list' command
    if args.deployment == "list":

        space_id = args.space_id
        deployment_type = args.deployment_type

        manage_wml_deployments.list_deployments(
            client=client,
            space_id=space_id,
            deployment_type=deployment_type
        )
