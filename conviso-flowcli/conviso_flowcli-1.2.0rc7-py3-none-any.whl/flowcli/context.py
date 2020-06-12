import click

from convisoappsec.flow import api


class FlowContext(object):
    def __init__(self):
        self.key = None
        self.url = None
        self.insecure = None

    def create_flow_api_client(self):
        return api.Client(
            key=self.key,
            url=self.url,
            insecure=self.insecure,
        )


pass_flow_context = click.make_pass_decorator(
    FlowContext, ensure=True
)
