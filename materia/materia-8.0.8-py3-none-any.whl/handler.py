import abc
import functools

import materia as mtr

__all__ = ["Handler"]


class Handler(abc.ABC):
    def run(self, result, task):
        if self.check(result=result, task=task):
            raise mtr.ActionSignal(
                result=result, actions=self.handle(result=result, task=task)
            )

    @abc.abstractmethod
    def check(self, result, task):
        # input: result of task to be checked and the task object itself
        # output: True if output indicates that self.handle should be called, else False
        pass

    @abc.abstractmethod
    def handle(self, result, task):
        # input: result of task to be checked and the task object itself
        # output: Actions object containing actions to be performed in order to repair task
        return []


# import re


# import materia


# from materia.handler import Handler
# from materia.actions import (
#     QChemModifyRSHParameter,
#     QChemIncreaseResponseIterations,
#     QChemIncreaseSCFIterations,
#     Rerun,
# )

# #
# __all__ = [
#     "QChemResponseDIISConvergence",
#     "QChemSCFConvergence",
# ]


# class QChemResponseDIISConvergence(Handler):
#     def __init__(self, increase_factor=2):
#         self.increase_factor = increase_factor

#     def check(self, result, task):
#         with open(task.io.out, "r") as f:
#             if re.search(
#                 r"DIIS\s*failed\s*to\s*converge\s*within\s*the\s*given\s*number\s*of\s*iterations",
#                 "".join(f.readlines()),
#             ):
#                 return True

#         return False

#     def handle(self, result, task):
#         return [
#             QChemIncreaseResponseIterations(increase_factor=self.increase_factor),
#             Rerun(),
#         ]


# class QChemSCFConvergence(Handler):
#     def __init__(self, increase_factor=2):
#         self.increase_factor = increase_factor

#     def check(self, result, task):
#         with open(task.output_path, "r") as f:
#             if re.search(
#                 r"gen_scfman_exception:\s*SCF\s*failed\s*to\s*converge",
#                 "".join(f.readlines()),
#             ):
#                 return True

#         return False

#     def handle(self, result, task):
#         return [
#             QChemIncreaseSCFIterations(increase_factor=self.increase_factor),
#             Rerun(),
#         ]

# # FIXME: implement a handler - the following error can be fixed by setting sym_ignore to true

# # ***ERROR*** Coordinates do not transform within specified threshold of.10000D-04

# # Q-Chem fatal error occurred in module 0, line  242:

# # Problem in GetRot
