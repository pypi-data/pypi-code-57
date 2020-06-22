# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import time

from ._utils import ArmDeploymentOrchestrator, get_arm_resource_id

from .arm_template_builder import (
    ArmTemplateBuilder,
    build_private_endpoint_resource,
    build_private_dns_zone_resource
)

PRIVATE_DNS_ZONE = "PrivateDnsZone"
PRIVATE_END_POINT = "PrivateEndPoint"


class PrivateEndPointArmDeploymentOrchestrator(ArmDeploymentOrchestrator):

    def __init__(self, auth, workspace_resource_group_name, location,
                 workspace_subscription_id, workspace_name, private_endpoint_config, private_endpoint_auto_approval,
                 deployment_name=None):

        import random

        super().__init__(auth, private_endpoint_config.vnet_resource_group,
                         private_endpoint_config.vnet_subscription_id, deployment_name if deployment_name else
                         '{0}_{1}'.format('Microsoft.PrivateEndpoint', random.randint(100, 99999)))
        self.auth = auth
        self.workspace_subscription_id = workspace_subscription_id
        self.workspace_resource_group_name = workspace_resource_group_name
        self.workspace_name = workspace_name
        self.master_template = ArmTemplateBuilder()
        self.location = location.lower().replace(" ", "")
        self.resources_being_deployed = {}

        self.private_endpoint_config = private_endpoint_config
        self.private_endpoint_auto_approval = private_endpoint_auto_approval

        self.error = None

    def deploy_private_endpoint(self, show_output=True):
        try:
            self._generate_private_endpoint_resource()
            # build the template
            template = self.master_template.build()

            # deploy the template
            self._arm_deploy_template(template)

            if show_output:
                while not self.poller.done():
                    self._check_deployment_status()
                    time.sleep(5)

                if self.poller._exception is not None:
                    self.error = self.poller._exception
                else:
                    # one last check to make sure all print statements make it
                    self._check_deployment_status()
            else:
                try:
                    self.poller.wait()
                except Exception:
                    self.error = self.poller._exception
        except Exception as ex:
            self.error = ex

        if self.error is not None:
            error_msg = "Unable to create the private endpoint for the workspace. \n {}".format(self.error)
            print(error_msg)

    def _generate_private_endpoint_resource(self):
        # The vnet, subnet should be precreated by user
        workspace_resource_id = get_arm_resource_id(self.workspace_resource_group_name,
                                                    "Microsoft.MachineLearningServices/workspaces",
                                                    self.workspace_name,
                                                    self.workspace_subscription_id)
        self.master_template.add_resource(build_private_endpoint_resource(self.private_endpoint_config,
                                                                          self.location,
                                                                          workspace_resource_id,
                                                                          self.private_endpoint_auto_approval))
        self.resources_being_deployed[self.private_endpoint_config.name] = (PRIVATE_END_POINT, None)

        if self.private_endpoint_auto_approval is not None and self.private_endpoint_auto_approval is True:
            # Create private dns zone only for auto approval.
            # For manual approval, users have to approve the PE and manually create the private DNS zone.
            vnet_resource_id = get_arm_resource_id(self.private_endpoint_config.vnet_resource_group,
                                                   "Microsoft.Network/virtualNetworks",
                                                   self.private_endpoint_config.vnet_name,
                                                   self.private_endpoint_config.vnet_subscription_id)
            private_dns = build_private_dns_zone_resource(self.private_endpoint_config, vnet_resource_id,
                                                          self._get_azure_private_dns_zone_name())
            self.master_template.add_resource(private_dns)
            self.resources_being_deployed[private_dns["name"]] = (PRIVATE_DNS_ZONE, None)

    def _get_azure_private_dns_zone_name(self):
        # If the location is master, the dns zone name is privatelink.api.azureml-test.ms
        if self.location == "centraluseuap":
            return "privatelink.api.azureml-test.ms"

        return "privatelink.api.azureml.ms"
