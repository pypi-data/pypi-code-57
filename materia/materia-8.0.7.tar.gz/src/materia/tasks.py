from __future__ import annotations
from typing import Any, Callable, Iterable, Optional, Tuple, Union

import dlib
import functools
import materia as mtr
from materia.utils import memoize

import re

# import scipy.optimize
import subprocess

__all__ = [
    "ExternalTask",
    "FunctionTask",
    "InputTask",
    "MaxLIPOTR",
    "ShellCommand",
    "Task",
]


class Task:
    def __init__(
        self,
        num_cores: Optional[int] = 1,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.num_cores = num_cores
        self.handlers = handlers or []
        self.name = (
            name
            or re.match("<class '(?P<cls>.*)'>", str(self.__class__))
            .group("cls")
            .rsplit(".")[-1]
        )

        self.requirements = []
        self.named_requirements = {}

    def requires(self, *args: Task, **kwargs: Task) -> None:
        self.requirements += [a if isinstance(a, Task) else InputTask(a) for a in args]
        self.named_requirements = dict(
            **self.named_requirements,
            **{
                k: v if isinstance(v, Task) else InputTask(v) for k, v in kwargs.items()
            },
        )

    def run(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.name


class ExternalTask(Task):
    def __init__(
        self,
        engine: mtr.Engine,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.engine = engine
        self.io = io
        super().__init__(self.engine.num_processors or 1, handlers=handlers, name=name)


class FunctionTask(Task):
    def __init__(
        self,
        f: Callable,
        handlers: Optional[Iterable[Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.f = f

    def run(self, **kwargs) -> None:
        return self.f(**kwargs)


class InputTask(Task):
    def __init__(
        self,
        value: Any,
        handlers: Optional[Iterable[Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(1, handlers=handlers, name=name)
        self.value = value

    def run(self, *args) -> Any:
        return self.value


class ShellCommand(Task):
    def __init__(
        self,
        command: str,
        handlers: Optional[Iterable[Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.command = command

    def run(self) -> None:
        subprocess.call(self.command.split())


def task(
    f: Callable = None,
    handlers: Optional[Iterable[Handler]] = None,
    name: Optional[str] = None,
) -> FunctionTask:
    # FIXME: this is incomptabile with mtr.Workflow.run(thread=False) (i.e. with multiprocessing) because FunctionTask cannot be serialized!
    if f is None:
        return functools.partial(task, handlers=handlers, name=name)

    return FunctionTask(f=f, handlers=handlers, name=name)


# class GoldenSectionSearch:
#     def __init__(self, objective_function):
#         self.objective_function = objective_function

#     @memoize
#     def evaluate_objective(self, x):
#         return self.objective_function(x)

#     def optimize(self, delta, tolerance):
#         bracket = self._find_gss_bracket(delta=delta)

#         return scipy.optimize.minimize_scalar(
#             fun=self.evaluate_objective, bracket=bracket, method="Golden", tol=tolerance
#         )

#     def _find_gss_bracket(self, delta):
#         # FIXME: ugly but it works...
#         phi = (1 + math.sqrt(5)) / 2

#         self.evaluate_objective(x=1e-3)
#         self.evaluate_objective(x=delta)

#         while self.evaluate_objective.cache.last_result(
#             n=1
#         ) <= self.evaluate_objective.cache.last_result(n=2):
#             _, last1 = self.evaluate_objective.cache.last_args(n=1)
#             _, last2 = self.evaluate_objective.cache.last_args(n=2)

#             self.evaluate_objective(x=last1["x"] + phi * (last1["x"] - last2["x"]))

#         if len(self.evaluate_objective.cache) > 2:
#             _, last3 = self.evaluate_objective.cache.last_args(n=3)
#             _, last1 = self.evaluate_objective.cache.last_args(n=1)
#             return (last3["x"], last1["x"])
#         else:
#             _, last2 = self.evaluate_objective.cache.last_args(n=2)
#             _, last1 = self.evaluate_objective.cache.last_args(n=1)
#             return (last2["x"], last1["x"])

#         return bracket

#     # def plot_results(self):
#     #     x, y = zip(*sorted(self.evaluate_objective.cache.items()))
#     #     plt.plot(x, y)
#     #     plt.show()


T = Union[int, float]


class MaxLIPOTR(Task):
    def __init__(
        self,
        objective_function: Callable[T, T],
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(1, handlers, name)
        self.objective_function = objective_function

    @memoize
    def _evaluate_objective(self, *args: T) -> T:
        return self.objective_function(*args)

    def run(
        self,
        x_min: Union[T, Iterable[T]],
        x_max: Union[T, Iterable[T]],
        num_evals: int,
        epsilon: Optional[float] = 0,
    ) -> Tuple[T, Union[int, float]]:

        return dlib.find_min_global(
            self._evaluate_objective,
            x_min if isinstance(x_min, list) else [x_min],
            x_max if isinstance(x_max, list) else [x_max],
            num_evals,
            solver_epsilon=epsilon,
        )

    # def plot_results(self):
    #     x, y = zip(*sorted(self.evaluate_objective.cache.items()))
    #     plt.plot(x, y)
    #     plt.show()
