# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.middlewares.wsgi_middleware import WSGIMiddleware
from contrast.agent.middlewares.route_coverage.falcon_routes import (
    create_falcon_routes,
    get_view_method,
    build_falcon_route,
)
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")


class FalconMiddleware(WSGIMiddleware):
    """
    Falcon apps should use this middleware like so:

    ```
    from contrast.agent.middlewares.falcon_middleware import FalconMiddleware as ContrastMiddleware

    contrast = ContrastMiddleware()
    app = falcon.API(middleware=[contrast])
    contrast.register_app(app)
    ```
    Calling register_app is required. See the method for why.
    """

    def __init__(self, app):
        # Since Falcon is WSGI-based, there is no way to retrieve the app name.
        # Use common config to define an app name.
        super(FalconMiddleware, self).__init__(app, app_name="Falcon Application")

        self.falcon_app = app
        # used for route coverage only for falcon middleware
        self.endpoint_cls = None

    @fail_safely("Unable to get route coverage", return_value={})
    def get_route_coverage(self, _):
        return create_falcon_routes(self.falcon_app)

    @fail_safely("Unable to get Falcon view func")
    def get_view_func(self, request):
        path = request.path
        if not path:
            return

        self.endpoint_cls, _, _, _ = self.falcon_app._router.find(path)
        view_func = get_view_method(self.endpoint_cls, request.method)
        return view_func

    @fail_safely("Unable to build route", return_value="")
    def build_route(self, view_func, url):
        return build_falcon_route(view_func, self.endpoint_cls)
