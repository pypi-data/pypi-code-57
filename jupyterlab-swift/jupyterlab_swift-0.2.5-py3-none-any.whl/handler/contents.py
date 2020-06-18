import json
from jupyterlab_swift.handler.base import SwiftBaseHandler
from jupyterlab_swift.handler.decorator import swift_proxy
from jupyterlab_swift.handler.exception import SwiftHandlerException, FileSizeExceeded
from keystoneauth1.exceptions import HttpError
from keystoneauth1.exceptions.base import ClientException
from notebook.utils import url_escape
from notebook.base.handlers import AuthenticatedFileHandler
from tornado import gen, web
from tornado.httputil import url_concat

class SwiftContentsHandler(SwiftBaseHandler, AuthenticatedFileHandler):
    """
    A Swift API proxy handler that handles requests for account/container/object
    metadata. Importantly does not handle requests for file contents.
    """

    CHUNK_HEADER = 'x-chunk'
    COPY_HEADER = 'x-copy-from'

    @web.authenticated
    @gen.coroutine
    @swift_proxy
    def get(self, path=''):
        """
        Proxy GET API requests to Swift with authenticated session.
        """
        self._check_path(path)

        api_path = self.api_path(path, self.api_params())

        head_response = self.swift.head(api_path)
        self._check_content_length(head_response.headers)

        response = self.swift.get(api_path)

        self.set_status(response.status_code)
        self.proxy_headers(response, self.OBJECT_HEADERS)
        self.proxy_headers(response, ['content-length', 'content-type'])
        self.finish(response.content)

    @web.authenticated
    @gen.coroutine
    @swift_proxy
    def put(self, path=''):
        """
        Proxy PUT API requests to Swift with authenticated session.
        """
        request_headers = self.request.headers
        self._check_path(path)

        swift_body = self.request.body
        swift_headers = {}

        if request_headers.get(self.COPY_HEADER, ''):
            copy_from = self.swift_path(request_headers.get(self.COPY_HEADER))
            swift_headers[self.COPY_HEADER] = copy_from

        swift_params = self.api_params()

        if request_headers.get(self.CHUNK_HEADER, ''):
            chunk_number = int(request_headers.get(self.CHUNK_HEADER))

            if chunk_number < 0:
                last_chunk = True
                chunks_response = self.swift.get(self.api_path('', dict(prefix=(path.replace('/', '') + self.DELIMITER),
                                                                        delimiter=self.DELIMITER,
                                                                        format='json')))
                chunks = chunks_response.json()

                if not chunks:
                    raise ValueError('Expected some chunks to exist')

                chunk_number = len(chunks) + 1
            else:
                last_chunk = False

            chunk_path = '{path}{delimiter}{chunk:06d}'.format(path=path.replace('/', ''),
                                                               delimiter=self.DELIMITER,
                                                               chunk=chunk_number)
            response = self.swift.put(self.api_path(chunk_path, swift_params),
                                      headers=swift_headers,
                                      data=swift_body)
            if last_chunk:
                swift_params['multipart-manifest'] = 'put'
                # Account for last chunk we just added
                chunks.append(dict(name=chunk_path,
                                   hash=response.headers.get('etag'),
                                   bytes=len(swift_body)))
                manifest = [{'path': '/'.join(['', self.root_container(), c['name']]),
                             'etag': c['hash'],
                             'size_bytes': c['bytes']} for c in chunks]
                response = self.swift.put(self.api_path(path, swift_params),
                                          data=json.dumps(manifest))
        else:
            response = self.swift.put(self.api_path(path, swift_params),
                                      headers=swift_headers,
                                      data=swift_body)

        self.set_status(response.status_code)
        self.proxy_headers(response, self.OBJECT_HEADERS)
        self.proxy_headers(response, ['content-length', 'content-type'])
        self.finish()

    @web.authenticated
    @gen.coroutine
    @swift_proxy
    def delete(self, path=''):
        """
        Proxy DELETE API requests to Swift with authenticated session.
        """
        self._check_path(path)
        params = self.api_params()

        head_response = self.swift.head(self.api_path(path))

        # In case it's a SLO manifest, ensure all segments are automatically deleted
        if head_response.headers.get('x-static-large-object', '') == 'True':
            params['multipart-manifest'] = 'delete'

        response = self.swift.delete(self.api_path(path, params))
        self.set_status(response.status_code)
        self.finish()

    def _check_path(self, path):
        """
        Ensure there is a path set on the request. Avoids problems where
        requests are made implicitly against the container itself rather
        than an object in a container (especially important for DELETE)
        """
        if not path.replace('/', ''):
            raise SwiftHandlerException('No path to file')

    def _check_content_length(self, headers):
        """
        Ensure the file does not exceed some maximum size. All file downloads
        and uploads are proxied through this handler, which causes strain, and the
        Jupyter interface doesn't deal well with huge files anyways.
        """
        # For some reason Swift doesn't return _any_ content-length
        # header if the size is 0
        file_size = int(headers.get('content-length', '0'))
        max_size = self.swift_config.max_file_size_bytes
        if file_size > max_size:
            raise FileSizeExceeded('File exceeds max size of {} bytes'.format(max_size))
