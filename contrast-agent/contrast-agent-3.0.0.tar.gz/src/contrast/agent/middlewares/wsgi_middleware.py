# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.webob import Request, Response

import contrast
from contrast.agent.assess.policy.trigger_node import TriggerNode
from contrast.agent.middlewares.base_middleware import BaseMiddleware
from contrast.agent.middlewares.environ_tracker import track_environ_sources
from contrast.agent.middlewares.response_wrappers.wsgi_response_wrapper import (
    WsgiResponseWrapper,
)
from contrast.agent.request_context import RequestContext
from contrast.utils.decorators import cached_property, fail_safely
from contrast.utils.exceptions.security_exception import SecurityException
from contrast.utils.exceptions.contrast_service_exception import (
    ContrastServiceException,
)

import logging

logger = logging.getLogger("contrast")


class WSGIMiddleware(BaseMiddleware):
    """
    This is not meant for Django; only for WSGI only frameworks like Pylons
    """

    def __init__(self, wsgi_app, app_name="WSGI Application"):
        self.app_name = app_name

        super(WSGIMiddleware, self).__init__()

        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        if self.settings and self.settings.is_agent_enabled():

            context = RequestContext(environ)

            if self.settings.is_assess_enabled():
                track_environ_sources("wsgi", context, environ)

            with contrast.CS__CONTEXT_TRACKER.lifespan(context):
                return self.call_with_agent(context, environ, start_response)

        return self.call_without_agent(environ, start_response)

    def call_with_agent(self, context, environ, start_response):
        self.log_start_request_analysis(environ.get("PATH_INFO"))

        context.timer.set_start("total")

        try:
            self.prefilter(context)

            response = Request(environ).get_response(self.wsgi_app)
            context.extract_response_to_context(WsgiResponseWrapper(response))

            self.update_libraries(context)

            self.postfilter(context)

            self.check_for_blocked(context)

            context.timer.set_end("total")
            return response(environ, start_response)

        except ContrastServiceException as e:
            logger.warning(e)
            return self.call_without_agent(environ, start_response)
        except Exception as e:
            response = self.handle_exception(e)
            return response(environ, start_response)
        finally:
            self.handle_ensure(context, context.request)
            self.log_end_request_analysis(environ.get("PATH_INFO"))
            if self.settings.is_assess_enabled():
                contrast.STRING_TRACKER.ageoff()

    def generate_security_exception_response(self):
        return Response(self.OVERRIDE_MESSAGE, SecurityException.STATUS)

    def call_without_agent(self, environ, start_response):
        """
        Normal without middleware call
        """
        super(WSGIMiddleware, self).call_without_agent()
        return self.wsgi_app(environ, start_response)

    def get_route_coverage(self, request):
        """
        Unlike frameworks, WSGI is a spec, so it does not have a way to register routes.
        As such, there is no way to discover routes. Instead, routes will be added as they
        are visited via check for new routes.

        :param request: either RequestContext or dict type
        :return: empty dict
        """
        return {}

    @cached_property
    def trigger_node(self):
        """
        WSGI-specific trigger node used by reflected xss postfilter rule

        The rule itself is implemented in the base middleware but we need to
        provide a WSGI-specific trigger node for reporting purposes.
        """
        method_name = (
            self.wsgi_app.__name__ if hasattr(self.wsgi_app, "__name__") else "wsgi_app"
        )

        module, class_name, args, instance_method = self._process_trigger_handler(
            self.wsgi_app
        )

        return (
            TriggerNode(module, class_name, instance_method, method_name, "RETURN"),
            args,
        )

    @fail_safely("Unable to get WSGI view func")
    def get_view_func(self, request):
        """
        While most frameworks define view functions, WSGI doesn't so we will rely
        on the path information for reporting.
        If there is no path information, return an empty string

        :param request: RequestContext instance
        :return: string of path information for this request
        """
        return request.environ.get("PATH_INFO", "")

    @fail_safely("Unable to build route", return_value="")
    def build_route(self, view_func, url):
        return url.replace("/", "")
