from __future__ import annotations
from typing import Iterable, Optional, Tuple

import materia as mtr
import pathlib
import re
import shlex
import subprocess

from .engine import Engine
from ..tasks import ExternalTask

__all__ = ["FragIt"]


class FragIt(Engine):
    def __init__(
        self,
        executable: Optional[str] = "fragit",
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

    def execute(self, io_params: materia.IO) -> str:
        with io_params() as io:
            cmd = self.command(io.inp, io.out, io.work_dir)
            with open(io.inp, "r") as inp:
                with open(io.out, "w") as out:
                    subprocess.call(
                        cmd, stdin=inp, stdout=out, env=self.env(), cwd=io.work_dir
                    )

            with open(io.out, "r") as f:
                return "".join(f.readlines())

    def fragment(
        self,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> FragItFragment:
        return FragItFragment(engine=self, io=io, handlers=handlers, name=name)


class FragItFragment(ExternalTask):
    """
    Task to fragment a structure using FragIt.

    Attributes:
        engine (mtr.FragItEngine): Engine which will be used to fragment structure.
    """

    def run(self, molecule: mtr.Molecule,) -> Tuple[mtr.Molecule]:
        with self.io() as io:
            molecule.structure.write(io.inp)

            self.engine.execute(self.io)
            name = pathlib.Path(io.inp).stem

            return tuple(
                mtr.Molecule(str(p))
                for p in pathlib.Path(io.work_dir).glob(f"{name}_fragment_*.xyz")
            )
