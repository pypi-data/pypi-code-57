import functools
import inspect

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from fn_graph import Composer


class QueryStore:
    def setup(self):
        pass

    def list_query_entries(
        self, page, id=None, composer_name=None, client_id=None, user=None, date=None
    ):
        pass

    def store_query_entry(self, composer_name, client_id):
        pass

    def store_parameters(self, query_id, parameters):
        pass

    def get_parameters(self, query_id):
        pass

    def store_signatures(self, query_id, composer):
        pass

    def get_signatures(self, query_id):
        pass

    def store_result(self, query_id, result_name, result):
        pass

    def get_result(self, query_id, result_name):
        pass

    def store_definitions(self, query_id, definition):
        pass

    def get_definitions(self, query_id):
        pass


@dataclass
class FnInformation:
    key: str
    signature: inspect.Signature
    _is_fn_graph_link: bool


class HistoryCache:
    """
    Pulls the cache from a query store.
    """

    def __init__(self, query_id, store: QueryStore):
        self.query_id = query_id
        self.store = store

    def valid(self, composer, key):
        return True

    def get(self, composer, key):
        return self.store.get_result(self.query_id, key)

    def set(self, composer, key, value):
        pass

    def invalidate(self, composer, key):
        pass


class QueryManager:
    def __init__(self, store: QueryStore):
        self.store = store

    def calculate_and_store(
        self,
        composer: Composer,
        outputs: List[str],
        parameters: Dict[str, Any],
        composer_name: str,
        client_id=None,
    ) -> Tuple[Dict[str, Any], str]:
        composer = composer.update_parameters(**parameters)
        results = composer.calculate(outputs, intermediates=True)
        query_id = self.store_query(
            composer, parameters, outputs, results, composer_name, client_id
        )
        return results, query_id

    def _serialize_signatures(self, composer, results):

        return {
            key: FnInformation(
                key, inspect.signature(fn), getattr(fn, "_is_fn_graph_link", False)
            )
            for key, fn in composer.functions().items()
            if key in results
        }

    def _serialize_definitions(self, composer, results):

        return {
            key: composer.get_source(key)
            for key in composer.functions()
            if key in results
        }

    def store_query(
        self, composer, parameters, outputs, results, composer_name, client_id
    ):
        store = self.store
        query_id = store.store_query_entry(composer_name, client_id)

        signatures = self._serialize_signatures(composer, results)
        definitions = self._serialize_definitions(composer, results)

        store.store_signatures(query_id, signatures)
        store.store_parameters(query_id, parameters)
        store.store_definitions(query_id, definitions)

        for key, result in results.items():
            store.store_result(query_id, key, result)

        return query_id

    def list_queries(
        self, page, id=None, composer_name=None, client_id=None, user=None, date=None
    ):
        return self.store.list_query_entries(
            page, id, composer_name, client_id, user, date
        )

    def make_dummy_fn(self, query_id, fn_information):
        def make_parameter_string(key, parameter):
            prefix = {
                inspect.Parameter.VAR_KEYWORD: "**",
                inspect.Parameter.VAR_POSITIONAL: "*",
            }.get(parameter.kind, "")
            suffix = (
                f"='DEFAULT_VALUE'"
                if parameter.default != inspect.Parameter.default
                else ""
            )
            return f"{prefix}{key}{suffix}"

        parameters_string = ",".join(
            [
                make_parameter_string(k, v)
                for k, v in fn_information.signature.parameters.items()
            ]
        )
        store = self.store
        fn = eval(f"lambda {parameters_string}: None", dict(store=store))

        if fn_information._is_fn_graph_link:
            fn._is_fn_graph_link = fn_information._is_fn_graph_link

        return fn

    def load_composer(self, query_id) -> Composer:
        store = self.store

        parameters = store.get_parameters(query_id)
        signatures = store.get_signatures(query_id)
        definitions = store.get_definitions(query_id)
        cache = HistoryCache(query_id, self.store)
        history = (
            (
                Composer()
                .update(
                    **{
                        key: self.make_dummy_fn(query_id, fn_information)
                        for key, fn_information in signatures.items()
                    }
                )
                .update_parameters(**parameters)
            )
            .set_source_map(definitions)
            .cache(backend=cache)
        )
        return history
