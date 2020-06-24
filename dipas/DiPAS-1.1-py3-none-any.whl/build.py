"""Functionality for building an accelerator lattice using PyTorch as a backend."""

from argparse import Namespace
from functools import partial, reduce, wraps
import inspect
import itertools as it
import math
import re
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple, Type, Union, get_type_hints
from typing_extensions import Literal
import warnings

from jinja2 import Environment, PackageLoader
import numpy as np
import pandas as pd
import pint
import scipy.constants as constants
import torch

from . import elements
from .elements import AlignmentError, LatticeElement, Segment, SelectionCriteria, SingleElementSelector, \
    setup_matching_criteria, match_element, tensor
from .external import Paramodi
from .madx.parser import Script, Command, Variable, DeferredExpression, parse_file, parse_script, extract_sequence, \
    particle_dict, label_every_element, pad_sequence, extract_error_definitions, generate_error_specifications, patterns
from .madx.builder import write_attribute_value as write_attribute_value_madx
from .madx.utils import convert_tfs


__all__ = ['Lattice', 'Beam',
           'from_file', 'from_script', 'from_twiss', 'from_device_data',
           'update_from_twiss', 'update_from_paramodi', 'assign_errors',
           'collect_device_data',
           'create_script', 'sequence_script', 'error_script', 'track_script']

PaddingSpec = SelectionCriteria[Union[float, Tuple[float, ...]]]
MADXCommand = Command


class BuildError(Exception):
    """Raised from errors occurring during the lattice building process."""


class Beam:
    """Beam particle and energy definition.

    The particle type must be specified by either `particle` or `(charge, mass)` and is considered in that order of
    precedence. The energy must be specified by one of `energy, pc, gamma, beta, brho` and is considered in that order
    of precedence.

    Attributes
    ----------
    particle : str, optional
        The name of the particle type; must be registered in `madx.parser.particle_dict`, otherwise use `mass` and
        `charge` to define the particle type. `particle` takes precedence over `(charge, mass)`.
    charge : int, optional
        Charge state in units of the elementary charge.
    mass : float, optional
        Rest mass in units of [GeV].
    energy : float, optional
        Total energy per particle in units of [GeV]. The order of precedence for beam energy definition is the same as
        attributes are listed here.
    pc : float, optional
        Particle momentum times the speed of light in units of [GeV].
    gamma : float, optional
        Relativistic gamma factor of the particles.
    beta : float, optional
        Relativistic beta factor of the particles.
    brho : float, optional
        Magnetic rigidity of the particles in units of [T*m].

    Raises
    ------
    ValueError
        If either the particle or the energy specification is incomplete.
    """
    particle : str
    charge : int
    mass : float
    energy : float
    pc : float
    gamma : float
    beta : float
    brho : float

    energy_definition_precedence = ('energy', 'pc', 'gamma', 'beta', 'brho')

    def __init__(self, particle: str = None, charge: int = None, mass: float = None, energy: float = None,
                 pc: float = None, gamma: float = None, beta: float = None, brho: float = None, **kwargs):
        if particle is not None:
            self.particle = particle
            if particle == 'ion' and charge is not None:
                self.charge = charge
            if particle == 'ion' and mass is not None:
                self.mass = mass
        elif charge is not None and mass is not None:
            self.charge = charge
            self.mass = mass
        else:
            raise ValueError('Either particle or charge and mass need to be specified')
        try:
            args = locals()
            setattr(self, *next((x, args[x]) for x in self.energy_definition_precedence if args[x] is not None))
        except StopIteration:
            raise ValueError(f'Beam energy must be specified via one of {self.energy_definition_precedence}') from None

    @property
    def particle(self) -> str:
        return self._particle

    @particle.setter
    def particle(self, name: str) -> None:
        try:
            particle = particle_dict[name]
        except KeyError:
            raise ValueError(f'Unknown particle type: {name}')
        self._charge = particle['charge']
        self._mass = particle['mass']
        self._particle = name

    @property
    def charge(self) -> int:
        return self._charge

    @charge.setter
    def charge(self, charge) -> None:
        self._charge = charge
        self._particle = 'custom'

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, mass) -> None:
        self._mass = mass
        self._particle = 'custom'

    @property
    def pc(self) -> float:
        return math.sqrt(self.energy**2 - self.mass**2)

    @pc.setter
    def pc(self, pc: float) -> None:
        self.energy = math.sqrt(pc**2 + self.mass**2)

    @property
    def gamma(self) -> float:
        return self.energy / self.mass

    @gamma.setter
    def gamma(self, gamma: float) -> None:
        self.energy = gamma * self.mass

    @property
    def beta(self) -> float:
        return math.sqrt(1. - 1./self.gamma**2)

    @beta.setter
    def beta(self, beta: float) -> None:
        self.energy = self.mass / math.sqrt(1. - beta**2)

    @property
    def brho(self) -> float:
        return self.pc / (abs(self.charge) * constants.speed_of_light * 1e-9)

    @brho.setter
    def brho(self, brho: float) -> None:
        self.pc = brho * abs(self.charge) * constants.speed_of_light * 1e-9

    def to_dict(self) -> dict:
        dict_ = {attr: getattr(self, attr) for attr in get_type_hints(type(self))}
        if dict_['particle'] == 'custom':
            del dict_['particle']
        return dict_

    @classmethod
    def remove_duplicates(cls, beam: dict) -> dict:
        """Remove duplicate specifications from the given beam dict.

        The order of precedence is determined by `Beam.energy_definition_precedence` as well as the fact that
        `particle` takes precedence over `(mass, charge)`.
        """
        beam = beam.copy()
        energy_specs = iter(cls.energy_definition_precedence)
        for spec in energy_specs:
            if spec in beam:
                for duplicate in set(energy_specs) & beam.keys():
                    del beam[duplicate]
        if beam.get('particle') in (particle_dict.keys() - {'ion'}):
            for duplicate in {'mass', 'charge'} & beam.keys():
                del beam[duplicate]
        return beam


