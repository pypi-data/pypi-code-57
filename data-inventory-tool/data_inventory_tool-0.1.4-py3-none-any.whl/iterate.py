import operator
from typing import Any
from typing import Dict
from typing import Iterator

from datainventory.core import Base
from datainventory.core import Column
from datainventory.core import Dataset
from datainventory.core import Filter
from datainventory.core import Manifest
from datainventory.core import MetaData
from datainventory.core import Model
from datainventory.core import Property
from datainventory.core import Resource


def iterrows(
    manifest: Manifest,
    including: Filter = None,
) -> Iterator[Dict[Column, Any]]:
    including = including or Filter()
    dataset = None
    resource = None
    models = manifest.models.values()
    models = sorted(models, key=operator.attrgetter('rowno'))

    for model in models:
        if including(model) is False:
            continue

        if model.resource:
            if dataset is None or dataset.name != model.resource.dataset.name:
                dataset = model.resource.dataset
                if including(model.resource.dataset):
                    yield torow(dataset, including)

            if resource is None or resource.name != model.resource.name:
                resource = model.resource
                if including(dataset):
                    yield torow(resource, including)

        if including(model.base):
            yield torow(model.base, including)
        else:
            yield {col: None for col in Column}

        yield torow(model, including)

        for prop in model.properties.values():
            if including(prop):
                yield torow(prop, including)


def torow(data: MetaData, including: Filter) -> Dict[Column, Any]:
    row = {col: None for col in Column}

    row[Column.id] = data.id

    if isinstance(data, Dataset):
        row[Column.dataset] = data.name
    elif isinstance(data, Resource):
        row[Column.resource] = data.name
    elif isinstance(data, Base):
        row[Column.base] = data.name
    elif isinstance(data, Model):
        relative = including.dataset and data.resource
        row[Column.model] = data.get_name(relative)
    elif isinstance(data, Property):
        row[Column.property] = data.name

    if data.source:
        row[Column.source] = data.source
        row[Column.prepare] = data.prepare

    row[Column.type] = data.type
    row[Column.ref] = data.ref
    row[Column.level] = data.level
    row[Column.access] = data.access
    row[Column.title] = data.title
    row[Column.description] = data.description

    return row
