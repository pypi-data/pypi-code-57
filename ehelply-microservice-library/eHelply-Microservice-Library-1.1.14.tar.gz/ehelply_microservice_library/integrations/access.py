from __future__ import annotations
from ehelply_bootstrapper.integrations.integration import Integration
from ehelply_microservice_library.integrations.fact import get_fact_endpoint
from ehelply_bootstrapper.utils.state import State
from ehelply_microservice_library.utils.paginate import Page
from fastapi import HTTPException, Header, Depends
from typing import List
import requests
from pydantic import BaseModel


class TypeGet(BaseModel):
    """
    Used for get endpoint
    """
    uuid: str
    name: str
    slug: str
    summary: str
    created_at: str


class TypeGets(BaseModel):
    types: List[TypeGet]


class TypeCreate(BaseModel):
    """
    Used for create endpoint
    """
    name: str
    summary: str


class NodeCreate(BaseModel):
    """
    Used for create endpoint
    """
    name: str
    node: str
    summary: str


class NodeGet(BaseModel):
    """
    Used for get endpoint
    """
    uuid: str
    name: str
    node: str
    type_uuid: str
    summary: str
    created_at: str


class TargetGet(BaseModel):
    """
    Used for get endpoint
    """
    uuid: str
    type_uuid: str
    target_uuid: str


class RoleCreate(BaseModel):
    """
    Used for create endpoint
    """
    name: str
    summary: str
    description: str


class Role(RoleCreate):
    """
    Used for creating Roles
    """
    nodes: List[str]


class GroupCreate(BaseModel):
    name: str
    summary: str
    default: bool = False


class Auth:
    def __init__(self, access=None, entity_uuid=None, entity_type="user", group_uuid=None, access_token=None,
                 secret_token=None) -> None:
        self.access = access
        self.entity_uuid = entity_uuid
        self.entity_type = entity_type
        self.group_uuid = group_uuid
        self.access_token = access_token
        self.secret_token = secret_token


