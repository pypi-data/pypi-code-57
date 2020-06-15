#from fastapi.routing import APIRouter
#from fastapi_utils.inferring_router import InferringRouter


from typing import TYPE_CHECKING, Any, Callable, get_type_hints
from fastapi import APIRouter
class InferringRouter(APIRouter):
    """
    Overrides the route decorator logic to use the annotated return type as the `response_model` if unspecified.
    """

    if not TYPE_CHECKING:  # pragma: no branch

        def add_api_route(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
            if kwargs.get("response_model") is None:
                kwargs["response_model"] = get_type_hints(endpoint).get("return")
            return super().add_api_route(path, endpoint, **kwargs)

class Router(InferringRouter):
    pass


class Routes:
    def __init__(self, app, prefix):
        self.app = app
        self.http = app.http
        self.prefix = prefix

    def controller(self, controller, prefix=''):
        #self.http.controller(controller.route, prefix=self.prefix)
        self.http.include_router(controller.route, prefix=self.prefix + str(prefix))