class BeamBetaGamma:
    """Relativistic beta and gamma factors."""
    beta : float
    gamma : float

    def __init__(self, beta: float = None, gamma: float = None):
        if gamma is not None:
            self.gamma = gamma
        elif beta is not None:
            self.beta = beta
        else:
            raise ValueError('Either beta or gamma must be specified')

    @property
    def beta(self) -> float:
        return math.sqrt(1 - 1/self.gamma**2)

    @beta.setter
    def beta(self, beta: float) -> None:
        self.gamma = 1 / math.sqrt(1 - beta**2)

    def to_dict(self) -> dict:
        """Convert the beam representation to a dict containing both 'beta' and 'gamma'."""
        return {attr: getattr(self, attr) for attr in get_type_hints(type(self))}


def augment_beam(beam: dict) -> dict:
    """Augment the given beam definition by the properties defined at :class:`Beam`."""
    try:
        return Beam(**beam).to_dict()
    except ValueError:
        if beam.keys() & {'beta', 'gamma'}:
            return BeamBetaGamma(**beam).to_dict()
        raise


class Lattice:
    """Helper class for building a lattice for a given beam definition.

    Parameters
    ----------
    beam : dict
        The beam definition, conforming to `build.augment_beam`.
    """
    Marker = elements.Marker
    Drift = elements.Drift
    Instrument = elements.Instrument
    Placeholder = elements.Placeholder
    Monitor = elements.Monitor
    HMonitor = elements.HMonitor
    VMonitor = elements.VMonitor
    Kicker = elements.Kicker
    HKicker = elements.HKicker
    VKicker = elements.VKicker
    TKicker = elements.TKicker
    Quadrupole = elements.Quadrupole
    Sextupole = elements.Sextupole
    SBend = elements.SBend
    RBend = elements.RBend
    Dipedge = elements.Dipedge
    ThinQuadrupole = elements.ThinQuadrupole
    ThinSextupole = elements.ThinSextupole

    def __init__(self, beam: dict, *, autolabel: bool = True):
        self.beam = augment_beam(beam)
        self.elements = []  # type: List[LatticeElement]
        self.positions = []  # type: List[float]
        self.labels = {}  # type: Dict[str, Tuple[float, LatticeElement]]
        self.autolabel = autolabel
        self.label_generator = (f'e{i}' for i in it.count(1))
        self._immediate_append = False

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def __enter__(self):
        self._immediate_append = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._immediate_append = False

    def __getattribute__(self, item):
        obj = super().__getattribute__(item)
        if inspect.isclass(obj) and issubclass(obj, torch.nn.Module):
            @wraps(obj)
            def _proxy(*args, **kwargs):
                kwargs.setdefault('beam', self.beam)
                if self.autolabel:
                    kwargs.setdefault('label', next(self.label_generator))
                element = obj(*args, **kwargs)
                if self._immediate_append:
                    self.append(element)
                return element
            return _proxy
        return obj

    def __iadd__(self, other):
        if isinstance(other, torch.nn.Module):
            self.append(other)
        else:
            self.extend(other)
        return self

    def __setitem__(self, position: Union[float, Tuple[str, float]], element: LatticeElement):
        """Add a lattice element at the specified position.

        Parameters
        ----------
        position : float or tuple of (str, float)
            Indicates the position of the entrance of `element`. If float then the absolute position in the lattice.
            Must be greater than or equal to the position of the exit of the last element. If tuple then the first item
            indicates the element w.r.t. which the position, the second item, is taken
            (i.e. ``position == (label, rel_pos)``). Note that ``rel_pos`` is the position relative to the exit of
            element ``label``.
        element : LatticeElement
        """
        if isinstance(position, tuple):
            s_ref, e_ref = self.labels[position[0]]
            position = s_ref + e_ref.l.item() + position[1]
        offset = position - self.s
        if offset < 0:
            raise BuildError(f'Negative offset between elements: {offset}')
        if offset > 0:
            self.append(elements.Drift(l=offset, beam=self.beam))
        self.append(element)

    def __getitem__(self, item: Union[int, str]):
        """Get a lattice element, either by index or by label.

        Parameters
        ----------
        item : int or str
            If int then the index position in the lattice, if str then the label of the element.
        """
        if isinstance(item, int):
            return self.elements[item]
        elif isinstance(item, str):
            return self.labels[item][1]
        else:
            raise TypeError(f'Invalid type for selecting a lattice element: {type(item)}')

    def __repr__(self):
        return '\n'.join(f'[{p:12.6f}]  {e!r}' for p, e in zip(self.positions, self.elements))

    @property
    def s(self) -> float:
        return (self.positions[-1] + self.elements[-1].l.item()) if self.positions else 0

    def append(self, element):
        self.positions.append(self.s)
        self.elements.append(element)
        self.labels[element.label] = (self.positions[-1], element)

    def extend(self, multiple_elements: Sequence[LatticeElement]):
        for element in multiple_elements:
            self.append(element)


