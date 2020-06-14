from gateways.apis.api_base_class import ApiBase


class ApiSettings(ApiBase):
    def cloud_providers(self):
        return self.build_route("settings/cloudproviders")

    def cloud_accounts(self):
        return self.build_route("settings/cloudaccounts")

    def status(self):
        return self.build_route("settings/status")

    def azure_cloud_accounts(self):
        return self.build_route("settings/cloudaccounts/azure")

    def aws_cloud_accounts(self):
        return self.build_route("settings/cloudaccounts/aws")

    def add_compute_service_aks(self):
        return self.build_route("settings/cloudaccounts/azure/computeservices/aks")

    def add_compute_service_aws_k8s_unmanaged(self):
        return self.build_route("settings/cloudaccounts/aws/computeservices/k8s_unmanaged")

    def aws_template(self):
        return self.build_route("settings/cloudaccounts/aws/template")

    def space_roles(self):
        return self.build_route("settings/spaceroles")

    def account_roles(self):
        return self.build_route("settings/accountroles")
