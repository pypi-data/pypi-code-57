#!/usr/bin/env python
import time
import jwt
from http import HTTPStatus
import logging
from functools import wraps

from flask import request, g, current_app
from flask_restx import abort

from platkit.config import Config

log = logging.getLogger("platkit")

config = Config()


DUMMY_USER = "dummy_user"

# pyjwt can use either PEM or ssh-keygen formatted public keys. We use the ssh-keygen one here for simplicity
DEVELOPMENT_PUBLIC_KEY = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCqG94nyS4WWo1ycEGvGVcsDtz+JztCDFIrNDx9VumiUAVWLk/PWC2K5dcsIS9mNynR5bHio9sReYrYBYAUlsEsM8aWXJhpFYONzLhMNsN2OENnFZxSE+jdI+SjIZHCa9WYRwthZ++pspqY74sgML8WZiWLp3aWCOK1GjyqXbOCkYWBSaYbJqZACsCtENE3o/ELiD922k2PKezvZCepj3+bhXL7UQr60DO03EX9tCklcuLGEQnuwmIXPLmICxWXgimjFt2kjE3k4L9I6I7nkbuKvC8R6+dsaTY2PXxCVJK/2wsD71NSxlDPXamj9kUkkI0jtmGRnvf5U/lW1xnWhbUP"""

DEVELOPMENT_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAqhveJ8kuFlqNcnBBrxlXLA7c/ic7QgxSKzQ8fVbpolAFVi5P
z1gtiuXXLCEvZjcp0eWx4qPbEXmK2AWAFJbBLDPGllyYaRWDjcy4TDbDdjhDZxWc
UhPo3SPkoyGRwmvVmEcLYWfvqbKamO+LIDC/FmYli6d2lgjitRo8ql2zgpGFgUmm
GyamQArArRDRN6PxC4g/dtpNjyns72QnqY9/m4Vy+1EK+tAztNxF/bQpJXLixhEJ
7sJiFzy5iAsVl4IpoxbdpIxN5OC/SOiO55G7irwvEevnbGk2Nj18QlSSv9sLA+9T
UsZQz12po/ZFJJCNI7ZhkZ73+VP5VtcZ1oW1DwIDAQABAoIBAQCX/87CPkGwN7ms
SCJpE3uRIrbVYrjQi7HgaQyj8sVRA6/BEiC+ZUxMkJN0GzL/Yss7gsMwgLl/I9us
qz2HKC30EU+hi5ukSlUCn6sObuC5Ag04T1cfACtTbn8eRSC5WSHCr7i7kOPV/oGl
pmXqnaQhn6Rs5XZRGh95M7iBgrikMW7pKIZlnTnmXAjLkDjQXlEHcTVK8xb3W0xs
VRvto+RMefatkUp19tvtuTE5jZQg5PGztXK+RO1kEv2BX7qhrjY6+LdKBNjzFmDS
6mI2MTUJ1X/UFvVKsXyiPv/KJ/YvS4/dPtKjQoDxo4BsfqA4tTz/q12IK1yELcMk
19VtfQgBAoGBANGkeWzTXXNXhaM5ibQXEZhBLdxBqQ/Pk4Xh+FEIxeLZvUe8l4f6
BlS2vw2rJmfvtsEtNAGMmQW14+s0KD2L/G1w04PwQWP5MAZqx0/pgiBuXGqKdW8w
4h+M0/R8VlaBTq0asZOrkFKiYALKsfQhiJBy+X5xJqDxo+ej/qi6Z0FRAoGBAM+5
dV3etlDUR6MDgX+/YurzeJ5CKmDQttc2H2wE8zip3kIDp+ucD7z6qhg0n1I2msGG
OggoSIFpdXoGQkRQcypADAOFBsYk1q90UtCduzPkpso5Bjx98jZ4eDXB5wMRN1Ek
fZv40I3BZTtXu3KfnW9zAmzVcyS9x9GMHiHojvhfAoGBALSY1MWsG8AGMKiZI4hR
qyWXWLN6mPJ25mYacTkVrqsq2gUXcQ6Bk7ycpV9YBkDZX31wvHFtNlGWDJ8NEnFa
y31YCc6KRTqjavzMNaEgzqmziMd7OYks+k8lmV3vUs04nZc//KPy0uRs3vrotH5T
+Po/IbEMNrPFFmaxfurJkbPRAoGBAIWfeZ5u27zXMVXttWomBU26XQcA7R3mZRe/
2yqzbHow26Z/j4+CjqU0YiK8Bxjtw1NmMwJ4V1vYKRfb2tjzH4I4PQIumpLvs6Ke
I3/LV1ckaR6A3EAhjKP5juqV1zMj6f+qh5rDzfTCSYqI/y3W+4Fr7E1yaWVjJ5zm
k6OgZAflAoGAQMUhk6wbay8e6Ppvqi9RCYOxJowTw3EKBQ4ZhTMpFCkNdR7/ktYT
d+C7K5joOyaGDy4fwpCdKZ2b16166BoGLmSQh0KQnRmq9fUrFFknK56W99/j5M6O
zfb6gh84GwkALsU8oTWqU37Ol/7mt11f05l/OruQbuzG0stjXIPK7Q8=
-----END RSA PRIVATE KEY-----"""


