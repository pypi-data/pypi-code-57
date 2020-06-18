from __future__ import annotations

import os
import materia as mtr
import re


__all__ = ["VASPInput"]

# FIXME: incomplete - need to add _potcar_str
# FIXME: replace os with pathlib throughout


class VASPInput:
    def __init__(self, settings: mtr.Settings) -> None:
        self.settings = settings

    def write(self, directory: str) -> None:
        with open(mtr.expand(os.path.join(directory), "INCAR"), "w") as f:
            f.write(_incar_str(self.settings["INCAR"]))
        with open(mtr.expand(os.path.join(directory), "POSCAR"), "w") as f:
            f.write(_poscar_str(self.settings["POSCAR"]))
        with open(mtr.expand(os.path.join(directory), "KPOINTS"), "w") as f:
            f.write(_kpoints_str(self.settings["KPOINTS"]))
        with open(mtr.expand(os.path.join(directory), "POTCAR"), "w") as f:
            f.write(_potcar_str(self.settings["POTCAR"]))

    def __str__(self) -> str:
        return "\n".join(
            _block_to_str(block_name=block_name, block_params=block_params)
            for block_name, block_params in self.settings.d.items()
        )


def _block_to_str(block_name: str, block_params) -> str:
    # FIXME: unsure how to annotate type hint for block_params...
    if block_name.lower() == "incar":
        return _incar_str(block_params)
    elif block_name.lower() == "poscar":
        return _poscar_str(block_params)
    elif block_name.lower() == "kpoints":
        return _kpoints_str(block_params)
    elif block_name.lower() == "potcar":
        return _potcar_str(block_params)
    else:
        return ""


def _incar_str(settings: mtr.Settings) -> str:
    s = ""
    try:
        s += str(settings["comment"])
    except KeyError:
        pass
    s += "\n"
    s += (
        "\n".join(
            f"{k} = {v}"
            if (isinstance(v, str) or not hasattr(v, "__iter__"))
            else f"{k} = " + " ".join(f"{x}" for x in v)
            for k, v in settings.items()
        )
        .replace("True", ".TRUE.")
        .replace("False", ".FALSE.")
    )
    return s


def _kpoints_str(settings: mtr.Settings) -> str:
    s = ""
    try:
        s += str(settings["comment"])
    except KeyError:
        pass

    s += "\n"

    try:
        s += str(settings["num_kpoints"]) + "\n"
    except KeyError:
        pass

    try:
        s += str(settings["mesh_type"]) + "\n"
    except KeyError:
        pass

    try:
        num_x, num_y, num_z = settings["grid"]
        s += f"{num_x}  {num_y}  {num_z}\n"
    except KeyError:
        pass

    try:
        shift_x, shift_y, shift_z = settings["shift"]
        s += f"{shift_x}  {shift_y}  {shift_z}\n"
    except KeyError:
        pass

    return s


def _poscar_str(settings: mtr.Settings) -> str:
    s = ""
    try:
        s += str(settings["comment"])
    except KeyError:
        pass

    s += "\n"

    try:
        s += str(settings["scaling"]) + "\n"
    except KeyError:
        pass

    try:
        a_1, a_2, a_3, b_1, b_2, b_3, c_1, c_2, c_3 = settings["bravais_matrix"]
        s += f"{a_1}  {a_2}  {a_3}\n{b_1}  {b_2}  {b_3}\n{c_1}  {c_2}  {c_3}\n"
    except KeyError:
        pass

    try:
        s += " ".join(str(n) for n in settings["num_atoms"]) + "\n"
    except KeyError:
        pass

    try:
        if settings["direct"]:
            direct = True
            s += "Direct\n"
    except KeyError:
        direct = False
    try:
        if settings["cartesian"]:
            cartesian = True
            s += "Cartesian\n"
    except KeyError:
        cartesian = False

    try:
        # FIXME: incorporate direct vs cartesian here (i.e. fractionalize when direct = True)
        structure = settings["structure"]
        s += "\n".join((f"{x}  {y}  {z}" for (x, y, z) in structure.atomic_positions.T))
    except KeyError:
        pass

    return s


