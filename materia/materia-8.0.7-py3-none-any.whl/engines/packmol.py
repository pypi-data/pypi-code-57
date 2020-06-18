from __future__ import annotations
from typing import Iterable, Optional, Tuple

import materia as mtr
import numpy as np

from .engine import Engine
from ..tasks import ExternalTask

__all__ = ["Packmol", "PackmolInput"]


class Packmol(Engine):
    def __init__(self, executable: Optional[str] = "packmol") -> None:
        super().__init__(executable=executable)

    def solvate(
        self,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> PackmolSolvate:
        return PackmolSolvate(engine=self, io=io, handlers=handlers, name=name)


class PackmolSolvate(ExternalTask):
    def _packing_params(
        self, shells: int, number_density: Optional[mtr.Quantity] = None
    ) -> Tuple[int, mtr.Quantity]:
        # these are the ideal gas packing values:
        n = int((2 / 3) * shells ** 3)
        sphere_radius = shells * (2 * np.pi * number_density) ** (-1 / 3)

        return n, sphere_radius

    def run(
        self,
        solute: mtr.Molecule,
        solvent: mtr.Molecule,
        shells: int,
        tolerance: float,
        solvent_density: mtr.Quantity,
    ) -> mtr.Molecule:
        if solvent_density.dimension == mtr.Dimension(M=1, L=-3):
            number_density = solvent_density / solvent.mass
        else:
            number_density = solvent_density

        n, sphere_radius = self._packing_params(
            shells=shells, number_density=number_density
        )

        with self.io() as io:
            inp = mtr.PackmolInput(
                tolerance=tolerance,
                filetype="xyz",
                output_name=mtr.expand(path="packed", dir=io.work_dir),
            )

            if isinstance(solute, str):
                solute_cm = contextlib.nullcontext(solute)
            else:
                solute_cm = solute.tempfile(suffix=".xyz", dir=io.work_dir)

            if isinstance(solvent, str):
                solvent_cm = contextlib.nullcontext(solvent)
            else:
                solvent_cm = solvent.tempfile(suffix=".xyz", dir=io.work_dir)

            with solute_cm as f, solvent_cm as g:
                inp.add_structure(
                    structure_filepath=mtr.expand(
                        path=f.name if hasattr(f, "name") else f, dir=io.work_dir
                    ),
                    number=1,
                    instructions=["fixed 0. 0. 0. 0. 0. 0."],
                )

                inp.add_structure(
                    structure_filepath=mtr.expand(
                        path=g.name if hasattr(g, "name") else g, dir=io.work_dir
                    ),
                    number=n - 1,
                    instructions=[
                        f"inside sphere 0. 0. 0. {sphere_radius.convert(mtr.angstrom).value}"
                    ],
                )

                inp.write(io.inp)

                self.engine.execute(self.io)

                return mtr.Molecule(mtr.expand(path="packed.xyz", dir=io.work_dir))


# ------------------------- INPUT ---------------------------- #


class PackmolInput:
    def __init__(
        self,
        tolerance: float,
        filetype: str,
        output_name: str,
        instructions: Optional[Iterable[str]] = None,
    ) -> None:
        self.tolerance = tolerance
        self.filetype = filetype
        self.output_name = output_name
        self.instructions = instructions or []
        self.structures = []

    def add_structure(
        self,
        structure_filepath: str,
        number: int,
        instructions: Optional[Iterable[str]] = None,
    ) -> None:
        self.structures.append((structure_filepath, number, instructions or []))

    def __str__(self) -> str:
        return (
            f"tolerance {self.tolerance}\noutput {self.output_name}.{self.filetype}\nfiletype {self.filetype}\n\n"
            + "\n".join(
                f"structure {sfp}\n  number {n}\n"
                + "".join(f"  {i}\n" for i in inst)
                + "end structure\n"
                for sfp, n, inst in self.structures
            )
        )

    def write(self, filepath: str) -> None:
        with open(mtr.expand(filepath), "w") as f:
            f.write(str(self))


# class PackmolInput:
#     def __init__(
#         self,
#         tolerance: float,
#         filetype: str,
#         output_name: str,
#         structures: Iterable[PackmolStructure],
#         instructions: Optional[Iterable[str]] = None,
#     ) -> None:
#         self.tolerance = tolerance
#         self.filetype = filetype
#         self.output_name = output_name
#         self.structures = structures
#         self.instructions = instructions or []

#     def _write_structure(self, structure, tmpdir):
#         while True:
#             filepath = os.path.join(tmpdir, f"{uuid.uuid4().hex}.{self.filetype}")
#             try:
#                 structure.write(mtr.expand(filepath))  # , overwrite=False
#                 break
#             except FileExistsError:
#                 continue

#         return filepath

#     def _structure_blocks(self, tmpdir, structure, number, structure_instructions):
#         filepath = (
#             structure
#             if isinstance(structure, str)
#             else self._write_structure(structure=structure, tmpdir=tmpdir)
#         )

#         return (
#             f"structure {filepath}\n  number {number}\n"
#             + "".join(f"  {i}\n" for i in structure_instructions)
#             + "end structure\n"
#         )

#     def __str__(self) -> str:
#         with tempfile.TemporaryDirectory(".") as tmpdir:
#             # structure_blocks = tuple(
#             #     self._structure_blocks(
#             #         tmpdir=tmpdir, structure=s, number=n, structure_instructions=si
#             #     )
#             #     for s, n, si in zip(
#             #         self.structures, self.numbers, self.structure_instructions
#             #     )
#             # )
#             for s in self.structures:
#                 while s.filepath is None:
#                     filepath = os.path.join(
#                         tmpdir, f"{uuid.uuid4().hex}.{self.filetype}"
#                     )
#                     try:
#                         s.write(mtr.expand(filepath))  # , overwrite=False
#                     except FileExistsError:
#                         continue

#             return (
#                 f"tolerance {self.tolerance}\noutput {self.output_name}.{self.filetype}\nfiletype {self.filetype}\n\n"
#                 + "\n".join(str(s) for s in self.structures)
#             )

#     def write(self, filepath: str) -> None:
#         with open(mtr.expand(filepath), "w") as f:
#             f.write(str(self))


# class PackmolStructure:
#     def __init__(
#         self,
#         structure: Union[mtr.Structure, str],
#         number: int,
#         instructions: Optional[Iterable[str]] = None,
#     ) -> None:
#         if isinstance(structure, str):
#             self.structure = None
#             self.filepath = mtr.expand(structure)
#         else:
#             self.structure = structure
#             self.filepath = None
#         self.number = number
#         self.instructions = instructions or []

#     def __str__(self) -> str:
#         return (
#             f"structure {self.filepath}\n  number {self.number}\n"
#             + "".join(f"  {i}\n" for i in self.instructions)
#             + "end structure\n"
#         )

#     def write(self, filepath: str) -> None:
#         if self.structure is not None:
#             self.structure.write(mtr.expand(filepath))
#             self.filepath = mtr.expand(filepath)


# class PackmolInput:
#     def __init__(
#         self,
#         tolerance: float,
#         output_filename: str,
#         output_filetype=None,
#         structure_blocks=(),
#         restart_to=None,
#         restart_from=None,
#         discale=None,
#         maxit=None,
#         movebadrandom=False,
#         add_amber_ter=False,
#         add_box_sides=None,
#         sidemax=None,
#         seed=None,
#         randominitialpoint=False,
#         avoid_overlap=None,
#         nloop=None,
#         precision=None,
#         writeout=None,
#         writebad=False,
#         iprint1=None,
#         iprint2=None,
#         fbins=None,
#         chkgrad=False,
#         use_short_tol=False,
#         short_tol_dist=None,
#         short_tol_scale=None,
#     ) -> None:
#         """Short summary.
#
#         Parameters
#         ----------
#         tolerance : type
#             Required distance tolerance (for systems at room temperature and pressure and coordinates in Angstroms, 2.0 Å is a good value). Some users have observed that with the 2.0 Angs tolerance some cyclic systems (toluene, for example) may eventually get linked during packing. If you observe that kind of behaviour, a small increase on the distance tolerance probably will solve your problem. For coarse-grained models, which are not atomistic, the distance tolerance desired might be larger than that generally used for atomistic systems. However, this is not always the case, as the usual tolerance may well be large enough to guarantee a proper initial packing of the system.
#         output_filename : string
#             Name of the output file to be created.
#         output_filetype : string
#             Format of the output file (pdb, tinker, xyz, or moldy). If `output_filetype` is None, then it will be inferred from the extension of `output_filename`.
#         structure_blocks: type
#             StructureBlock objects whose contents should be added to the input file.
#         restart_to : type
#             This option tells Packmol to write restart information to the specified file.
#         restart_from : type
#             This option tells Packmol to read restart information from the specified file.
#         discale : type
#             This option controls the distance tolerance actually used in the local optimization method. It was found that using larger distances helps sometimes. Try setting discale to 1.5, for example.
#         maxit : type
#             This is the maximum number of iterations of the local optimizer (GENCAN) per loop. The default value is currently 20, changing it may improve (or worse) the convergence.
#         movebadrandom : type
#             One of the convergence heuristics of Packmol consists in moving molecules that are badly placed. If this option is set, the molecules will be placed in new random position in the box. If not (default), the molecules are moved to positions nearby molecules that are well packed. Using this option can help when the restraints are complex, but will probably be bad if there are large structures, because the new random position might overlap with those..
#         add_amber_ter : type
#             Add the TER flag betwen every molecule (AMBER uses this).
#         add_box_sides : type
#             Add box side information to output PDB File (GROMACS uses this), where the `1.0` is an optional real number that will be added to the length of each side, if the actual sides of your simulation box will not be exactly the same as the maximum and minimum coordinates of the molecules of the system (usually, if you are using periodic boundary conditions, you may want to add `1.0` to avoid clashes at the boundary).
#         sidemax : type
#             Increase maximum system dimensions. `sidemax` is used to build an initial approximation of the molecular distribution. Increase `sidemax` if your system is very large, or your system may look cut out by this maximum dimension. All system coordinates must fit within `-sidemax` and `+sidemax`, and using a `sidemax` that approximately fits your system may accelerate a little bit the packing calculation.
#         seed : type
#             Change random number generator seed. Use `-1` to generate a seed automatically from the computer time.
#         randominitialpoint : type
#             Use a truly random initial point for the minimization (the default option is to generate a roughly homogeneous-density initial approximation).
#         avoid_overlap : type
#             Avoid, or not, overlap with fixed molecules at initial point (avoiding this overlaps is generally recommended, but sometimes generates gaps that are too large).
#         nloop : type
#             Change the maximum number of optimization loops.
#         precision : type
#             Change the precision required for the solution: how close the solution must be to the desired distances to be considered correct.
#         writeout : type
#             Change the frequency of output file writing.
#         writebad : type
#             Write the current point to output file even if it is worse than the the best point so far (used for checking purposes only).
#         iprint1 : type
#             Change the optimization subroutine printing output.
#         iprint2 : type
#             Change the optimization subroutine printing output.
#         fbins : type
#             Change the number of bins of the linked-cell method (technical).
#         chkgrad : boolean
#             Compare analytical and finite-difference gradients: This is only for testing purposes. Writes chkgrad.log file containing the comparison.
#         use_short_tol : boolean
#             These options define a new penalty tolerance for short distances, to increase the repulsion between atoms when they are too close to each other. The "use" parameter turns on this feature, using default parameters (dist=tolerance/2; scale=3).
#         short_tol_dist : float
#              These options define a new penalty tolerance for short distances, to increase the repulsion between atoms when they are too close to each other. The "dist" parameter defines from which distance the penalty is applied. This affects the penalty of all atoms. Remember that the "tolerance" is twice the size of the "radius" of each atom.
#         short_tol_scale : float
#             These options define a new penalty tolerance for short distances, to increase the repulsion between atoms when they are too close to each other. The "scale" parameter how greater this penalty is relative to the default penalty. This affects the penalty of all atoms. Remember that the "tolerance" is twice the size of the "radius" of each atom.
#         """
#         self.tolerance = tolerance
#         self.output_filename = output_filename
#         self.output_filetype = output_filetype
#         self.structure_blocks = structure_blocks
#         self.restart_to = restart_to
#         self.restart_from = restart_from
#         self.discale = discale
#         self.maxit = maxit
#         self.movebadrandom = movebadrandom
#         self.add_amber_ter = add_amber_ter
#         self.add_box_sides = add_box_sides
#         self.sidemax = sidemax
#         self.seed = seed
#         self.randominitialpoint = randominitialpoint
#         self.avoid_overlap = avoid_overlap
#         self.nloop = nloop
#         self.precision = precision
#         self.writeout = writeout
#         self.writebad = writebad
#         self.iprint1 = iprint1
#         self.iprint2 = iprint2
#         self.fbins = fbins
#         self.chkgrad = chkgrad
#         self.use_short_tol = use_short_tol
#         self.short_tol_dist = short_tol_dist
#         self.short_tol_scale = short_tol_scale
#
#     def write(self, filepath: str) -> None:
#         with open(mtr.expand(filepath), "w") as f:
#             f.write(str(self))
#
#     def __str__(self) -> str:
#         s = f"tolerance {self.tolerance}\n"
#         s += f"output {self.output_filename}\n"
#         if self.output_filetype is None:
#             *_, output_filetype = self.output_filename.split(".")
#             s += f"filetype {output_filetype}\n"
#         else:
#             s += f"filetype {self.output_filetype}\n"
#         s += f"restart_to {self.restart_to}\n" if self.restart_to is not None else ""
#         s += (
#             f"restart_from {self.restart_from}\n"
#             if self.restart_from is not None
#             else ""
#         )
#         s += f"discale {self.discale}\n" if self.discale is not None else ""
#         s += f"maxit {self.maxit}\n" if self.maxit is not None else ""
#         s += f"movebadrandom\n" if self.movebadrandom else ""
#         s += f"add_amber_ter\n" if self.add_amber_ter else ""
#         s += (
#             f"add_box_sides {self.add_box_sides}\n"
#             if self.add_box_sides is not None
#             else ""
#         )
#         s += (
#             f'sidemax {".d".join(self.sidemax.split("."))}\n'
#             if self.sidemax is not None
#             else ""
#         )
#         s += f"seed {self.seed}\n" if self.seed is not None else ""
#         s += f"randominitialpoint\n" if self.randominitialpoint else ""
#         s += (
#             f'avoid_overlap {"yes" if self.avoid_overlap else "no"}\n'
#             if self.avoid_overlap
#             else ""
#         )
#         s += f"nloop {self.nloop}\n" if self.nloop is not None else ""
#         s += f"precision {self.precision}\n" if self.precision is not None else ""
#         s += f"writeout {self.writeout}\n" if self.writeout is not None else ""
#         s += f"writebad\n" if self.writebad else ""
#         s += f"iprint1 {self.iprint1}\n" if self.iprint1 is not None else ""
#         s += f"iprint2 {self.iprint2}\n" if self.iprint2 is not None else ""
#         s += f"fbins {self.fbins}\n" if self.fbins is not None else ""
#         s += f"chkgrad {self.chkgrad}\n" if self.chkgrad else ""
#         s += f"use_short_tol {self.use_short_tol}\n" if self.use_short_tol else ""
#         s += (
#             f"short_tol_dist {self.short_tol_dist}\n"
#             if self.short_tol_dist is not None
#             else ""
#         )
#         s += (
#             f"short_tol_scale {self.short_tol_scale}\n"
#             if self.short_tol_scale is not None
#             else ""
#         )
#         s += "\n".join(str(sb) for sb in self.structure_blocks)
#         # FIXME: include all the other self attribute strings
#         return s
#
#
# class PackmolStructureBlock:
#     def __init__(
#         self,
#         molecule_structure_file,
#         number,
#         constraints=(),
#         atoms_blocks=(),
#         radius=None,
#         residue_number=None,
#         restart_to=None,
#         restart_from=None,
#         fscale=None,
#         short_radius=None,
#         short_radius_scale=None,
#         nloop=None,
#     ):
#         self.molecule_structure_file = mtr.expand(molecule_structure_file)
#         self.number = number
#         self.constraints = constraints
#         self.atoms_blocks = atoms_blocks
#         self.radius = radius
#         self.residue_number = residue_number
#         self.restart_to = restart_to
#         self.restart_from = restart_from
#         self.fscale = fscale
#         self.short_radius = short_radius
#         self.short_radius_scale = short_radius_scale
#         self.nloop = nloop
#
#     def __str__(self) -> str:
#         s = "structure "
#         s += f"{self.molecule_structure_file}\n"
#         s += f"  number {self.number}\n"
#         s += "".join(f"  {str(c)}\n" for c in self.constraints)
#         s += "".join(f"  {str(ab)}\n" for ab in self.atoms_blocks)
#         s += f"  radius {radius}\n" if self.radius is not None else ""
#         s += (
#             f"  resnumber {self.residue_number}\n"
#             if self.residue_number is not None
#             else ""
#         )
#         s += f"  restart_to {self.restart_to}\n" if self.restart_to is not None else ""
#         s += (
#             f"  restart_to {self.restart_from}\n"
#             if self.restart_from is not None
#             else ""
#         )
#         s += f"  fscale {self.fscale}\n" if self.fscale is not None else ""
#         s += (
#             f"  short_radius {self.short_radius}\n"
#             if self.short_radius is not None
#             else ""
#         )
#         s += (
#             f"  short_radius_scale {self.short_radius_scale}\n"
#             if self.short_radius_scale is not None
#             else ""
#         )
#         s += f"  nloop {self.nloop}\n" if self.nloop is not None else ""
#         s += "end structure\n"
#
#         return s
#
#
# class PackmolAtomsBlock:
#     def __init(
#         self,
#         atoms,
#         constraints=(),
#         radius=None,
#         fscale=None,
#         short_radius=None,
#         short_radius_scale=None,
#     ):
#         self.atoms = atoms
#         self.constraints = constraints
#         self.radius = radius
#         self.fscale = fscale
#         self.short_radius = short_radius
#         self.short_radius_scale = short_radius_scale
#
#     def __str__(self) -> str:
#         atoms_str = " ".join(str(a) for a in atoms)
#         constraints_str = "".join(f"  {str(c)}\n" for c in self.constraints)
#         radius_str = f"  radius {radius}\n" if self.radius is not None else ""
#         fscale_str = f"  fscale {self.fscale}\n" if self.fscale is not None else ""
#         short_radius_str = (
#             f"  short_radius {self.short_radius}\n"
#             if self.short_radius is not None
#             else ""
#         )
#         short_radius_scale_str = (
#             f"  short_radius_scale {self.short_radius_scale}\n"
#             if self.short_radius_scale is not None
#             else ""
#         )
#
#         return (
#             f"atoms {atoms_str}\n"
#             + constraints_str
#             + radius_str
#             + fscale_str
#             + short_radius_str
#             + short_radius_scale_str
#             + "end atoms\n"
#         )
#
#
# # CONSTRAINTS
#
#
# class PackmolFixed:
#     def __init__(self, x, y, z, a, b, c) -> None:
#         self.x = x
#         self.y = y
#         self.z = z
#         self.a = a
#         self.b = b
#         self.c = c
#
#     def __str__(self) -> str:
#         return f"fixed {self.x} {self.y} {self.z} {self.a} {self.b} {self.c}"
#
#
# class PackmolCube:
#     def __init__(self, xmin, ymin, zmin, d, inside) -> None:
#         self.xmin = xmin
#         self.ymin = ymin
#         self.zmin = zmin
#         self.d = d
#         self.inside_outside = "inside" if inside else "outside"
#
#     def __str__(self) -> str:
#         return (
#             f"{self.inside_outside} cube {self.xmin} {self.ymin} {self.zmin} {self.d}"
#         )
#
#
# class PackmolBox:
#     def __init__(self, xmin, ymin, zmin, xmax, ymax, zmax, inside) -> None:
#         self.xmin = xmin
#         self.ymin = ymin
#         self.zmin = zmin
#         self.xmax = xmax
#         self.ymax = ymax
#         self.zmax = zmax
#         self.inside_outside = "inside" if inside else "outside"
#
#     def __str__(self) -> str:
#         return f"{self.inside_outside} box {self.xmin} {self.ymin} {self.zmin} {self.xmax} {self.ymax} {self.zmax}"
#
#
# class PackmolSphere:
#     def __init__(self, a, b, c, d, inside) -> None:
#         self.a = a
#         self.b = b
#         self.c = c
#         self.d = d
#         self.inside_outside = "inside" if inside else "outside"
#
#     def __str__(self) -> str:
#         return f"{self.inside_outside} sphere {self.a} {self.b} {self.c} {self.d}"
#
#
# class PackmolEllipsoid:
#     def __init__(self, a1, b1, c1, a2, b2, c2, d, inside) -> None:
#         self.a1 = a1
#         self.b1 = b1
#         self.c1 = c1
#         self.a2 = a2
#         self.b2 = b2
#         self.c2 = c2
#         self.d = d
#         self.inside_outside = "inside" if inside else "outside"
#
#     def __str__(self) -> str:
#         return f"{self.inside_outside} ellipsoid {self.a1} {self.b1} {self.c1} {self.a2} {self.b2} {self.c2} {self.d}"
#
#
# class PackmolPlane:
#     def __init__(self, a, b, c, d, over) -> None:
#         self.a = a
#         self.b = b
#         self.c = c
#         self.d = d
#         self.over_below = "over" if over else "below"
#
#     def __str__(self) -> str:
#         return f"{self.over_below} plane {self.a} {self.b} {self.c} {self.d}"
#
#
# class PackmolCylinder:
#     def __init__(self, a1, b1, c1, a2, b2, c2, d, l, inside) -> None:
#         self.a1 = a1
#         self.b1 = b1
#         self.c1 = c1
#         self.a2 = a2
#         self.b2 = b2
#         self.c2 = c2
#         self.d = d
#         self.l = l
#         self.inside_outside = "inside" if inside else "outside"
#
#     def __str__(self) -> str:
#         return f"{self.inside_outside} cylinder {self.a1} {self.b1} {self.c1} {self.a2} {self.b2} {self.c2} {self.d} {self.l}"
#
#
# class PackmolConstrainRotation:
#     def __init__(self, axis, angle, variance) -> None:
#         self.axis = axis
#         self.angle = angle
#         self.variance = variance
#
#     def __str__(self) -> str:
#         return f"constrain_rotation {self.axis} {self.angle} {self.variance}"
#
#
# # import mtr
# #
# # class PackmolInput:
# #     def __init__(self, tolerance, output_filename, output_filetype=None, structure_blocks=(), restart_to=None, restart_from=None, discale=None,
# #                  maxit=None, movebadrandom=False, add_amber_ter=False, add_box_sides=None, sidemax=None, seed=None, randominitialpoint=False,
# #                  avoid_overlap=None, nloop=None, precision=None, writeout=None, writebad=False, iprint1=None, iprint2=None, fbins=None,
# #                  chkgrad=False, use_short_tol=False, short_tol_dist=None, short_tol_scale=None):
# #         """Short summary.
# #
# #         Parameters
# #         ----------
# #         tolerance : type
# #             Required distance tolerance (for systems at room temperature and pressure and coordinates in Angstroms, 2.0 Å is a good value). Some users have observed that with the 2.0 Angs tolerance some cyclic systems (toluene, for example) may eventually get linked during packing. If you observe that kind of behaviour, a small increase on the distance tolerance probably will solve your problem. For coarse-grained models, which are not atomistic, the distance tolerance desired might be larger than that generally used for atomistic systems. However, this is not always the case, as the usual tolerance may well be large enough to guarantee a proper initial packing of the system.
# #         output_filename : string
# #             Name of the output file to be created.
# #         output_filetype : string
# #             Format of the output file (pdb, tinker, xyz, or moldy). If `output_filetype` is None, then it will be inferred from the extension of `output_filename`.
# #         structure_blocks: type
# #             StructureBlock objects whose contents should be added to the input file.
# #         restart_to : type
# #             This option tells Packmol to write restart information to the specified file.
# #         restart_from : type
# #             This option tells Packmol to read restart information from the specified file.
# #         discale : type
# #             This option controls the distance tolerance actually used in the local optimization method. It was found that using larger distances helps sometimes. Try setting discale to 1.5, for example.
# #         maxit : type
# #             This is the maximum number of iterations of the local optimizer (GENCAN) per loop. The default value is currently 20, changing it may improve (or worse) the convergence.
# #         movebadrandom : type
# #             One of the convergence heuristics of Packmol consists in moving molecules that are badly placed. If this option is set, the molecules will be placed in new random position in the box. If not (default), the molecules are moved to positions nearby molecules that are well packed. Using this option can help when the restraints are complex, but will probably be bad if there are large structures, because the new random position might overlap with those..
# #         add_amber_ter : type
# #             Add the TER flag betwen every molecule (AMBER uses this).
# #         add_box_sides : type
# #             Add box side information to output PDB File (GROMACS uses this), where the `1.0` is an optional real number that will be added to the length of each side, if the actual sides of your simulation box will not be exactly the same as the maximum and minimum coordinates of the molecules of the system (usually, if you are using periodic boundary conditions, you may want to add `1.0` to avoid clashes at the boundary).
# #         sidemax : type
# #             Increase maximum system dimensions. `sidemax` is used to build an initial approximation of the molecular distribution. Increase `sidemax` if your system is very large, or your system may look cut out by this maximum dimension. All system coordinates must fit within `-sidemax` and `+sidemax`, and using a `sidemax` that approximately fits your system may accelerate a little bit the packing calculation.
# #         seed : type
# #             Change random number generator seed. Use `-1` to generate a seed automatically from the computer time.
# #         randominitialpoint : type
# #             Use a truly random initial point for the minimization (the default option is to generate a roughly homogeneous-density initial approximation).
# #         avoid_overlap : type
# #             Avoid, or not, overlap with fixed molecules at initial point (avoiding this overlaps is generally recommended, but sometimes generates gaps that are too large).
# #         nloop : type
# #             Change the maximum number of optimization loops.
# #         precision : type
# #             Change the precision required for the solution: how close the solution must be to the desired distances to be considered correct.
# #         writeout : type
# #             Change the frequency of output file writing.
# #         writebad : type
# #             Write the current point to output file even if it is worse than the the best point so far (used for checking purposes only).
# #         iprint1 : type
# #             Change the optimization subroutine printing output.
# #         iprint2 : type
# #             Change the optimization subroutine printing output.
# #         fbins : type
# #             Change the number of bins of the linked-cell method (technical).
# #         chkgrad : boolean
# #             Compare analytical and finite-difference gradients: This is only for testing purposes. Writes chkgrad.log file containing the comparison.
# #         use_short_tol : boolean
# #             These options define a new penalty tolerance for short distances, to increase the repulsion between atoms when they are too close to each other. The "use" parameter turns on this feature, using default parameters (dist=tolerance/2; scale=3).
# #         short_tol_dist : float
# #              These options define a new penalty tolerance for short distances, to increase the repulsion between atoms when they are too close to each other. The "dist" parameter defines from which distance the penalty is applied. This affects the penalty of all atoms. Remember that the "tolerance" is twice the size of the "radius" of each atom.
# #         short_tol_scale : float
# #             These options define a new penalty tolerance for short distances, to increase the repulsion between atoms when they are too close to each other. The "scale" parameter how greater this penalty is relative to the default penalty. This affects the penalty of all atoms. Remember that the "tolerance" is twice the size of the "radius" of each atom.
# #         """
# #         self.tolerance = tolerance
# #         self.output_filename = output_filename
# #         self.output_filetype = output_filetype
# #         self.structure_blocks = structure_blocks
# #         self.restart_to = restart_to
# #         self.restart_from = restart_from
# #         self.discale = discale
# #         self.maxit = maxit
# #         self.movebadrandom = movebadrandom
# #         self.add_amber_ter = add_amber_ter
# #         self.add_box_sides = add_box_sides
# #         self.sidemax = sidemax
# #         self.seed = seed
# #         self.randominitialpoint = randominitialpoint
# #         self.avoid_overlap = avoid_overlap
# #         self.nloop = nloop
# #         self.precision = precision
# #         self.writeout = writeout
# #         self.writebad = writebad
# #         self.iprint1 = iprint1
# #         self.iprint2 = iprint2
# #         self.fbins = fbins
# #         self.chkgrad = chkgrad
# #         self.use_short_tol = use_short_tol
# #         self.short_tol_dist = short_tol_dist
# #         self.short_tol_scale = short_tol_scale
# #
# #     def write(self, filepath):
# #         with open(mtr.expand(filepath),'w') as f:
# #             f.write(str(self))
# #
# #     def __str__(self) -> str:
# #         s = f'tolerance {self.tolerance}\n'
# #         s += f'output {self.output_filename}\n'
# #         if self.output_filetype is None:
# #             *_,output_filetype = self.output_filename.split('.')
# #             s += f'filetype {output_filetype}\n'
# #         else:
# #             s += f'filetype {self.output_filetype}\n'
# #         s += f'restart_to {self.restart_to}\n' if self.restart_to is not None else ''
# #         s += f'restart_from {self.restart_from}\n' if self.restart_from is not None else ''
# #         s += f'discale {self.discale}\n' if self.discale is not None else ''
# #         s += f'maxit {self.maxit}\n' if self.maxit is not None else ''
# #         s += f'movebadrandom\n' if self.movebadrandom else ''
# #         s += f'add_amber_ter\n' if self.add_amber_ter else ''
# #         s += f'add_box_sides {self.add_box_sides}\n' if self.add_box_sides is not None else ''
# #         s += f'sidemax {".d".join(self.sidemax.split("."))}\n' if self.sidemax is not None else ''
# #         s += f'seed {self.seed}\n' if self.seed is not None else ''
# #         s += f'randominitialpoint\n' if self.randominitialpoint else ''
# #         s += f'avoid_overlap {"yes" if self.avoid_overlap else "no"}\n' if self.avoid_overlap else ''
# #         s += f'nloop {self.nloop}\n' if self.nloop is not None else ''
# #         s += f'precision {self.precision}\n' if self.precision is not None else ''
# #         s += f'writeout {self.writeout}\n' if self.writeout is not None else ''
# #         s += f'writebad\n' if self.writebad else ''
# #         s += f'iprint1 {self.iprint1}\n' if self.iprint1 is not None else ''
# #         s += f'iprint2 {self.iprint2}\n' if self.iprint2 is not None else ''
# #         s += f'fbins {self.fbins}\n' if self.fbins is not None else ''
# #         s += f'chkgrad {self.chkgrad}\n' if self.chkgrad else ''
# #         s += f'use_short_tol {self.use_short_tol}\n' if self.use_short_tol else ''
# #         s += f'short_tol_dist {self.short_tol_dist}\n' if self.short_tol_dist is not None else ''
# #         s += f'short_tol_scale {self.short_tol_scale}\n' if self.short_tol_scale is not None else ''
# #         s += '\n'.join(str(sb) for sb in self.structure_blocks)
# #         # FIXME: include all the other self attribute strings
# #         return s
# #
# # class PackmolStructureBlock:
# #     def __init__(self, molecule_structure_file, number, constraints=(), atoms_blocks=(), radius=None, residue_number=None, restart_to=None, restart_from=None,
# #                  fscale=None, short_radius=None, short_radius_scale=None, nloop=None):
# #         self.molecule_structure_file = mtr.expand(molecule_structure_file)
# #         self.number = number
# #         self.constraints = constraints
# #         self.atoms_blocks = atoms_blocks
# #         self.radius = radius
# #         self.residue_number = residue_number
# #         self.restart_to = restart_to
# #         self.restart_from = restart_from
# #         self.fscale = fscale
# #         self.short_radius = short_radius
# #         self.short_radius_scale = short_radius_scale
# #         self.nloop = nloop
# #
# #     def __str__(self) -> str:
# #         s = 'structure '
# #         s += f'{self.molecule_structure_file}\n'
# #         s += f'  number {self.number}\n'
# #         s += ''.join(f'  {str(c)}\n' for c in self.constraints)
# #         s += ''.join(f'  {str(ab)}\n' for ab in self.atoms_blocks)
# #         s += f'  radius {radius}\n' if self.radius is not None else ''
# #         s += f'  resnumber {self.residue_number}\n' if self.residue_number is not None else ''
# #         s += f'  restart_to {self.restart_to}\n' if self.restart_to is not None else ''
# #         s += f'  restart_to {self.restart_from}\n' if self.restart_from is not None else ''
# #         s += f'  fscale {self.fscale}\n' if self.fscale is not None else ''
# #         s += f'  short_radius {self.short_radius}\n' if self.short_radius is not None else ''
# #         s += f'  short_radius_scale {self.short_radius_scale}\n' if self.short_radius_scale is not None else ''
# #         s += f'  nloop {self.nloop}\n' if self.nloop is not None else ''
# #         s += 'end structure\n'
# #
# #         return s
# #
# # class PackmolAtomsBlock:
# #     def __init(self, atoms, constraints=(), radius=None, fscale=None, short_radius=None, short_radius_scale=None):
# #         self.atoms = atoms
# #         self.constraints = constraints
# #         self.radius = radius
# #         self.fscale = fscale
# #         self.short_radius = short_radius
# #         self.short_radius_scale = short_radius_scale
# #
# #     def __str__(self) -> str:
# #         atoms_str = ' '.join(str(a) for a in atoms)
# #         constraints_str = ''.join(f'  {str(c)}\n' for c in self.constraints)
# #         radius_str = f'  radius {radius}\n' if self.radius is not None else ''
# #         fscale_str = f'  fscale {self.fscale}\n' if self.fscale is not None else ''
# #         short_radius_str = f'  short_radius {self.short_radius}\n' if self.short_radius is not None else ''
# #         short_radius_scale_str = f'  short_radius_scale {self.short_radius_scale}\n' if self.short_radius_scale is not None else ''
# #
# #         return f'atoms {atoms_str}\n' + constraints_str + radius_str + fscale_str + short_radius_str + short_radius_scale_str + 'end atoms\n'
# #
# # # CONSTRAINTS
# #
# # class PackmolFixed:
# #     def __init__(self, x, y, z, a, b, c) -> None:
# #         self.x = x
# #         self.y = y
# #         self.z = z
# #         self.a = a
# #         self.b = b
# #         self.c = c
# #
# #     def __str__(self) -> str:
# #         return f'fixed {self.x} {self.y} {self.z} {self.a} {self.b} {self.c}'
# #
# # class PackmolCube:
# #     def __init__(self, xmin, ymin, zmin, d, inside) -> None:
# #         self.xmin = xmin
# #         self.ymin = ymin
# #         self.zmin = zmin
# #         self.d = d
# #         self.inside_outside = 'inside' if inside else 'outside'
# #
# #     def __str__(self) -> str:
# #         return f'{self.inside_outside} cube {self.xmin} {self.ymin} {self.zmin} {self.d}'
# #
# # class PackmolBox:
# #     def __init__(self, xmin, ymin, zmin, xmax, ymax, zmax, inside) -> None:
# #         self.xmin = xmin
# #         self.ymin = ymin
# #         self.zmin = zmin
# #         self.xmax = xmax
# #         self.ymax = ymax
# #         self.zmax = zmax
# #         self.inside_outside = 'inside' if inside else 'outside'
# #
# #     def __str__(self) -> str:
# #         return f'{self.inside_outside} box {self.xmin} {self.ymin} {self.zmin} {self.xmax} {self.ymax} {self.zmax}'
# #
# # class PackmolSphere:
# #     def __init__(self, a, b, c, d, inside) -> None:
# #         self.a = a
# #         self.b = b
# #         self.c = c
# #         self.d = d
# #         self.inside_outside = 'inside' if inside else 'outside'
# #
# #     def __str__(self) -> str:
# #         return f'{self.inside_outside} sphere {self.a} {self.b} {self.c} {self.d}'
# #
# # class PackmolEllipsoid:
# #     def __init__(self, a1, b1, c1, a2, b2, c2, d, inside) -> None:
# #         self.a1 = a1
# #         self.b1 = b1
# #         self.c1 = c1
# #         self.a2 = a2
# #         self.b2 = b2
# #         self.c2 = c2
# #         self.d = d
# #         self.inside_outside = 'inside' if inside else 'outside'
# #
# #     def __str__(self) -> str:
# #         return f'{self.inside_outside} ellipsoid {self.a1} {self.b1} {self.c1} {self.a2} {self.b2} {self.c2} {self.d}'
# #
# # class PackmolPlane:
# #     def __init__(self, a, b, c, d, over) -> None:
# #         self.a = a
# #         self.b = b
# #         self.c = c
# #         self.d = d
# #         self.over_below = 'over' if over else 'below'
# #
# #     def __str__(self) -> str:
# #         return f'{self.over_below} plane {self.a} {self.b} {self.c} {self.d}'
# #
# # class PackmolCylinder:
# #     def __init__(self, a1, b1, c1, a2, b2, c2, d, l, inside) -> None:
# #         self.a1 = a1
# #         self.b1 = b1
# #         self.c1 = c1
# #         self.a2 = a2
# #         self.b2 = b2
# #         self.c2 = c2
# #         self.d = d
# #         self.l = l
# #         self.inside_outside = 'inside' if inside else 'outside'
# #
# #     def __str__(self) -> str:
# #         return f'{self.inside_outside} cylinder {self.a1} {self.b1} {self.c1} {self.a2} {self.b2} {self.c2} {self.d} {self.l}'
# #
# # class PackmolConstrainRotation:
# #     def __init__(self, axis, angle, variance) -> None:
# #         self.axis = axis
# #         self.angle = angle
# #         self.variance = variance
# #
# #     def __str__(self) -> str:
# #         return f'constrain_rotation {self.axis} {self.angle} {self.variance}'
