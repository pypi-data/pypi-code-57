from __future__ import annotations

from typing import Dict

import dataclasses
import enum


class Column(enum.IntEnum):
    id = 0
    dataset = 1
    resource = 2
    base = 3
    model = 4
    property = 5
    source = 6
    prepare = 7
    type = 8
    ref = 9
    level = 10
    access = 11
    title = 12
    description = 13


TYPES = [
    'integer',
]


class Level(enum.IntEnum):
    # Data do not exist.
    absent = 0

    # Data exists in any form, for example txt, pdf, etc...
    available = 1

    # Data is structured, for example xls, xml, etc...
    structured = 2

    # Data provided using an open format, csv, tsv, sql, etc...
    open = 3

    # Individual data objects have unique identifiers.
    identifiable = 4

    # Data is linked with a known vocabulary.
    linked = 5


class Access(enum.IntEnum):
    # Private properties can be accesses only if an explicit property scope is
    # given. If client does not have required scope, then private properties
    # can't bet selected, but can be used in query conditions, in sorting.
    private = 0

    # Property is exposed only to authorized user, who has access to model.
    # Authorization token is given manually to each user.
    protected = 1

    # Property can be accessed by anyone, but only after accepting terms and
    # conditions, that means, authorization is still needed and data can only be
    # used as specified in provided terms and conditions. Authorization token
    # can be obtained via WebUI.
    public = 2

    # Open data, anyone can access this data, no authorization is required.
    open = 3


class Manifest:
    models: Dict[str, Model] = None

    def __init__(self):
        self.models = {}


class _Computed:
    level: Level = None
    access: Access = None


class MetaData:
    rowno: int = None

    id: str = None
    name: str = None
    source: str = None
    prepare: str = None
    type: str = None
    ref: str = None
    level: Level = None
    access: Access = None
    title: str = None
    description: str = None

    comp: _Computed = None

    def __init__(self):
        self.comp = _Computed()


class Dataset(MetaData):
    resources: Dict[str, Resource] = None

    def __init__(self, name: str):
        self.name = name
        self.resources = {}
        super().__init__()


class Resource(MetaData):
    models: Dict[str, Model] = None
    dataset: Dataset = None

    def __init__(self, name: str, dataset: Dataset):
        self.name = name
        self.dataset = dataset
        self.dataset.resources[name] = self
        super().__init__()


class Base(MetaData):
    pass


class Model(MetaData):
    rowno: int = 0
    resource: Resource = None
    base: Base = None
    properties: Dict[str, Property] = None

    def get_name(self, relative: bool = False) -> str:
        return self.name


class Property(MetaData):

    def __init__(self, name: str, model: Model):
        self.name = name
        self.model = model
        self.model.properties[name] = self
        super().__init__()


@dataclasses.dataclass
class Filter:
    dataset: bool = True
    base: bool = True
    source: bool = True
    access: Access = Access.private
    level: Level = Level.absent

    def __call__(self, data: MetaData = None):
        if data is None:
            return False

        if isinstance(data, Dataset) and not self.dataset:
            return False

        elif isinstance(data, Base) and not self.base:
            return False

        if data.comp.access < self.access:
            return False

        if data.comp.level < self.level:
            return False

        return True


def set_computed_values(data: MetaData):
    if isinstance(data, Model):
        _set_model_comp_values(data)
    else:
        raise NotImplementedError


def _set_model_comp_values(model: Model):
    model.comp.access = max(
        prop.access or Access.protected
        for prop in model.properties.values()
    )
    model.comp.level = min(
        prop.comp.level
        for prop in model.properties.values()
    )
    _update_resource_comp_values(model.resource, model)


def _update_resource_comp_values(resource: Resource, model: Model) -> None:
    if resource.comp.access is None:
        resource.comp.access = model.comp.access
    else:
        resource.comp.access = max(
            resource.comp.access,
            model.comp.access,
        )

    if resource.comp.level is None:
        resource.comp.level = model.comp.level
    else:
        resource.comp.level = max(
            resource.comp.level,
            model.comp.level,
        )

    _update_dataset_comp_values(resource.dataset, resource)


def _update_dataset_comp_values(dataset: Dataset, resource: Resource) -> None:
    if dataset.comp.access is None:
        dataset.comp.access = resource.comp.access
    else:
        dataset.comp.access = max(
            dataset.comp.access,
            resource.comp.access,
        )

    if dataset.comp.level is None:
        dataset.comp.level = resource.comp.level
    else:
        dataset.comp.level = max(
            dataset.comp.level,
            resource.comp.level,
        )
