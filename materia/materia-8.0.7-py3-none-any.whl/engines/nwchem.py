# from __future__ import annotations
# import materia
# from typing import Optional

# __all__ = [
#     "NWChemInput",
#     "NWChemTopBlock",
#     "NWChemTopMemorySubblock",
#     "NWChemTopSetSubblock",
#     "NWChemTopUnsetSubblock",
#     "NWChemTopChargeSubblock",
#     "NWChemTopTaskSubblock",
#     "NWChemGeometryBlock",
#     "NWChemBasisBlock",
#     "NWChemDFTBlock",
#     "NWChemDFTSemidirectSubblock",
#     "NWChemDFTConvergenceSubblock",
#     "NWChemDFTXCSubblock",
#     "NWChemDFTGridSublock",
#     "NWChemDFTVectorsSubblock",
#     "NWChemRTTDDFTBlock",
#     "NWChemRTTDDFTFieldSubblock",
#     "NWChemRTTDDFTExciteSubblock",
#     "NWChemRTTDDFTVisualizationSubblock",
#     "NWChemCosmoBlock",
#     "NWChemRamanBlock",
#     "NWChemPropertyBlock",
# ]


# class NWChemInput:
#     def __init__(self) -> None:
#         self.input_strings = []

#         self.block_class_lookup_dict = {
#             "top": NWChemTopBlock,
#             "geometry": NWChemGeometryBlock,
#             "basis": NWChemBasisBlock,
#             "dft": NWChemDFTBlock,
#             "rttddft": NWChemRTTDDFTBlock,
#             "cosmo": NWChemCosmoBlock,
#             "raman": NWChemRamanBlock,
#             "property": NWChemPropertyBlock,
#         }

#     def __str__(self) -> str:
#         return "\n".join(self.input_strings).rstrip()

#     def add_block(
#         self, **block_params
#     ) -> None:  # FIXME: not sure how to annotate **block_params with type hints...
#         self.input_strings.append(
#             "\n".join(
#                 str(self.block_class_lookup_dict[k](**v))
#                 for k, v in block_params.items()
#             )
#         )

#     def write(self, filepath: str) -> None:
#         with open(materia.expand(filepath), "w") as f:
#             f.write(str(self))


# # TOP LEVEL


# class NWChemTopBlock:
#     # print & noprint not implemented
#     def __init__(  # FIXME: not sure how to annotate all of these with type hints...
#         self,
#         title: Optional[str] = None,
#         echo: bool = False,
#         scratch_dir: Optional[str] = None,
#         permanent_dir: Optional[str] = None,
#         start: bool = False,
#         restart: bool = False,
#         memory_params=None,
#         set_params=None,
#         unset_params=None,
#         task_params=None,
#     ):
#         self.title = title
#         self.echo = echo
#         self.scratch_dir = scratch_dir
#         self.permanent_dir = permanent_dir
#         self.start = start
#         self.restart = restart
#         self.memory_subblock = (
#             NWChemTopMemorySubblock(**memory_params)
#             if memory_params is not None
#             else None
#         )
#         self.set_subblock = (
#             NWChemTopSetSubblock(**set_params) if set_params is not None else None
#         )
#         self.unset_subblock = (
#             NWChemTopUnsetSubblock(**unset_params) if unset_params is not None else None
#         )
#         self.task_subblock = (
#             NWChemTopTaskSubblock(**task_params) if task_params is not None else None
#         )

#     def __str__(self) -> str:
#         s = []
#         s.append(f'title "{self.title}"\n' if self.title is not None else "")
#         s.append("echo\n" if self.echo else "")
#         s.append(
#             f"scratch_dir {self.scratch_dir}\n" if self.scratch_dir is not None else ""
#         )
#         s.append(
#             f"permanent_dir {self.permanent_dir}\n"
#             if self.permanent_dir is not None
#             else ""
#         )
#         s.append(str(self.memory_subblock) if self.memory_subblock is not None else "")
#         s.append(str(self.set_subblock) if self.set_subblock is not None else "")
#         s.append(str(self.unset_subblock) if self.unset_subblock is not None else "")
#         s.append(str(self.task_subblock) if self.task_subblock is not None else "")
#         s.append(f'start "{self.title}"\n' if self.start else "")
#         s.append(f'restart "{self.title}"\n' if self.restart else "")

#         return "".join(s)


# class NWChemTopMemorySubblock:
#     def __init__(
#         self,
#         total_mem=None,
#         total_units=None,
#         stack_mem=None,
#         stack_units=None,
#         global_mem=None,
#         global_units=None,
#         heap_mem=None,
#         heap_units=None,
#     ):
#         self.total_mem = total_mem
#         self.total_units = total_units
#         self.stack_mem = stack_mem
#         self.stack_units = stack_units
#         self.global_mem = global_mem
#         self.global_units = global_units
#         self.heap_mem = heap_mem
#         self.heap_units = heap_units

#     def __str__(self) -> str:
#         s = []
#         if not (
#             self.total_mem is None
#             and self.stack_mem is None
#             and self.global_mem is None
#             and self.heap_mem is None
#         ):
#             s.append("memory")
#         if self.total_mem is not None and self.total_units is not None:
#             s.append(f" total {self.total_mem} {self.total_units}")
#         if self.stack_mem is not None and self.stack_units is not None:
#             s.append(f" stack {self.stack_mem} {self.stack_units}")
#         if self.global_mem is not None and self.global_units is not None:
#             s.append(f" global {self.global_mem} {self.global_units}")
#         if self.heap_mem is not None and self.heap_units is not None:
#             s.append(f" heap {self.heap_mem} {self.heap_units}")
#         s.append("\n")

#         return "".join(s)


# class NWChemTopSetSubblock:
#     def __init__(self, variable_name, variable_value, variable_type=None) -> None:
#         self.variable_name = variable_name
#         self.variable_value = variable_value
#         self.variable_type = variable_type

#     def __str__(self) -> str:
#         if self.variable_type is not None:
#             return (
#                 f"set {self.variable_name} {self.variable_type} {self.variable_value}\n"
#             )
#         else:
#             return f"set {self.variable_name} {self.variable_value}\n"


# class NWChemTopUnsetSubblock:
#     def __init__(self, variable_name) -> None:
#         self.variable_name = variable_name

#     def __str__(self) -> str:
#         return f"unset {self.variable_name}\n"


# class NWChemTopChargeSubblock:
#     def __init__(self, charge) -> None:
#         self.charge = charge

#     def __str__(self) -> str:
#         return f"charge {self.charge}\n"


# class NWChemTopTaskSubblock:
#     def __init__(self, theory_level, operation=None, ignore=False) -> None:
#         self.theory_level = theory_level
#         self.operation = operation
#         self.ignore = ignore

#     def __str__(self) -> str:
#         s = []
#         s.append(f"task {self.theory_level}")
#         s.append(f" {self.operation}" if self.operation is not None else "")
#         s.append(" ignore" if self.ignore else "")
#         s.append("\n")

#         return "".join(s)


# # GEOMETRY


# class NWChemGeometryBlock:
#     def __init__(
#         self,
#         title,
#         xyz_filepath,
#         units="angstroms",
#         center=True,
#         autosym=True,
#         autoz=True,
#     ):
#         self.title = title
#         self.xyz_filepath = xyz_filepath
#         self.units = units
#         self.center = "center" if center else "nocenter"
#         self.autosym = "autosym" if autosym else "noautosym"
#         self.autoz = "autoz" if autoz else "noautoz"

#     def __str__(self) -> str:
#         s = []
#         s.append(
#             f'geometry "{self.title}" units {self.units} {self.center} {self.autosym} {self.autoz}\n'
#         )
#         s.append(f'  LOAD "{self.xyz_filepath}"\n')
#         s.append("end\n")

#         return "".join(s)


# # BASIS


# class NWChemBasisBlock:
#     def __init__(
#         self,
#         atom_strings,
#         library_strings,
#         angular_type="cartesian",
#         segment=True,
#         print_bool=True,
#     ):
#         self.atom_strings = atom_strings
#         self.library_strings = library_strings
#         self.angular_type = angular_type
#         self.segment = "segment" if segment else "nosegment"
#         self.print_bool = "print" if print_bool else "noprint"

#     def __str__(self) -> str:
#         s = []
#         s.append(f"basis {self.angular_type} {self.segment} {self.print_bool}\n")
#         for atom, library in zip(self.atom_strings, self.library_strings):
#             s.append(f"  {atom} library {library}\n")
#         s.append("end\n")

#         return "".join(s)


# # DFT


# class NWChemDFTBlock:
#     # cdft,fon,occup,tolerances,cgmin,rodft,sic,mulliken,fukui,bsse,disp,noscf,print,sodft,max_ovel not implemented yet
#     def __init__(
#         self,
#         iterations=None,
#         smear=None,
#         direct=None,
#         incore=None,
#         noio=None,
#         odft=False,
#         mult=None,
#         semidirect_params=None,
#         xc_params=None,
#         convergence_params=None,
#         grid_params=None,
#         vectors_params=None,
#     ):
#         self.iterations = iterations
#         self.smear = smear
#         self.direct = direct
#         self.incore = incore
#         self.noio = noio
#         self.odft = odft
#         self.mult = mult

#         self.semidirect_subblock = (
#             NWChemDFTSemidirectSubblocbk(**semidirect_params)
#             if semidirect_params is not None
#             else None
#         )
#         self.xc_subblock = (
#             NWChemDFTXCSubblock(**xc_params) if xc_params is not None else None
#         )
#         self.convergence_subblock = (
#             NWChemDFTConvergenceSubblock(**convergence_params)
#             if convergence_params is not None
#             else None
#         )
#         self.grid_subblock = (
#             NWChemDFTGridSubblock(**grid_params) if grid_params is not None else None
#         )
#         self.vectors_subblock = (
#             NWChemDFTVectorsSubblock(**vectors_params)
#             if vectors_params is not None
#             else None
#         )

