#!/usr/bin/env python

"""
Module that sets up the app, error handling and token verification.
"""

from http import HTTPStatus
import logging
import time

from flask import request, current_app, make_response, jsonify, Blueprint
from flask_restx import abort, Model
from flask_httpauth import HTTPTokenAuth
from werkzeug.utils import find_modules, import_string
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from platkit.librarypatches import PatchedApi as Api
from platkit.exceptions import InvalidUsage
from platkit.utils import CustomJSONEncoder
from platkit import logsetup
from platkit.config import Config
from platkit.middleware.reverse_proxied import ReverseProxied
from platkit.prometheus import metrics
from platkit.cli import setup_commands

log = logging.getLogger("platkit")


DUMMY_USER = "dummy_user"


def discover_blueprints(app, api_info={}):
    app_module_name = app.config["APP_MODULE_NAME"]
    # register blueprint, namespaces and models, assuming a certain directory structure
    blueprint = Blueprint("api", __name__)
    authorizations = {"jwt": {"type": "apiKey", "in": "header", "name": "Authorization"}}
    api = Api(blueprint, doc="/doc/", authorizations=authorizations, security="jwt", **api_info)
    app.api = api

    # remove 'Default' namespace if it is empty to clean up Swagger documentation
    api.namespaces = [x for x in api.namespaces if x.name != "default" or len(x.resources) > 0]

    endpoints_module_name = app_module_name + ".endpoints"
    models_module_name = app_module_name + ".models"
    lst = []
    # namespaces are in [myapp].endpoints
    endpoint_modules = list(find_modules("platkit.endpoints"))
    dev_endpoints = ["platkit.endpoints.auth"]

    if not app.debug:
        endpoint_modules = [x for x in endpoint_modules if x not in dev_endpoints]
    else:
        print("Including dev endpoints: " + str(dev_endpoints))

    endpoint_modules.extend(list(find_modules(endpoints_module_name)))

    models_modules = list(find_modules("platkit.models"))
    models_modules.extend(list(find_modules(models_module_name)))

    for name in endpoint_modules:
        mod = import_string(name)
        if hasattr(mod, "ns"):
            log.debug("Registering namespace '%s'", str(mod))
            api.add_namespace(mod.ns)
            lst.append(str(mod.__name__))
    print("Registered namespaces: %s" % ", ".join(lst))

    lst = []
    # response models are in [myapp].models.responses
    for name in models_modules:
        mod = import_string(name)
        for obj in mod.__dict__.values():
            if isinstance(obj, Model):
                log.debug("Registering model '%s'", obj.name)
                api.models[obj.name] = obj
                lst.append(obj.name)
    print("Registered models: %s" % ", ".join(lst))
    return blueprint


def create_app(app_module_name, api_info={}):
    t = time.time()

    print("Creating app '%s'..." % app_module_name)
    app_module = import_string(app_module_name)
    build_info = getattr(app_module, "build_info", None)
    config_module_name = app_module_name + ".config"
    cfg = import_string(config_module_name)
    app = Flask(cfg.APP_NAME)

    app.config.from_object(cfg)
    app.config["BUILD_INFO"] = build_info
    app.config["APP_MODULE_NAME"] = app_module_name
    if build_info:
        app_version = build_info.get("version")
    app.config["VERSION"] = app_version
    Config(app.config)
    api_info["version"] = app_version

    # assuming an LB and Traefik
    num_proxies = 2
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=num_proxies)
    app.wsgi_app = ReverseProxied(app)

    blueprint = discover_blueprints(app, api_info)

    app.register_blueprint(blueprint)

    if app.config.get("METRICS_ENABLED"):
        metrics.init_app(app)
        metrics.info("app_info", "Application info", **build_info)
    else:
        print("Metrics disabled. Enable in config with 'METRICS_ENABLED=True'")

    setup_base_app(app)
    setup_commands(app)

    print("App %s v%s is ready in %.2f seconds." % (app_module_name, app_version, time.time() - t))
    return app


def setup_base_app(app):
    auth = HTTPTokenAuth("Bearer")
    app.auth = auth

    # Datetime fix
    app.json_encoder = CustomJSONEncoder

    @app.errorhandler(500)
    @app.errorhandler(503)
    @app.errorhandler(409)
    @app.errorhandler(405)
    @app.errorhandler(404)
    @app.errorhandler(403)
    @app.errorhandler(401)
    @app.errorhandler(400)
    @app.errorhandler(InvalidUsage)
    def _handle_error(e):
        return handle_error(e)

    logsetup.setup(app)

    @app.before_request
    def _default_login_required():
        return default_login_required(app)

    if app.config.get("SENTRY_DSN"):
        log.info("Configuring sentry with dsn '%s'", app.config.get("SENTRY_DSN"))
        sentry_sdk.init(
            dsn=app.config["SENTRY_DSN"],
            integrations=[
                SqlalchemyIntegration(),
                FlaskIntegration(),
                LoggingIntegration(event_level=None, level=None),
            ],
            environment=app.config.get("ENVIRONMENT_NAME") or "N/A",
            release="{}@{}".format(app.config["APP_NAME"], app.config["VERSION"]),
        )
        with sentry_sdk.configure_scope() as scope:
            for k, v in app.config["BUILD_INFO"].items():
                scope.set_tag(k, v)
    else:
        log.warning("Sentry is not configured")


def default_login_required(app):
    """All endpoints require login except for ones listed in
    login_not_required list in view class"""
    if not request.endpoint:
        return

    # a dummy callable to execute the login_required logic
    login_required_dummy_view = app.auth.login_required(lambda: None)

    required_major_version = request.headers.get("Api-Major-Version")
    app_version = app.config["VERSION"]

    if required_major_version and app_version:
        my_major_version = int(app_version.split(".")[0])
        if int(required_major_version) != my_major_version:
            abort(
                HTTPStatus.BAD_REQUEST,
                message="You require API Major Version {} "
                "but server has version {}. "
                "Please upgrade your tool.".format(required_major_version, app_version),
            )

    # special case for swagger documentation endpoints and prometheus metrics
    view = current_app.view_functions[request.endpoint]
    if view.__name__ in ("render_doc", "specs", "send_static_file", "prometheus_metrics"):
        return
    if hasattr(view, "view_class"):
        exempt = [f.upper() for f in getattr(view.view_class, "login_not_required", [])]
        if request.method.upper() in exempt:
            return

    return login_required_dummy_view()


def handle_error(e):
    log.warning("Got error: %s", e)
    is_server_error = not isinstance(e, HTTPException) and not isinstance(e, InvalidUsage)

    ret = {}
    error = {"request_id": getattr(request, "request_id", None)}
    ret["error"] = error

    if is_server_error:
        ret["code"] = 500
        ret["message"] = "Internal Server Error"
        error["type"] = "exception"
    else:
        ret["code"] = e.code
        ret["message"] = e.name
        error["type"] = "generic_error" if e.code < 500 else "server_error"
        error["description"] = e.description

        # Support for Flask Restful 'data' property in exceptions.
        if hasattr(e, "data") and e.data:
            error.update(e.data)

            # Legacy field 'message'. If it's in the 'data' payload, rename the field
            # to 'description'.
            if "message" in e.data:
                error["description"] = error.pop("message")

    return make_response(jsonify(ret), ret["code"])