def from_file(f_name: str, *, beam: dict = None,
              errors: Union[bool, pd.DataFrame] = True,
              paramodi: Union[str, pd.DataFrame] = None,
              padding: PaddingSpec = None) -> Segment:
    """Build lattice from MADX script file.

    Uses the first beam command and the first sequence encountered via `USE` when parsing the script. If no `USE`
    command is found then the first `SEQUENCE` in the script is considered.

    Parameters
    ----------
    f_name : str
        File path pointing to the MADX script.
    beam : dict, optional
        Beam specification similar to the MADX command `beam`. If not provided then the script will be searched for a
        `beam` command instead. Otherwise the user provided beam specification will override any specification in the
        script.
    errors : bool or str, optional
        Whether and how to assign alignment errors to lattice elements. The following options are available:
          * `False` - Ignore error specifications in the script.
          * `True` - Apply error specifications from the script, interpreting any involved expressions. In case no
            random functions are involved in error specification the final values will be the same (when comparing the
            thus built lattice and MADX). However if random functions are involved then, even if the same seed for the
            random number generator (RNG) is used, the final values are likely to differ because MADX uses a different
            RNG than the present parser. Hence this option will result in alignment errors for the same elements and
            values from the same random variates, but not exactly the same values.
          * `pd.DataFrame` - For details about the structure see :func:`apply_errors`. Using a data frame the exact same
             values (from MADX) will be assigned. In order to ensure compatibility across multiple runs of the script,
             make sure to also set ``eoption, seed = <rng_seed>``.
    paramodi : str or pd.DataFrame, optional
        Device settings to be used when building the lattice. Can be either the file path pointing to a paramodi file
        or a corresponding data frame, as returned by :meth:`external.Paramodi.parse`.
        Note that the first encountered `purpose` is used, if that is undesired, the data frame should be filtered
        accordingly. For details see :func:`update_from_paramodi`.
    padding : float or tuple or dict, optional
        Additional padding applied to lattice elements. See :class:`elements.Aperture`.

    Returns
    -------
    lattice : Segment

    See Also
    --------
    :func:`assign_errors` -- For application of error definitions.
    :func:`update_from_paramodi` -- For parameter updates from paramodi files.
    """
    return _from_command_list(parse_file(f_name), beam=beam, errors=errors, paramodi=paramodi, padding=padding)


def from_script(script: str, *, beam: dict = None,
                errors: Union[bool, pd.DataFrame] = True,
                paramodi: Union[str, pd.DataFrame] = None,
                padding: PaddingSpec = None) -> Segment:
    """Build lattice from MADX script (for details see :func:`from_file`)."""
    return _from_command_list(parse_script(script), beam=beam, errors=errors, paramodi=paramodi, padding=padding)


def from_twiss(twiss: Union[str, pd.DataFrame], *, beam: dict,
               center: bool = False,
               errors: Optional[pd.DataFrame] = None,
               paramodi: Optional[pd.DataFrame] = None,
               padding: Optional[PaddingSpec] = None) -> Segment:
    """Build lattice from the given device data (optionally applying errors and/or paramodi specifications).

    Parameters
    ----------
    twiss : str or pd.DataFrame
        File path pointing to a TWISS file or corresponding data frame such as returned by
        :func:`dipas.madx.utils.convert_tfs`. Must contain the following columns:
        ``NAME, KEYWORD, S, ... any required element attributes ...``.
    errors : pd.DataFrame
        See :func:`from_file`.
    paramodi : pd.DataFrame
        See :func:`from_file`.
    padding : PaddingSpec
        See :func:`from_file`.

    Returns
    -------
    lattice : Segment
    """
    if isinstance(twiss, str):
        twiss = convert_tfs(twiss, meta=False)
    twiss = twiss.set_index('NAME')
    twiss.columns = twiss.columns.str.lower()
    length_scale = 0.5 if center else 1.0
    commands = []
    sequence = twiss.iterrows()
    s = next(sequence)[1]['s']
    for label, data in sequence:
        data = data.to_dict()
        keyword = data.pop('keyword').lower()
        if keyword in {'hkicker', 'vkicker'}:
            data['kick'] = data.get(keyword[:-2], 0)
            data.pop('hkick', None)
            data.pop('vkick', None)
        length = (data['s'] - s) / length_scale
        s = data['s'] + length * (1 - length_scale)
        if length > 0:
            for kl in (f'k{i}{skew}l' for i in range(1, 21) for skew in ('', 's')):
                data[kl[:-1]] = data.get(kl) / length
        data = {k: v for k, v in data.items() if k in get_attribute_names(elements.elements[keyword])}
        data.update(l=length)
        commands.append(MADXCommand(keyword, data, label.lower()))
    lattice = _from_sequence(beam, commands, padding=padding)
    if paramodi is not None:
        update_from_paramodi(lattice, paramodi)
    if errors:
        assign_errors(lattice, errors)
    return lattice