#     def __str__(self) -> str:
#         s = []
#         s.append("dft\n")
#         s.append(
#             f"  iterations {self.iterations}\n" if self.iterations is not None else ""
#         )
#         s.append(f"  smear {self.smear}\n" if self.smear is not None else "")
#         s.append("  direct\n" if self.direct else "")
#         s.append("  incore\n" if self.incore else "")
#         s.append("  noio\n" if self.noio else "")
#         s.append(
#             str(self.semidirect_subblock)
#             if self.semidirect_subblock is not None
#             else ""
#         )
#         s.append("  odft\n" if self.odft else "")
#         s.append(f"  mult {self.mult}\n" if self.mult is not None else "")
#         s.append(str(self.xc_subblock) if self.xc_subblock is not None else "")
#         s.append(
#             str(self.convergence_subblock)
#             if self.convergence_subblock is not None
#             else ""
#         )
#         s.append(str(self.grid_subblock) if self.grid_subblock is not None else "")
#         s.append(
#             str(self.vectors_subblock) if self.vectors_subblock is not None else ""
#         )
#         s.append("end\n")

#         return "".join(s)


# class NWChemDFTSemidirectSubblock:
#     def __init__(self, filesize=None, memsize=None, filename=None) -> None:
#         self.filesize = filesize
#         self.memsize = memsize
#         self.filename = filename

#     def __str__(self) -> str:
#         s = []
#         s.append("  semidirect")
#         s.append(f" filesize {self.filesize}" if self.filesize is not None else "")
#         s.append(f" memsize {self.memsize}" if self.memsize is not None else "")
#         s.append(f" filename {self.filename}" if self.filename is not None else "")
#         s.append("\n")

#         return "".join(s)


# class NWChemDFTConvergenceSubblock:
#     def __init__(
#         self,
#         energy=None,
#         density=None,
#         gradient=None,
#         hl_tol=None,
#         damp=None,
#         diis=None,
#         lshift=None,
#         dampon=None,
#         dampoff=None,
#         diison=None,
#         diisoff=None,
#         levlon=None,
#         levloff=None,
#         ncydp=None,
#         ncyds=None,
#         ncysh=None,
#         rabuck=None,
#         nodamping=False,
#         nodiis=False,
#         nolevelshifting=False,
#     ):
#         self.energy = energy
#         self.density = density
#         self.gradient = gradient
#         self.hl_tol = hl_tol
#         self.damp = damp
#         self.diis = diis
#         self.lshift = lshift
#         self.dampon = dampon
#         self.dampoff = dampoff
#         self.diison = diison
#         self.diisoff = diisoff
#         self.levlon = levlon
#         self.levloff = levloff
#         self.ncydp = ncydp
#         self.ncyds = ncyds
#         self.ncysh = ncysh
#         self.rabuck = rabuck
#         self.nodamping = nodamping
#         self.nodiis = nodiis
#         self.nolevelshifting = nolevelshifting

#     def __str__(self) -> str:
#         s = []
#         s.append("  convergence ")
#         if self.energy is not None:
#             s.append(f"energy {self.energy} ")
#         if self.density is not None:
#             s.append(f"density {self.density} ")
#         if self.gradient is not None:
#             s.append(f"gradient {self.gradient} ")
#         if self.hl_tol is not None:
#             s.append(f"hl_tol {self.hl_tol} ")
#         if self.damp is not None:
#             s.append(f"damp {self.damp} ")
#         if self.diis is not None:
#             s.append(f"diis {self.diis} ")
#         if self.lshift is not None:
#             s.append(f"lshift {self.lshift} ")
#         if self.dampon is not None:
#             s.append(f"dampon {self.dampon} ")
#         if self.dampoff is not None:
#             s.append(f"dampoff {self.dampoff} ")
#         if self.diison is not None:
#             s.append(f"diison {self.diison} ")
#         if self.diisoff is not None:
#             s.append(f"diisoff {self.diisoff} ")
#         if self.levlon is not None:
#             s.append(f"levlon {self.levlon} ")
#         if self.levloff is not None:
#             s.append(f"levloff {self.levloff} ")
#         if self.ncydp is not None:
#             s.append(f"ncydp {self.ncydp} ")
#         if self.ncyds is not None:
#             s.append(f"ncyds {self.ncyds} ")
#         if self.ncysh is not None:
#             s.append(f"ncysh {self.ncysh} ")
#         if self.rabuck is not None:
#             s.append(f"rabuck {self.rabuck} ")
#         if self.nodamping:
#             s.append("nodamping ")
#         if self.nodiis:
#             s.append("nodiis ")
#         if self.nolevelshifting:
#             s.append("nolevelshifting ")

#         s.append("\n")

#         return "".join(s)


# class NWChemDFTXCSubblock:
#     def __init__(
#         self,
#         xc_functional_strings=(),
#         xc_weights=(),
#         xc_local_weights=(),
#         xc_nonlocal_weights=(),
#         cam=None,
#         cam_alpha=None,
#         cam_beta=None,
#     ) -> None:
#         self.xc_functional_strings = xc_functional_strings
#         self.xc_weights = xc_weights + (None,) * (
#             len(xc_functional_strings) - len(xc_weights)
#         )
#         self.xc_local_weights = xc_local_weights + (None,) * (
#             len(xc_functional_strings) - len(xc_local_weights)
#         )
#         self.xc_nonlocal_weights = xc_nonlocal_weights + (None,) * (
#             len(xc_functional_strings) - len(xc_nonlocal_weights)
#         )
#         self.cam = cam
#         self.cam_alpha = cam_alpha
#         self.cam_beta = cam_beta

#     def __str__(self) -> str:
#         s = []
#         s.append("  xc")
#         for xc, weight, local_weight, nonlocal_weight in zip(
#             self.xc_functional_strings,
#             self.xc_weights,
#             self.xc_local_weights,
#             self.xc_nonlocal_weights,
#         ):
#             s.append(f" {xc}")
#             if weight is not None:
#                 s.append(f" {weight}")
#             if local_weight is not None:
#                 s.append(f" local {local_weight}")
#             if nonlocal_weight is not None:
#                 s.append(f" nonlocal {nonlocal_weight}")
#         s.append("\n")
#         if None not in (self.cam, self.cam_alpha, self.cam_beta):
#             s.append(
#                 f"  cam {self.cam} cam_alpha {self.cam_alpha} cam_beta {self.cam_beta}\n"
#             )

#         return "".join(s)


# class NWChemDFTGridSublock:
#     def __init__(
#         self,
#         size=None,
#         radial_type=None,
#         nodisk=False,
#         gausleg_points=(),
#         gausleg_atoms=(),
#         gausleg_atom_points=(),
#         lebedev_points=(),
#         lebedev_atoms=(),
#         lebedev_atom_points=(),
#         partition_function=None,
#     ) -> None:

#         self.size = size
#         self.radial_type = radial_type
#         self.nodisk = nodisk
#         self.gausleg_points = gausleg_points
#         self.gausleg_atoms = gausleg_atoms
#         self.gausleg_atom_points = gausleg_atom_points
#         self.lebedev_points = lebedev_points
#         self.lebedev_atoms = lebedev_atoms
#         self.lebedev_atom_points = lebedev_atom_points
#         self.partition_function = partition_function

#     def __str__(self) -> str:
#         s = []
#         s.append("  grid")
#         s.append(f" {self.size}" if size is not None else "")
#         s.append(f" {self.radial_type}")
#         s.append(
#             " gausleg"
#             + " ".join(str(p) for p in self.gausleg_points)
#             + " ".join(
#                 f"{a} {rad} {ang}"
#                 for a, (rad, ang) in zip(self.gausleg_atoms, self.gausleg_atom_points)
#             )
#         )
#         s.append(
#             " lebedev"
#             + " ".join(str(p) for p in self.lebedev_points)
#             + " ".join(
#                 f"{a} {rad} {ang}"
#                 for a, (rad, ang) in zip(self.lebedev_atoms, self.lebedev_atom_points)
#             )
#         )
#         s.append(
#             f" {self.partitioning_function}"
#             if self.partitioning_function is not None
#             else ""
#         )
#         s.append(" nodisk" if self.nodisk else "")
#         s.append("\n")

#         return "".join(s)


# class NWChemDFTVectorsSubblock:
#     def __init__(
#         self,
#         input_filename=None,
#         project_basisname=None,
#         project_filename=None,
#         fragment_filenames=(),
#         reorder_pairs=(),
#         swap_pairs=(),
#         swap_alpha_pairs=(),
#         swap_beta_pairs=(),
#         rotate_input_geometry=None,
#         rotate_input_movecs=None,
#         output_filename=None,
#     ) -> None:

#         self.input_filename = input_filename
#         self.project_basisname = project_basisname
#         self.project_filename = project_filename
#         self.fragment_filenames = fragment_filenames
#         self.reorder_pairs = reorder_pairs
#         self.swap_pairs = swap_pairs
#         self.swap_alpha_pairs = swap_alpha_pairs
#         self.swap_beta_pairs = swap_beta_pairs
#         self.rotate_input_geometry = rotate_input_geometry
#         self.rotate_input_movecs = rotate_input_movecs
#         self.output_filename = output_filename

