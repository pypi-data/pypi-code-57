from directory_client_core.authentication import SessionSSOAuthenticator
from directory_api_client.base import AbstractAPIClient


url_exportplan_create = '/exportplan/company-export-plan/'
url_exportplan_update = '/exportplan/company-export-plan/{pk}/'
url_exportplan_detail = '/exportplan/company-export-plan/{pk}/'
url_exportplan_list = '/exportplan/company-export-plan/'

url_exportplan_objectives_create = '/exportplan/company-objectives/'
url_exportplan_objectives_update = '/exportplan/company-objectives/{pk}/'
url_exportplan_objectives_detail = '/exportplan/company-objectives/{pk}/'
url_exportplan_objectives_list = '/exportplan/company-objectives/'


class ExportPlanAPIClient(AbstractAPIClient):
    authenticator = SessionSSOAuthenticator

    def exportplan_update(self, sso_session_id, id, data):
        return self.patch(
            url=url_exportplan_update.format(pk=id), data=data, authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_detail(self, sso_session_id, id):
        return self.get(
            url=url_exportplan_detail.format(pk=id),
            use_fallback_cache=True,
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_create(self, sso_session_id, data):
        return self.post(url=url_exportplan_create, data=data, authenticator=self.authenticator(sso_session_id))

    def exportplan_list(self, sso_session_id):
        return self.get(url=url_exportplan_list, authenticator=self.authenticator(sso_session_id))

    def exportplan_objectives_update(self, sso_session_id, id, data):
        return self.patch(
            url=url_exportplan_objectives_update.format(pk=id),
            data=data,
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_objectives_delete(self, sso_session_id, id):
        return self.delete(
            url=url_exportplan_objectives_update.format(pk=id),
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_objectives_detail(self, sso_session_id, id):
        return self.get(
            url=url_exportplan_objectives_detail.format(pk=id),
            use_fallback_cache=True,
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_objectives_create(self, sso_session_id, data):
        return self.post(
            url=url_exportplan_objectives_create,
            data=data,
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_objectives_list(self, sso_session_id):
        return self.get(url=url_exportplan_objectives_list, authenticator=self.authenticator(sso_session_id))