def unpack_user_jwt():
    """Decodes and returns the auth jwt from the request if any"""
    current_user = None
    try:
        if request.headers.get("Authorization"):
            token = request.headers.get("Authorization").split("Bearer ")[1]
            current_user = jwt.decode(token, algorithms=["RS256"], verify=False)
    except Exception:
        pass
    return current_user


def get_private_key():
    """
    Returns a development public key which matches the public key from get_public_key
    This can be overridden by `PRIVATE_KEY` in config.
    This key is used for creating JWT's
    """
    private_key = config.get("PRIVATE_KEY")
    if not private_key:
        return DEVELOPMENT_PRIVATE_KEY

    return private_key


def get_public_key():
    """
    Returns a development public key which matches the private key from get_private_key
    This can be overridden by `PUBLIC_KEY` in config.
    """
    public_key = config.get("PUBLIC_KEY")
    if not public_key:
        return DEVELOPMENT_PUBLIC_KEY

    return public_key


DEFAULT_USERNAME = "LocalUser"
DEFAULT_CLIENTID = "local-client"
DEFAULT_TOKEN_TYPE = "Bearer"
DEFAULT_EXPIRATION = 5


def create_development_jwt_token(
    user_name=DEFAULT_USERNAME,
    client_id=DEFAULT_CLIENTID,
    token_type=DEFAULT_TOKEN_TYPE,
    expires_in_minutes=DEFAULT_EXPIRATION,
    roles=None,
):
    """Generates a JWT for use in local development using the development private key embedded in the library.
    This can be called:
    'python -c "from platkit.auth import create_development_jwt_token; print(create_development_jwt_token())"'
    """
    if not roles:
        roles = []
    roles.append("uma_authorization")
    if token_type == "Offline":
        roles.append("offline_access")

    payload = create_token(user_name, client_id, token_type, roles, expires_in_minutes)
    payload["email"] = user_name

    token = encode_token(payload)

    return token


def create_token(
    user_name=DEFAULT_USERNAME,
    client_id=DEFAULT_CLIENTID,
    token_type=DEFAULT_TOKEN_TYPE,
    roles=None,
    expires_in_minutes=DEFAULT_EXPIRATION,
):
    exp = 0
    if expires_in_minutes:
        exp = int((time.time())) + expires_in_minutes * 60

    payload = {
        "exp": int(time.time()) + exp,
        "iat": int(time.time()),
        "iss": "http://localhost:8080/devauth/",
        "aud": client_id,
        "typ": token_type,
        "azp": client_id,
        "roles": roles,
        "realm_access": {"roles": roles},
        "allowed-origins": ["http://localhost:8080"],
    }

    if user_name is not None:
        payload.update({"name": user_name, "preferred_username": user_name})

    return payload


def encode_token(payload):
    algorithm = "RS256"
    private_key = get_private_key()
    token = jwt.encode(payload, private_key, algorithm=algorithm).decode("utf-8")

    return token


def validate_self_issued_jwt(token):
    # verify that the private key matches our public key
    try:
        jwt.decode(
            token,
            get_public_key(),
            algorithms=["RS256"],
            verify=True,
            options={"verify_exp": False, "verify_aud": False},
        )
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Could not decode token: %s" % repr(e))


def get_auth_payload(user_name, client_id="api-key-client", roles=None):
    """Create a valid token and put into authentication payload similar to OpenID connect payloads.
    """
    access_token = create_development_jwt_token(user_name, client_id, "Bearer", 5 * 60, roles)
    refresh_token = create_development_jwt_token(None, client_id, "Offline", 0, roles)

    auth_payload = {"access_token": access_token, "refresh_token": refresh_token}

    return auth_payload


def get_auth_payload_from_refresh_token(user_name, refresh_token):
    """Generates token pairs from a refresh token, for development
    """
    try:
        payload = jwt.decode(refresh_token.encode("UTF-8"), verify=False)
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, message="Refresh token is invalid: %s" % repr(e))
    access_token = create_development_jwt_token(user_name, payload["aud"], "Bearer", 5 * 60)

    auth_payload = {"access_token": access_token, "refresh_token": refresh_token}

    return auth_payload


def get_token_username(jwt_contents):
    if "email" in jwt_contents:
        return jwt_contents["email"]
    elif "preferred_username" in jwt_contents:
        return jwt_contents["preferred_username"]
    else:
        log.error("User does not have an email field in their JWT Token.")
        abort(HTTPStatus.BAD_REQUEST, message="Token is invalid")


def get_token_roles(jwt_contents):
    roles = []
    if "roles" in jwt_contents:
        roles = jwt_contents["roles"]
    elif "realm_access" in jwt_contents:
        roles = jwt_contents["realm_access"].get("roles") or []
    return roles


def get_token_global_roles(jwt_contents):
    roles = get_token_roles(jwt_contents)
    return [r for r in roles if "##" not in r]