#     def __str__(self) -> str:
#         s = []
#         s.append("  vectors")
#         s.append(
#             f" input {self.input_filename}" if self.input_filename is not None else ""
#         )
#         s.append(
#             f" project {self.project_basisname} {self.project_filename}"
#             if self.project_basisname is not None and self.project_filename is not None
#             else ""
#         )
#         s.append(
#             " fragment"
#             + "".join(f" {filename}" for filename in self.fragment_filenames)
#             if self.fragment_filenames != ()
#             else ""
#         )
#         s.append(
#             " reorder"
#             + "".join(
#                 f" {coeff_num1} {coeff_num2}"
#                 for (coeff_num1, coeff_num2) in self.reorder_pairs
#             )
#             if self.reorder_pairs != ()
#             else ""
#         )
#         s.append(
#             " swap"
#             + "".join(
#                 f" {swap_num1} {swap_num2})"
#                 for (swap_num1, swap_num2) in self.swap_pairs
#             )
#             if self.swap_pairs != ()
#             else ""
#         )
#         s.append(
#             " swap alpha"
#             + "".join(
#                 f" {swap_num1} {swap_num2})"
#                 for (swap_num1, swap_num2) in self.swap_alpha_pairs
#             )
#             if self.swap_alpha_pairs != ()
#             else ""
#         )
#         s.append(
#             " swap beta"
#             + "".join(
#                 f" {swap_num1} {swap_num2})"
#                 for (swap_num1, swap_num2) in self.swap_beta_pairs
#             )
#             if self.swap_beta_pairs != ()
#             else ""
#         )
#         s.append(
#             f" rotate {self.rotate_input_geometry} {self.rotate_input_movecs}"
#             if self.rotate_input_geometry is not None
#             and self.rotate_input_movecs is not None
#             else ""
#         )
#         s.append(
#             f" output {self.output_filename}"
#             if self.output_filename is not None
#             else ""
#         )
#         s.append("\n")

#         return "".join(s)


# # RTTDDFT


# class NWChemRTTDDFTBlock:
#     # load_type options: 'scf','vectors'
#     # propagator options: 'euler','rk4','magnus'
#     def __init__(
#         self,
#         tmax=None,
#         dt=None,
#         tag=None,
#         load_type=None,
#         load_from=None,
#         nchecks=None,
#         nprints=None,
#         nrestarts=None,
#         tolerances_zero=None,
#         tolerances_series=None,
#         tolerances_interpol=None,
#         propagator=None,
#         exp=None,
#         prof=False,
#         noprop=False,
#         static=False,
#         print_dipole=False,
#         print_quadrupole=False,
#         print_field=False,
#         print_moocc=False,
#         print_energy=False,
#         print_cputime=False,
#         print_charge=False,
#         print_convergence=False,
#         print_s2=False,
#         print_dipcontribs=False,
#         print_all=False,
#         field_params=None,
#         excite_params=None,
#         visualization_params=None,
#     ) -> None:

#         self.tmax = tmax
#         self.dt = dt
#         self.tag = tag
#         self.load_type = load_type
#         self.load_from = load_from
#         self.nchecks = nchecks
#         self.nprints = nprints
#         self.nrestarts = nrestarts
#         self.tolerances_zero = tolerances_zero
#         self.tolerances_series = tolerances_series
#         self.tolerances_interpol = tolerances_interpol
#         self.propagator = propagator
#         self.exp = exp
#         self.prof = prof
#         self.noprop = noprop
#         self.static = static
#         self.print_dipole = print_dipole
#         self.print_quadrupole = print_quadrupole
#         self.print_field = print_field
#         self.print_moocc = print_moocc
#         self.print_energy = print_energy
#         self.print_cputime = print_cputime
#         self.print_charge = print_charge
#         self.print_convergence = print_convergence
#         self.print_s2 = print_s2
#         self.print_dipcontribs = print_dipcontribs
#         self.print_all = print_all
#         self.field_subblock = (
#             NWChemRTTDDFTFieldSubblock(**field_params)
#             if field_params is not None
#             else None
#         )
#         self.excite_subblock = (
#             NWChemRTTDDFTExciteSubblock(**excite_params)
#             if excite_params is not None
#             else None
#         )
#         self.visualization_subblock = (
#             NWChemRTTDDFTVisualizationSubblock(**visualization_params)
#             if visualization_params is not None
#             else None
#         )

#     def __str__(self) -> str:
#         s = []
#         s.append("rttddft\n")
#         s.append(f"  tmax {self.tmax}\n" if self.tmax is not None else "")
#         s.append(f"  dt {self.dt}\n" if self.dt is not None else "")
#         s.append(f"  tag {self.tag}\n" if self.tag is not None else "")
#         s.append(
#             f"  load {self.load_type} {self.load_from}\n"
#             if self.load_type is not None and self.load_from is not None
#             else ""
#         )
#         s.append(f"  nchecks {self.nchecks}\n" if self.nchecks is not None else "")
#         s.append(f"  nprints {self.nprints}\n" if self.nprints is not None else "")
#         s.append(
#             f"  nrestarts {self.nrestarts}\n" if self.nrestarts is not None else ""
#         )
#         if not (
#             self.tolerances_zero is None
#             and self.tolerances_series is None
#             and self.tolerances_interpol is None
#         ):
#             s.append("  tolerances")
#             s.append(
#                 f" zero {self.tolerances_zero}"
#                 if self.tolerances_zero is not None
#                 else ""
#             )
#             s.append(
#                 f" series {self.tolerances_series}"
#                 if self.tolerances_series is not None
#                 else ""
#             )
#             s.append(
#                 f" interpol {self.tolerances_interpol}"
#                 if self.tolerances_interpol is not None
#                 else ""
#             )
#             s.append("\n")
#         s.append(
#             f"  propagator {self.propagator}\n" if self.propagator is not None else ""
#         )
#         s.append(f"  exp {self.exp}\n" if self.exp is not None else "")
#         s.append("  prof\n" if self.prof else "")
#         s.append("  noprop\n" if self.noprop else "")
#         s.append("  static\n" if self.static else "")
#         if (
#             self.print_dipole
#             or self.print_quadrupole
#             or self.print_field
#             or self.print_moocc
#             or self.print_energy
#             or self.print_cputime
#             or self.print_charge
#             or self.print_convergence
#             or self.print_s2
#             or self.print_dipcontribs
#             or self.print_all
#         ):
#             s.append("  print")
#             s.append(" dipole" if self.print_dipole else "")
#             s.append(" quadrupole" if self.print_quadrupole else "")
#             s.append(" field" if self.print_field else "")
#             s.append(" moocc" if self.print_moocc else "")
#             s.append(" energy" if self.print_energy else "")
#             s.append(" cputime" if self.print_cputime else "")
#             s.append(" charge" if self.print_charge else "")
#             s.append(" convergence" if self.print_convergence else "")
#             s.append(" s2" if self.print_s2 else "")
#             s.append(" dipcontribs" if self.print_dipcontribs else "")
#             s.append(" *" if self.print_all else "")
#             s.append("\n")
#         if self.field_subblock is not None:
#             s.append(str(self.field_subblock))
#         if self.excite_subblock is not None:
#             s.append(str(self.excite_subblock))
#         if self.visualization_subblock is not None:
#             s.append(str(self.visualization_subblock))
#         s.append("end\n")

#         return "".join(s)


# class NWChemRTTDDFTFieldSubblock:
#     def __init__(
#         self,
#         field_name=None,
#         shape=None,
#         polarization=None,
#         frequency=None,
#         center=None,
#         width=None,
#         max=None,
#         spin=None,
#     ):

#         self.field_name = field_name
#         self.shape = shape
#         self.polarization = polarization
#         self.frequency = frequency
#         self.center = center
#         self.width = width
#         self.max = max
#         self.spin = spin

#     def __str__(self) -> str:
#         s = []
#         s.append(f'  field "{self.field_name}"\n')
#         s.append(f"    type {self.shape}\n")
#         s.append(f"    polarization {self.polarization}\n")
#         s.append(
#             f"    frequency {self.frequency}\n" if self.frequency is not None else ""
#         )
#         s.append(f"    center {self.center}\n" if self.center is not None else "")
#         s.append(f"    width {self.width}\n" if self.width is not None else "")
#         s.append(f"    max {self.max}\n" if self.max is not None else "")
#         s.append(f"    spin {self.spin}\n" if self.spin is not None else "")
#         s.append("  end\n")

#         return "".join(s)


# class NWChemRTTDDFTExciteSubblock:
#     def __init__(self, geometry_name=None, field_name=None) -> None:
#         self.geometry_name = geometry_name
#         self.field_name = field_name

#     def __str__(self) -> str:
#         return f'  excite "{self.geometry_name}" with "{self.field_name}"\n'


# class NWChemRTTDDFTVisualizationSubblock:
#     def __init__(self, tstart=None, tend=None, treference=None, dplot=False) -> None:
#         self.tstart = tstart
#         self.tend = tend
#         self.treference = treference
#         self.dplot = dplot

#     def __str__(self) -> str:
#         s = []
#         s.append("  visualization\n")
#         s.append(f"    tstart {self.tstart}\n" if self.tstart is not None else "")
#         s.append(f"    tend {self.tend}\n" if self.tend is not None else "")
#         s.append(
#             f"    treference {self.treference}\n" if self.treference is not None else ""
#         )
#         s.append(f"    dplot\n" if self.dplot else "")
#         s.append("  end\n")

#         return "".join(s)


# # COSMO


# class NWChemCosmoBlock:
#     def __init__(
#         self,
#         dielec=None,
#         parameters_file=None,
#         radii=(),
#         iscren=None,
#         minbem=None,
#         ificos=None,
#         lineq=None,
#         zeta=None,
#         gamma_s=None,
#         sw_tol=None,
#         do_gasphase=None,
#         do_cosmo_ks=None,
#         do_cosmo_yk=None,
#     ):

