"""Used by the backend and CLI.
Placed in frontend/cli/anyscale package to be in the PYTHONPATH when
autoscaler searches for the module.
"""
import logging
import queue
import subprocess
import time
from typing import Any, Dict, List, Optional
import uuid

import ray
from ray.autoscaler.node_provider import NodeProvider
from ray.autoscaler.updater import (
    HASH_MAX_LENGTH,
    NODE_START_WAIT_S,
    SSHCommandRunner,
    with_interactive,
)

logger = logging.getLogger(__name__)
RequestID = str
GatewayRequest = Dict[str, Any]
GatewayResponse = Dict[str, Any]


class ServerNodeProvider(NodeProvider):  # type: ignore
    """Interface for getting and returning nodes from a Cloud gateway.

    Servers are namespaced by the `cluster_name` parameter,
    and operate on nodes within that namespace.

    Unlike standard NodeProviders, the functionality of ServerNodeProvider relies on HTTP requests
    and responses from the Cloud gateway.
    """

    def __init__(self, provider_config: Dict[Any, Any], cluster_name: str):
        NodeProvider.__init__(self, provider_config, cluster_name)
        self.provider_config = provider_config
        self.cluster_name = cluster_name

    def get_response(self, request: GatewayRequest) -> Any:
        request["request_id"] = str(uuid.uuid4())
        ray_actor_handler = ray.util.get_actor("GatewayRouterActor")
        ray.get(ray_actor_handler.push_request.remote(request))
        # TODO(ameer): make this a long-running async method call
        while not ray.get(ray_actor_handler.response_is_ready.remote(request)):
            time.sleep(0.1)
        response = ray.get(ray_actor_handler.pull_response.remote(request))
        return response["data"]

    def non_terminated_nodes(self, tag_filters: Dict[Any, Any]) -> Any:
        request = {"type": "non_terminated_nodes", "args": (tag_filters,)}
        return self.get_response(request)

    def is_running(self, node_id: str) -> Any:
        request = {"type": "is_running", "args": (node_id,)}
        return self.get_response(request)

    def is_terminated(self, node_id: str) -> Any:
        request = {"type": "is_terminated", "args": (node_id,)}
        return self.get_response(request)

    def node_tags(self, node_id: str) -> Any:
        request = {"type": "node_tags", "args": (node_id,)}
        return self.get_response(request)

    def external_ip(self, node_id: str) -> Any:
        request = {"type": "external_ip", "args": (node_id,)}
        response = self.get_response(request)
        return response

    def internal_ip(self, node_id: str) -> Any:
        request = {"type": "internal_ip", "args": (node_id,)}
        response = self.get_response(request)
        return response

    def create_node(
        self, node_config: Dict[Any, Any], tags: Dict[Any, Any], count: int
    ) -> None:
        request = {"type": "create_node", "args": (node_config, tags, count)}
        self.get_response(request)

    def set_node_tags(self, node_id: str, tags: Dict[Any, Any]) -> None:
        request = {"type": "set_node_tags", "args": (node_id, tags)}
        self.get_response(request)

    def terminate_node(self, node_id: str) -> None:
        request = {"type": "terminate_node", "args": (node_id,)}
        self.get_response(request)

    def terminate_nodes(self, node_ids: str) -> None:
        request = {"type": "terminate_nodes", "args": (node_ids,)}
        self.get_response(request)

    def cleanup(self) -> None:
        request = {"type": "cleanup", "args": ()}
        self.get_response(request)

    def get_command_runner(
        self,
        log_prefix: str,
        node_id: str,
        auth_config: Dict[Any, Any],
        cluster_name: str,
        process_runner: Any,
        use_internal_ip: bool,
        docker_config: Any = None,
    ) -> Any:
        """Overwrites the `run` function of the original SSHCommandRunner.

        The new `run` function uses a different process runner when running `run`."""

        return GatewaySSHCommandRunner(
            log_prefix,
            node_id,
            self,
            auth_config,
            cluster_name,
            process_runner,
            use_internal_ip,
        )

    def check_output(self, cmd: List[str]) -> Any:
        """This function has to send ssh commands to the remote cloud gateway."""
        request = {"type": "check_output", "args": (cmd,)}
        response = self.get_response(request)
        if response == "subprocess.CalledProcessError":
            raise subprocess.CalledProcessError
        else:
            return response

    def check_call(self, cmd: List[str]) -> None:
        """check_call function has to send ssh commands to the remote cloud gateway."""
        request = {"type": "check_call", "args": (cmd,)}
        response = self.get_response(request)
        if response == "subprocess.CalledProcessError":
            raise subprocess.CalledProcessError


class GatewaySSHCommandRunner(SSHCommandRunner):  # type: ignore
    """Forwards the SSH commands to the gateway.

    Overwrites the run function of SSHCommandRunner, so that SSH commands are redirected to
    the gateway instead of using local subprocess."""

    def run(self, *args, **kwargs) -> Any:  # type: ignore
        process_runner = self.process_runner  # type: ignore
        self.process_runner = self.provider
        try:
            result = super().run(*args, **kwargs)
            self.process_runner = process_runner
        except subprocess.CalledProcessError:
            self.process_runner = process_runner
            raise
        return result


@ray.remote
class GatewayRouter:
    """Mediator between the cloudgateway and the server node provider.

    The server node provider enqueues requests to this named/global actor.
    FastAPI forwards these requests to the cloud gateway and stores the responses
    in the actor's hash table.
    """

    def __init__(self) -> None:
        self.request_queue: queue.Queue[GatewayRequest] = queue.Queue()
        self.response_hash_table: Dict[RequestID, GatewayResponse] = {}

    def push_response(self, response: GatewayResponse) -> None:
        self.response_hash_table[response["request_id"]] = response
        # TODO(ameer): assumes the gateway returns responses in order (can be improved).
        self.request_queue.get()

    def response_is_ready(self, request: GatewayRequest) -> bool:
        return request["request_id"] in self.response_hash_table

    def pull_response(self, request: GatewayRequest) -> GatewayResponse:
        response = self.response_hash_table[request["request_id"]]
        del self.response_hash_table[request["request_id"]]
        return response

    def push_request(self, request: GatewayRequest) -> None:
        self.request_queue.put(request)

    def next_request_ready(self) -> bool:
        if self.request_queue.empty():
            return False
        else:
            return True

    def get_next_request(self) -> GatewayRequest:
        # Does not remove the request until receiving the response (for fault tolerance)
        queue_top: GatewayRequest = self.request_queue.queue[0]
        return queue_top
