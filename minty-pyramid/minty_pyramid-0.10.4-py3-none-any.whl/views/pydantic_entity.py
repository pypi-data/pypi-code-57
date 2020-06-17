import logging
import re
from minty_pyramid.session_manager import (
    check_user_permission,
    get_logged_in_user,
)
from pyramid.httpexceptions import HTTPForbidden

log = logging.getLogger(__name__)


# This will be moved to minty-pyramid in a next iteration
class JSONAPIEntityView:
    """View Base class for Pyramid Views which return Entity objects

    Use this as a base class for your own view. E.g.

        class DogView(JSONAPIEntityView):
            view_mapper = {
                "GET": {
                    "get_dog": {
                        "cq": "query",
                        "auth_permissions": ["gebruiker"],
                        "domain": "zsnl_domains.case_management",
                        "run": "get_dog_by_uuid",
                        "from": {"request_params": {"uuid": "uuid"}},
                    },
                    "filter_dogs": {
                        "cq": "query",
                        "auth_permissions": ["gebruiker"],
                        "domain": "zsnl_domains.case_management",
                        "run": "get_dog_by_uuid",
                        "from": {"request_params": {"filter[]": "filter_params"}},
                    }
                },
                "POST": {
                    "create_dog": {
                        "cq": "command",
                        "auth_permissions": ["gebruiker"],
                        "domain": "zsnl_domains.case_management",
                        "run": "create_dog",
                        "from": {
                            "request_params": {"uuid": "uuid"},
                            "json": {"_all": True},
                        },
                        "command_primary": "uuid",
                        "entity_type": "dog",
                    }
                }
            }

            def create_link_from_entity(
                self, entity=None, entity_type=None, entity_id=None
            ):
                if entity is not None:
                    entity_type = entity.entity_type
                    entity_id = str(entity.entity_id)

                if entity_type == "dog":
                    return self.request.route_url(
                        "get_dog_object", _query={"uuid": entity_id}, _scheme="https"
                    )

    The view_mappers has as it's first key the method of the API call, e.g.
    POST or GET. Define the action in the url as the first key of the following
    dict (get_dog, create_dog) in the above example.

    Other parameters:
        cq (Enum("query", "command")):  Defines whether to call on the Query or
                                        Command class
        auth_permissions (List[str]): The list of permissions to check
        domain (str): The domain to run this command or query against
        run (str): the command or query to run
        from (dict): A dict of parameters, see below
        command_primary (str):  The "reference" of the command extracted from
                                the given "parameter
        entity_type (str):  The string entity_type, so we know when we got no
                            Entity as a return value, which type to set

    The "from" parameter extracts input parameters from either the given
    "request_parameters" or the "json_body" of the request. The following
    dict contains a key value pair. The key correspondents to the key from the
    input. The value correspondents to the key for the command to run.

    Using array[] options in request_params:
    When a key of a request_params ends with the characters [] (e.g.: see
    filter_dogs above), then it will transform the variables into a dict.

    For instance: ?filter[name]=frits&filter[gender]=male
    Will transform into:
        {
            "name": "frits",
            "gender": "male"
        }

    """

    def __init__(self, context, request):
        """Initializes this object from Pyramid"""

        self.request = request
        self.call = request.matched_route.name

    def _check_protected_route(self, calldata):
        """Verifies authentication permissions against our session"""

        user_info = get_logged_in_user(self.request, log)
        if not check_user_permission(calldata["auth_permissions"], user_info):
            raise HTTPForbidden(
                json={"error": "You do not have permission to access this."}
            )

        return user_info

    def _get_cqrs_instance(self, calldata, user_info):
        """Gets the command or query instance for the called api view"""
        cq = calldata["cq"]

        cmdqry = getattr(self.request, f"get_{cq}_instance")
        return cmdqry(
            domain=calldata["domain"],
            user_info=user_info,
            user_uuid=user_info.user_uuid,
        )

    def __call__(self):
        """Reads and runs the called API route defined in view_mapper"""

        calldata = self.view_mapper[self.request.method][self.call]

        user_info = self._check_protected_route(calldata)
        cqinstance = self._get_cqrs_instance(calldata, user_info)

        run = getattr(cqinstance, calldata["run"])
        params = self._collect_params(calldata)

        response = None
        if "wrapper" in calldata:
            wrapper = getattr(self, calldata["wrapper"])
            response = wrapper(run, params)
        else:
            response = run(**params)

        return self.transform_response_from_command_or_query(
            response, calldata, params
        )

    def transform_response_from_command_or_query(
        self, response, calldata, params
    ):
        """Transforms a response from a command to a proper JSONApi structure

        Args:
            response (Optional[Entity]): The response from our query or command
            calldata (dict): The configuration defined in our view_mapper
            params (dict): The collected parameters from our query and jsonbody

        Returns:
            Structured dict for our jsonapi serializer:

                {
                    "data": {
                        "links": {
                            "self": "http://url",
                        },
                        "type": "name_of_entity",
                        "id": "12434-abcde-1234-acbewe-233aba"
                    }
                }

        """
        if calldata["cq"] == "command":
            try:
                if (
                    calldata["command_primary"]
                    and params[calldata["command_primary"]]
                ):
                    return {
                        "data": {
                            "links": {
                                "self": self.create_link_from_entity(
                                    entity_type=calldata["entity_type"],
                                    entity_id=params[
                                        calldata["command_primary"]
                                    ],
                                )
                            },
                            "type": calldata["entity_type"],
                            "id": params[calldata["command_primary"]],
                        }
                    }
            except KeyError:
                return {"data": None}

        if calldata["cq"] == "query":
            if response:
                return {
                    "data": response,
                    "links": {"self": self.request.current_route_path()},
                }
            else:
                return {"data": None}

    def _collect_params_as_array(self, k, v, params):
        for pk, pv in self.request.params.items():
            match = re.search(k + r"\[(.+)\]", pk)

            if match:
                if k not in params:
                    params[v] = {}

                params[v][match[1]] = pv

    def _collect_params(self, calldata):
        """Collects parameters according to the configuration in view_mapper"""
        params = {}

        if "request_params" in calldata["from"]:
            for k, v in calldata["from"]["request_params"].items():
                # Special array functionality
                if k.endswith("[]"):
                    k = k.replace("[]", "")
                    self._collect_params_as_array(k, v, params)

                    continue

                if k not in self.request.params:
                    continue

                params[v] = self.request.params[k]

        if "json" in calldata["from"]:
            if (
                "_all" in calldata["from"]["json"]
                and calldata["from"]["json"]["_all"] is True
            ):
                for k in self.request.json_body.keys():
                    params[k] = self.request.json_body[k]
            else:
                for k, v in calldata["from"]["json"].items():
                    if k not in self.request.json_body:
                        continue
                    params[v] = self.request.json_body[k]

        return params