#         self.dielec = dielec
#         self.parameters_file = parameters_file
#         self.radii = radii
#         self.iscren = iscren
#         self.minbem = minbem
#         self.ificos = ificos
#         self.lineq = lineq
#         self.zeta = zeta
#         self.gamma_s = gamma_s
#         self.sw_tol = sw_tol
#         self.do_gasphase = do_gasphase
#         self.do_cosmo_ks = do_cosmo_ks
#         self.do_cosmo_yk = do_cosmo_yk

#     def __str__(self) -> str:
#         s = []
#         s.append("cosmo\n")
#         s.append(f"  dielec {self.dielec}\n" if self.dielec is not None else "")
#         s.append(
#             f"  parameters {self.parameters_file}\n"
#             if self.parameters_file is not None
#             else ""
#         )
#         if self.radii != ():
#             s.append(f"  radius {self.radii[0]}\n")
#             for radius in self.radii[1:]:
#                 s.append(f"         {radius}\n")
#         s.append(f"  iscren {self.iscren}\n" if self.iscren is not None else "")
#         s.append(f"  minbem {self.minbem}\n" if self.minbem is not None else "")
#         s.append(f"  ificos {self.ificos}\n" if self.ificos is not None else "")
#         s.append(f"  lineq {self.lineq}\n" if self.lineq is not None else "")
#         s.append(f"  zeta {self.zeta}\n" if self.zeta is not None else "")
#         s.append(f"  gamma_s {self.gamma_s}\n" if self.gamma_s is not None else "")
#         s.append(f"  sw_tol {self.sw_tol}\n" if self.sw_tol is not None else "")
#         s.append(
#             f"  do_gasphase {self.do_gasphase}\n"
#             if self.do_gasphase is not None
#             else ""
#         )
#         s.append(
#             f"  do_cosmo_ks {self.do_cosmo_ks}\n"
#             if self.do_cosmo_ks is not None
#             else ""
#         )
#         s.append(
#             f"  do_cosmo_yk {self.do_cosmo_yk}\n"
#             if self.do_cosmo_yk is not None
#             else ""
#         )
#         s.append("end\n")

#         return "".join(s)


# # RAMAN


# class NWChemRamanBlock:
#     def __init__(
#         self,
#         normal=False,
#         resonance=False,
#         lorentzian=False,
#         gaussian=False,
#         low=None,
#         high=None,
#         first=None,
#         last=None,
#         width=None,
#         dq=None,
#     ):
#         self.normal = normal
#         self.resonance = resonance
#         self.lorentzian = lorentzian
#         self.gaussian = gaussian
#         self.low = low
#         self.high = high
#         self.first = first
#         self.last = last
#         self.width = width
#         self.dq = dq

#     def __str__(self) -> str:
#         s = []
#         s.append("raman\n")
#         s.append("  normal\n" if self.normal else "")
#         s.append("  resonance\n" if self.resonance else "")
#         s.append("  lorentzian\n" if self.lorentzian else "")
#         s.append("  gaussian\n" if self.gaussian else "")
#         s.append(f"  low {self.low}\n" if self.low is not None else "")
#         s.append(f"  high {self.high}\n" if self.high is not None else "")
#         s.append(f"  first {self.first}\n" if self.first is not None else "")
#         s.append(f"  last {self.last}\n" if self.last is not None else "")
#         s.append(f"  width {self.width}\n" if self.width is not None else "")
#         s.append(f"  dq {self.dq}\n" if self.dq is not None else "")
#         s.append("end\n")

#         return "".join(s)


# # PROPERTY


# class NWChemPropertyBlock:
#     # gauge options: 'dipole', 'velocity'
#     # center options: 'com', 'coc', 'origin', 'arb'
#     # molden_norm options: 'janpa', nwchem', 'none'
#     # grid not implemented yet
#     def __init__(
#         self,
#         nbofile=False,
#         dipole=False,
#         quadrupole=False,
#         octupole=False,
#         mulliken=False,
#         esp=False,
#         efield=False,
#         efieldgrad=False,
#         efieldgradz4=False,
#         gshift=False,
#         aimfile=False,
#         moldenfile=False,
#         molden_norm=None,
#         electrondensity=False,
#         vectors_filename=None,
#         hyperfine_num_atoms=None,
#         hyperfine_atoms=(),
#         shielding_num_atoms=None,
#         shielding_atoms=(),
#         spinspin_num_pairs=None,
#         spinspin_atom_pairs=(),
#         response_order=None,
#         response_frequency=None,
#         response_gauge=None,
#         response_damping=None,
#         response_convergence=None,
#         response_orbeta=False,
#         response_giao=False,
#         response_bdtensor=False,
#         response_analysis=False,
#         all=False,
#         center=None,
#         center_coords=None,
#     ):

#         self.nbofile = nbofile
#         self.dipole = dipole
#         self.quadrupole = quadrupole
#         self.octupole = octupole
#         self.mulliken = mulliken
#         self.esp = esp
#         self.efield = efield
#         self.efieldgrad = efieldgrad
#         self.efieldgradz4 = efieldgradz4
#         self.gshift = gshift
#         self.aimfile = aimfile
#         self.moldenfile = moldenfile
#         self.molden_norm = molden_norm
#         self.electrondensity = electrondensity
#         self.vectors_filename = vectors_filename
#         self.hyperfine_num_atoms = hyperfine_num_atoms
#         self.hyperfine_atoms = hyperfine_atoms
#         self.shielding_num_atoms = shielding_num_atoms
#         self.shielding_atoms = shielding_atoms
#         self.spinspin_num_pairs = spinspin_num_pairs
#         self.spinspin_atom_pairs = spinspin_atom_pairs
#         self.response_order = response_order
#         self.response_frequency = response_frequency
#         self.response_gauge = response_gauge
#         self.response_damping = response_damping
#         self.response_convergence = response_convergence
#         self.response_orbeta = response_orbeta
#         self.response_giao = response_giao
#         self.response_bdtensor = response_bdtensor
#         self.response_analysis = response_analysis
#         self.all = all
#         self.center = center
#         self.center_coords = center_coords

#     def __str__(self) -> str:
#         s = []
#         s.append("property\n")
#         s.append(f"  nbofile\n" if self.nbofile else "")
#         s.append(f"  dipole\n" if self.dipole else "")
#         s.append(f"  quadrupole\n" if self.quadrupole else "")
#         s.append(f"  octupole\n" if self.octupole else "")
#         s.append(f"  mulliken\n" if self.mulliken else "")
#         s.append(f"  esp\n" if self.esp else "")
#         s.append(f"  efield\n" if self.efield else "")
#         s.append(f"  efieldgrad\n" if self.efieldgrad else "")
#         s.append(f"  efieldgradz4\n" if self.efieldgradz4 else "")
#         s.append(f"  gshift\n" if self.gshift else "")
#         s.append(f"  electrondensity\n" if self.electrondensity else "")
#         if self.hyperfine_num_atoms is not None and self.hyperfine_atoms != ():
#             s.append(
#                 f"  hyperfine {self.hyperfine_num_atoms} "
#                 + " ".join(f"{a}" for a in self.hyperfine_atoms)
#                 + "\n"
#             )
#         if self.shielding_num_atoms is not None and self.shielding_atoms != ():
#             s.append(
#                 f"  shielding {self.shielding_num_atoms} "
#                 + " ".join(f"{a}" for a in self.shielding_atoms)
#                 + "\n"
#             )
#         if self.spinspin_num_pairs is not None and self.spinspin_atom_pairs != ():
#             s.append(
#                 f"  spinspin {self.spinspin_num_pairs} "
#                 + " ".join(f"{a1} {a2}" for (a1, a2) in self.spinspin_atom_pairs)
#                 + "\n"
#             )
#         s.append(
#             f"  response {self.response_order} {self.response_frequency}\n"
#             if self.response_order is not None and self.response_frequency is not None
#             else ""
#         )
#         s.append(
#             f"  {self.response_gauge}\n" if self.response_gauge is not None else ""
#         )
#         s.append(
#             f"  damping {self.response_damping}\n"
#             if self.response_damping is not None
#             else ""
#         )
#         s.append(
#             f"  convergence {self.response_convergence}\n"
#             if self.response_convergence is not None
#             else ""
#         )
#         s.append("  orbeta\n" if self.response_orbeta else "")
#         s.append("  giao\n" if self.response_giao else "")
#         s.append("  bdtensor\n" if self.response_bdtensor else "")
#         s.append("  analysis\n" if self.response_analysis else "")
#         s.append(
#             f"  vectors {self.vectors_filename}\n"
#             if self.vectors_filename is not None
#             else ""
#         )
#         if self.center == "arb":
#             s.append(f"  center " + " ".join(f"{c}" for c in self.center_coords) + "\n")
#         elif self.center is not None:
#             s.append(f"  center {self.center}\n")
#         s.append(f"  aimfile {self.aimfile}\n" if self.aimfile else "")
#         s.append(f"  moldenfile {self.moldenfile}\n" if self.moldenfile else "")
#         s.append(
#             f"  molden_norm {self.molden_norm}\n"
#             if self.molden_norm is not None
#             else ""
#         )
#         s.append(f"  all\n" if self.all else "")
#         s.append("end\n")

#         return "".join(s)

# from __future__ import annotations
# import collections
# import materia
# from typing import Iterable, List, Tuple

# __all__ = ["NWChemOutput"]


# class NWChemOutput:
#     def __init__(self, filename: str) -> None:
#         self.filename = materia.expand(filename)
#         self.output_dict = collections.OrderedDict()

