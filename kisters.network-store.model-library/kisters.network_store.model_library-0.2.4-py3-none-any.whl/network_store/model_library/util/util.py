import json
from typing import Any, Dict, List, Set

import pkg_resources

from kisters.network_store.model_library.base import BaseElement


def _get_all_subclasses(cls: Any) -> Set[Any]:
    return set(cls.__subclasses__()).union(
        (s for c in cls.__subclasses__() for s in _get_all_subclasses(c))
    )


all_nodes: List[BaseElement] = []
all_links: List[BaseElement] = []
elements_mapping: Dict[str, Dict[str, Dict[str, BaseElement]]] = {}
for entry_point in pkg_resources.iter_entry_points(
    "kisters.network_store.model_library.util"
):
    ep = entry_point.load()
    elements_mapping[entry_point.name] = {
        "links": {
            elem.__name__: elem
            for elem in _get_all_subclasses(ep.links._Link)
            if not elem.__name__.startswith("_")
        },
        "nodes": {
            elem.__name__: elem
            for elem in _get_all_subclasses(ep.nodes._Node)
            if not elem.__name__.startswith("_")
        },
    }
    all_links.extend(elements_mapping[entry_point.name]["links"].values())
    all_nodes.extend(elements_mapping[entry_point.name]["nodes"].values())


def element_from_dict(obj: Dict[str, Any], validate: bool = True) -> BaseElement:
    domain = obj.get("domain")
    if not domain:
        raise ValueError(f"Missing attribute 'domain': {obj}")
    if domain not in elements_mapping:
        raise ValueError(f"Domain '{domain}' is not recognized.")
    kind = "nodes" if obj.get("source_uid") is None else "links"
    element_class = obj.get("element_class")
    if not element_class:
        raise ValueError("Cannot instantiate: missing attribute 'element_class'")
    if element_class not in elements_mapping[domain][kind]:
        raise ValueError(
            f"Element class {domain}.{kind}.{element_class} is not recognized."
        )
    element_class = elements_mapping[domain][kind][element_class]
    if not validate:
        return element_class.construct(obj)
    return element_class.parse_obj(obj)


def element_to_dict(elem: BaseElement) -> Dict[str, Any]:
    return json.loads(elem.json(exclude_none=True))
