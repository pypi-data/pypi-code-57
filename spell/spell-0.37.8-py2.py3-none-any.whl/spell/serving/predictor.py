import inspect
from typing import Callable, Optional

from starlette.requests import Request
from starlette.responses import JSONResponse

from spell.serving.background import BackgroundTasks
from spell.serving.exceptions import InvalidPredictor
from spell.serving.types import (
    PredictorArgumentGenerator,
    PredictorMethod,
    PredictorMethodArguments,
)


class _InjectedParams:
    __slots__ = ["background_tasks", "request"]

    def __init__(
        self, background_tasks: Optional[str] = None, request: Optional[str] = None
    ) -> None:
        self.background_tasks = background_tasks
        self.request = request

    @staticmethod
    def from_func(func: PredictorMethod):
        injected_params = getattr(func, "__injected_params__", _InjectedParams())
        for param, type_ in func.__annotations__.items():
            if type_ == BackgroundTasks:
                if injected_params.background_tasks:
                    raise InvalidPredictor(
                        "Found both annotation and decorator for background tasks"
                    )
                injected_params.background_tasks = param
            elif type_ == Request:
                if injected_params.request:
                    raise InvalidPredictor("Found both annotation and decorator for full request")
                injected_params.request = param
        return injected_params

    def make_arguments(self, request: Request) -> PredictorMethodArguments:
        tasks = None
        kwargs = {}
        if self.background_tasks:
            tasks = BackgroundTasks()
            kwargs[self.background_tasks] = tasks
        if self.request:
            kwargs[self.request] = request
        return kwargs, tasks


class BasePredictor:
    def health(self):
        return JSONResponse({"status": "ok"})

    @classmethod
    def get_predict_argument_generator(cls) -> PredictorArgumentGenerator:
        return cls._create_argument_generator(cls.predict)

    @classmethod
    def get_health_argument_generator(cls) -> PredictorArgumentGenerator:
        return cls._create_argument_generator(cls.health)

    @staticmethod
    def _create_argument_generator(func: PredictorMethod) -> PredictorArgumentGenerator:
        """Creates a function which generates the arguments to either the predict or health
        methods. This is done to remove as much processing of the annotations and decorators out of
        the runtime of calling the method during a request.
        """
        return _InjectedParams.from_func(func).make_arguments

    @classmethod
    def validate(cls) -> None:
        init = cls._get_func_or_raise("__init__")
        init_args = inspect.getfullargspec(init).args
        if len(init_args) != 2:
            raise InvalidPredictor(
                f"Invalid signature for __init__. Expected 2 arguments, "
                f"but found {len(init_args)}."
            )
        cls._validate_function_signature("predict", min_args=1)
        cls._validate_function_signature("health", min_args=0)

    @classmethod
    def _validate_function_signature(cls, func_name: str, min_args: int) -> None:
        func = cls._get_func_or_raise(func_name)
        func_args = inspect.getfullargspec(func).args

        annotations_set = set(func.__annotations__)
        if len(annotations_set) != len(func.__annotations__):
            raise InvalidPredictor(f"All annotations in {func_name} must be unique")

        # If the function is not a staticmethod, then we need to ignore the first parameter
        self_param = None
        if not cls._is_staticmethod(func_name):
            if func_args:
                self_param = func_args.pop(0)
            elif min_args == 0:
                # example: health() rather than health(self)
                raise InvalidPredictor(
                    f"Expected a self or cls argument in {func_name} but found none. Add a self "
                    "or cls argument or mark as a staticmethod"
                )
            if self_param in annotations_set:
                annotations_set.remove(self_param)

        if len(func_args) < min_args:
            raise InvalidPredictor(f"{func_name} function must have at least {min_args} arguments")
        if len(func_args) > min_args:
            # Get all the args which do not have annotations
            unaccounted_args = set(func_args) - annotations_set

            # Find all the params which are indicated using decorators
            decorator_params = getattr(func, "__injected_params__", _InjectedParams())

            # Check that the decorators don't refer to the same param
            if (
                decorator_params.background_tasks is not None
                and decorator_params.background_tasks == decorator_params.request
            ):
                raise InvalidPredictor(
                    "Both request and background tasks are using the same param name "
                    f"{decorator_params.request} in {func_name} function"
                )

            # Check that the decorated params do not refer to the self/cls param we are ignoring
            if self_param:
                if decorator_params.background_tasks == self_param:
                    raise InvalidPredictor(
                        f"The background tasks decorator cannot refer to {self_param}"
                    )
                if decorator_params.request == self_param:
                    raise InvalidPredictor(
                        f"The full request decorator cannot refer to {self_param}"
                    )

            # For all the params indicated in the decorators, ensure that it's in the set of
            # non-annotated params and remove it from that set because it has been accounted for
            for param in (decorator_params.background_tasks, decorator_params.request):
                if param is not None and param not in annotations_set:
                    if param in unaccounted_args:
                        unaccounted_args.remove(param)
                    else:
                        raise InvalidPredictor(
                            f"A decorator is expecting an argument named {param}, but it was not "
                            f"found in the signature for {func_name}"
                        )
            # Any args remaining in unaccounted args should the min params, like
            # (self, payload) for predict
            if len(unaccounted_args) > min_args:
                raise InvalidPredictor(
                    f"Found ({unaccounted_args}) extra arguments in {func_name} function. "
                    f"{func_name} expects at least {min_args} arguments. All additional "
                    "arguments must have a type annotation or use decorators to indicate their "
                    "use."
                )

    @classmethod
    def _get_func_or_raise(cls, func_name: str) -> Callable:
        func = getattr(cls, func_name, None)
        if not func:
            raise InvalidPredictor(f'Required function "{func_name}" is not defined')
        if not callable(func):
            raise InvalidPredictor(f'"{func_name}" is defined, but is not a function')
        return func

    @classmethod
    def _is_staticmethod(cls, func_name):
        # Unfortunately, getattr won't work properly here, so we need to directly use cls.__dict__,
        # but calling this on a subclass won't look in its base classes, which is a problem for the
        # health function. We could use cls.__base__, but this won't look further up a class
        # hierarchy, or mixins, so we need to manually traverse the entire method resolution order
        # (__mro__).
        cls_with_definition = next(
            (cls_ for cls_ in cls.__mro__ if cls_.__dict__.get(func_name) is not None), None
        )
        if cls_with_definition is None:
            # This should never happen because when this method is called,
            # getattr(cls, func_name) has returned a valid callable, so the user is doing
            # something seriously pathological here. We'll optimistically return False.
            return False
        return isinstance(cls_with_definition.__dict__[func_name], staticmethod)
