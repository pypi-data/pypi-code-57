from __future__ import annotations
from typing import Dict, Iterable, Optional

import shlex
import subprocess

__all__ = ["Engine"]


class Engine:
    def __init__(
        self,
        executable: str,
        num_processors: Optional[int] = None,
        num_threads: Optional[int] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> None:

        self.executable = executable
        self.num_processors = num_processors
        self.num_threads = num_threads
        self.arguments = arguments or []

    def env(self) -> Dict[str, str]:
        return None

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
        return shlex.split(f"{self.executable} {arg_str}")

    def execute(self, io: materia.IO, arguments: Optional[Iterable[str]] = None) -> str:
        with io() as _io:
            cmd = self.command(_io.inp, _io.out, _io.work_dir, arguments)
            with open(_io.inp, "r") as inp:
                with open(_io.out, "w") as out:
                    env = self.env()
                    if env is None:
                        subprocess.call(cmd, stdin=inp, stdout=out, cwd=io.work_dir)
                    else:
                        subprocess.call(
                            cmd, stdin=inp, stdout=out, env=self.env(), cwd=io.work_dir
                        )

            with open(_io.out, "r") as f:
                return "".join(f.readlines())
