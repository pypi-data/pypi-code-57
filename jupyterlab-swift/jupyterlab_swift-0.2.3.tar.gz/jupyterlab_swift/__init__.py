from jupyterlab_swift.config import SwiftConfig
from jupyterlab_swift.handler import SwiftConfigHandler, SwiftContentsHandler, SwiftMetadataHandler
from keystoneauth1.adapter import Adapter
from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from notebook.utils import url_path_join

import logging

class SwiftClientFactory():
    def __init__(self, config):
        self.config = config
        self._clients = {}

    def default(self):
        return self.for_project(self.config.project_name)

    def for_project(self, project_name):
        if not project_name in self._clients:
            conf = self.config
            auth = v3.Token(auth_url=conf.auth_url,
                            token=conf.token,
                            project_name=conf.project_name,
                            project_domain_name=conf.project_domain_name)
            session = Session(auth=auth)
            self._clients[project_name] = Adapter(session=session,
                                                  service_type='object-store',
                                                  interface=conf.interface,
                                                  region_name=conf.region_name)

        return self._clients[project_name]

def _jupyter_server_extension_paths():
    return [{
        'module': 'jupyterlab_swift'
    }]

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    config = web_app.settings['config']

    ksalogger = logging.getLogger('keystoneauth')
    ksalogger.setLevel(nb_server_app.log.getEffectiveLevel())

    base_url = web_app.settings['base_url']
    base_endpoint = url_path_join(base_url, 'swift')

    config_endpoint = url_path_join(base_endpoint, 'config')
    contents_endpoint = url_path_join(base_endpoint, 'contents')
    meta_endpoint = url_path_join(base_endpoint, 'meta')

    swift_config = SwiftConfig(config=config)
    client_factory = SwiftClientFactory(swift_config)
    handler_params = {
        'config': swift_config,
        'client_factory': client_factory
    }

    nb_server_app.log.debug("Registering handlers at {}".format(base_endpoint))

    handlers = [(config_endpoint + "(.*)", SwiftConfigHandler, handler_params),
                (contents_endpoint + "(.*)", SwiftContentsHandler, handler_params),
                (meta_endpoint + "(.*)", SwiftMetadataHandler, handler_params)]

    host_pattern = '.*$'
    web_app.add_handlers(host_pattern, handlers)
