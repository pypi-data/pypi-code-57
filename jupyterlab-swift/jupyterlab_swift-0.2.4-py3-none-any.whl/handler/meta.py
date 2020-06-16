import json
from jupyterlab_swift.handler.base import SwiftBaseHandler
from jupyterlab_swift.handler.decorator import swift_proxy
from keystoneauth1.exceptions.catalog import EndpointNotFound
from keystoneauth1.exceptions.http import BadRequest, NotFound, Unauthorized
from notebook.utils import url_escape
from notebook.base.handlers import APIHandler
import re
from tornado import gen, web
from tornado.httputil import url_concat

class SwiftMetadataHandler(SwiftBaseHandler, APIHandler):
    """
    A Swift API proxy handler that handles requests for account/container/object
    metadata. Importantly does not handle requests for file contents.
    """
    @web.authenticated
    @gen.coroutine
    @swift_proxy
    def get(self, path=''):
        """Proxy API requests to Swift with authenticated session.
        """
        params = self.api_params()
        params.update(format='json')
        params.update(delimiter=self.DELIMITER)

        prefix = params.get('prefix', '')

        if prefix:
            # Strip trailing slash to attempt lookup as full object URI
            object_path = re.sub(r'/+$', '', prefix)

            try:
                self.log.debug(f'Checking if {object_path} is an object')
                object_response = self.swift.head(self.api_path(object_path))

                if not self._is_directory_response(object_response):
                    self._finish_from_swift_response(object_response, object_path)
                    return
            except (NotFound, EndpointNotFound):
                pass

        listing_path = self.api_path('', params)

        try:
            listing_response = self.swift.get(listing_path)

        except NotFound as err:
            if err.message == 'No token in the request':
                # Ceph/swift can return a 404 in the event of an unauthorized
                # request; ensure we report this properly.
                raise Unauthorized()

            if not prefix:
                self.log.debug((
                    'Failed to list objects, checking if container is created'))
                # Likely we were trying to list a container that doesn't
                # exist. Attempt to create it one time to be nice.
                self.swift.put(self.api_path(''))
                listing_response = self.swift.get(listing_path)
            else:
                raise

        except EndpointNotFound:
            region_name = self.swift.region_name
            raise BadRequest(
                f'No Swift endpoint exists for region {region_name}')

        self._finish_from_swift_response(listing_response, prefix)


    def _finish_from_swift_response(self, response, prefix):
        """Write a upstream response based on a downstream response from Swift.

        Handles adding minimal type hints for the client about what kinds of
        objects are being returned, as well as making sure to proxy metadata
        headers.
        """
        headers = response.headers

        self.set_status(response.status_code)
        self.set_header('content-type', 'application/json')

        if 'x-account-object-count' in headers:
            # This is an account response
            self.proxy_headers(response, self.ACCOUNT_HEADERS)
            containers = response.json()
            [c.update(type='container') for c in containers]
            self.finish(json.dumps(containers))

        elif 'x-container-object-count' in headers:
            # This is a container response
            self.proxy_headers(response, self.CONTAINER_HEADERS)
            objects = response.json()
            mapped_objects = []

            def subdir_is_segment_dir(subdir):
                subdir_name = subdir.get('subdir')
                for o in objects:
                    # Flag subdirectories that are linked to an object
                    # with the same name (these should be hidden by Swift as
                    # they are parts of SLO segments... but Swift still returns
                    # them.)
                    if 'name' in o and (o.get('name') + self.DELIMITER) == subdir_name:
                        return True
                return False

            for o in objects:
                if 'subdir' in o:
                    if subdir_is_segment_dir(o):
                        continue
                    o.update(type='subdir', name=o.pop('subdir'))
                else:
                    o.update(type='object')

                if prefix is not None and self.DELIMITER in prefix:
                    prefix = prefix[0 : prefix.rfind(self.DELIMITER) + 1]
                    name_without_prefix = o.get('name').replace(prefix, '')
                    o.update(name=name_without_prefix)

                mapped_objects.append(o)

            self.finish(json.dumps(mapped_objects))

        else:
            # Assume a file response
            self.proxy_headers(response, self.OBJECT_HEADERS)
            self.finish(json.dumps({
                'name': prefix[prefix.rfind(self.DELIMITER) + 1 :],
                'hash': headers.get('etag'),
                'last_modified': headers.get('x-timestamp'),
                # For some reason Swift doesn't return _any_ content-length
                # header if the size is 0
                'bytes': int(headers.get('content-length', '0')),
                'content_type': headers.get('content-type'),
                'type': 'object',
            }))

    def _is_directory_response(self, response):
        """
        Determines if a response is for a directory-like entity (account or
        container) based on returned headers.
        """
        headers = response.headers
        return ('x-account-object-count' in headers) or ('x-container-object-count' in headers)