#         self.chunk_dict = {
#             "input": "echo of input deck",
#             "titlecard": "Northwest Computational Chemistry Package (NWChem)",
#             "jobinfo": "Job information",
#             "meminfo": "Memory information",
#             "directoryinfo": "Directory information",
#             "dftmodule": "NWChem DFT Module",
#             "responsemodule": "*** RESPONSE ***",
#             "tddftmodule": "NWChem TDDFT Module",
#             "rttddftmodule": "NWChem Real-Time TDDFT Module",
#             "gastats": "GA Statistics for process",
#         }

#         # chunk the output into major sections
#         chunk_starts, chunk_types = zip(*self._chunk_file())
#         chunks = self._get_chunks(chunk_starts=chunk_starts, chunk_types=chunk_types)

#         def get(self, *quantity_names: str):
#             method_dict = dict(inspect.getmembers(self, predicate=inspect.isroutine))

#             with open(self.filepath, "r") as f:
#                 lines = "".join(f.readlines())

#             quantities = tuple(
#                 method_dict[name.lower()](lines=lines) for name in quantity_names
#             )

#             if len(quantities) == 1:
#                 return quantities[0]
#             return quantities

#         # fragment each chunk into minor sections
#         def modify_chunk_type(x, data={}):
#             if x in data:
#                 data[x] += 1
#             else:
#                 data[x] = 0

#             return "{0}{1}".format(x, data[x])

#         for chunk, chunk_type in zip(chunks, chunk_types):

#             def modify_frag_type(
#                 x, data={}
#             ):  # this is some clever trickery with the default value data={}
#                 if x in data:
#                     data[x] += 1
#                 else:
#                     data[x] = 0
#                 return "{0}{1}".format(x, data[x])

#             fragment_starts, fragment_types = zip(
#                 *self._fragment_chunk(chunk=chunk, chunk_type=chunk_type)
#             )

#             unique_fragment_types = [
#                 modify_frag_type(x=frag_type) for frag_type in fragment_types
#             ]
#             fragments = self._get_fragments(
#                 chunk=chunk, fragment_starts=fragment_starts
#             )

#             self.output_dict[modify_chunk_type(x=chunk_type)] = collections.OrderedDict(
#                 zip(unique_fragment_types, fragments)
#             )

#     def _chunk_file(self: str) -> List[Tuple[str, str]]:
#         return sorted(
#             [
#                 (x, chunk_type)
#                 for chunk_type, chunk_keyword in self.chunk_dict.items()
#                 for x in self._find_chunk_keyword_in_file(chunk_keyword=chunk_keyword)
#             ]
#         )

#     def _find_chunk_keyword_in_file(self, chunk_keyword: str) -> List[int]:
#         with open(self.filename, "r") as f:
#             return [linenum for linenum, line in enumerate(f) if chunk_keyword in line]

#     def _get_chunks(
#         self, chunk_starts: Iterable[int], chunk_types: Iterable[str]
#     ) -> List[str]:
#         cur_ind = 0
#         chunk_start = chunk_starts[cur_ind]
#         chunk_end = (
#             chunk_starts[cur_ind + 1]
#             if cur_ind != len(chunk_starts) - 1
#             else float("inf")
#         )
#         cur_chunk = ""
#         chunks = []
#         with open(self.filename, "r") as f:
#             for linenum, line in enumerate(f):
#                 if linenum < chunk_start:
#                     pass
#                 elif linenum >= chunk_start and linenum < chunk_end:
#                     cur_chunk += line
#                 else:
#                     cur_ind += 1
#                     chunk_start = chunk_starts[cur_ind]
#                     chunk_end = (
#                         chunk_starts[cur_ind + 1]
#                         if cur_ind != len(chunk_starts) - 1
#                         else float("inf")
#                     )
#                     chunks.append(cur_chunk)
#                     cur_chunk = line
#         chunks.append(cur_chunk)

#         return chunks

#     def _fragment_chunk(self, chunk, chunk_type):
#         if chunk_type == "input":
#             fragment_dict = {"input": "echo of input deck"}
#         elif chunk_type == "titlecard":
#             fragment_dict = {
#                 "titlecard": "Northwest Computational Chemistry Package (NWChem)"
#             }
#         elif chunk_type == "jobinfo":
#             fragment_dict = {"jobinfo": "Job information"}
#         elif chunk_type == "meminfo":
#             fragment_dict = {"meminfo": "Memory information"}
#         elif chunk_type == "directoryinfo":
#             fragment_dict = {"directoryinfo": "Directory information"}
#         elif chunk_type == "dftmodule":
#             fragment_dict = {
#                 "basis": 'Basis "ao basis"',
#                 "basissummary": 'Summary of "ao basis"',
#                 "geninfo": "General Information",
#                 "xcinfo": "XC Information",
#                 "gridinfo": "Grid Information",
#                 "convergenceinfo": "Convergence Information",
#                 "screeninginfo": "Screening Tolerance Information",
#                 "guess": "Superposition of Atomic Density Guess",
#                 "scf": "Memory utilization after 1st SCF pass",
#                 "orbitals": "DFT Final Molecular Orbital Analysis",
#                 "alpha_orbitals": "DFT Final Alpha Molecular Orbital Analysis",
#                 "beta_orbitals": "DFT Final Beta Molecular Orbital Analysis",
#                 "com": "center of mass",
#                 "moments": "moments of inertia",
#                 "multipole": "Multipole analysis of the density",
#             }
#         elif chunk_type == "responsemodule":
#             fragment_dict = {
#                 "header": "Response module for NWChem",
#                 "field": "Solving response equations for perturbing field",
#                 "cphf": "NWChem CPHF Module",
#                 "electricdipoleresponse": "Electric Dipole Response Matrix",
#                 "linearresponsepolarizability": "DFT Linear Response polarizability",
#                 "magneticdipoleresponse": "Magnetic Dipole Response Matrix",
#             }
#         elif chunk_type == "tddftmodule":
#             fragment_dict = {
#                 "geninfo": "General Information",
#                 "xcinfo": "XC Information",
#                 "tddftinfo": "TDDFT Information",
#                 "meminfo": "Memory Information",
#                 "evaldiffs": "smallest eigenvalue differences",
#             }
#         elif chunk_type == "rttddftmodule":
#             fragment_dict = {
#                 "basissummary": 'Summary of "ao basis"',
#                 "geninfo": "General Information",
#                 "xcinfo": "XC Information",
#                 "convergenceinfo": "Convergence Information",
#                 "screeninginfo": "Screening Tolerance Information",
#                 "propparams": "Propagation parameters",
#                 "dipolequadrupole": "Dipole and quadrupole matrices",
#                 "appliedfields": "Applied fields",
#                 "excitationrules": "Excitation rules",
#                 "propheader": "shell propagation",
#                 "propstart": "Propagation started",
#                 "checkspassed": "Checks passed",
#                 "savedrestart": "Saved restart file",
#                 "tddipole": "Dipole moment [system]",
#                 "istart": "istart",
#                 "dipcontribx": "Mu-X i-a Contrib",
#                 "dipcontriby": "Mu-Y i-a Contrib",
#                 "dipcontribz": "Mu-Z i-a Contrib",
#                 "propfinish": "Propagation finished",
#             }
#         elif chunk_type == "gastats":
#             fragment_dict = {
#                 "summary": "Summary of allocated global arrays",
#                 "stats": "GA Statistics",
#             }

#         return sorted(
#             [
#                 (x, frag_type)
#                 for frag_type, frag in fragment_dict.items()
#                 for x in self._find_fragment_in_chunk(
#                     chunk=chunk.split("\n"), fragment=frag
#                 )
#             ]
#         )

#     def _find_fragment_in_chunk(self, chunk, fragment):
#         return [linenum for linenum, line in enumerate(chunk) if fragment in line]

#     def _get_fragments(self, chunk, fragment_starts):
#         cur_ind = 0
#         fragment_start = fragment_starts[cur_ind]
#         fragment_end = (
#             fragment_starts[cur_ind + 1]
#             if cur_ind != len(fragment_starts) - 1
#             else float("inf")
#         )
#         cur_fragment = ""
#         fragments = []
#         for linenum, line in enumerate(chunk.split("\n")):
#             if linenum < fragment_start:
#                 pass
#             elif linenum >= fragment_start and linenum < fragment_end:
#                 cur_fragment += line + "\n"
#             else:
#                 cur_ind += 1
#                 fragment_start = fragment_starts[cur_ind]
#                 fragment_end = (
#                     fragment_starts[cur_ind + 1]
#                     if cur_ind != len(fragment_starts) - 1
#                     else float("inf")
#                 )
#                 fragments.append(cur_fragment)
#                 cur_fragment = line

#         fragments.append(cur_fragment)

#         return fragments

#     def get_orbital_info(
#         self, orbitals=None, spin=None, dftmodule_num=0, orbitals_fragment_num=0
#     ):
#         dft_key = "dftmodule{0}".format(dftmodule_num)

#         if spin is None:
#             orbital_key = "orbitals{0}".format(orbitals_fragment_num)
#         elif hasattr(spin, "lower") and spin.lower() == "alpha":
#             orbital_key = "alpha_orbitals{0}".format(orbitals_fragment_num)
#         elif hasattr(spin, "lower") and spin.lower() == "beta":
#             orbital_key = "beta_orbitals{0}".format(orbitals_fragment_num)
#         else:
#             raise ValueError(
#                 "Invalid value for argument spin, which can take values 'alpha','beta', or None."
#             )

#         orbital_fragment = self.output_dict[dft_key][orbital_key]

#         energies = []
#         vector_nums = []
#         occupancies = []

#         mo_centers = []
#         mo_r2s = []  # shows how diffuse an orbital is

#         for line in orbital_fragment.split("\n"):
#             if "Vector" in line:
#                 partial_1, partial_2, energy = line.split("=")
#                 _, vector_num, _ = partial_1.split()
#                 occupancy, _ = partial_2.split()