def get_token_context_roles(jwt_contents):
    roles = get_token_roles(jwt_contents)
    ret = {}
    for r in roles:
        lst = r.split("##")
        if len(lst) == 2:
            ret[lst[0]] = lst[1]

    return ret


def verify_token(app, token):
    """
    Verify that a token is valid.
    """
    # jwt.decode variables
    config = Config()
    data_secure = {}
    public_key = get_public_key()

    if not token:
        if config.get("DEBUG") and config.get("SKIPAUTH"):
            data_secure = {
                "preferred_username": DUMMY_USER,
                "email": "{dummy}@{dummy}.com".format(dummy=DUMMY_USER),
            }
            return data_secure
        else:
            auth_header = request.headers.get("Authorization")
            if auth_header and not auth_header.lower().startswith("bearer "):
                abort(
                    HTTPStatus.UNAUTHORIZED,
                    message="Invalid Authorization header. It should start with 'Bearer '",
                )
            abort(HTTPStatus.UNAUTHORIZED, message="please log-in")

    if not data_secure:

        try:
            # This manipulation is to test the integrity of the token.
            # ! this payload is insecure and will not be used outside of this test
            data_unsecure = jwt.decode(token, algorithms=["RS256"], verify=False)
            aud = data_unsecure.get("aud")
        except jwt.InvalidTokenError:
            abort(HTTPStatus.UNAUTHORIZED, message="Token is indecipherable")

        try:
            # Token verification with public key - secure
            data_secure = jwt.decode(token, public_key, algorithms=["RS256"], verify=True, audience=aud)
        except jwt.ExpiredSignatureError:
            abort(HTTPStatus.UNAUTHORIZED, message="Token has expired. Please re-authenticate.")
        except jwt.InvalidTokenError as kex:
            if "Signature verification failed" in str(kex):
                log.error(
                    "In all likelyhood we have a wrong public key for keycloak server "
                    "or the user is using a token for another keycloak server. "
                    "Our public key is:\n%s\nToken contains:\n%s",
                    public_key,
                    data_unsecure,
                )
            # the most likely reason we end up here is an incorrect public key
            # but we might also have a wrong realm so we send the information to the client
            # so that they can debug the issue.
            issuer = data_unsecure["iss"]
            expected_issuer = config.get("TOKEN_ISSUER")
            abort(
                HTTPStatus.UNAUTHORIZED,
                message=str(kex),
                issuer=issuer,
                expected_issuer=expected_issuer,
                public_key=public_key,
            )

    if not data_secure.get("email"):
        abort(HTTPStatus.UNAUTHORIZED, message="Token is invalid - missing fields")

    return data_secure


def requires_roles(_roles):
    """
        endpoint decorator to lock down an endpoint
        on a set of roles (comma delimitered)
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not _roles or (config.get("DEBUG") and config.get("SKIPAUTH")):
                return fn(*args, **kwargs)
            current_user = g.user
            if not current_user:
                abort(
                    HTTPStatus.UNAUTHORIZED,
                    message="You need to be logged in to access this resource",
                )
            if not isinstance(current_user, dict):
                current_user = current_user.__dict__
            required_roles = set(_roles.split(","))
            user_roles = set(current_user["roles"] or [])
            if not required_roles.intersection(user_roles):
                if not current_app.debug:
                    log.warning(
                        "User does not have the needed roles for this "
                        "call. User roles = '%s', Required roles = "
                        "'%s'. current_user = '%s'",
                        current_user["roles"],
                        _roles,
                        current_user,
                    )
                abort(
                    HTTPStatus.UNAUTHORIZED,
                    message="You do not have access to this resource. It requires role '%s'"
                    % _roles,
                )

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def ensure_user_exists(session, user_name, model):
    """
    Create a user in the database and return the user_id integer
    """
    user = session.query(model).filter(model.user_name.ilike(user_name)).first()
    if not user:
        user = model(user_name=user_name)
        session.add(user)
        session.commit()
    return user.user_id


# cache users in memory to save on db access
users = {}


def get_user_from_token(app, session, token, model=None):
    """
    Returns a dictionary containing user information from JWT
    along with a user_id from the database (if model is specified).
    Caches the user_name->user_id mapping in memory to minimize db access
    """
    jwt_contents = verify_token(app, token)
    if not jwt_contents:
        return None
    user_name = get_token_username(jwt_contents)
    roles = get_token_global_roles(jwt_contents)

    # keep the user_id in memory to save on the db dip
    if user_name not in users:
        user_id = None
        if model:
            user_id = ensure_user_exists(session, user_name, model)
        users[user_name] = user_id
    else:
        user_id = users[user_name]

    roles = get_token_global_roles(jwt_contents)
    admin_role = app.config.get("ADMIN_ROLE")
    is_admin = False
    if admin_role:
        is_admin = admin_role in roles
    ret = {
        "user_name": get_token_username(jwt_contents),
        "user_id": user_id,
        "roles": roles,
        "projects": get_token_context_roles(jwt_contents),
        "admin": is_admin,
    }
    return ret