class Access(Integration):
    """
    Note integration is used to talk to the ehelply-notes microservice
    """

    def __init__(self, name: str, summary: str, nodes: List[NodeCreate]) -> None:
        super().__init__("access")
        self.type_name = name
        self.summary = summary
        self.nodes = nodes
        self.access_type: TypeGet = None
        self.m2m = State.integrations.get("m2m")

    def get_base_url(self) -> str:
        return get_fact_endpoint('ehelply-access')

    def init(self):
        super().init()

    def load(self):
        """
        Precreates nodes and the access type
        :return:
        """
        try:
            # Ensures we have a database setup of all the nodes we need
            access_type: list = self.search_types(self.type_name).items

            if len(access_type) < 1:
                self.create_type(TypeCreate(name=self.type_name, summary=self.summary))
                access_type: list = self.search_types(self.type_name).items

            self.access_type: TypeGet = access_type[0]

            for node in self.nodes:
                self.create_node(type_uuid=self.access_type.uuid, node=node)
        except:
            State.logger.warning("Unable to get access type and create nodes. This is probably bad unless this is the ehelply-access microservice.")

    def search_types(self, name: str) -> Page:
        """
        Search access types
        :param name:
        :return:
        """
        # response = self.m2m.requests.get(self.get_base_url() + "/types", params={"name": name})
        #
        # return TypeGets(types=response.json()['items'])

        return self.m2m.search(self.get_base_url() + "/types", item_model=TypeGet, params={"name": name})

    def create_type(self, access_type: TypeCreate):
        """
        Create access type
        :param access_type:
        :return:
        """
        response = self.m2m.requests.post(self.get_base_url() + "/types", json={"type": access_type.dict()})

        return response.json()

    def create_target(self, target_uuid: str) -> str:
        """
        Create target
        A target is an instance of some access type
        :param target_uuid:
        :return:
        """
        payload: dict = {
            "target": {
                "target_uuid": target_uuid
            }
        }
        return self.m2m.requests.post(self.get_base_url() + "/types/" + self.access_type.uuid + "/targets", json=payload).json()[
            'uuid']

    def search_targets(self, type_uuid: str, target_uuid: str) -> Page:
        """
        Search targets
        :param type_uuid:
        :param target_uuid:
        :return:
        """
        # response = self.m2m.requests.get(self.get_base_url() + "/types/" + type_uuid + "/targets",
        #                         params={"target_uuid": target_uuid})
        #
        # return response.json()['items']

        return self.m2m.search(self.get_base_url() + "/types/" + type_uuid + "/targets", params={"target_uuid": target_uuid})

    def create_node(self, type_uuid: str, node: NodeCreate):
        """
        Create a new permission node
        :param type_uuid:
        :param node:
        :return:
        """
        response = self.m2m.requests.post(self.get_base_url() + "/types/" + type_uuid + "/nodes", json={"node": node.dict()})

        return response.json()

    def create_group(self, group: GroupCreate) -> str:
        """
        Create a group
        :param group:
        :return:
        """
        payload: dict = {
            "group": group.dict()
        }

        return self.m2m.requests.post(self.get_base_url() + "/groups", json=payload).json()['uuid']

    def attach_entity_group(self, entity_uuid: str, group_uuid: str, entity_type: str = "user"):
        """
        Attach an entity to a group
        :param entity_uuid:
        :param group_uuid:
        :param entity_type:
        :return:
        """
        self.m2m.requests.post(self.get_base_url() + "/groups/" + group_uuid + "/entities/" + entity_uuid,
                      params={"entity_type": entity_type})

    def create_role(self, role: Role) -> str:
        """
        Create a role and attach permission nodes to it
        :param role:
        :return:
        """
        payload: dict = {
            "role": {
                "name": role.name,
                "summary": role.summary,
                "description": role.description
            }
        }
        response = self.m2m.requests.post(self.get_base_url() + "/roles", json=payload)

        role_uuid: str = response.json()['uuid']

        for node in role.nodes:
            response = self.m2m.requests.get(self.get_base_url() + "/types/" + self.access_type.uuid + "/nodes",
                                    params={"node": node}).json()
            if len(response) < 1:
                continue

            response = self.m2m.requests.post(self.get_base_url() + "/roles/" + role_uuid + "/nodes/" + response[0]['uuid'])

        return role_uuid

    def attach_role_group_target(self, role_uuid: str, group_uuid: str, target_uuid: str):
        """
        Attach a group to a target with a role
        :param role_uuid:
        :param group_uuid:
        :param target_uuid:
        :return:
        """
        self.m2m.requests.post(self.get_base_url() + "/roles/" + role_uuid + "/groups/" + group_uuid + "/targets/" + target_uuid)

    def create_role_group_target(self, role: Role, group: GroupCreate, target_uuid: str, entity_uuid: str = None,
                                 entity_type: str = "user"):
        """
        Automates the process of creating a new role, attaching nodes to the role, creating a new group,
          adding an entity to the group, creating a new target,
          and then attaching the created group to the created target with the created role
        :param role:
        :param group:
        :param target_uuid:
        :param entity_uuid:
        :param entity_type:
        :return:
        """
        role_uuid: str = self.create_role(role=role)

        group_uuid: str = self.create_group(group=group)

        if entity_uuid and not group.default:
            self.attach_entity_group(entity_uuid=entity_uuid, group_uuid=group_uuid, entity_type=entity_type)

        target_uuid: str = self.create_target(target_uuid=target_uuid)

        self.attach_role_group_target(role_uuid=role_uuid, group_uuid=group_uuid, target_uuid=target_uuid)

        return {
            "role_uuid": role_uuid,
            "group_uuid": group_uuid,
            "target_uuid": target_uuid
        }

    def entity_has_node(self, entity_uuid: str, target_uuid: str, node: str, entity_type: str = "user"):
        """
        Determines whether an entity has a permission node
        :param entity_uuid:
        :param target_uuid:
        :param node:
        :param entity_type:
        :return:
        """
        response = self.m2m.requests.get(
            self.get_base_url() + "/entities/" + entity_uuid + "/targets/" + target_uuid + "/nodes/" + node,
            params={"entity_type": entity_type})

        if response.json() is True and response.status_code == 200:
            return True

        return False

    def group_has_node(self, group_uuid: str, target_uuid: str, node: str):
        """
        Determines whether a group has a permission node
        :param group_uuid:
        :param target_uuid:
        :param node:
        :return:
        """
        response = self.m2m.requests.get(
            self.get_base_url() + "/groups/" + group_uuid + "/targets/" + target_uuid + "/nodes/" + node)

        if response.json() is True and response.status_code == 200:
            return True

        return False

    def key_has_node(self, access: str, secret: str, target_uuid: str, node: str):
        """
        Determines whether a key has a permission node
        :param access:
        :param secret:
        :param target_uuid:
        :param node:
        :return:
        """
        headers: dict = {
            "X-Access-Token": access,
            "X-Secret-Token": secret
        }
        response = self.m2m.requests.get(
            self.get_base_url() + "/keys/targets/" + target_uuid + "/nodes/" + node, headers=headers)

        if response.json() is True and response.status_code == 200:
            return True

        return False


