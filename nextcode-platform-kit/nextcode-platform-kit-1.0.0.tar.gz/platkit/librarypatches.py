#!/usr/bin/env python
"""
Patching 3rd party libraries
"""

import re
import os
from flask import make_response
from flask.json import dumps
import flask_restx


# monkeypatch the Api class to remove hard-coded '/' rules so that we can put something that
# is not swagger into the root. Hopefully this will be solved in flask_restx at some point
# https://github.com/noirbizarre/flask-restx/issues/247
class PatchedApi(flask_restx.Api):
    def _register_doc(self, app_or_blueprint):
        if self._add_specs and self._doc:
            app_or_blueprint.add_url_rule(self._doc, "doc", self.render_doc)

    @property
    def base_path(self):
        return ""


# Remove Flask restx exception handlers so that we can use our own
# Otherwise we cannot have custom structured error messages from the Api
def patched_init_app(self, app):
    self._register_specs(self.blueprint or app)
    self._register_doc(self.blueprint or app)

    if len(self.resources) > 0:
        for resource, urls, kwargs in self.resources:
            self._register_view(app, resource, *urls, **kwargs)

    self._register_apidoc(app)
    self._validate = (
        self._validate if self._validate is not None else app.config.get("RESTX_VALIDATE", False)
    )
    app.config.setdefault("RESTX_MASK_HEADER", "X-Fields")
    app.config.setdefault("RESTX_MASK_SWAGGER", True)


flask_restx.Api._init_app = patched_init_app


# Install proper json dumper for Flask restx library.
# This is needed because we need to use Flask's JSON converter which can
# handle more variety of Python types than the standard converter.
def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj, indent=4), code)
    resp.headers.extend(headers or {})
    return resp


flask_restx.api.DEFAULT_REPRESENTATIONS = [("application/json", output_json)]


# Adding the reverse-proxy prefix to restx's extract_path method to
# fix swagger documentation functionality which doesn't account for reverse proxies.
def patched_extract_path(path):
    RE_URL = re.compile(r"<(?:[^:<>]+:)?([^<>]+)>")
    prefix = os.environ.get("WXNC_RESTFUL_PREFIX", "")
    return prefix + RE_URL.sub(r"{\1}", path)


flask_restx.swagger.extract_path = patched_extract_path
