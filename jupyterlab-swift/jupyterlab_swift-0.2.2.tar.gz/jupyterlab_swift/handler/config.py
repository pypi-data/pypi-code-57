import json
from jupyterlab_swift.handler.base import SwiftBaseHandler
from keystoneauth1.exceptions import HttpError
from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from notebook.base.handlers import APIHandler
from tornado import escape, gen, web

# This needs to match the ConfigurableProperty type in `src/config.ts`.
CONFIGURABLE_PROPERTIES = [
    'project_name',
    'project_domain_name',
    'region',
]

class SwiftConfigHandler(SwiftBaseHandler, APIHandler):
    """
    A handler that provides the UI with information about the configuration
    of the server extension. Fetches some additional information relevant to
    the modification of configuration as well, such as the list of all Keystone
    projects the user is associated with.
    """

    @web.authenticated
    @gen.coroutine
    def get(self, path=''):
        conf = self.swift_config

        try:
            auth = v3.Token(auth_url=conf.auth_url, token=conf.token)
            sess = Session(auth=auth)
            project_response = sess.get('{}/auth/projects'.format(conf.auth_url))
            projects = [dict(
                id=p['id'],
                name=p['name'],
                domain_id=p['domain_id'],
            ) for p in project_response.json()['projects'] if p['enabled']]
            # Sort by name to be nice
            projects.sort(key=lambda p: p['name'])
        except HttpError as err:
            self.log.warn('Failed to fetch list of projects for user: {}'.format(err.details))
            projects = []
            pass

        self.set_status(200)
        self.set_header('content-type', 'application/json')
        self.finish(json.dumps(dict(
            auth_url=conf.auth_url,
            project_name=conf.project_name,
            project_domain_name=conf.project_domain_name,
            region_name=conf.region_name,
            max_file_size_bytes=conf.max_file_size_bytes,
            projects=projects
        )))

    @web.authenticated
    @gen.coroutine
    def put(self, path=''):
        conf = self.swift_config

        body = escape.json_decode(self.request.body)
        for key, value in body.items():
            if not key in CONFIGURABLE_PROPERTIES:
                self.log.debug(('Skipping configuration of {} as it is not in '
                                'the list of configurable properties').format(key))
                continue
            """
            NOTE: this will mutate the shared configuration by design. The
            configuration instance is defined at server start and is shared
            by all handlers. This "works" because of the model of the Jupyter
            server, which has a single instance and tends to only be used by
            a single user.
            """
            setattr(conf, key, value)

        self.set_status(204)
        self.set_header('content-type', 'application/json')
        self.finish()