"""
Access Check
"""


def u_access(access: Access, entity_uuid: str, target_uuid: str, node: str, entity_type: str = "user",
             exception_if_unauthorized=True) -> bool:
    """
    User Access (Really it's Entity Access though)
    Authorizes that a user has access to a permission node on a target
    :param access:
    :param entity_uuid:
    :param target_uuid:
    :param node:
    :param entity_type:
    :param exception_if_unauthorized:
    :return:
    """
    try:
        result = access.search_targets(type_uuid=access.access_type.uuid, target_uuid=target_uuid).items[0]
        target: TargetGet = TargetGet(**result)

        if access.entity_has_node(entity_uuid=entity_uuid, target_uuid=target.uuid, node=node,
                                  entity_type=entity_type):
            return True

    except:
        pass

    if exception_if_unauthorized:
        raise HTTPException(status_code=403, detail="Unauthorized")
    else:
        return False


def g_access(access: Access, group_uuid: str, target_uuid: str, node: str, exception_if_unauthorized=True) -> bool:
    """
    Group Access
    Authorizes that a group has access to a permission node on a target
    :param access:
    :param group_uuid:
    :param target_uuid:
    :param node:
    :param exception_if_unauthorized:
    :return:
    """
    try:
        result = access.search_targets(type_uuid=access.access_type.uuid, target_uuid=target_uuid).items[0]
        target: TargetGet = TargetGet(**result)

        if access.group_has_node(group_uuid=group_uuid, target_uuid=target.uuid, node=node):
            return True

    except:
        pass

    if exception_if_unauthorized:
        raise HTTPException(status_code=403, detail="Unauthorized")
    else:
        return False


def k_access(access: Access, access_token: str, secret_token: str, target_uuid: str, node: str,
             exception_if_unauthorized=True) -> bool:
    """
    Key Access
    Authorizes that a key has access to a permission node on a target
    :param access:
    :param access_token:
    :param secret_token:
    :param target_uuid:
    :param node:
    :param exception_if_unauthorized:
    :return:
    """
    try:
        result = access.search_targets(type_uuid=access.access_type.uuid, target_uuid=target_uuid).items[0]
        target: TargetGet = TargetGet(**result)

        if access.key_has_node(access=access_token, secret=secret_token, target_uuid=target.uuid, node=node):
            return True

    except:
        pass

    if exception_if_unauthorized:
        raise HTTPException(status_code=403, detail="Unauthorized")
    else:
        return False


def a_access(access: Access, target_uuid: str, node: str, entity_uuid: str = None, entity_type: str = "user",
             group_uuid: str = None, access_token: str = None, secret_token: str = None, auth: Auth = None,
             exception_if_unauthorized=True) -> bool:
    """
    Any Access
    Authorizes that a user, group, or key has access to a permission node on a target.
    Passes authorization if at least one of the provided schemes is authorized.
    This acts as an OR not as an AND
    :param access:
    :param target_uuid:
    :param node:
    :param entity_uuid:
    :param entity_type:
    :param group_uuid:
    :param access_token:
    :param secret_token:
    :param exception_if_unauthorized:
    :return:
    """
    if auth:
        entity_uuid = auth.entity_uuid
        entity_type = auth.entity_type
        group_uuid = auth.group_uuid
        access_token = auth.access_token
        secret_token = auth.secret_token

    if entity_uuid:
        try:
            u_access(access, entity_uuid=entity_uuid, target_uuid=target_uuid, node=node, entity_type=entity_type)
            return True
        except:
            pass

    if group_uuid:
        try:
            g_access(access, group_uuid=group_uuid, target_uuid=target_uuid, node=node)
            return True
        except:
            pass

    if access_token and secret_token:
        try:
            k_access(access, access_token=access_token, secret_token=secret_token, target_uuid=target_uuid, node=node)
            return True
        except:
            pass

    if exception_if_unauthorized:
        raise HTTPException(status_code=403, detail="Unauthorized")
    else:
        return False
