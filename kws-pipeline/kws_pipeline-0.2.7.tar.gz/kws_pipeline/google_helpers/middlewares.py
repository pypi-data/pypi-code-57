from google.cloud import ndb


class NDBClientMiddleware:
    client = ndb.Client()

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        with self.client.context():
            return self.wsgi_app(environ, start_response)
