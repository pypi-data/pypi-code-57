import re
import warnings
from collections import OrderedDict
from typing import Dict

from dli.client.exceptions import CatalogueEntityNotFoundException
from dli.models.paginator import Paginator
from dli.client.components.urls import package_urls
from dli.models.package_model import PackageModel


class PackageModule:

    @staticmethod
    def _search_terms_to_filters(search_terms, start_count):

        def to_dict(k, op, v):
            return {'key': k.strip(), 'op': op.strip(), 'val': v.strip()}

        def partition_search_term(x):
            split = re.split("(<|>|=>|<=|=|!=| contains | like | ilike )", x)
            if len(split) == 3:
                return to_dict(*split)
            else:
                return None

        arguments = map(partition_search_term, search_terms)
        enumerated_partitions = [
            (x, y) for x, y in enumerate(arguments, start=start_count)
            if y is not None
        ]
        opmp = {
            "=": "eq",
            ">=": "gte",
            "<=": "lte",
            ">": "gt",
            "<": "lt",
        }

        wildcard = lambda op, val:  \
            "%" + val + "%" if op in ["like", "ilike"] else val

        to_numbered_filter = lambda partition: (lambda idx, x: {
            f'filter[{idx}][field]': x['key'],
            f'filter[{idx}][operator]': opmp.get(x['op'], x['op']),
            f'filter[{idx}][value]': wildcard(x['op'], x['val'])

        })(*partition)

        yield from map(to_numbered_filter, enumerated_partitions)

    @staticmethod
    def _filter_creation(search_term, only_mine):
        bump = 0
        if only_mine:
            yield {
                'filter[0][value]': True,
                'filter[0][operator]': 'eq',
                'filter[0][field]': 'has_access',
            }
            bump = 1
        else:
            yield {}

        if type(search_term) is str:
            search_term = [search_term]

        if search_term and type(search_term) is list:
            yield from PackageModule._search_terms_to_filters(search_term, bump)

    def __call__(self, search_term=None, only_mine=True) \
            -> Dict[str, PackageModel]:
        """
        See packages we can access at the top level.

        :param bool only_mine: Specify whether to collect packages only
        accessible to you (user) or to discover packages that you may
        want to discover.

        :returns: Ordered dictionary of id to PackageModel.
        :rtype: OrderedDict[id: str, PackageModel]
        """

        # search_term = ["y=z", "a>c", "d", "f contains pull", "f ilike pig"]
        filters = {}
        for x in PackageModule._filter_creation(search_term, only_mine):
            filters.update(x)

        search_paginator = Paginator(
            package_urls.v2_package_index,
            self._client._Package,
            self._client._Package._from_v2_response_unsheathed,
            page_size=5000,
            filters=filters
        )

        return OrderedDict([(v.name, v) for v in search_paginator])

    def get(self, name) -> PackageModel:
        """
        Find a PackageModel with the matching name. If not found then
        returns None.

        :param str name: The name of the package to collect
        (short codes are yet to be implemented for packages)
        :returns: PackageModel with matching name.
        :rtype: PackageModel
        """
        warnings.warn(
            'Getting a package by name'
            'will be deprecated in future. Short-codes will replace this.',
            PendingDeprecationWarning
        )

        res = self._client.packages(search_term=[f"name={name}"]).get(name)
        if res:
            return res
        else:
            raise CatalogueEntityNotFoundException(f"No such package {name}")