def from_device_data(devices: pd.DataFrame, *, beam: dict,
                     errors: Optional[pd.DataFrame] = None,
                     paramodi: Optional[pd.DataFrame] = None,
                     padding: Optional[PaddingSpec] = None) -> Segment:
    """Build lattice from the given device data (optionally applying errors and/or paramodi specifications).

    Parameters
    ----------
    devices : pd.DataFrame
        Indices are element labels and columns are attributes. For details see :func:`collect_device_data`.
    errors : pd.DataFrame
        See :func:`from_file`.
    paramodi : pd.DataFrame
        See :func:`from_file`.
    padding : PaddingSpec
        See :func:`from_file`.

    Returns
    -------
    lattice : Segment
    """
    sequence = []
    for label, data in devices.iterrows():
        if data['type'] in {'hkicker', 'vkicker'}:
            data = data.drop(['hkick', 'vkick'], errors='ignore')
        type_ = data.pop('type')
        data = data.dropna().to_dict()
        a_errors = {k: data.pop(k) for err_cls in elements.alignment_errors.values() if err_cls is not elements.Tilt
                    for k in get_attribute_names(err_cls) if k in data}
        sequence.append(MADXCommand(type_, data, label))
        if a_errors:
            errors.setdefault(label, {}).update(a_errors)
    lattice = _from_sequence(beam, sequence, padding=padding)
    if paramodi is not None:
        update_from_paramodi(lattice, paramodi)
    if errors:
        assign_errors(lattice, errors)
    return lattice


def _from_command_list(script: Script, *, beam: dict = None,
                       errors: Union[bool, pd.DataFrame] = True,
                       paramodi: Union[str, pd.DataFrame] = None,
                       padding: PaddingSpec = None) -> Segment:
    """Build lattice from the parsed script (for details see :func:`from_file`)"""
    if not beam:
        try:
            beam = next(c for c in script.commands if c.keyword == 'beam').attributes
        except StopIteration:
            raise BuildError("'beam' command not found") from None
    try:
        seq_label = next(c for c in script.commands if c.keyword == 'use')['sequence']
    except StopIteration:
        seq_label = None
    seq_pars, sequence = extract_sequence(script.commands, script.context, label=seq_label)
    if 'l' in seq_pars:
        sequence = list(pad_sequence(sequence, seq_pars.pop('l'), **seq_pars))
    if errors is True:
        # Generating errors must come before labelling because range selectors only work without labels.
        errors = generate_error_specifications(extract_error_definitions(script.commands, seq_label), sequence)
        sequence = label_every_element(sequence)
        # build_lattice skips over unknown elements so we can't use absolute positions in the sequence for errors specs.
        pos_to_label = pd.DataFrame.from_dict({i: {'label': c.label} for i, c in enumerate(sequence)}, orient='index')
        pos_to_label = pos_to_label.assign(count=pos_to_label.groupby('label').cumcount())
        errors = {tuple(pos_to_label.loc[i]): err for i, err in errors.items()}
    lattice = _from_sequence(beam, label_every_element(sequence), padding=padding)
    if paramodi is not None:
        update_from_paramodi(lattice, paramodi)
    if isinstance(errors, (dict, pd.DataFrame)):
        assign_errors(lattice, errors)
    return lattice


