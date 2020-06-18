from __future__ import annotations
from typing import Iterable, Optional

import materia as mtr
import pathlib
import re
import shlex
import subprocess

from .engine import Engine
from ..tasks import ExternalTask

__all__ = ["XTB"]


class XTB(Engine):
    def __init__(
        self,
        executable: Optional[str] = "xtb",
        arguments: Optional[Iterable[str]] = None,
    ) -> None:
        super().__init__(executable=executable, arguments=arguments)

    def command(
        self,
        out: str,
        work_dir: str,
        coord: str,
        arguments: Optional[Iterable[str]] = None,
    ) -> str:
        args = list(self.arguments) + list(arguments or [])
        arg_str = " ".join(args)
        # FIXME: shlex.quote should be used but it doesn't work...
        return shlex.split(f"{self.executable} {coord} {arg_str}")

    def execute(
        self, coord: str, io: materia.IO, arguments: Optional[Iterable[str]] = None
    ) -> str:
        with io() as _io:
            cmd = self.command(_io.out, _io.work_dir, mtr.expand(coord), arguments)
            with open(_io.out, "w") as out:
                env = self.env()
                if env is None:
                    subprocess.call(
                        cmd, stdout=out, stderr=subprocess.STDOUT, cwd=io.work_dir
                    )
                else:
                    subprocess.call(
                        cmd,
                        stdout=out,
                        stderr=subprocess.STDOUT,
                        env=self.env(),
                        cwd=io.work_dir,
                    )

            with open(_io.out, "r") as f:
                return "".join(f.readlines())

    def optimize(
        self,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> XTBOptimize:
        return XTBOptimize(engine=self, io=io, handlers=handlers, name=name)


class XTBOptimize(ExternalTask):
    def parse(self, output: str) -> mtr.Structure:
        with open(output, "r") as f:
            structure_file = re.search(
                r"optimized geometry written to:\s*(?P<structure>.*)\s*",
                "".join(f.readlines()),
            ).group("structure")

        return mtr.Structure.read(f"{pathlib.Path(output).parent}/{structure_file}")

    def run(self, molecule: mtr.Molecule) -> mtr.Molecule:
        with self.io() as io:
            with molecule.structure.tempfile(suffix=".xyz", dir=io.work_dir) as f:
                self.engine.execute(f.name, self.io, arguments=["--opt"])

            molecule.structure = self.parse(io.out)
            return molecule
