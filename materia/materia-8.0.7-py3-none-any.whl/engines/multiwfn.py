from __future__ import annotations
from typing import Any, Iterable, Optional, Tuple, Union

import materia as mtr
import subprocess

from .engine import Engine
from ..tasks import ExternalTask

__all__ = ["Multiwfn", "MultiwfnInput", "MultiwfnOutput"]


class MultiwfnInput:
    """
    Interface for inputting commands to Multiwfn.

    Attributes:
        commands (str): Iterable of commands which will be fed sequentially to Multiwfn.
    """

    def __init__(self, filepath: str, *commands: str) -> None:
        self.commands = tuple((mtr.expand(filepath), *commands))

    def write(self, filepath: str) -> None:
        """
        Write Multiwfn input to a file.

        Args:
            filepath: Path to file to which the input will be written. Can be an absolute or a relative path.
        """
        with open(mtr.expand(filepath), "w") as f:
            f.write(str(self))

    def __str__(self) -> str:
        return "\n".join(str(c) for c in self.commands) + "\n"


class MultiwfnOutput:
    def __init__(self, filepath: str) -> None:
        self.filepath = mtr.expand(filepath)

    @property
    def volume(self) -> mtr.Quantity:
        with open(self.filepath, "r") as f:
            lines = "".join(f.readlines())

        # read off the volume in atomic units (i.e. cubic Bohr)
        volume_pattern = re.compile(
            r"\s*Molecular\s*volume\s*:\s*\d*\.\d*\s*Bohr\^3,\s*\(\s*(\d*\.\d*)\s*Angstrom\^3\s*,\s*\d*\.\d*\s*cm\^3\/mol\)\s*"
        )
        # Molecular volume:    0.000 Bohr^3, (    0.000 Angstrom^3,    0.000 cm^3/mol)
        # the last match is the molecular volume (Multiwfn likes to spit out
        # other volumes earlier in the script as well)
        *_, volume_str = volume_pattern.search(lines).groups()

        return float(volume_str) * mtr.angstrom ** 3


class Multiwfn(Engine):
    def __init__(
        self,
        executable: Optional[str] = "Multiwfn",
        num_processors: Optional[int] = None,
        num_threads: Optional[int] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> None:
        super().__init__(executable, num_processors, num_threads, arguments)

    def execute(self, io_params: mtr.IO) -> str:
        env = self.env()

        with io_params() as io:
            cmd = self.command(io.inp, io.out, io.work_dir)

            with open(io.inp, "r") as inp:
                input_lines = "".join(inp.readlines())

            if self.num_processors is not None:
                input_lines = ["1000\n", "10\n", f"{self.num_processors}\n"]

            with open(io.out, "w") as out:
                # For Multiwfn 3.6
                # FIXME: printf is system-specific - is there any other way to pipe in input_lines?
                pipe_command_string = subprocess.Popen(
                    args=["printf", input_lines],
                    stdout=subprocess.PIPE,
                    encoding="utf-8",
                    env=env,
                )
                multiwfn = subprocess.Popen(
                    cmd,
                    stdin=pipe_command_string.stdout,
                    stdout=out,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    env=env,
                )
                pipe_command_string.stdout.close()
                multiwfn.communicate()

    def nto(
        self,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> MultiwfnNTO:
        return MultiwfnNTO(engine=self, io=io, handlers=handlers, name=name)

    def volume(
        self,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> MultiwfnVolume:
        return MultiwfnVolume(engine=self, io=io, handlers=handlers, name=name)


class MultiwfnBaseTask(ExternalTask):
    def commands(self) -> Iterable[Union[str, int, float]]:
        raise NotImplementedError

    def parse(self, output: str) -> Any:
        raise NotImplementedError

    def run(self, filepath: str) -> Any:
        inp = mtr.MultiwfnInput(mtr.expand(filepath), *self.commands(), -10)

        with self.io() as io:
            inp.write(io.inp)

            self.engine.execute(self.io)

            return self.parse(io.out)


class MultiwfnNTO(MultiwfnBaseTask):
    def commands(
        self, excitation_filepath: str, work_dir: str
    ) -> Tuple[Union[str, int, float]]:
        return (
            18,
            *(
                a
                for i in range(40)
                for a in [6]
                + ([excitation_filepath] if i == 0 else [])
                + [i + 1, 2, mtr.expand(f"{work_dir}/S{i+1}.fch")]
            ),
            0,
        )

    def parse(self, output: str) -> None:
        # FIXME: is there some useful output to return?
        return None

    def run(self, filepath: str, excitation_filepath: str) -> Any:
        with self.io() as io:
            inp = mtr.MultiwfnInput(
                mtr.expand(filepath),
                *self.commands(excitation_filepath, io.work_dir),
                -10,
            )
            inp.write(io.inp)

            self.engine.execute(self.io)

            return self.parse(io.out)


# class MultiwfnTotalESP(MultiwfnBaseTask):
#     def __init__(
#         self,
#         grid_quality: str,
#         engine: mtr.Engine,
#         io: mtr.IO,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         self.grid_quality = grid_quality
#         super().__init__(engine=engine, io=io, handlers=handlers, name=name)

#     def commands(self):
#         grid_quality = dict(low=1, medium=2, high=3)
#         # FIXME: finish implementing this
#         raise NotImplementedError
#         return (
#             5,
#             12,
#             grid_quality[self.grid_quality],
#             "0,0,0",
#             0,
#         )

#     def parse(self, output: str) -> mtr.Quantity:
#         # FIXME: finish implementing this
#         raise NotImplementedError
#         return mtr.MultiwfnOutput(output).get("volume")


class MultiwfnVolume(MultiwfnBaseTask):
    def commands(self):
        integration_mesh_exp = 9  #: int = 9,
        density_isosurface = 1e-3  #: float = 0.001,
        box_size_factor = 1.7  #: float = 1.7
        return (
            100,
            3,
            f"{integration_mesh_exp},{density_isosurface},{box_size_factor}",
            "0,0,0",
            0,
        )

    def parse(self, output: str) -> mtr.Quantity:
        return mtr.MultiwfnOutput(output).get("volume")


# class ExecuteMultiwfn(Task):
#     def __init__(
#         self,
#         input_path: str,
#         engine: mtr.MultiwfnEngine,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(handlers=handlers, name=name)
#         self.input_path = input_path
#         self.engine = engine

#     def run(self) -> None:
#         self.engine.execute(input_path=self.input_path)


# excitations = mtr.QChemOutput(filepath=filepath).get("electronic_excitations")
# excitation_filepath = mtr.expand(f"{io.work_dir}/excitations.txt")
# with open(excitation_filepath, "w") as f:
#     f.write(excitations.to_gaussian())

# inp = mtr.MultiwfnInput(mtr.expand(filepath), *self.commands(excitation_filepath), -10)
# inp.write(io.inp)


# class WriteMultiwfnInput(Task):
#     def __init__(
#         self,
#         input_name: str,
#         in_filepath: str,  # FIXME: awful name for this variable, fix here and analogous issues throughout this file
#         commands: Iterable[str],
#         work_directory: str = ".",
#         handlers: Iterable[Handler] = None,
#         name: str = None,
#     ):
#         super().__init__(handlers=handlers, name=name)
#         self.input_path = mtr.expand(os.path.join(work_directory, input_name))
#         self.in_filepath = mtr.expand(in_filepath)
#         self.commands = commands

#         try:
#             os.makedirs(mtr.expand(work_directory))
#         except FileExistsError:
#             pass

#     def run(self):
#         mtr.MultiwfnInput(self.in_filepath, *self.commands).write(self.input_path)
