# coding: utf-8
from otrs_somconnexio.otrs_models.abstract_article import AbstractArticle


class VfProvisioningArticle(AbstractArticle):
    def __init__(self, provisioning_ticket):
        self.provisioning_ticket = provisioning_ticket
        self.subject = "Aprovisionament del tiquet de Vodafone #####"
        # soon provisioning_ticket will have a ticket id as a foreignKey, then I would go for:
        # self.subject = "Aprovisionament del tiquet de Vodafone {}".format(self.provisioning_ticket["ticket_id"])
        self.body = self._body()

    def _body(self):
        body = ""

        for field in sorted(self.provisioning_ticket):
            value = self.provisioning_ticket[field]
            if value:
                body = u"{}{}: {}\n".format(body, field, value)

        return body
