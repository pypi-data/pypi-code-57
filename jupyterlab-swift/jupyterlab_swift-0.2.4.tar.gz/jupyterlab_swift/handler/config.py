import json

from jupyterlab_swift.handler.base import SwiftBaseHandler
from keystoneauth1.exceptions import HttpError
from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from notebook.base.handlers import APIHandler
from tornado import escape, gen, web

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
            projects = self.client_factory.all_projects()
            # Sort by name to be nice
            projects.sort(key=lambda p: p['name'])
        except HttpError as err:
            self.log.warn('Failed to fetch list of projects for user: {}'.format(err.details))
            projects = []

        self.set_status(200)
        self.set_header('content-type', 'application/json')
        self.finish(json.dumps(dict(
            max_file_size_bytes=conf.max_file_size_bytes,
            projects=projects
        )))
