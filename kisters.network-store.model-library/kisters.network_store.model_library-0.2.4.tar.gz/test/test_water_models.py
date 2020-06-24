from typing import Any, Dict

import pytest

from kisters.network_store.model_library.util import (
    all_links,
    all_nodes,
    element_from_dict,
    element_to_dict,
    elements_mapping,
)

elements = [
    {
        "uid": "delay",
        "created": "2020-03-04T11:02:16.790000+00:00",
        "source_uid": "junction",
        "target_uid": "storage",
        "transit_time": 10.0,
        "display_name": "delay",
        "element_class": "Delay",
        "domain": "water",
    },
    {
        "uid": "flow_controlled_structure",
        "source_uid": "junction",
        "target_uid": "storage",
        "min_flow": -1.0,
        "max_flow": 1.0,
        "display_name": "flow_controlled_structure",
        "element_class": "FlowControlledStructure",
        "domain": "water",
    },
    {
        "uid": "pipe",
        "source_uid": "junction",
        "target_uid": "storage",
        "diameter": 1.0,
        "length": 10.0,
        "roughness": 10.0,
        "model": "hazen-williams",
        "check_valve": False,
        "display_name": "pipe",
        "element_class": "Pipe",
        "domain": "water",
    },
    {
        "uid": "valve",
        "source_uid": "junction",
        "target_uid": "storage",
        "diameter": 10.0,
        "model": "prv",
        "coefficient": 1.0,
        "setting": 0.0,
        "display_name": "valve",
        "element_class": "Valve",
        "domain": "water",
    },
    {
        "uid": "flow_boundary",
        "location": {"x": 0.0, "y": 0.0, "z": 0.0},
        "display_name": "flow_boundary",
        "schematic_location": {"x": 0.0, "y": 0.0, "z": 0.0},
        "element_class": "FlowBoundary",
        "domain": "water",
    },
    {
        "uid": "junction",
        "location": {"x": 0.0, "y": 1.0, "z": 0.0},
        "display_name": "junction",
        "schematic_location": {"x": 0.0, "y": 1.0, "z": 0.0},
        "element_class": "Junction",
        "domain": "water",
    },
    {
        "uid": "level_boundary",
        "location": {"x": 1.0, "y": 0.0, "z": 0.0},
        "display_name": "level_boundary",
        "schematic_location": {"x": 1.0, "y": 0.0, "z": 0.0},
        "element_class": "LevelBoundary",
        "domain": "water",
    },
    {
        "uid": "storage",
        "location": {"x": 1.0, "y": 1.0, "z": 0.0},
        "level_volume": [
            {"level": 0.0, "volume": 0.0},
            {"level": 10.0, "volume": 10.0},
        ],
        "display_name": "storage",
        "schematic_location": {"x": 1.0, "y": 1.0, "z": 0.0},
        "element_class": "Storage",
        "domain": "water",
    },
]

bad_elements = [
    {
        "uid": "delay",
        "created": "2020-03-04T11:02:16.790000+00:00",
        "source_uid": "junction",
        "target_uid": "storage",
        "transit_time": 10.0,
        "display_name": "delay",
        "element_class": "IDontExist",  # Does not exist
        "domain": "water",
    },
    {
        "uid": "delay",
        "created": "2020-03-04T11:02:16.790000+00:00",
        "source_uid": "junction",
        "target_uid": "storage",
        "transit_time": 10.0,
        "display_name": "delay",
        # "element_class": "Delay", # Missing
        "domain": "water",
    },
    {
        "uid": "delay",
        "created": "2020-03-04T11:02:16.790000+00:00",
        "source_uid": "junction",
        "target_uid": "storage",
        "transit_time": 10.0,
        "display_name": "delay",
        "element_class": "Delay",
        # "domain": "water", # Missing
    },
    {
        "uid": "delay",
        "created": "2020-03-04T11:02:16.790000+00:00",
        "source_uid": "junction",
        "target_uid": "storage",
        "transit_time": 10.0,
        "display_name": "delay",
        "element_class": "Delay",
        "domain": "idontexist",  # Does not exist
    },
]


@pytest.mark.parametrize("element", elements)
def test_parse(element: Dict[str, Any]) -> None:
    instance = element_from_dict(element)
    reserialised = element_to_dict(instance)
    assert element == reserialised


@pytest.mark.parametrize("element", bad_elements)
def test_bad_elements(element: Dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        element_from_dict(element)


def test_util_entry_point() -> None:
    assert elements_mapping["water"]["links"]
    assert elements_mapping["water"]["nodes"]
    assert set(elements_mapping["water"]["links"].values()).issubset(set(all_links))
    assert set(elements_mapping["water"]["nodes"].values()).issubset(set(all_nodes))


@pytest.mark.parametrize("element", elements)
def test_correct_element_class(element: Any) -> None:
    instance = element_from_dict(element)
    assert instance.element_class == instance.__class__.__name__
