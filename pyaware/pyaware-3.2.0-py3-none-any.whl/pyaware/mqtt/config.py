import datetime
import os
from dataclasses import dataclass, field
import logging
import jwt

import pyaware.config
import pyaware.mqtt

log = logging.getLogger(__name__)


class MQTTConfigBase:
    """
    Used to store the cloud configuration information as well as keep jwt tokens fresh
    """
    authentication_required: bool
    client_id: str
    host: str
    port: str
    keepalive: int
    bind_address: str
    clean_session: bool
    private_key_path: str
    ca_certs_path: str
    ssl_algorithm: str
    _private_key: str
    _token: str
    token_exp: datetime.datetime
    parsers: dict
    subscribe_qos: int
    publish_qos: int
    token_life: int

    @property
    def private_key(self):
        if not self._private_key:
            try:
                with open(self.private_key_path, 'r') as f:
                    self._private_key = f.read()
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    "Could not find the ssl private key file as specified in the cloud config") from e
        return self._private_key

    @property
    def jwt_token(self):
        if datetime.datetime.utcnow() > self.token_exp - datetime.timedelta(minutes=1):
            self._create_jwt()
        return self._token

    def _create_jwt(self):
        pass


def credential_factory(cred):
    def _tmp():
        return os.path.join(pyaware.config.aware_path, "credentials", cred)

    return _tmp


def default_gcp_parsers():
    return {
        "telemetry": {
            "factory": {"name": "telemetry_v1"},
            "transforms":
                [
                    {"name": "remove_keys", "keys": {"raw_values"}}
                ],
            "model": {"name": "TelemetryV1"}
        }
    }


def default_local_parsers():
    return {
        "telemetry": {
            "factory": {"name": "telemetry_v2"},
            "transforms":
                [
                    {"name": "remove_keys", "keys": {"raw_values"}},
                ],
            "model": {"name": "TelemetryV2"}
        }
    }


@dataclass
class LocalConfig(MQTTConfigBase):
    client_id: str
    device_id: str
    authentication_required: bool = False
    host: str = "127.0.0.1"
    port: str = 1883
    keepalive: int = 60
    bind_address: str = ""
    clean_session: bool = False
    parsers: dict = field(default_factory=default_local_parsers)
    subscribe_qos: int = 1
    publish_qos: int = 0
    token_life = 0


@dataclass
class GCPCloudConfig(MQTTConfigBase):
    """
    Used to store the cloud configuration information as well as keep jwt tokens fresh
    """
    device_id: str
    project_id: str = "aware-iot"
    registry_id: str = "aware-iot"
    cloud_region: str = "asia-east1"
    host: str = "mqtt.googleapis.com"
    port: str = 8883
    keepalive: int = 60
    bind_address: str = ""
    clean_session: bool = True
    private_key_path: str = field(default_factory=credential_factory("rsa_private.pem"))
    ca_certs_path: str = field(default_factory=credential_factory("google_roots.pem"))
    ssl_algorithm: str = "RS256"
    token_life: int = 60  # In Minutes
    _private_key: str = ""
    _token: str = ""
    authentication_required: bool = True
    token_exp: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.utcnow() + datetime.timedelta(minutes=10))
    parsers: dict = field(default_factory=default_gcp_parsers)
    subscribe_qos: int = 1
    publish_qos: int = 1

    @property
    def client_id(self):
        if any(len(x) == 1 for x in [self.project_id, self.cloud_region, self.registry_id, self.device_id]):
            raise ValueError("Cannot return client id if not all parameters are set")
        return 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
            self.project_id, self.cloud_region, self.registry_id, self.device_id)

    @property
    def private_key(self):
        if not self._private_key:
            try:
                with open(self.private_key_path, 'r') as f:
                    self._private_key = f.read()
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    "Could not find the ssl private key file as specified in the cloud config") from e
        return self._private_key

    @property
    def jwt_token(self):
        self._create_jwt()
        return self._token

    def _create_jwt(self):
        log.info("Creating new jwt token")
        token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=self.token_life)
        token = {
            # The time that the token was issued at
            'iat': datetime.datetime.utcnow(),
            # The time the token expires.
            'exp': token_exp,
            # The audience field should always be set to the GCP project id.
            'aud': self.project_id
        }
        self._token = jwt.encode(token, self.private_key, algorithm=self.ssl_algorithm)
        self.token_exp = token_exp