#                 energy = float(energy.replace("D", "e"))
#                 energies.append(energy)

#                 vector_nums.append(int(vector_num))

#                 occupancy = float(occupancy.replace("D", "e"))
#                 occupancies.append(occupancy)
#             elif "MO Center" in line:
#                 _, partial_1, r2 = line.split("=")
#                 x, y, z, _, = partial_1.strip().split(",")

#                 x = float(x.replace("D", "e"))
#                 y = float(y.replace("D", "e"))
#                 z = float(z.replace("D", "e"))
#                 mo_centers.append((x, y, z))

#                 r2 = float(r2.replace("D", "e"))
#                 mo_r2s.append(r2)

#         orbital_dicts = (
#             {
#                 "energy": units.Qty(value=eng, unit=units.hartree),
#                 "occupancy": units.Qty(value=occ, unit=units.Unit(base="unitless")),
#                 "center": units.Qty(value=moc, unit=units.Unit(base="bohr")),
#                 "R2": units.Qty(value=mor2, unit=units.Unit(base="bohr") ** 2),
#             }
#             for eng, occ, moc, mor2 in zip(energies, occupancies, mo_centers, mo_r2s)
#         )

#         if orbitals is None:
#             return dict(zip(vector_nums, orbital_dicts))
#         else:
#             return {
#                 num: od
#                 for num, od in zip(vector_nums, orbital_dicts)
#                 if num in orbitals
#             }

#     def get_homo_lumo(self, dftmodule_num=0, orbitals_fragment_num=0):
#         dft_key = "dftmodule{0}".format(dftmodule_num)

#         if self.is_spin_polarized(dftmodule_num=dftmodule_num):
#             alpha_info = self.get_orbital_info(
#                 spin="alpha",
#                 dftmodule_num=dftmodule_num,
#                 orbitals_fragment_num=orbitals_fragment_num,
#             )
#             alpha_homo = max(
#                 od["energy"] for od in alpha_info.values() if od["occupancy"] != 0
#             )
#             alpha_lumo = min(
#                 od["energy"] for od in alpha_info.values() if od["occupancy"] == 0
#             )

#             beta_info = self.get_orbital_info(
#                 spin="beta",
#                 dftmodule_num=dftmodule_num,
#                 orbitals_fragment_num=orbitals_fragment_num,
#             )
#             beta_homo = max(
#                 od["energy"] for od in beta_info.values() if od["occupancy"] != 0
#             )
#             beta_lumo = min(
#                 od["energy"] for od in beta_info.values() if od["occupancy"] == 0
#             )

#             homo = max(alpha_homo, beta_homo)
#             lumo = min(alpha_lumo, beta_lumo)
#         else:
#             orbital_info = self.get_orbital_info(
#                 dftmodule_num=dftmodule_num, orbitals_fragment_num=orbitals_fragment_num
#             )
#             homo = max(
#                 [od["energy"] for od in orbital_info.values() if od["occupancy"] != 0]
#             )
#             lumo = min(
#                 [od["energy"] for od in orbital_info.values() if od["occupancy"] == 0]
#             )

#         return {"homo": homo, "lumo": lumo, "gap": lumo - homo}

#     def is_spin_polarized(self, dftmodule_num=0):
#         dft_key = "dftmodule{0}".format(dftmodule_num)
#         return (
#             sum(
#                 (k.startswith("alpha_orbitals") or k.startswith("beta_orbitals"))
#                 for k in self.output_dict[dft_key].keys()
#             )
#             > 0
#         )

#     def get_total_energies(self, dftmodule_num=0, scf_fragment_num=0):
#         dft_key = "dftmodule{0}".format(dftmodule_num)
#         scf_key = "dftmodule{0}".format(scf_fragment_num)

#         energy_fragment = self.output_dict[dft_key][scf_key]

#         energy_dict = {}
#         for line in energy_fragment.split("\n"):
#             if "Total DFT energy" in line:
#                 _, total_energy = line.split("=")
#                 total_energy = float(total_energy.replace("D", "e"))
#                 energy_dict["total_energy"] = units.Qty(
#                     value=total_energy, unit=units.hartree
#                 )
#             elif "One electron energy" in line:
#                 _, one_electron_energy = line.split("=")
#                 one_electron_energy = float(one_electron_energy.replace("D", "e"))
#                 energy_dict["one_electron_energy"] = units.Qty(
#                     value=one_electron_energy, unit=units.hartree
#                 )
#             elif "Coulomb energy" in line:
#                 _, coulomb_energy = line.split("=")
#                 coulomb_energy = float(coulomb_energy.replace("D", "e"))
#                 energy_dict["coulomb_energy"] = units.Qty(
#                     value=coulomb_energy, unit=units.hartree
#                 )
#             elif "Exchange-Corr. energy" in line:
#                 _, xc_energy = line.split("=")
#                 xc_energy = float(xc_energy.replace("D", "e"))
#                 energy_dict["xc_energy"] = units.Qty(
#                     value=xc_energy, unit=units.hartree
#                 )
#             elif "Nuclear repulsion energy" in line:
#                 _, nuclear_repulsion_energy = line.split("=")
#                 nuclear_repulsion_energy = float(
#                     nuclear_repulsion_energy.replace("D", "e")
#                 )
#                 energy_dict["nuclear_repulsion_energy"] = units.Qty(
#                     value=nuclear_repulsion_energy, unit=units.hartree
#                 )
#             elif "COSMO energy" in line:
#                 _, cosmo_energy = line.split("=")
#                 cosmo_energy = float(cosmo_energy.replace("D", "e"))
#                 energy_dict["cosmo_energy"] = units.Qty(
#                     value=cosmo_energy, unit=units.hartree
#                 )

#         return energy_dict

#     def get_polarizability(self, responsemodule_num=0, polarize_fragment_num=0):
#         response_key = "responsemodule{0}".format(responsemodule_num)
#         polarize_key = "linearresponsepolarizability{0}".format(polarize_fragment_num)

#         polarizability_fragment = self.output_dict[response_key][polarize_key].split(
#             "\n"
#         )

#         header_string = polarizability_fragment[:4]
#         matrix_string = polarizability_fragment[4:7]
#         eigenvalues_string = polarizability_fragment[8]
#         isotropic_string = polarizability_fragment[9]
#         anisotropic_string = polarizability_fragment[10]

#         matrix_elements = [
#             float(str)
#             for m in matrix_string
#             for str in m.split()
#             if str not in ("X", "Y", "Z")
#         ]
#         polarizability_matrix = np.array(matrix_elements).reshape((3, 3))

#         _, _, eig1, eig2, eig3 = eigenvalues_string.split()
#         eigenvalues = (float(eig1), float(eig2), float(eig3))

#         _, _, iso = isotropic_string.split()
#         isotropic_polarizability = float(iso)

#         _, _, aniso = anisotropic_string.split()
#         anisotropy = float(aniso)

#         return units.Qty(value=polarizability_matrix, unit=units.au_volume)

#         # return {'polarizability_matrix': units.Qty(value=polarizability_matrix,unit=units.au_volume),
#         #         'polarizability_eigenvalues': units.Qty(value=eigenvalues,unit=units.au_volume),
#         #         'isotropic_polarizability': units.Qty(value=isotropic_polarizability,unit=units.au_volume),
#         #         'polarizability_anisotropy': units.Qty(value=anisotropy,unit=units.au_volume),
#         #        }

#     def get_tddipole(self, rttddftmodule_num=None, field_tag=None, appliedfields_num=0):
#         if rttddftmodule_num is None:
#             rttddft_keys = (
#                 k for k in self.output_dict.keys() if k.startswith("rttddftmodule")
#             )
#         else:
#             rttddft_keys = (f"rttddftmodule{rttddftmodule_num}",)

#         result_dict = {}

#         for rttddft_key in rttddft_keys:
#             rttddft_dict = self.output_dict[rttddft_key]

#             tddipole_keys = [k for k in rttddft_dict.keys() if k.startswith("tddipole")]

#             if field_tag is None:
#                 field_tags = (
#                     tag
#                     for tag, _, _, _, _, _, _, _, _ in (
#                         rttddft_dict[k].split() for k in tddipole_keys
#                     )
#                 )
#             else:
#                 field_tags = (field_tag,)

#             result = {}

#             for ft in field_tags:
#                 tddipole_keys = [
#                     k for k in rttddft_dict.keys() if k.startswith("tddipole")
#                 ]
#                 time, mu_x, mu_y, mu_z = zip(
#                     *(
#                         (float(t), float(x), float(y), float(z))
#                         for tag, t, x, y, z, _, _, _, _ in (
#                             rttddft_dict[k].split() for k in tddipole_keys
#                         )
#                         if tag == ft
#                     )
#                 )

#                 applied_field_fragment = rttddft_dict[
#                     f"appliedfields{appliedfields_num}"
#                 ].split("\n")
#                 applied_field_header = applied_field_fragment[:3]
#                 (
#                     applied_field_type_str,
#                     applied_field_polarization_str,
#                     applied_field_maximum_str,
#                     _,
#                     _,
#                     _,
#                 ) = applied_field_fragment[3:]

#                 _, _, applied_field_type = applied_field_type_str.split()
#                 (
#                     _,
#                     _,
#                     applied_field_polarization,
#                 ) = applied_field_polarization_str.split()
#                 (
#                     _,
#                     _,
#                     _,
#                     _,
#                     _,
#                     _,
#                     applied_field_maximum,
#                     _,
#                 ) = applied_field_maximum_str.split()

#                 time_unit = units.Unit("au_time")
#                 dipole_unit = units.au_dipole_moment
#                 applied_field_unit = units.volt / units.Unit("nanometer")