def _from_sequence(beam: dict, sequence: Iterable[Command], *, padding: PaddingSpec = None) -> Segment:
    """Build lattice from the given sequence of commands.

    Parameters
    ----------
    beam : dict
        Beam definition analogue to MADX.
    sequence : iterable
        List of commands which form the sequence.
    padding : float or tuple or dict
        Additional padding applied to lattice elements. See :class:`elements.Aperture`. For details on how to use dict
        keys to fine-tune the padding per element see :meth:`elements.Segment.makethin` (this works similarly).

    Returns
    -------
    lattice : Segment
        Containing elements' corresponding backend instances.
    """
    beam = augment_beam(beam)
    padding = setup_matching_criteria(padding, (float, tuple), optional=True, default=0.)
    lattice = []
    for command in sequence:
        try:
            cls = elements.elements[command.root.keyword]
        except KeyError:
            warnings.warn(f'Skipping element (no equivalent implementation found): {command}')
            continue
        attributes = {}
        # noinspection PyTypeChecker
        aperture = {'padding': next((v for k, v in padding if (inspect.isclass(k) and issubclass(cls, k)
                                                               or match_element(k, Namespace(label=command.label)))))}
        for key, value in _convert_attribute_values(command.attributes).items():
            if key.startswith('aper'):
                if key != 'aperture':
                    key = re.sub(r'(?<=^)aper_?', '', key, 1)
                if key == 'type':
                    value = elements.aperture_types[value]
                aperture[key] = value
            else:
                attributes[key] = value
        if aperture.get('type') is elements.ApertureCircle and 'aperture' in aperture and len(aperture['aperture'].shape):
            aperture['aperture'] = aperture['aperture'][0]
        if attributes.get('tilt', 0) != 0:
            tilt = partial(elements.Tilt, psi=attributes.pop('tilt'))
        else:
            tilt = False
        attributes.setdefault('l', 0.)
        attributes['beam'] = beam
        attributes['label'] = command.label
        attributes['aperture'] = aperture.pop('type', elements.ApertureCircle)(**aperture)
        attributes.pop('at', None)
        attributes.pop('from', None)
        element = cls(**attributes)
        if tilt:
            element = tilt(element)
        lattice.append(element)
    return Segment(lattice)


def update_from_twiss(lattice: Segment, twiss: Union[str, pd.DataFrame]) -> None:
    """Update the given lattice with the attributes specified in the given TWISS data.

    Parameters
    ----------
    lattice : :class:`Segment`
    twiss : str or pd.DataFrame
        File name pointing to the TWISS file or equivalent data frame (such as returned by
        :func:`dipas.madx.utils.convert_tfs`).
    """
    if isinstance(twiss, str):
        twiss = convert_tfs(twiss, meta=False)
    else:
        twiss = twiss.copy()
    if twiss.index.name is None:
        twiss = twiss.set_index('NAME')
    twiss.columns = twiss.columns.str.lower()
    for element in lattice:
        try:
            specs = twiss.loc[element.label].to_dict()
        except KeyError:
            continue
        if isinstance(element, AlignmentError):
            element = element.element
        if element.l > 0:
            for kl in (f'k{i}{skew}l' for i in range(1, 21) for skew in ('', 's')):
                if kl in specs:  # Only update data if present (no fallback on zero).
                    specs[kl[:-1]] = specs[kl] / element.l.item()
        for name in set(get_attribute_names(element)) & specs.keys():
            getattr(element, name).data = tensor(specs[name])
        element.update_transfer_map()


def update_from_paramodi(lattice: Segment, paramodi: Union[str, pd.DataFrame]) -> None:
    """Apply the specified paramodi definitions to the given lattice in-place.

    The following paramodi specifications are currently supported (others are ignored):

    * **[SBend]**
      * ``hkick`` - Increases/Decreases the SBend's ``angle`` attribute.
    * **[Quadrupole]**
      * ``kl`` - Replaces the Quadrupole's ``k1`` attribute.
    * **[HKicker]**
      * ``hkick`` - Replaces the HKicker's ``kick`` attribute.
    * **[VKicker]**
      * ``vkick`` - Replaces the VKicker's ``kick`` attribute.

    Parameters
    ----------
    lattice : :class:`Segment`
    paramodi : str or pd.DataFrame
        File name pointing to the paramodi file or data frame with layout corresponding to :meth:`external.Paramodi.parse`.
    """
    if isinstance(paramodi, str):
        paramodi = Paramodi.parse(paramodi)
    ur = pint.UnitRegistry()
    for element in lattice:
        try:
            specs = paramodi.loc[element.label]
        except KeyError:
            continue
        attributes = specs.groupby(level=0).first()  # Select first purpose.
        attributes = dict(Paramodi.apply_units(attributes))
        if isinstance(element, AlignmentError):
            element = element.element
        if isinstance(element, elements.SBend):
            try:
                h_kick = tensor(attributes['hkick'].to(ur.rad).magnitude)
            except KeyError:
                continue
            else:
                element.angle.data += h_kick
                element.dk0.data += h_kick / element.l
        elif isinstance(element, elements.Quadrupole):
            try:
                element.k1.data = attributes['kl'].to(1 / ur.meter).magnitude / element.l
            except KeyError:
                continue
        elif isinstance(element, (elements.HKicker, elements.VKicker)):
            try:
                kick = attributes['hkick'] if isinstance(element, elements.HKicker) else attributes['vkick']
            except KeyError:
                continue
            else:
                element.kick.data = tensor(kick.to(ur.rad).magnitude)
        element.update_transfer_map()


