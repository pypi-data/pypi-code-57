# coding: utf-8
from otrs_somconnexio.otrs_models.abstract_article import AbstractArticle


class InternetArticle(AbstractArticle):
    def __init__(self, service_type, eticom_contract):
        self.subject = "Sol·licitud {} {}".format(
            service_type,
            eticom_contract.id
        )