#                 result[ft] = {
#                     "time": units.Qty(value=np.array(time), unit=time_unit),
#                     "mu_x": units.Qty(value=np.array(mu_x), unit=dipole_unit),
#                     "mu_y": units.Qty(value=np.array(mu_y), unit=dipole_unit),
#                     "mu_z": units.Qty(value=np.array(mu_z), unit=dipole_unit),
#                     "E_max": units.Qty(
#                         value=applied_field_maximum, unit=applied_field_unit
#                     ),
#                     "E_shape": applied_field_type,
#                     "E_polarization": applied_field_polarization,
#                 }

#             result_dict[rttddft_key] = result

#         return result_dict

#     def plot_tddipole(self, rttddftmodule_num=None, field_tag=None):
#         tddipole_dict = self.get_tddipole(
#             field_tag=field_tag, rttddftmodule_num=rttddftmodule_num
#         )
#         for rttddftmodule_num, result_dict in tddipole_dict.items():
#             for field_tag, result in result_dict.items():
#                 time = result["time"]
#                 mu_x = result["mu_x"]
#                 mu_y = result["mu_y"]
#                 mu_z = result["mu_z"]

#                 plt.plot(
#                     time.value, mu_x.value, label=f"x_{field_tag}_{rttddftmodule_num}"
#                 )
#                 plt.plot(
#                     time.value, mu_y.value, label=f"y_{field_tag}_{rttddftmodule_num}"
#                 )
#                 plt.plot(
#                     time.value, mu_z.value, label=f"z_{field_tag}_{rttddftmodule_num}"
#                 )
#                 plt.title("Dynamic dipole moments")
#                 plt.xlabel("Time ({0})".format(time.unit))
#                 plt.ylabel("Dipole moment ({0})".format(mu_x.unit))

#         plt.legend()
#         plt.show()

#     def get_dipcontribs(self, dipcontrib_dir, rttddftmodule_num=0, i=None, a=None):
#         # FIXME: there is currently no way to get dipcontribs by field tag like
#         # there is with get_tddipole; consider fixing by not fragmenting dipcontribs
#         # and tddipoles apart but rather storing them together
#         rttddft_key = "rttddftmodule{0}".format(rttddftmodule_num)
#         rttddft_dict = self.output_dict[rttddft_key]

#         # dipcontrib_keys = [k for k in rttddft_dict.keys() if k.startswith('dipcontrib')]
#         # dipcontribx_keys = [k for k in dipcontrib_keys if k.startswith('dipcontribx')]
#         # dipcontriby_keys = [k for k in dipcontrib_keys if k.startswith('dipcontriby')]
#         # dipcontribz_keys = [k for k in dipcontrib_keys if k.startswith('dipcontribz')]
#         #
#         # for direction in ('x','y','z'):
#         #     dipcontrib_dir_keys = [k for k in dipcontrib_keys if k.startswith('dipcontrib{0}'.format(direction))]
#         #     from_orbitals_key,to_orbitals_key,propagation_keys = dipcontrib_dir_keys[0],dipcontrib_dir_keys[1],dipcontrib_dir_keys[2:]
#         #
#         #     orbital_pairs = [(int(i),int(a)) for i,a in zip(rttddft_dict[from_orbitals_key].split(),rttddft_dict[to_orbitals_key].split()) if i not in ('#Mu-X','#Mu-Y','#Mu-Z','i-a','Contrib','CLOSED') and a not in ('#Mu-X','#Mu-Y','#Mu-Z','i-a','Contrib','CLOSED')]
#         #
#         #     np.array([[float(p) for p in rttddft_dict[k].split()[:-4]] for k in propagation_keys]))
#         #
#         #
#         #
#         # from_orbital_nums = tuple(int(i) for i in rttddft_dict[dipcontrib_keys[0]].split()[:-4])
#         # to_orbital_nums = tuple(int(a) for a in rttddft_dict[dipcontrib_keys[1]].split()[:-4])
#         #
#         # zip(*((float(t),float(x),float(y),float(z)) for tag,t,x,y,z,_,_,_,_ in (rttddft_dict[k].split() for k in propagation_keys) if tag == field_tag))
#         #
#         # print(len(rttddft_dict[dipcontrib_keys[2]].split()[:-4]))
#         #
#         # print(len(list(zip(from_orbital_nums,to_orbital_nums))))

#         dipcontribs = [
#             [float(x) for x in rttddft_dict[k].split()[:-4]]
#             for k in rttddft_dict.keys()
#             if "dipcontrib{0}".format(dipcontrib_dir) in k
#         ]
#         # need to cut out first two rows (don't currently understand these outputs from NWChem)
#         # first column (first row after transpose) represents the time
#         ia_pairs = np.array([(int(x), int(y)) for x, y in zip(*dipcontribs[0:2])])
#         dipcontrib_array = np.array(dipcontribs[2:]).T
#         time = dipcontrib_array[0]

#         return {
#             "time": units.Qty(value=time, unit=units.Unit(base="au_time")),
#             "dipole_contributions": units.Qty(
#                 value=dipcontribs, unit=units.au_dipole_moment
#             ),
#             "orbital_pairs": units.Qty(
#                 value=ia_pairs, unit=units.Unit(base="unitless")
#             ),
#         }

#         # if i is not None or a is not None:
#         #     if i is not None and a is None:
#         #         plot_inds = [ind+1 for ind,(j,b) in enumerate(ia_pairs) if j == i]
#         #     elif i is None and a is not None:
#         #         plot_inds = [ind+1 for ind,(j,b) in enumerate(ia_pairs) if b == a]
#         #     elif i is not None and a is not None:
#         #         plot_inds = [ind+1 for ind,(j,b) in enumerate(ia_pairs) if j == i and b == a]
#         #
#         #     ia_pair_inds = [ind-1 for ind in plot_inds]
#         #
#         #     return ia_pairs[ia_pair_inds],time,dipcontrib_array[plot_inds]
#         # else:

#     #     #     return ia_pairs,time,dipcontrib_array[1:]
#     #
#     # def plot_dipcontrib(self,rttddft_key,dipcontrib_dir,i=None,a=None):
#     #     ia_pairs,time,dipcontrib_array = self.get_dipcontribs(rttddft_key=rttddft_key,dipcontrib_dir=dipcontrib_dir)
#     #
#     #     if i is not None and a is None:
#     #         ia_pair_inds = [ind for ind,(j,b) in enumerate(ia_pairs) if j == i]
#     #     elif i is None and a is not None:
#     #         ia_pair_inds = [ind for ind,(j,b) in enumerate(ia_pairs) if b == a]
#     #     elif i is not None and a is not None:
#     #         ia_pair_inds = [ind for ind,(j,b) in enumerate(ia_pairs) if j == i and b == a]
#     #     else:
#     #         ia_pair_inds = [ind for ind,(j,b) in enumerate(ia_pairs)]
#     #
#     #     #!!! the * notation here is not correct yet - some occupied orbitals are included!!
#     #     for row in dipcontrib_array[ia_pair_inds]:
#     #         plt.plot(time,row)
#     #     plt.legend(['{0} --> {1}*'.format(x,y) for x,y in ia_pairs[ia_pair_inds]])
#     #     plt.show()
#     #
#     #     plt.plot(-0.5*np.sum(dipcontrib_array,0))


# # def parse_dipole(filename):
# #     dipole_dict = {}
# #     with open(filename,'r') as f:
# #         dmx_lines = [line for line in f if 'DMX' in line]
# #     with open(filename,'r') as f:
# #         dmy_lines = [line for line in f if 'DMY' in line]
# #     with open(filename,'r') as f:
# #         dmz_lines = [line for line in f if 'DMZ' in line]
# #
# #     dipole_dict['dmx_au'] = float(dmx_lines[0].split()[1])
# #     dipole_dict['dmx_efc_au'] = float(dmx_lines[0].split()[-1])
# #     dipole_dict['dmx_debye'] = float(dmx_lines[1].split()[1])
# #     dipole_dict['dmx_efc_debye'] = float(dmx_lines[1].split()[-1])
# #
# #     dipole_dict['dmy_au'] = float(dmy_lines[0].split()[1])
# #     dipole_dict['dmy_efc_au'] = float(dmy_lines[0].split()[-1])
# #     dipole_dict['dmy_debye'] = float(dmy_lines[1].split()[1])
# #     dipole_dict['dmy_efc_debye'] = float(dmy_lines[1].split()[-1])
# #
# #     dipole_dict['dmz_au'] = float(dmz_lines[0].split()[1])
# #     dipole_dict['dmz_efc_au'] = float(dmz_lines[0].split()[-1])
# #     dipole_dict['dmz_debye'] = float(dmz_lines[1].split()[1])
# #     dipole_dict['dmz_efc_debye'] = float(dmz_lines[1].split()[-1])
# #
# #     dipole_dict['total_dipole_au'] = np.linalg.norm([dipole_dict['dmx_au']+dipole_dict['dmx_efc_au'],dipole_dict['dmy_au']+dipole_dict['dmy_efc_au'],dipole_dict['dmz_au']+dipole_dict['dmz_efc_au']])
# #     dipole_dict['total_dipole_debye'] = np.linalg.norm([dipole_dict['dmx_debye']+dipole_dict['dmx_efc_debye'],dipole_dict['dmy_debye']+dipole_dict['dmy_efc_debye'],dipole_dict['dmz_debye']+dipole_dict['dmz_efc_debye']])
# #
# #     return dipole_dict


# from __future__ import annotations
# import os
# import subprocess

# from ...workflow.tasks.task import Task

# __all__ = ["ExecuteNWChem"]


