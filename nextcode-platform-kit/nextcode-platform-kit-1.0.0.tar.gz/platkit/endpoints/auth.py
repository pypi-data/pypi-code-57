#!/usr/bin/env python
from http import HTTPStatus
import jwt
import time

from flask import Blueprint, current_app
from flask_restx import Resource, Namespace, abort, reqparse, Model, fields

from platkit.auth import (
    get_auth_payload,
    get_auth_payload_from_refresh_token,
    validate_self_issued_jwt,
)
from platkit.models.responses import auth_model

ns = Namespace("devauth", description="Authentication endpoint for local development")


@ns.route("/", defaults={"path": ""})
@ns.route("/<path:path>")
class Auth(Resource):
    login_not_required = ["post"]

    post_parser = reqparse.RequestParser(bundle_errors=True)
    post_parser.add_argument("grant_type", type=str, required=False)
    post_parser.add_argument("client_id", type=str, default="api-key-client")
    post_parser.add_argument("refresh_token", type=str, required=False)
    post_parser.add_argument("username", type=str)
    post_parser.add_argument("password", type=str)

    @ns.expect(post_parser)
    @ns.marshal_with(auth_model)
    def post(self, path):
        """This is a 'fake' authentication endpoint for local development.
        The endpoint mimics the behavior of keycloak allowing the client application to use it in the same way as if
        this was a keycloak server. Note that this endpoint is only loaded in debug mode, see flasksetup.py.
        You can call this with POST '/auth/realms/wuxinextcode.com/protocol/openid-connect/token'. You only need to
        include a username+password or a refresh_token.
        """
        if not current_app.debug:
            abort(HTTPStatus.BAD_REQUEST, message="This endpoint is only available with DEBUG=True")
        args = self.post_parser.parse_args()

        user_name = args.get("username")
        if args.get("refresh_token"):
            ret = get_auth_payload_from_refresh_token(user_name, args.get("refresh_token"))
        else:
            ret = get_auth_payload(user_name, args.get("client_id"))

        validate_self_issued_jwt(ret["access_token"])

        return ret