# import numpy as np
# import mtr
# from mtr.workflow.interfaces.vasp.input import _incar_str,_kpoints_str,_poscar_str,VASPInput
# s = mtr.Settings()
# s['incar','PREC'] = 'Normal'
# s['incar','ENCUT'] = 550
# s['incar','IBRION'] = -1
# s['incar','NSW'] = 0
# s['incar','ISIF'] = 2
# s['incar','NELMIN'] = 2
# s['incar','EDIFF'] = 1.0e-5
# s['incar','EDIFFG' = -0.02
# s['incar','VOSKOWN'] = 1
# s['incar','NBLOCK'] = 1
# s['incar','NWRITE'] = 1
# s['incar','NELM'] = 60
# s['incar','LUSE_VDW'] = True
# s['incar','LASPH'] = True
# s['incar','AGGAC'] = 0.0000
# s['incar','GGA'] = 'MK'
# s['incar','PARAM1'] = 0.1234
# s['incar','PARAM2'] = 1.0000
# s['incar','ALGO'] = 'Normal (blocked Davidson)'
# s['incar','ISPIN'] = 2
# s['incar','INIWAV'] = 1
# s['incar','ISTART'] = 0
# s['incar','ICHARG'] = 2
# s['incar','LWAVE'] = False
# s['incar','LCHARG'] = False
# s['incar','ADDGRID'] = False
# s['incar','ISMEAR'] = 1
# s['incar','SIGMA'] = 0.2
# s['incar','LREAL'] = False
# s['incar','RWIGS'] = (1.17,0.73)
# s['incar','LDAU'] = True
# s['incar','LDAUTYPE'] = 2
# s['incar','LDAUL'] = (2,-1)
# s['incar','LDAUU'] = (8.00,0.00)
# s['incar','LDAUJ'] = (4.00,0.00)
# s['incar','LDAUPRINT'] = 2
# s['poscar','comment'] = '(Fe2 O3)24  (P1) ~ (COD #9015065)_1_2x2x1_1 0 0 1  surface_1 (#1)_2x2x1_1 (MD #5) (VASP)'
# s['poscar','scaling'] = 1.0
# s['poscar','bravais_matrix'] = np.hstack([[10.0498,0,0],[0,8.7034,0],[0,0,28.7163]])
# s['poscar','Direct'] = True
# s['poscar','num_atoms'] = (48,72)
# s['kpoints','comment'] = 'Automatic grid'
# s['kpoints','mesh_type'] = 'Gamma'
# s['kpoints','grid'] = (4,4,1)
# s['kpoints','shift'] = (0.0,0.0,0.0)
# print(VASPInput(s))


# from __future__ import annotations
# import cclib
# import os
# import mtr
# import subprocess
# from typing import Any, Iterable, Optional

# from ...workflow.tasks.task import Task

# __all__ = ["ExecuteVASP"]


# class ExecuteVASP(Task):
#     def __init__(
#         self,
#         output_name: str,
#         executable: str = "vasp_std",
#         work_directory: str = ".",
#         num_cores: int = 1,
#         parallel: bool = False,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__()
#         self.settings["executable"] = executable
#         self.settings["output_path"] = os.path.join(
#             work_directory, mtr.expand(output_name)
#         )
#         self.settings["work_directory"] = mtr.expand(work_directory)

#         self.settings["num_cores"] = num_cores
#         self.settings["parallel"] = parallel

#         try:
#             os.makedirs(self.settings["work_directory"])
#         except FileExistsError:
#             pass

#     def run(self, **kwargs: Any) -> Any:
#         with open(self.settings["output_path"], "w") as f:
#             if self.settings["parallel"]:
#                 subprocess.call(
#                     [
#                         "mpirun",
#                         "np",
#                         str(self.settings["num_cores"]),
#                         self.settings["executable"],
#                     ],
#                     stdout=f,
#                     stderr=subprocess.STDOUT,
#                 )
#             else:
#                 subprocess.call([self.settings["executable"]], stdout=f)
