from spintop.analytics import AbstractSingerTarget

from .persistence_facade import default_spintop_api

class SpintopAPIAnalytics(AbstractSingerTarget):
    def __init__(self, spintop_api=None, uri=None, database_name=None, env=None):
        super().__init__()

        if spintop_api is None:
            spintop_api = default_spintop_api(env, uri, database_name)

        self.spintop_api = spintop_api
        spintop_api.register_analytics(self)

    @property
    def session(self):
        return self.spintop_api.session

    def send_messages(self, messages_str):
        return self.session.put(self.spintop_api.get_link('analytics.stream_update'), json=messages_str)
