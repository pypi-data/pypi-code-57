from __future__ import annotations
from typing import Dict, Iterable, Optional

import materia as mtr
import pathlib

from .engine import Engine

__all__ = ["CCDC", "CCDCInput", "CCDCOutput"]


class CCDCInput:
    """
    Interface to write inputs which can be run with CCDC.

    Attributes:
        ccdc_script (str): String representation of CCDC input.
    """

    def __init__(self, ccdc_script: str) -> None:
        self.ccdc_script = ccdc_script

    def __str__(self) -> str:
        """
        Get string representation of CCDC input.
        """
        return self.ccdc_script

    def write(self, filepath: str) -> None:
        """
        Write CCDC input to a file.

        Args:
            filepath: Path to file to which the input will be written. Can be an absolute or a relative path.
        """
        with open(mtr.expand(filepath), "w") as f:
            f.write(str(self))


class CCDCOutput:
    """
    Interface for outputs from tasks run with CCDC.

    Attributes:
        filepath (str): Absolute path to file from which output will be read.
    """

    def __init__(self, filepath: str) -> None:
        """
        Args:
            filepath: Path to file from which output will be read. Can be an absolute or a relative path.
        """
        self.filepath = mtr.expand(filepath)
        # FIXME: implement
        raise NotImplementedError


class CCDC(Engine):
    def __init__(
        self,
        ccdc_root: str,
        num_processors: Optional[int] = None,
        num_threads: Optional[int] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> None:
        self.ccdc_root = mtr.expand(ccdc_root)
        # FIXME: generalize past 2019 version of CCDC code
        executable = mtr.expand(
            pathlib.Path(
                self.ccdc_root, "Python_API_2019", "miniconda", "bin", "python"
            )
        )
        super().__init__(executable, num_processors, num_threads, arguments)

    def env(self) -> Dict[str, str]:
        # FIXME: generalize past 2019 version of CCDC code
        return {"CSDHOME": mtr.expand(pathlib.Path(self.ccdc_root, "CSD_2019"))}


# from __future__ import annotations
# import os
# import mtr
# import textwrap
# from typing import Iterable, Optional

# from ...workflow.tasks.task import Task

# __all__ = ["CCDCUnitCellStructure"]


# class CCDCUnitCellStructure(Task):
#     def __init__(
#         self,
#         input_name: str,
#         molecule_name: str,
#         engine: mtr.CCDCEngine,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         self.input_name = input_name
#         self.engine = engine
#         name = "'" + molecule_name + "'"
#         self.input_string = textwrap.dedent(
#             f"""\
#                     import numpy as np
#                     import ccdc.search
#                     tns = ccdc.search.TextNumericSearch()
#                     tns.add_compound_name({name})
#                     try:
#                         hit = next(hit for hit in tns.search() if hit.entry.chemical_name == {name})
#                         print('atomic_symbols: {{0}}\\n'.format(tuple(a.atomic_symbol for a in hit.molecule.atoms)))
#                         print('coordinates: {{0}}\\n'.format(np.vstack([a.coordinates for a in hit.molecule.atoms])))
#                         print('spacegroup_number_and_setting: {{0}}\\n'.format(hit.crystal.spacegroup_number_and_setting))
#                         print('cell_lengths: {{0}}\\n'.format(np.array(hit.crystal.cell_lengths)))
#                         print('cell_angles: {{0}}\\n'.format(np.array(hit.crystal.cell_angles)))
#                     except StopIteration:
#                         pass
#                     """
#         )

#     def run(self):
#         # FIXME: catch StopIteration in CCDC code
#         # FIXME: generalize past 2019 version of CCDC code
#         # FIXME: add more rigorous/better checking for CCDC crystal matches

#         # FIXME: where does input_path come from? must include self.input_name but also must include engine.work_dir...
#         mtr.CCDCInput(ccdc_script=self.input_string).write(self.input_path)

#         self.engine.execute(input_path=self.input_path)
