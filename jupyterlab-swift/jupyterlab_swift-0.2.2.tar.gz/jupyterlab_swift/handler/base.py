from jupyterlab_swift.config import SwiftConfig
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_escape
from re import sub
from tornado.httputil import url_concat

class SwiftBaseHandler(IPythonHandler):
    DELIMITER = '/'

    ACCOUNT_NAME_HEADER = 'x-account-name'

    ACCOUNT_HEADERS = (
        'x-account-access-control',
        'x-account-bytes-used',
        'x-account-container-count',
        'x-account-meta-name',
        'x-account-meta-quota-bytes',
        'x-account-meta-temp-url-key-2',
        'x-account-meta-temp-url-key',
        'x-account-object-count',
        'x-account-storage-policy-name-bytes-used',
        'x-account-storage-policy-name-container-count',
        'x-account-storage-policy-name-object-count',
        'x-openstack-request-id',
        'x-timestamp',
    )

    CONTAINER_HEADERS = (
        'x-container-bytes-used',
        'x-container-meta-name',
        'x-container-meta-quota-bytes',
        'x-container-meta-quota-count',
        'x-container-meta-temp-url-key-2',
        'x-container-meta-temp-url-key',
        'x-container-object-count',
        'x-container-read',
        'x-container-sync-key',
        'x-container-sync-to',
        'x-container-write',
        'x-history-location',
        'x-openstack-request-id',
        'x-storage-policy',
        'x-timestamp',
        'x-versions-location',
    )

    OBJECT_HEADERS = (
        'x-delete-at',
        'x-object-manifest',
        'x-object-meta-name',
        'x-openstack-request-id',
        'x-static-large-object',
        'x-symlink-target-account',
        'x-symlink-target',
        'x-timestamp',
    )

    """
    A base clase for a Swift API proxy handler.
    """
    def initialize(self, client_factory, config):
        self.client_factory = client_factory
        self.swift_config = config
        self.swift = self.swift_client()

    def proxy_headers(self, response, names):
        headers = response.headers
        [self.set_header(x, headers.get(x)) for x in names if x in headers]

    def swift_client(self):
        request_headers = self.request.headers
        if self.ACCOUNT_NAME_HEADER in request_headers:
            return self.client_factory.for_project(request_headers[self.ACCOUNT_NAME_HEADER])
        else:
            return self.client_factory.default()

    def swift_path(self, path):
        container = self.root_container()
        path_parts = list(filter(None, [container, sub('^/', '', path)]))
        return self.DELIMITER.join(path_parts)

    def api_path(self, path, params=None):
        return url_concat(url_escape(self.swift_path(path)), params)

    def api_params(self):
        query = self.request.query_arguments
        return { key: query[key][0].decode() for key in query }

    def root_container(self):
        conf = self.swift_config
        if not conf.root_container:
            return None
        return conf.root_container.format(project_name=conf.project_name)
