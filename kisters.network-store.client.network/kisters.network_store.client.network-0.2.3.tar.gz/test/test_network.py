import os
import uuid
from datetime import datetime

from kisters.network_store.model_library.base import LocationSet
from kisters.network_store.model_library.water import links, nodes
from kisters.network_store.client.network import Network
from kisters.water.rest_client import RESTClient
from kisters.water.rest_client.auth import OpenIDConnect

import pytest

test_links = [
    links.Channel(
        uid="channel",
        source_uid="junction",
        target_uid="storage",
        length=100.0,
        created="2019-06-27T16:53:05Z",
    ),
    links.Delay(
        uid="delay",
        source_uid="junction",
        target_uid="storage",
        transit_time=10.0,
        created="2019-06-27T16:53:05Z",
    ),
    links.FlowControlledStructure(
        uid="flow_controlled_structure",
        source_uid="junction",
        target_uid="storage",
        min_flow=-1.0,
        max_flow=1.0,
        created="2019-06-27T16:53:05Z",
    ),
    links.Pipe(
        uid="pipe",
        source_uid="junction",
        target_uid="storage",
        diameter=1.0,
        length=10.0,
        roughness=10.0,
        model="hazen-williams",
        created="2019-06-27T16:53:05Z",
    ),
    links.Valve(
        uid="valve",
        source_uid="junction",
        target_uid="storage",
        diameter=10.0,
        model="prv",
        coefficient=1.0,
        setting=0.0,
        created="2019-06-27T16:53:05Z",
    ),
]
test_nodes = [
    nodes.FlowBoundary(
        uid="flow_boundary",
        location={"x": 0.0, "y": 0.0, "z": 0.0},
        created="2019-06-27T16:53:05Z",
    ),
    nodes.Junction(
        uid="junction",
        location={"x": 0.0, "y": 1.0, "z": 0.0},
        created="2019-06-27T16:53:05Z",
    ),
    nodes.LevelBoundary(
        uid="level_boundary",
        location={"x": 1.0, "y": 0.0, "z": 0.0},
        created="2019-06-27T16:53:05Z",
    ),
    nodes.Storage(
        uid="storage",
        location={"x": 1.0, "y": 1.0, "z": 0.0},
        level_volume=[{"level": 0.0, "volume": 0.0}, {"level": 10.0, "volume": 10.0}],
        created="2019-06-27T16:53:05Z",
    ),
]

rest_client = RESTClient(
    url=os.environ["HYDRAULIC_NETWORK_STORE_URL"],
    authentication=OpenIDConnect(
        client_id=os.environ["HYDRAULIC_NETWORK_CLIENT_ID"],
        client_secret=os.environ["HYDRAULIC_NETWORK_CLIENT_SECRET"],
        issuer_url="https://auth.water.kisters.cloud/auth/realms/external",
    ),
)


@pytest.fixture
def empty_network():
    network_name = f"test_{str(uuid.uuid4())[:8]}"
    network = Network(network_name, rest_client, drop_existing=True)
    yield network
    network.drop(purge=True)


@pytest.fixture
def network(empty_network):
    empty_network.initialize(nodes=test_nodes, links=test_links)
    return empty_network  # no longer empty


def test_initialize(empty_network):
    empty_network.initialize(nodes=test_nodes, links=test_links)


def test_no_auth():
    unauth_client = RESTClient(url=os.environ["HYDRAULIC_NETWORK_STORE_URL"])
    with pytest.raises(Exception):
        unauth_client.get(("rest", "networks"))


def test_get_extents(network):
    extent = network.get_extent()
    assert extent.dict() == {"x": (0, 1), "y": (0, 1), "z": (0, 0)}
    schematic_extent = network.get_extent(location_set=LocationSet.SCHEMATIC)
    assert schematic_extent.dict() == {"x": (0, 1), "y": (0, 1), "z": (0, 0)}


def test_get_nodes(network):
    remote = network.get_nodes()
    remote = sorted(remote, key=lambda e: e.uid)
    assert test_nodes == remote


def test_get_links(network):
    remote = network.get_links()
    remote = sorted(remote, key=lambda e: e.uid)
    assert test_links == remote


def test_get_nodes_filtered(network):
    remote = network.get_nodes(dt=datetime(2019, 6, 27, 16, 53, 4))
    assert remote == []
    remote = network.get_nodes(dt=datetime(2019, 6, 27, 16, 53, 5))
    remote = sorted(remote, key=lambda e: e.uid)
    assert test_nodes == remote

    subset_nodes = test_nodes[:2]
    remote = network.get_nodes(uids=[e.uid for e in subset_nodes])
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == subset_nodes

    subset_nodes = test_nodes[:2]
    remote = network.get_nodes(display_names=[e.display_name for e in subset_nodes])
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == subset_nodes

    subset_node = test_nodes[0]
    remote = network.get_nodes(element_class=subset_node.element_class)
    assert remote == [subset_node]

    subset_node = test_nodes[0]
    remote = network.get_nodes(element_class=type(subset_node))
    assert remote == [subset_node]

    subset_nodes = test_nodes[:2]
    remote = network.get_nodes(extent={"x": [-0.5, 0.5]})
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == subset_nodes

    subset_nodes = test_nodes[:2]
    remote = network.get_nodes(schematic_extent={"x": [-0.5, 0.5]})
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == subset_nodes

    remote = network.get_nodes(extent={"z": [-0.5, 0.5]})
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == test_nodes

    remote = network.get_nodes(schematic_extent={"z": [-0.5, 0.5]})
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == test_nodes


def test_get_links_filtered(network):
    remote = network.get_links(dt=datetime(2019, 6, 27, 16, 53, 4))
    assert remote == []
    remote = network.get_links(dt=datetime(2019, 6, 27, 16, 53, 5))
    remote = sorted(remote, key=lambda e: e.uid)
    assert test_links == remote

    subset_links = test_links[:2]
    remote = network.get_links(uids=[e.uid for e in subset_links])
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == subset_links

    subset_links = test_links[:2]
    remote = network.get_links(display_names=[e.display_name for e in subset_links])
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == subset_links

    subset_link = test_links[0]
    remote = network.get_links(element_class=subset_link.element_class)
    assert remote == [subset_link]

    subset_link = test_links[0]
    remote = network.get_links(element_class=type(subset_link))
    assert remote == [subset_link]

    remote = network.get_links(adjacent_nodes=["junction", "storage"])
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == test_links

    remote = network.get_links(adjacent_nodes=["junction"])
    assert remote == []

    remote = network.get_links(adjacent_nodes=["junction"], only_interior=False)
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == test_links


def test_drop_nodes(network):
    network.drop_nodes([node.uid for node in test_nodes])
    nodes = network.get_nodes()
    assert nodes == []


def test_drop_links(network):
    network.drop_links([node.uid for node in test_links])
    links = network.get_links()
    assert links == []


def test_save_nodes(empty_network):
    empty_network.save_nodes(test_nodes)
    remote = empty_network.get_nodes()
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == test_nodes


def test_save_links(empty_network):
    empty_network.save_links(test_links)
    remote = empty_network.get_links()
    remote = sorted(remote, key=lambda e: e.uid)
    assert remote == test_links


def test_ValueError(network):
    with pytest.raises(ValueError):
        network.save_nodes(test_links)
    with pytest.raises(ValueError):
        network.save_links(test_nodes)


def test_drop(network):
    network.drop()
    links = network.get_links()
    assert links == []
    nodes = network.get_nodes()
    assert nodes == []