def assign_errors(lattice: Segment,
                  errors: Union[pd.DataFrame, Dict[SingleElementSelector, Dict[str, Any]]]) -> None:
    """Assign alignment errors to lattice elements (modifies the given lattice in-place, replacing elements).

    .. Note:: Only non-zero error values will be considered.

    Parameters
    ----------
    lattice : Segment
    errors : pd.DataFrame or dict of (identifier, dict)
        If a data frame is given and it contains a column ``NAME`` (or ``name``) this column will be taken as the
        element labels, otherwise the row index must contain the element labels. The column names must correspond to
        error names.
        If a dict is given, `identifier` should be a type matching `elements.SingleElementSelector` and thus uniquely
        identify an element when used as ``lattice[identifier]``. The dicts should contain the error definition for the
        corresponding element.
        For a data frame with a unique index, providing ``df`` and ``df.to_dict(orient='index')`` is equivalent.

    Raises
    ------
    BuildError
        If the data frame contains unsupported error specifications with non-zero values.

    Examples
    --------
    >>> from dipas.madx import convert
    >>> errors = convert('errors.tfs')  # previously generated via `esave` command
    >>> assign_errors(lattice, errors)
    """
    if isinstance(errors, pd.DataFrame):
        errors = errors.copy()
        errors.columns = errors.columns.str.lower()
        if 'name' not in errors.columns:
            errors.index.name = 'name'
            errors.reset_index(inplace=True)
        errors['name'] = errors['name'].str.lower()
        errors['name_count'] = errors.groupby(errors['name']).cumcount()
        errors.set_index(['name', 'name_count'], inplace=True)
        errors = errors.to_dict(orient='index')
    for identifier, error_dict in errors.items():
        error_dict = _convert_attribute_values(error_dict)
        error_dict = {k.lower(): v for k, v in error_dict.items() if v != 0}
        if not error_dict:
            continue
        element = lattice[identifier]
        error_cls = filter(
            lambda tup: any(x != 0 for x in tup[1].values()),
            map(lambda cls: (cls, {n: error_dict.pop(t, 0.) for n, t in zip(get_attribute_names(cls), cls.triggers)}),
                elements.alignment_errors.values()))
        error_cls = sorted(error_cls, key=lambda tup: tup[0].__name__)
        if error_cls:
            lattice[identifier] = reduce(lambda e, tup: tup[0](e, **tup[1]), error_cls, element)
        if not error_dict:
            continue
        if isinstance(element, AlignmentError):
            element = element.element
        for name, value in error_dict.items():  # Field errors.
            if isinstance(element, elements.Kicker) and name in ('k0l', 'k0sl'):
                name = 'hkick' if name == 'k0l' else 'vkick'
            if name not in element.field_errors and name.endswith('l') and name[:-1] in element.field_errors:
                if element.l == 0:
                    raise BuildError(f"Can't assign integrated field error {name!r} to zero length element: {element}")
                name = name[:-1]
                value = value / element.l
            if name in element.field_errors:
                old_value = getattr(element, element.field_errors[name])
                old_value.data += value
                if isinstance(value, elements.Parameter) and not isinstance(old_value, elements.Parameter):
                    setattr(element, element.field_errors[name], elements.Parameter(old_value))
            else:
                raise BuildError(f'Unsupported field error specification {name!r} for element {element}')
        element.update_transfer_map()


def _convert_attribute_values(obj: dict) -> dict:
    """Convert Variable and DeferredExpression to appropriate counterparts."""
    new = {}
    for key, value in obj.items():
        if isinstance(value, (DeferredExpression, Variable)):
            is_variable, value = Variable.unwrap(value)
        else:
            is_variable = False
        value = elements.prepare_attribute_value(value)
        if is_variable:
            value = elements.Parameter(value)
        new[key] = value
    return new


def collect_device_data(lattice: Segment) -> pd.DataFrame:
    """Collect the attributes of lattice elements in a data frame.

    .. Note:: Values are NaN where the corresponding attribute is not applicable to a particular element.

    Parameters
    ----------
    lattice : Segment

    Returns
    -------
    device_data : pd.DataFrame
        Row indices are element labels and column names are attribute names.
    """
    devices = {}
    for element in lattice:
        data = {}
        while isinstance(element, AlignmentError):
            data.update({k: getattr(element, k).numpy() for k in get_attribute_names(type(element))})
            if type(element) is elements.Tilt:
                data['tilt'] = data.pop('psi')
            element = element.target
        data.update({k: getattr(element, k).detach().numpy() for k in get_attribute_names(element)})
        data.update({k: getattr(element, k).detach().numpy() for k in element.field_errors.values()})
        data.update(type=type(element).__name__.lower())
        if element.aperture is not None:
            data.update(apertype=type(element.aperture).__name__.lower().replace('aperture', '', 1),
                        aperture=element.aperture.aperture.numpy(),
                        aper_offset=element.aperture.offset.numpy())
        devices[element.label] = data
    return pd.DataFrame.from_dict(devices, orient='index')


def get_attribute_names(element: Union[LatticeElement, Type[LatticeElement]]) -> List[str]:
    """Return a list containing the element's attribute names."""
    element_type = element if isinstance(element, type) else type(element)
    return [name for name in get_type_hints(element_type)]


class SerializerError(Exception):
    """Exception raised upon errors encountered when serializing a lattice to a MADX script."""
    pass


class Command(dict):
    def __init__(self, keyword, attributes):
        super().__init__()
        self['keyword'] = keyword
        self['attributes'] = attributes


