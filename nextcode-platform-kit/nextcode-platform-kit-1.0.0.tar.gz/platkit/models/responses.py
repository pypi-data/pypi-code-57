from flask_restx import Model, fields

auth_model = Model(
    "auth",
    {
        "access_token": fields.String(
            description="Access token that can be used with other endpoints as 'Bearer XXX'"
        ),
        "refresh_token": fields.String(
            description="Refresh token for consistency with Keycloak API. "
            "Can be used to re-authenticate against this endpoint."
        ),
    },
)


# this belongs to error_model
class HttpErrorIntegerField(fields.Integer):
    # This is the only way to write to the Example section.
    # The default example error code is 0 which is confusing.
    __schema_example__ = 400


inner_error_model = Model(
    "InnerError",
    {"description": fields.String(), "request_id": fields.String(), "type": fields.String()},
)


# Used to document errors in API doc
error_model = Model(
    "Error",
    {
        "code": HttpErrorIntegerField(description="HTTP status code"),
        "error": fields.Nested(inner_error_model),
        "message": fields.String(),
    },
)
