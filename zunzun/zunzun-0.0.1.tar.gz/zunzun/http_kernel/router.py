from .. import inspect
from werkzeug.routing import Map, Rule
from injector import Injector, inject, singleton


@singleton
class Router:
    @inject
    def __init__(self, injector: Injector):
        self.routers_map = Map()
        self.injector = injector

    def _get_parameters(self, action, parameters):
        args_spec = inspect.getfullargspec(action)
        parameters = {
            **parameters,
            **self._load_parameter_by_type(args_spec.annotations),
        }
        if args_spec.varkw or args_spec.varargs:
            return parameters
        parameters_result = dict()
        for item in args_spec.args:
            parameters_result[item] = parameters.get(item)
        return parameters_result

    def _load_parameter_by_type(self, parameters):
        values = dict()
        for k, v in parameters.items():
            values[k] = self._create_object(v)
        return values

    def _run_action(self, action, **kwargs):
        parameters = self._get_parameters(action, kwargs)
        cls = inspect.findclass(action)
        if cls:
            parameters["self"] = self._create_controller(cls)
        return action(**parameters)

    def _create_controller(self, cls):
        args_spec = inspect.getfullargspec(cls)
        parameters = self._load_parameter_by_type(args_spec.annotations)
        return cls(**parameters)

    def _create_object(self, cls):
        return self.injector.get(cls)

    def _add_route(self, path, **kwargs):
        self.routers_map.add(Rule(path, **kwargs))

    def any(self, path, **kwargs):
        def wrapper(action):
            self._add_route(
                path,
                endpoint=lambda **parameters: self._run_action(action, **parameters),
                **kwargs
            )

        return wrapper

    def get(self, path, **kwargs):
        return self.any(path, methods=["GET"], **kwargs)

    def post(self, path, **kwargs):
        return self.any(path, methods=["POST"], **kwargs)

    def patch(self, path, **kwargs):
        return self.any(path, methods=["PATCH"], **kwargs)

    def delete(self, path, **kwargs):
        return self.any(path, methods=["DELETE"], **kwargs)
