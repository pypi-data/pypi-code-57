from http.client import RemoteDisconnected
import json
import logging
from shlex import quote
import subprocess
import threading
import time
from typing import Any, Dict, Tuple

from ray.autoscaler.autoscaler import validate_config
from ray.autoscaler.node_provider import get_node_provider, NODE_PROVIDERS, NodeProvider
import yaml

from anyscale.util import send_json_request

logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    logger.exception(
        "Couldn't import `requests` library. Try installing it with `pip install requests`."
    )


class CloudGatewayRunner:
    def __init__(
        self,
        cluster_name: str,
        autoscaler_config: str,
        anyscale_address: str = "/cloudgateway",
    ) -> None:
        self.cluster_name = cluster_name
        self.autoscaler_config = autoscaler_config
        self.anyscale_address = anyscale_address
        self.node_provider, self.config = self.get_provider_with_config(
            self.cluster_name, self.autoscaler_config
        )

    def get_provider_with_config(
        self, cluster_name: str, path_to_yaml: str
    ) -> Tuple[NodeProvider, Any]:
        """Receives the path_to_yaml and returns the node provider and resolved configs."""
        with open(path_to_yaml) as f:
            config = yaml.safe_load(f)
            validate_config(config)
            node_provider = get_node_provider(config["provider"], cluster_name)
            try:
                importer = NODE_PROVIDERS.get(config["provider"]["type"])
            except NotImplementedError:
                raise NotImplementedError(
                    "Unsupported provider {}".format(config["provider"])
                )
            bootstrap_config, _ = importer()
            if bootstrap_config:
                resolved_config = bootstrap_config(config)
            else:
                resolved_config = config
        return node_provider, resolved_config

    def get_node_config_from_external_tags(
        self, config: Dict[Any, Any], tags: Dict[Any, Any]
    ) -> Any:
        """Get the configs of the head_node/worker_nodes.

        Uses external node provider's tags to index into the gateways's config.
        This is helpful when the server does not know the default configs of the
        remote cluster like SubnetIDs.
        """

        if tags["ray-node-type"] == "head":
            return config["head_node"]
        else:
            return config["worker_nodes"]

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Receives the request and processes it."""
        if request["type"] == "cleanup":
            response = getattr(self.node_provider, request["type"])()
        elif request["type"] == "create_node":
            _, tags, count = request["args"]
            node_config = self.get_node_config_from_external_tags(self.config, tags)
            response = getattr(self.node_provider, request["type"])(
                node_config, tags, count
            )
        elif request["type"] == "check_call" or request["type"] == "check_output":
            cmd = request["args"][0]
            try:
                response = getattr(subprocess, request["type"])(cmd)
            except subprocess.CalledProcessError:
                quoted_cmd = " ".join(cmd[:-1] + [quote(cmd[-1])])
                logger.error("Command failed: \n\n  {}\n".format(quoted_cmd))
                response = "subprocess.CalledProcessError"
        else:
            response = getattr(self.node_provider, request["type"])(*request["args"])

        response_message = {"data": response}
        return response_message

    def gateway_run_forever(self) -> None:
        """Long polls anyscale server with infinite timeout."""
        thread = threading.Thread(target=self._run, args=())
        thread.daemon = True
        thread.start()

    def _run(self) -> None:
        response_message = {"data": "first_message"}
        while 1:
            try:
                # TODO(ameerh): long poll instead.
                request = send_json_request(
                    self.anyscale_address, response_message, method="GET",
                )
            except (RemoteDisconnected, requests.exceptions.ConnectionError):
                response_message = {"data": "first_message"}
                time.sleep(0.1)
                continue
            logger.info("received request " + str(request))
            response_message = self.process_request(request)
