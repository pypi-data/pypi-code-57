# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import deque
from copy import copy
from importlib import import_module

from django.utils.regex_helper import normalize

from contrast.agent.middlewares.route_coverage.coverage_utils import (
    CoverageUtils,
    DEFAULT_ROUTE_METHODS,
)
from contrast.agent.settings_state import SettingsState
from contrast.extern.functools_lru_cache import lru_cache

import logging

logger = logging.getLogger("contrast")


@lru_cache(maxsize=1)
def is_django_2():
    settings = SettingsState()
    return settings.framework.version.major == "2"


def create_url(pattern_or_resolver):
    if is_django_2():
        pattern = pattern_or_resolver.pattern.regex.pattern
    else:
        pattern = pattern_or_resolver.regex.pattern

    try:
        normalized = normalize(pattern)[0][0]
        url = normalized.replace("%(", "{").replace(")", "}")
    except Exception:
        url = pattern_or_resolver.name

    return url


def get_method_info(pattern_or_resolver):
    method_types = []
    method_arg_names = "()"

    lowest_function = CoverageUtils.get_lowest_function_call(
        pattern_or_resolver.callback
    )

    if lowest_function is not None:
        method_arg_names = CoverageUtils.build_args_from_function(lowest_function)

        # this method returns a dict because it uses one to store state in the recursive function
        method_types_dict = CoverageUtils.check_for_http_decorator(lowest_function)
        method_types = method_types_dict.get("require_http_methods", [])

        if not isinstance(method_types, list):
            method_types = [method_types]

    return method_types or DEFAULT_ROUTE_METHODS, method_arg_names


def create_one_route(routes, method_type, method_arg_names, pattern_or_resolver):
    """
    Create a new RouteCoverage object and adds it to routes dict

    :param routes: dict of routes
    :param method_type:
    :param method_arg_names:
    :param pattern_or_resolver:
    :return: None, adds to routes dict which is updated through pass-by-reference
    """
    route = build_django_route(pattern_or_resolver, method_arg_names)

    route_id = str(id(pattern_or_resolver.callback))

    key = CoverageUtils.build_key(route_id, method_type)

    routes[key] = CoverageUtils.build_route_coverage(
        verb=method_type, url=create_url(pattern_or_resolver), route=route
    )


def create_routes(urlpatterns):
    if is_django_2():
        try:
            from django.urls.resolvers import (
                URLPattern as RegexURLPattern,
                URLResolver as RegexURLResolver,
            )
        except Exception as exception:
            logger.error("Failed to import from django.urls.resolvers: %s", exception)
            return
    else:
        try:
            # Django 1.10 and above
            from django.urls.resolvers import RegexURLPattern, RegexURLResolver
        except ImportError:
            # Django 1.9 and below
            from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

    routes = {}

    urlpatterns_deque = deque(urlpatterns)

    while urlpatterns_deque:
        url_pattern = urlpatterns_deque.popleft()

        if isinstance(url_pattern, RegexURLResolver):
            urlpatterns_deque.extend(url_pattern.url_patterns)

        elif isinstance(url_pattern, RegexURLPattern):
            method_types, method_arg_names = get_method_info(url_pattern)
            for method_type in method_types:
                create_one_route(routes, method_type, method_arg_names, url_pattern)
    return routes


def create_django_routes():
    """
    Grabs all URL's from the root settings and searches for possible required_method decorators

    In Django there is no implicit declaration of GET or POST. Often times decorators are used to fix this.

    Returns a dict of key = id, value = RouteCoverage.
    """

    from django.conf import settings

    if not settings.ROOT_URLCONF:
        logger.info("Application does not define settings.ROOT_URLCONF")
        logger.debug("Skipping enumeration of urlpatterns")
        return

    try:
        root_urlconf = import_module(settings.ROOT_URLCONF)
    except Exception as exception:
        logger.error("Failed to import ROOT_URLCONF: %s", exception)
        return

    try:
        urlpatterns = root_urlconf.urlpatterns or []
    except Exception as exception:
        logger.error("Failed to get urlpatterns: %s", exception)
        return

    url_patterns = copy(urlpatterns)
    return create_routes(url_patterns)


def build_django_route(pattern_or_resolver, method_arg_names=None):
    if hasattr(pattern_or_resolver, "lookup_str"):
        route = pattern_or_resolver.lookup_str
    elif hasattr(pattern_or_resolver, "callback"):
        cb = pattern_or_resolver.callback
        route = cb.__module__ + "." + cb.__name__
    else:
        # TODO: PYT-821 fix route coverage for Django 3
        return ""

    if method_arg_names is None:
        method_arg_names = CoverageUtils.build_args_from_function(pattern_or_resolver)

    route += method_arg_names
    return route
