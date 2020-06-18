from __future__ import annotations
from typing import Iterable, Optional

import shlex

from .engine import Engine

__all__ = ["Openbabel"]


class Openbabel(Engine):
    def __init__(
        self,
        executable: Optional[str] = "obabel",
        arguments: Optional[Iterable[str]] = None,
    ) -> None:
        super().__init__(executable=executable, arguments=arguments)

    def command(
        self,
        inp: str,
        out: str,
        work_dir: str,
        arguments: Optional[Iterable[str]] = None,
    ) -> str:
        args = list(self.arguments) + list(arguments or [])
        arg_str = " ".join(args)
        # FIXME: shlex.quote should be used but it doesn't work...
        return shlex.split(f"{self.executable} {inp} {arg_str}")


# from __future__ import annotations
# import contextlib
# import os
# import mtr
# import re
# import tempfile
# from typing import Iterable, Optional, Union

# from ...workflow.tasks.task import Task

# __all__ = [
#     "OpenbabelConvertToFile",
#     "OpenbabelConvertToMol",
#     "OpenbabelConvertToPDB",
#     "OpenbabelConvertToSMILES",
#     "OpenbabelConvertToSDF",
# ]


# class OpenbabelConvertToFile(Task):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         filetype: str,
#         output_name: Optional[str] = None,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(handlers=handlers, name=name)
#         self.engine = engine
#         self.filetype = filetype
#         self.output_name = output_name
#         self.log_name = log_name
#         self.work_dir = work_dir
#         self.keep_logs = keep_logs

#     def run(self, structure: Union[str, mtr.Structure]) -> str:
#         with mtr.work_dir(self.work_dir) as wd:
#             arguments = [f"-o{self.filetype}"]

#             if self.output_name is not None:
#                 output_path = (
#                     f"{mtr.expand(self.output_name,dir=wd)}.{self.filetype}"
#                 )
#                 arguments.append(f"-O{output_path}")

#             with contextlib.nullcontext(structure) if isinstance(
#                 structure, str
#             ) else structure.tempfile(suffix=".xyz") as fp:
#                 input_filepath = mtr.expand(
#                     path=fp.name if hasattr(fp, "name") else fp, dir=wd
#                 )
#                 self.engine.execute(
#                     input_filepath=input_filepath,
#                     log_filepath=mtr.expand(path=self.log_name, dir=wd),
#                     arguments=arguments,
#                 )

#             if self.output_name is not None:
#                 with open(output_path, "r") as f:
#                     return "".join(f.readlines())


# class OpenbabelConvertToMol(OpenbabelConvertToFile):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         output_name: str,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(
#             engine=engine,
#             filetype="mol",
#             output_name=output_name,
#             log_name=log_name,
#             work_dir=work_dir,
#             keep_logs=keep_logs,
#             handlers=handlers,
#             name=name,
#         )


# class OpenbabelConvertToPDB(OpenbabelConvertToFile):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         output_name: str,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(
#             engine=engine,
#             filetype="pdb",
#             output_name=output_name,
#             log_name=log_name,
#             work_dir=work_dir,
#             keep_logs=keep_logs,
#             handlers=handlers,
#             name=name,
#         )


# class OpenbabelConvertToSDF(OpenbabelConvertToFile):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         output_name: str,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(
#             engine=engine,
#             filetype="sdf",
#             output_name=output_name,
#             log_name=log_name,
#             work_dir=work_dir,
#             keep_logs=keep_logs,
#             handlers=handlers,
#             name=name,
#         )


# class OpenbabelConvertToSMILES(OpenbabelConvertToFile):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         output_name: str,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(
#             engine=engine,
#             filetype="smi",
#             output_name=output_name,
#             log_name=log_name,
#             work_dir=work_dir,
#             keep_logs=keep_logs,
#             handlers=handlers,
#             name=name,
#         )

#     def run(self, structure: Union[str, mtr.Structure]) -> str:
#         super().run(structure=structure)

#         with open(
#             f"{mtr.expand(self.output_name,dir=self.work_dir)}.smi", "r"
#         ) as f:
#             smiles, *_ = re.search(r"([^\s]*).*", "".join(f.readlines())).groups()

#         return smiles