get_template = Environment(loader=PackageLoader('dipas'), trim_blocks=True, lstrip_blocks=True).get_template


def create_script(beam: dict, *,
                  sequence: Union[str, Segment],
                  errors: Union[Literal[True], Segment, str] = '',
                  track: str = '') -> str:
    """Create a MADX script that can be used for particle tracking in the given sequence.

    .. Note:: The `sequence` string must start with the sequence's label.

    Parameters
    ----------
    beam : dict
        Beam configuration that will be transformed to the "beam" command.
    sequence : str or :class:`Segment`
        Part of the script describing the sequence.
    errors : True or :class:`Segment` or str
        Part of the script describing error definitions. If `True` then `sequence` must be a Segment and it will be used
        to generate the error specifications.
    track : str
        Part of the script describing the tracking.

    Returns
    -------
    script : str
        The compound MADX script.

    Raises
    ------
    SerializerError
        If the `sequence` string does not start with a label.
    """
    beam = Beam.remove_duplicates(beam)
    if errors is True:
        if not isinstance(sequence, Segment):
            raise ValueError(f'If errors is True then sequence must be a Segment (got {type(sequence)} instead)')
        errors = sequence
    if isinstance(errors, Segment):
        errors = error_script(errors)
    if isinstance(sequence, Segment):
        sequence = sequence_script(sequence)
    sequence_cmd = sequence.splitlines()[0].rstrip(';')
    match = re.match(patterns['command'], sequence_cmd)
    if match is None or match.group('label') is None:
        raise SerializerError(f'Invalid sequence command (must contain a label): {sequence_cmd}')
    return get_template('script.madx.j2').render(
        beam=Command('beam', beam), sequence=sequence, use=Command('use', {'sequence': match.group('label')}),
        errors=errors, track=track
    ).rstrip('\n')


def sequence_script(lattice: Segment, label: str = 'seq', *, markup: str = 'madx') -> str:
    """Convert the given lattice to a corresponding MADX sequence script or HTML file.

    .. Important:: The sequence must not assume implicit drift spaces; elements are laid out as presented.

    Parameters
    ----------
    lattice: Segment
        The lattice to be converted. Elements are placed one after another (no implicit drifts).
    label: str, optional
        The label of the sequence to be used in the script.
    markup: str, optional
        The markup language which is used for dumping the sequence; one of {"madx", "html"}.

    Returns
    -------
    script : str
    """
    sequence = lattice.flat().elements
    at = [0.] + np.cumsum([element.l for element in sequence]).tolist()
    variables = {
        'label': label,
        'sequence': Command('sequence', {'l': write_attribute_value(at[-1]), 'refer': 'entry'}),
        'elements': [{'label': e.label or f'element_{i}', 'command': serialize_element(e), 'at': at[i]}
                     for i, e in enumerate(sequence)]
    }
    return get_template(f'sequence.{markup.lower()}.j2').render(**variables).rstrip('\n')


def error_script(lattice: Segment) -> str:
    """Convert error definitions in form of `AlignmentError` to a corresponding MADX script.

    .. Important:: Elements which have associated errors must have a (unique) label (uniqueness is not checked for).

    Parameters
    ----------
    lattice : Segment

    Returns
    -------
    script : str
        The corresponding MADX statements for assigning the associated errors.

    Raises
    ------
    SerializerError
        If an element with associated errors has no label.
    """
    sequence = lattice.flat().elements
    statements = [Command('eoption', {'add': 'true'})]
    for item in sequence:
        element, errors = strip_errors(item)
        errors = [*serialize_errors(errors), *serialize_field_errors(element)]
        if errors:
            if element.label is None:
                raise SerializerError(f'Element without label: {element} (errors: {errors})')
            statements.append(Command('select', {'flag': 'error', 'clear': 'true'}))
            statements.append(Command('select', {'flag': 'error', 'range': write_attribute_value(element.label)}))
            statements.extend(errors)
    return get_template('errors.madx.j2').render(errors=statements).rstrip('\n')


def track_script(particles: Union[np.ndarray, torch.Tensor], observe: Sequence[str],
                 aperture: bool = True, recloss: bool = True,
                 turns: int = 1, maxaper: Union[tuple, list] = (0.1, 0.01, 0.1, 0.01, 1.0, 0.1)) -> str:
    """Convert particle array / tensor to corresponding MADX track script.

    Uses ``onetable = true`` and hence the results will be available at the file "trackone".

    Parameters
    ----------
    particles : array
        Array / tensor of shape `(6, N)` where `N` is the number of particles.
    observe : list or tuple
        Labels of places where to observe.
    aperture : bool
    recloss : bool
    turns : int
    maxaper : tuple or list

    Returns
    -------
    script : str

    Raises
    ------
    ValueError
        If the given particle array has an illegal shape (must be (6,N) where `N` is the number of particles).
    """
    if isinstance(particles, torch.Tensor):
        particles = particles.numpy()
    if not (len(particles.shape) == 2 and particles.shape[0] == 6):
        raise ValueError(f'Invalid shape of particle array, should be (6, N), not {particles.shape}')
    variables = {
        'aperture': aperture,
        'recloss': recloss,
        'turns': turns,
        'maxaper': '{' + ', '.join(map(str, maxaper)) + '}',
        'particles': np.transpose(particles),
        'observe': observe,
    }
    return get_template('track.madx.j2').render(**variables).rstrip('\n')