# class ExecuteNWChem(Task):
#     def __init__(
#         self,
#         input_name,
#         output_name,
#         executable="nwchem",
#         work_directory=".",
#         num_cores=1,
#         parallel=False,
#         handlers=None,
#         name=None,
#     ):
#         super().__init__(handlers=handlers)
#         self.settings["input_path"] = materia.expand(
#             os.path.join(work_directory, input_name)
#         )
#         self.settings["output_path"] = materia.expand(
#             os.path.join(work_directory, output_name)
#         )
#         self.settings["scratch_directory"] = materia.expand(scratch_directory)

#         self.settings["executable"] = executable
#         self.settings["work_directory"] = materia.expand(work_directory)

#         self.settings["num_cores"] = num_cores
#         self.settings["parallel"] = parallel

#         try:
#             os.makedirs(self.settings["work_directory"])
#         except FileExistsError:
#             pass

#     def run(self):
#         with open(self.settings["output_path"], "w") as f:
#             if self.settings["parallel"]:
#                 subprocess.call(
#                     [
#                         "mpirun",
#                         "-np",
#                         str(self.settings["num_cores"]),
#                         self.settings["executable"],
#                         self.settnigs["input_path"],
#                     ],
#                     stdout=f,
#                 )
#             else:
#                 subprocess.call(
#                     [self.settings["executable"], self.settings["input_path"]], stdout=f
#                 )


# # from ..calculation import Calculation
# #
# # class NWChemPolarizability(Calculation):
# #     def __init__(self):
# #         raise NotImplementedError
# #
# # class NWChemRTTDDFT(Calculation):
# #     def __init__(self):
# #         raise NotImplementedError
# #
# # def compute_polarizability(self, molecule, num_cores, parallel, header_params={},\
# #                            geometry_params={}, set_geometry_params={}, basis_params={},\
# #                            dft_params={}, property_params={}, task_params={}):
# #
# #     input_path = os.path.join(self.scratch_directory,'polarizability.in')
# #     output_path = os.path.join(self.scratch_directory,'polarizability.out')
# #
# #     default_header_params = {'title':'molecule','echo':True,'scratch_dir':'./scratch','permanent_dir':'./permanent','start': True}
# #     merged_header_params = self._merge_new_params(old_params=default_header_params,new_params=header_params)
# #
# #     default_geometry_params = {'title': 'system', 'xyz_filepath': molecule.xyz.filepath}
# #     merged_geometry_params = self._merge_new_params(old_params=default_geometry_params,new_params=geometry_params)
# #
# #     default_set_geometry_params = {'set_params': {'variable_name': 'geometry', 'variable_value': '\"system\"'}}
# #     merged_set_geometry_params = self._merge_new_params(old_params=default_set_geometry_params,new_params=set_geometry_params)
# #
# #     default_basis_params = {'atom_strings': ('*',), 'library_strings': ('6-311G**',)}
# #     merged_basis_params = self._merge_new_params(old_params=default_basis_params,new_params=basis_params)
# #
# #     default_dft_params = {'direct': True, 'xc_params': {'xc_functional_strings': ('b3lyp',)}}
# #     merged_dft_params = self._merge_new_params(old_params=default_dft_params,new_params=dft_params)
# #
# #     default_property_params = {'response_order': 1, 'response_frequency': 0}
# #     merged_property_params = self._merge_new_params(old_params=default_property_params,new_params=property_params)
# #
# #     default_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'property'}}
# #     merged_task_params = self._merge_new_params(old_params=default_task_params,new_params=task_params)
# #
# #     input = NWChemInput()
# #     input.add_block(top=merged_header_params)
# #     input.add_block(geometry=merged_geometry_params)
# #     input.add_block(top=merged_set_geometry_params)
# #     input.add_block(basis=merged_basis_params)
# #     input.add_block(dft=merged_dft_params)
# #     input.add_block(property=merged_property_params)
# #     input.add_block(top=merged_task_params)
# #     input.write_input(filename=input_path)
# #
# #     self.execute(input_path=input_path,output_path=output_path,num_cores=num_cores,parallel=parallel)
# #
# #     output = NWChemOutput(filename=output_path)
# #
# #     molecule.polarizability = output.get_polarizability()
# #
# # def compute_dynamic_dipole_moment(self, molecule, num_cores, parallel,
# #                                   x=True, y=True, z=True, header_params={},
# #                                   geometry_params={}, set_geometry_params={},
# #                                   basis_params={}, dft_params={}, dft_task_params={},
# #                                   rttddft_x_params={}, rttddft_x_task_params={},
# #                                   rttddft_y_params={}, rttddft_y_task_params={},
# #                                   rttddft_z_params={}, rttddft_z_task_params={}):
# #
# #     input_path = os.path.join(self.scratch_directory,'dynamic_dipole_moment.in')
# #     output_path = os.path.join(self.scratch_directory,'dynamic_dipole_moment.out')
# #
# #     input = NWChemInput()
# #
# #     default_header_params = {'title':'molecule','echo':True,'scratch_dir':'./scratch','permanent_dir':'./permanent','start': True}
# #     merged_header_params = self._merge_new_params(old_params=default_header_params,new_params=header_params)
# #     input.add_block(top=merged_header_params)
# #
# #     default_geometry_params = {'title': 'system', 'xyz_filepath': molecule.xyz.filepath}
# #     merged_geometry_params = self._merge_new_params(old_params=default_geometry_params,new_params=geometry_params)
# #     input.add_block(geometry=merged_geometry_params)
# #
# #     default_set_geometry_params = {'set_params': {'variable_name': 'geometry', 'variable_value': '\"system\"'}}
# #     merged_set_geometry_params = self._merge_new_params(old_params=default_set_geometry_params,new_params=set_geometry_params)
# #     input.add_block(top=merged_set_geometry_params)
# #
# #     default_basis_params = {'atom_strings': ('*',), 'library_strings': ('6-311G**',)}
# #     merged_basis_params = self._merge_new_params(old_params=default_basis_params,new_params=basis_params)
# #     input.add_block(basis=merged_basis_params)
# #
# #     default_dft_params = {'direct': True, 'xc_params': {'xc_functional_strings': ('b3lyp',)}}
# #     merged_dft_params = self._merge_new_params(old_params=default_dft_params,new_params=dft_params)
# #     input.add_block(dft=merged_dft_params)
# #
# #     default_dft_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'energy'}}
# #     merged_dft_task_params = self._merge_new_params(old_params=default_dft_task_params,new_params=dft_task_params)
# #     input.add_block(top=merged_dft_task_params)
# #
# #     if x:
# #         default_rttddft_x_params = {'tmax':500.0,'dt':0.1,'tag':'kickx','print_dipole':True,
# #                                     'load_type': 'vectors', 'load_from': os.path.join(self.scratch_directory,'permanent','molecule.movecs'),
# #                                     'field_params':{'field_name':'kick','shape':'delta','polarization':'x','max': 1e-4},
# #                                     'excite_params':{'geometry_name':'system','field_name':'kick'}}
# #         merged_rttddft_x_params = self._merge_new_params(old_params=default_rttddft_x_params,new_params=rttddft_x_params)
# #         input.add_block(rttddft=merged_rttddft_x_params)
# #
# #         default_rttddft_x_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'rt_tddft'}}
# #         merged_rttddft_x_task_params = self._merge_new_params(old_params=default_rttddft_x_task_params,new_params=rttddft_x_task_params)
# #         input.add_block(top=merged_rttddft_x_task_params)
# #
# #     if y:
# #         default_rttddft_y_params = {'tmax':500.0,'dt':0.1,'tag':'kicky','print_dipole':True,
# #                                     'load_type': 'vectors', 'load_from': os.path.join(self.scratch_directory,'permanent','molecule.movecs'),
# #                                     'field_params':{'field_name':'kick','shape':'delta','polarization':'y','max': 1e-4},
# #                                     'excite_params':{'geometry_name':'system','field_name':'kick'}}
# #         merged_rttddft_y_params = self._merge_new_params(old_params=default_rttddft_y_params,new_params=rttddft_y_params)
# #         input.add_block(rttddft=merged_rttddft_y_params)
# #
# #         default_rttddft_y_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'rt_tddft'}}
# #         merged_rttddft_y_task_params = self._merge_new_params(old_params=default_rttddft_y_task_params,new_params=rttddft_y_task_params)
# #         input.add_block(top=merged_rttddft_y_task_params)
# #
# #     if z:
# #         default_rttddft_z_params = {'tmax':500.0,'dt':0.1,'tag':'kickz','print_dipole':True,
# #                                     'load_type': 'vectors', 'load_from': os.path.join(self.scratch_directory,'permanent','molecule.movecs'),
# #                                     'field_params':{'field_name':'kick','shape':'delta','polarization':'z','max': 1e-4},
# #                                     'excite_params':{'geometry_name':'system','field_name':'kick'}}
# #         merged_rttddft_z_params = self._merge_new_params(old_params=default_rttddft_z_params,new_params=rttddft_z_params)
# #         input.add_block(rttddft=merged_rttddft_z_params)
# #
# #         default_rttddft_z_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'rt_tddft'}}
# #         merged_rttddft_z_task_params = self._merge_new_params(old_params=default_rttddft_z_task_params,new_params=rttddft_z_task_params)
# #         input.add_block(top=merged_rttddft_z_task_params)
# #
# #     input.write_input(input_path)
# #
# #     self.execute(input_path=input_path,output_path=output_path,num_cores=num_cores,parallel=parallel)
# #
# #     output = NWChemOutput(filename=output_path)
# #
# #     tddipole_dict = output.get_tddipole()
# #
# #     molecule.tddipole_x = (tddipole_dict['time'],tddipole_dict['mu_x'])
# #     molecule.tddipole_y = (tddipole_dict['time'],tddipole_dict['mu_y'])
# #     molecule.tddipole_z = (tddipole_dict['time'],tddipole_dict['mu_z'])
