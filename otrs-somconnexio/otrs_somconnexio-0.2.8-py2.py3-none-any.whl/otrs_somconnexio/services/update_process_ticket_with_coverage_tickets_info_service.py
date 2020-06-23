# coding: utf-8
from otrs_somconnexio.otrs_models.coverage_article import CoverageArticle
from otrs_somconnexio.client import OTRSClient


class UpdateProcessTicketWithCoverageTicketsInfoService:
    """
    Update the process ticket adding articles with the coverage data.

    Receives a TicketID (provisioning process ticket) and a list of coverage tickets.
    From this list of tickets, it creates articles with the information required to
    update the provisioning process ticket.
    """
    def __init__(self, ticket_id, coverage_tickets):
        self.coverage_tickets = coverage_tickets
        self.ticket_id = ticket_id

    def run(self):
        otrs_client = OTRSClient()

        for ticket in self.coverage_tickets:
            article = CoverageArticle(ticket).call()
            otrs_client.update_ticket(self.ticket_id, article)