def strip_errors(item: LatticeElement) -> Tuple[LatticeElement, List['AlignmentError']]:
    """Strip alignment errors from a lattice element (`Tilt` is not considered an error)."""
    errors = []
    while isinstance(item, AlignmentError):
        if not isinstance(item, elements.Tilt):
            errors.append(item)
        item = item.target
    return item, errors


def serialize_errors(errors: List[AlignmentError]) -> Iterator[Command]:
    """Convert the list of alignment errors to a corresponding `dict` representations."""
    for error in errors:
        yield Command('ealign', {name: write_attribute_value(value)
                                 for name, value in sorted(get_attributes(error).items())})


def serialize_field_errors(element: LatticeElement) -> Iterator[Command]:
    """Convert the field errors of the given element to a corresponding `dict` representation."""
    if not element.field_errors:
        return
    field_errors = {'n': {}, 's': {}}
    if isinstance(element.element, elements.Kicker):
        field_errors['n'][0] = element.dkh
        field_errors['s'][0] = element.dkv
    else:
        for name in element.field_errors.values():
            value = getattr(element, name)
            if not name.endswith('l'):
                if element.l == 0:
                    raise SerializerError(f'Cannot compute integrated field error {name!r} for element with zero length: {element}')
                value = value * element.l
            else:
                name = name[:-1]
            field_errors['n'][int(name[-1])] = value.item()
    efcomp_attributes = {}
    for err_type, err_values in field_errors.items():
        if all(x == 0 for x in err_values.values()):
            continue
        field_error_list = [0.] * (max(err_values) + 1)
        for order, value in err_values.items():
            field_error_list[order] = value
        efcomp_attributes[f'dk{err_type}'] = write_attribute_value(field_error_list)
    if efcomp_attributes:
        yield Command('efcomp', efcomp_attributes)


def serialize_element(element: LatticeElement) -> dict:
    """Convert a lattice element to a corresponding `dict` representation."""
    attributes = unwrap_attributes(element)
    if isinstance(element, AlignmentError):
        element = element.element
    cmd_keyword = type(element).__name__.lower()
    aperture = element.aperture
    if aperture is not None and np.isfinite(aperture.aperture.numpy()).all():
        attributes['apertype'] = type(aperture).__name__.lower().replace('aperture', '', 1)
        attributes['aperture'] = (aperture.aperture.detach().numpy() - aperture.padding.numpy()).tolist()
        if torch.any(aperture.offset != 0):
            attributes['aper_offset'] = aperture.offset.detach().numpy()
        if type(element) is elements.Drift:
            # Using a "quadrupole" here because "collimator" wants "makethin" in tracking.
            cmd_keyword = elements.Quadrupole.__name__.lower()
            attributes['k1'] = 0.
    if isinstance(element, (elements.ThinQuadrupole, elements.ThinSextupole)):
        cmd_keyword = 'multipole'
        if isinstance(element, elements.ThinQuadrupole):
            attributes['knl'] = [0., attributes.pop('k1l')]
        if isinstance(element, elements.ThinSextupole):
            attributes['knl'] = [0., 0., attributes.pop('k2l')]
    if isinstance(element, (elements.HKicker, elements.VKicker)):
        del attributes['hkick']
        del attributes['vkick']
    return Command(cmd_keyword, {name: write_attribute_value(value) for name, value in sorted(attributes.items())})


def unwrap_attributes(e: LatticeElement) -> dict:
    """Get all attributes of the given lattice element (including `tilt`, excluding field errors)."""
    if isinstance(e, elements.Tilt):
        return dict(unwrap_attributes(e.target), **get_attributes(e))
    elif isinstance(e, AlignmentError):
        return unwrap_attributes(e.target)
    else:
        return get_attributes(e)


def get_attributes(e: LatticeElement) -> dict:
    """Get all (local) attributes from the given lattice element (excluding field errors)."""
    attr_names = get_attribute_names(e)
    attr_keys = e.triggers if isinstance(e, AlignmentError) else attr_names
    return {key: getattr(e, name) for key, name in zip(attr_keys, attr_names)}


def convert_attribute_value(x):
    """Convert an attribute value to its corresponding built-in representation, covering np.ndarray and torch.Tensor."""
    if isinstance(x, (tuple, list)):
        x = type(x)(map(convert_attribute_value, x))
    if isinstance(x, torch.Tensor):
        x = x.detach().numpy()
    if isinstance(x, np.ndarray):
        x = x.tolist()
    return x


def write_attribute_value(x: Any) -> str:
    """Convert an attribute value to its corresponding MADX representation, covering np.ndarray and torch.Tensor."""
    return write_attribute_value_madx(convert_attribute_value(x))
