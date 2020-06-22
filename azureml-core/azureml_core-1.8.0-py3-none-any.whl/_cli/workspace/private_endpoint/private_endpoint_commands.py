# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml._cli.workspace.private_endpoint.private_endpoint_subgroup import WorkspacePrivateEndPointSubGroup
from azureml._cli.cli_command import command
from azureml._cli.workspace.private_endpoint.private_endpoint_arguments import PE_NAME_ARGUMENT, \
    PE_VNET_NAME_ARGUMENT, PE_SUBNET_NAME_ARGUMENT, PE_SUBSCRIPTION_ID_ARGUMENT, PE_RESOURCE_GROUP_ARGUMENT, \
    PE_AUTO_APPROVAL_ARGUMENT, PE_CONNECTION_RESOURCE_ID


from azureml.core.private_endpoint import PrivateEndPointConfig, PrivateEndPoint


@command(
    subgroup_type=WorkspacePrivateEndPointSubGroup,
    command="add",
    short_description="Add private endpoint to a workspace.",
    argument_list=[
        PE_NAME_ARGUMENT,
        PE_VNET_NAME_ARGUMENT,
        PE_SUBNET_NAME_ARGUMENT,
        PE_SUBSCRIPTION_ID_ARGUMENT,
        PE_RESOURCE_GROUP_ARGUMENT,
        PE_AUTO_APPROVAL_ARGUMENT
    ])
def workspace_add_private_endpoint(
        workspace=None, pe_name=None,
        pe_vnet_name=None,
        pe_subnet_name=None, pe_subscription_id=None, pe_resource_group=None, pe_auto_approval=None,
        logger=None):

    if pe_name is not None:
        private_endpoint_config = PrivateEndPointConfig(pe_name, pe_vnet_name, pe_subnet_name,
                                                        pe_subscription_id, pe_resource_group)
        workspace.add_private_endpoint(private_endpoint_config, pe_auto_approval)


@command(
    subgroup_type=WorkspacePrivateEndPointSubGroup,
    command="list",
    short_description="List all private endpoints in a workspace.",
    argument_list=[
    ])
def workspace_list_private_endpoint(
        workspace=None,
        logger=None):

    private_endpoints = workspace.private_endpoints
    serialized_pe_list = list()
    for pe in private_endpoints:
        serialized_pe_list.append(private_endpoints[pe].__dict__)

    return serialized_pe_list


@command(
    subgroup_type=WorkspacePrivateEndPointSubGroup,
    command="delete",
    short_description="Delete the specified private endpoint Connection in the workspace.",
    argument_list=[
        PE_CONNECTION_RESOURCE_ID
    ])
def workspace_delete_private_endpoint(
        resource_id,
        logger=None):
    private_endpoint = PrivateEndPoint(private_endpoint_connection_resource_id=resource_id)
    private_endpoint.delete()
