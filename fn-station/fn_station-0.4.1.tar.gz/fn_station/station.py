from dataclasses import dataclass, field
from importlib import import_module
from typing import Any
from typing import List, Dict

from dash import dash
from fn_graph import Composer
from fn_graph_studio import ExternalStudio
from instant_api import InstantAPI, InstantError

from fn_station.blueprint import make_blueprint
from fn_station.utils import slugify
from ._json import FnJSONEncoder
from .queries import QueryManager


@dataclass
class StationComposer:
    slug: str
    url: str
    title: str
    composer: Composer
    description: str
    tags: List[str]


@dataclass
class ComposerCalculationResponse:
    id: int
    client_id: str
    nodes: Dict[str, Any]


@dataclass
class HistoricalQueryRequest:
    query_id: int


@dataclass
class Dashboard:
    slug: str
    url: str
    title: str
    description: str


SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": "composer_api",
            "route": "/composer_api.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "title": "API Endpoints",
    "version": None,
    "description": None,
    "termsOfService": None,
    "hide_top_bar": True,
}


class ComposerStation:
    def calculate(
        self,
        composer,
        parameters,
        outputs,
        composer_name,
        client_id=None,
        user=None,
        intermediates=False,
        store_query=False,
    ):

        if not store_query:
            return (
                composer.update_parameters(**parameters).calculate(
                    outputs, intermediates=intermediates
                ),
                -1,
            )
        else:
            return self.query_manager.calculate_and_store(
                composer, outputs, parameters, composer_name, client_id=client_id
            )

    def __init__(self, app, *, query_store=None, url_prefix="", store_query=False):
        self.app = app
        if url_prefix:
            url_prefix = "/" + url_prefix.strip("/")
        self.url_prefix = url_prefix
        self.composers: Dict[str, StationComposer] = {}
        self.dashboards = []
        self.endpoints = []
        self.blueprint = make_blueprint(self, url_prefix)
        self.store_query = store_query

        self.query_manager = QueryManager(query_store)
        app.register_blueprint(self.blueprint)
        self.instant_api = InstantAPI(app, swagger_kwargs=dict(config=SWAGGER_CONFIG))

        # Set a JsonEncoder we can control
        app.json_encoder = FnJSONEncoder

        # Query History Studio
        url = f"{self.url_prefix}/query/"
        history_dash_app = dash.Dash(server=self.app, url_base_pathname=url)
        app.enable_dev_tools = True

        def get_history_composer(url):
            query_id = int(url.split("/")[-1])
            return self.query_manager.load_composer(query_id)

        ExternalStudio(
            history_dash_app,
            get_composer=get_history_composer,
            show_profiler=False,
            editable_parameters=False,
            title="Query History",
        )

        @self.register_endpoint("Composers")
        def composer_calculate(
                name: str,
                outputs: List[str],
                parameters: Dict[str, Any] = None,
                client_id: str = None,
                intermediates: bool = False,
                store_query: bool = False,
        ) -> ComposerCalculationResponse:
            if parameters is None:
                parameters = {}
            if name not in self.composers:
                raise InstantError(
                    code=4040,
                    http_code=404,
                    message=f"Composer {name} not found",
                    data={
                        "composers": list(self.composers.keys()),
                    }
                )

            composer = self.composers[name]

            results, query_id = self.calculate(
                composer_name=name,
                composer=composer.composer,
                client_id=client_id,
                user="TODO@businessoptics.biz",
                parameters=parameters,
                outputs=outputs,
                store_query=store_query,
                intermediates=intermediates,
            )

            return ComposerCalculationResponse(
                id=query_id, client_id=client_id, nodes=results
            )

    def register_composer(self, slug, title, composer: Composer, **kwargs):
        url = f"{self.url_prefix}/composer_studio/{slug}/"
        if slug in self.composers:
            raise ValueError(f"{slug} is already a registered composer")
        self.composers[slug] = StationComposer(slug, url, title, composer, **kwargs)
        dash_app = dash.Dash(server=self.app, url_base_pathname=url)
        ExternalStudio(dash_app, get_composer=lambda url: composer, title=title)
        return self

    def register_dash(
        self,
        module_name,
        title,
        description,
        slug=None,
        # icon=None,
        # ignore_default_stylesheets=False,
    ):
        slug = slug or slugify(title)
        url = f"{self.url_prefix}/dash/{slug}/"

        def factory(name, **kwargs):
            external_stylesheets = kwargs.pop("external_stylesheets", [])
            # if not ignore_default_stylesheets:
            #     external_stylesheets = (
            #         external_stylesheets + self.default_dash_stylesheets
            #     )
            return dash.Dash(
                name,
                server=self.app,
                url_base_pathname=url,
                external_stylesheets=external_stylesheets,
                **kwargs,
            )

        import_module(module_name).create_app(factory)

        self.dashboards.append(
            Dashboard(
                slug=slug,
                title=title,
                description=description,
                # icon=icon,
                url=url,
            )
        )

        return self

    def register_endpoint(self, section):
        def registration(func):
            return self.instant_api(func, swagger_view_attrs=dict(tags=[section]))

        return registration

    def register_permissions(self):
        def decorator(func):
            return func  # TODO

        return decorator

    def register_authentication(self):
        def decorator(func):
            return func  # TODO

        return decorator
