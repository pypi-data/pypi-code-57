import argparse
from functools import lru_cache

from jupyterlab_swift.config import SwiftConfig
from jupyterlab_swift.handler import SwiftConfigHandler, SwiftContentsHandler, SwiftMetadataHandler
from keystoneauth1 import adapter, loading, session
from notebook.utils import url_path_join

import logging

class SwiftClientFactory():
    def __init__(self, config):
        self.config = config

    def _adapter(self, service_type, **session_kwargs):
        sess, args = self._session(**session_kwargs)
        # Wrap session in adapter that sets interface/region
        return adapter.Adapter(sess, service_type=service_type,
                               interface=args.os_interface,
                               region_name=args.os_region_name)

    def _session(self, auth_url=None, project_name=None,
                 project_domain_id=None, region_name=None):
        fake_argv = []
        if auth_url:
            fake_argv.extend(['--os-auth-url', auth_url])
        if project_name:
            fake_argv.extend(['--os-project-name', project_name])
        if project_domain_id:
            fake_argv.extend(['--os-project-domain-id', project_domain_id])
        if region_name:
            fake_argv.extend(['--os-region-name', region_name])

        parser = argparse.ArgumentParser()
        loading.cli.register_argparse_arguments(
            parser, fake_argv, default='token')
        loading.session.register_argparse_arguments(parser)
        loading.adapter.register_argparse_arguments(parser)
        args = parser.parse_args(fake_argv)

        auth = loading.cli.load_from_argparse_arguments(args)
        sess = loading.session.load_from_argparse_arguments(args, auth=auth)
        return sess, args

    def all_projects(self, auth_url=None):
        sess, _ = self._session()
        if not auth_url:
            auth_url = sess.auth.auth_url
        project_response = sess.get(f'{auth_url}/auth/projects')
        projects = project_response.json()['projects']
        projects = [
            p for p in projects
            if p['enabled'] and p['name'] != 'openstack'
        ]
        return projects

    @lru_cache(maxsize=128)
    def scoped(self, **kwargs):
        if not kwargs.get('project_name'):
            projects = self.all_projects(auth_url=kwargs.get('auth_url'))
            if projects:
                # Choose first one by default
                # TODO(jason): this could be smarter and look at last project
                # the user was interacting w/ in the plugin somehow.
                project = projects[0]
                kwargs['project_name'] = project['name']
                kwargs['project_domain_id'] = project['domain_id']

        return self._adapter('object-store', **kwargs)

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
