"""Accelerator lattice elements represented by PyTorch Modules.

The various element classes are made available together with the corresponding MADX command name in the following dicts.

Attributes
----------
elements : dict
    Maps MADX command names to corresponding `Element` backend classes.
alignment_errors : dict
    Maps MADX ``EALIGN`` command attributes to corresponding `AlignmentError` backend classes.
aperture_types : dict
    Maps MADX ``apertypes`` definitions to corresponding `Aperture` backend classes.
"""

from __future__ import annotations

import abc
from collections import Counter
import copy
from functools import partial, reduce, singledispatch, wraps
import logging
import inspect
import itertools as it
from pprint import pformat
import re
import scipy.linalg
from typing import Any, Callable, Dict, Iterator, List, NoReturn, Optional, Pattern, Sequence, Tuple, Type, \
    TypeVar, Union, get_type_hints
from typing_extensions import Literal, Protocol
import warnings

import numpy as np
import torch

from .utils import autodoc, copy_doc, setattr_multi, singledispatchmethod


__all__ = ['ApertureCircle', 'ApertureEllipse', 'ApertureRectangle', 'ApertureRectEllipse',
           'Marker', 'Drift', 'Instrument', 'Placeholder', 'Monitor', 'HMonitor', 'VMonitor',
           'Kicker', 'HKicker', 'VKicker', 'TKicker', 'Quadrupole', 'Sextupole', 'SBend', 'RBend', 'Dipedge', 'SBendBody',
           'ThinQuadrupole', 'ThinSextupole',
           'Tilt',
           'Offset', 'LongitudinalRoll', 'BPMError',
           'Segment']

logger = logging.getLogger(__name__)

Tensor = torch.Tensor
Parameter = torch.nn.Parameter
tensor = partial(torch.tensor, dtype=torch.float64)
torch.set_default_dtype(torch.float64)
Number = Union[int, float, Tensor]
Numbers = Union[List[Union[int, float]], Tuple[Union[int, float], ...], Tensor]
ArgumentValue = TypeVar('ArgumentValue')
Parameterizable = Union[ArgumentValue, Parameter]


class BaseElement(Protocol):
    """Protocol for lattice elements that support particle tracking and aperture checks with particle loss.

    The various tracking methods expect the particles' coordinates as a tensor of shape (6, N) where `N` is the number
    of particles and the coordinates are ordered as `x, px, y, py, t, pt`. These methods either return a new tensor
    or modify the given input tensor in-place.
    """

    l : Tensor
    label : str
    aperture: Aperture
    field_errors : dict

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> Tensor:
        """This method exists for compatibility with the torch.nn.Module API."""
        raise NotImplementedError

    @abc.abstractmethod
    def forward(self, x: Tensor, *, method: str) -> Tensor:
        """This method exists for compatibility with the torch.nn.Module API."""
        raise NotImplementedError

    @abc.abstractmethod
    def exact(self, x: Tensor) -> Tensor:
        """Exact analytic solution for tracking through the element."""
        raise NotImplementedError

    @abc.abstractmethod
    def linear(self, x: Tensor) -> Tensor:
        """Linear tracking through the element."""
        raise NotImplementedError

    @abc.abstractmethod
    def second_order(self, x: Tensor) -> Tensor:
        """Second order tracking through the element."""
        raise NotImplementedError

    @abc.abstractmethod
    def loss(self, x: Tensor) -> Tensor:
        """Compute the loss value for each particle according to the element's aperture type.

        .. Note::
           The resulting loss values are greater than or equal to zero and values > 0 indicate that the corresponding
           particle has hit the aperture. In case the particle is position exactly at the aperture
           (e.g. ``(x, y) = (2, 0)`` for ``ApertureCircle(2.0)``) then the returned loss value will be
           zero. Only for positions outside the aperture the loss value will be greater than zero. In case that behavior
           is undesired the effective aperture can be reduced by a small margin by using the `padding` argument of the
           aperture type.

        Parameters
        ----------
        x : Tensor
            The 6D phase-space coordinates of shape (6, N).

        Returns
        -------
        loss : Tensor
            Tensor of shape (N,) where loss > 0 indicates that the corresponding particle has hit the aperture.
        """
        raise NotImplementedError


class CompactElement(BaseElement):
    """Protocol for lattice elements which have a transfer map."""

    @property
    @abc.abstractmethod
    def d(self) -> Tensor:
        """Zero order coefficients of the element's transfer map."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def R(self) -> Tensor:
        """First order coefficients of the element's transfer map."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def T(self) -> Tensor:
        """Second order coefficients of the element's transfer map."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def transfer_map(self) -> TransferMap:
        """Coefficients of the series expansion of the element's transfer map up to second order."""
        raise NotImplementedError

    @abc.abstractmethod
    def update_transfer_map(self, *, reset=False) -> None:
        """Update the element's transfer map coefficients (d, R, T) to correspond to the elements' parameters.

        This method should be called after any of the elements' parameters have been modified in order to update the
        transfer map to correspond to the new values.

        Parameters
        ----------
        reset : bool
            If True then the tensors corresponding to transfer map coefficients are replaced by new tensor objects before
            their values are updated. In this case the resulting tensors guarantee to reflect any change in the elements
            attribute, parametrized and non-parametrized (see notes below).

        Notes
        -----
        This method guarantees to incorporate the values of all parameters but not for non-parameter attributes (such as
        the length of an element; these are only guaranteed to be incorporated if ``reset=True``). For ``reset=False``
        these non-parameter attributes might be reflected in the transfer map update but this is an implementation detail
        that should not be relied on. Even though this method is only relevant for elements that cache their transfer map
        and for others it is a no-op, this caching property also is an implementation detail that should not be relied on.
        Hence after having modified an element the `update_transfer_map` method should be called.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def makethin(self, n: int, *, style: Optional[str] = None) -> Union[Element, ThinElement]:
        """Transform element to a sequence of `n` thin elements using the requested slicing style.

        .. Important::
           If optimization of parameters is required then it is important to call `makethin` before *each* forward pass
           in order to always use the up-to-date parameter values from the original elements. Calling `makethin` only
           once at the beginning and then reusing the resulting sequence on every iteration would reuse the initial
           parameter values and hence make the optimization ineffective.

        Parameters
        ----------
        n : int
            The number of slices (thin elements).
        style : str, optional
            The slicing style to be used. For available styles see :meth:`ThinElement.create_thin_sequence`.

        Returns
        -------
        ThinElement
            A segment containing the slices (thin elements) separated by drifts.
        """
        raise NotImplementedError


class PartitionedElement(BaseElement):
    """Protocol for lattice elements which consist of multiple successive transfer maps."""
    elements : List[LatticeElement]

    @abc.abstractmethod
    def compute_transfer_maps(self, method: str, *, order: Literal[1, 2] = 2, index: Optional[Literal[0, 1, 2]] = None,
                              symplectify: bool = True, unfold_alignment_errors: bool = False,
                              d0: Optional[Tensor] = None, R0: Optional[Tensor] = None, T0: Optional[Tensor] = None
                              ) -> Iterator[TransferMap]:
        """Compute the transfer maps of the element.

        Parameters
        ----------
        method : str
            Determines how the transfer maps are computed (for details see implementing class).
        order : int
            Transfer map order used in computations.
        index : int
            Only transfer map coefficients up to the specified `index` are stored in the results; others are `None`.
            If `None` then defaults to `order`.
        symplectify : bool
            Whether to symplectify the first order coefficients (transfer matrix) after second order feed-down terms
            have been included.
        unfold_alignment_errors : bool
            Whether to treat alignment error transformations as separate transfer maps rather than contracting them with
            the wrapped lattice element.
        d0, R0, T0 : Tensor
            Starting values at the beginning of the element (``d0`` corresponds to the closed orbit value).

        Yields
        ------
        transfer_map : :class:`TransferMap`
            Depending on the selected `method`.
        """
        raise NotImplementedError


LatticeElement = Union[CompactElement, PartitionedElement, 'AlignmentError']


TransferMap = Tuple[Optional[Tensor], ...]
LabelSelector = Union[str, Pattern]
SubSegmentSelector = slice
MultiElementSelector = Union[LabelSelector, Type[LatticeElement]]
SingleElementSelector = Union[int, str, LatticeElement, Tuple[MultiElementSelector, int]]
MatchingCriteria = Union[SingleElementSelector, MultiElementSelector,
                         List[Union[SingleElementSelector, MultiElementSelector]]]
SelectionKey = Union[MultiElementSelector, SingleElementSelector, None]
SelectionValue = TypeVar('SelectionValue')
SelectionCriteria = Union[SelectionValue,
                          Tuple[SelectionKey, SelectionValue],
                          List[Tuple[SelectionKey, SelectionValue]],
                          Dict[SelectionKey, SelectionValue]]


class TrackingError(Exception):
    pass


def safeguard_thick(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.l >= self.makethin_min_length:
            raise TrackingError(f'Cannot use {func.__name__!r} of thick {type(self).__name__} (use makethin beforehand): {self}')
        return func(self, *args, **kwargs)
    return wrapper


def prepare_attribute_value(value, *, types: Tuple[type, ...] = (int, float)):
    if isinstance(value, types):
        value = tensor(value)
    elif isinstance(value, np.ndarray):
        value = torch.from_numpy(value.astype(float))
    return value


class AnnotationTypedAttributes:
    def __setattr__(self, key, value):
        if key in get_type_hints(type(self)):
            value = prepare_attribute_value(value)
        super().__setattr__(key, value)


class Aperture(AnnotationTypedAttributes, torch.nn.Module):
    """Aperture of a lattice element.

    Parameters
    ----------
    aperture : Tensor
        Values specifying the aperture, interpreted by the subclasses (corresponding to "apertype").
    offset : Tensor, shape (2,)
        Horizontal and vertical offset of the aperture.
    padding : Tensor
        Additional padding applied to the aperture's values. That means each item in `aperture` is effectively reduced
        by the corresponding item in `padding`. This is useful for imposing tighter constraints on the aperture than
        are specified in the sequence files. Should have the same shape as `aperture`.
    """
    aperture : Union[Tensor, Parameter]
    offset : Tensor
    padding : Tensor

    def __init__(self, aperture: Parameterizable[Tensor], padding: Tensor, offset: Numbers = torch.zeros(2)):
        super().__init__()
        self.aperture = aperture
        self.padding = padding
        self.offset = prepare_attribute_value(offset, types=(list, tuple))

    def __call__(self, xy: Tensor) -> Tensor:
        return super().__call__(xy)

    # noinspection PyUnresolvedReferences
    def __repr__(self):
        return f'{type(self).__name__}(aperture={self.aperture}, offset={self.offset}, padding={self.padding})'

    def forward(self, xy: Tensor) -> Tensor:
        """This method exists for compatibility with the torch.nn.Module API."""
        return self.loss(xy - self.offset[:, None], self.aperture - self.padding)

    @classmethod
    def loss(cls, xy: Tensor, aperture: Tensor) -> Tensor:
        """Compute the loss values for the given xy-positions.

        Parameters
        ----------
        xy : Tensor
            Tensor of shape `(2, N)` where `N` is the number of particles and rows are x- and y-positions, respectively,
            centered within the aperture.
        aperture : Tensor
            The effective aperture of the element, interpreted by the particular subclass.

        Returns
        -------
        loss_val : Tensor
            Tensor of shape `(N,)`, zero where positions are inside the aperture (including exactly at the aperture)
            and greater than zero where positions are outside the aperture.
        """
        raise NotImplementedError


class ApertureEllipse(Aperture):
    """Elliptical aperture.

    Parameters
    ----------
    aperture : Tensor, shape (2,)
        Horizontal and vertical semi-axes of the ellipse.
    """
    # noinspection PyTypeChecker
    def __init__(self, aperture: Parameterizable[Numbers] = tensor([np.inf, np.inf]), padding: Numbers = torch.zeros(2),
                 offset: Numbers = torch.zeros(2)):
        super().__init__(prepare_attribute_value(aperture, types=(list, tuple)),
                         prepare_attribute_value(padding, types=(list, tuple)),
                         offset)

    @classmethod
    def loss(cls, xy: Tensor, aperture: Tensor) -> Tensor:
        return torch.nn.functional.relu(torch.sum(xy**2 / aperture[:, None]**2, dim=0) - 1)


class ApertureCircle(Aperture):
    """Circular aperture.

    Parameters
    ----------
    aperture : Tensor, scalar (shape [])
        Radius of the circle.
    """
    def __init__(self, aperture: Parameterizable[Number] = tensor(np.inf), padding: Number = tensor(0.),
                 offset: Numbers = torch.zeros(2)):
        super().__init__(prepare_attribute_value(aperture, types=(int, float)),
                         prepare_attribute_value(padding, types=(int, float)),
                         offset)

    @classmethod
    def loss(cls, xy: Tensor, aperture: Tensor) -> Tensor:
        return ApertureEllipse.loss(xy, torch.stack((aperture, aperture)))


class ApertureRectangle(Aperture):
    """Rectangular aperture.

    Parameters
    ----------
    aperture : Tensor, shape (2,)
        Half width (horizontal) and half height (vertical) of the rectangle.
    """
    def __init__(self, aperture: Parameterizable[Numbers] = tensor([np.inf, np.inf]), padding: Numbers = torch.zeros(2),
                 offset: Numbers = torch.zeros(2)):
        super().__init__(prepare_attribute_value(aperture, types=(list, tuple)),
                         prepare_attribute_value(padding, types=(list, tuple)),
                         offset)

    @classmethod
    def loss(cls, xy: Tensor, aperture: Tensor) -> Tensor:
        return torch.sum(torch.nn.functional.relu(torch.abs(xy) - aperture[:, None]), dim=0)


class ApertureRectEllipse(Aperture):
    """Overlay of rectangular and elliptical aperture.

    Parameters
    ----------
    aperture : Tensor, shape (4,)
        Half width (horizontal) and half height (vertical) of the rectangle followed by horizontal and vertical
        semi-axes of the ellipse.
    """
    def __init__(self, aperture: Parameterizable[Numbers] = tensor([np.inf]*4), padding: Numbers = torch.zeros(4),
                 offset: Numbers = torch.zeros(2)):
        super().__init__(prepare_attribute_value(aperture, types=(list, tuple)),
                         prepare_attribute_value(padding, types=(list, tuple)),
                         offset)

    @classmethod
    def loss(cls, xy: Tensor, aperture: Tensor) -> Tensor:
        return ApertureRectangle.loss(xy, aperture[:2]) + ApertureEllipse.loss(xy, aperture[2:])


@CompactElement.register
@autodoc(CompactElement)
class Element(AnnotationTypedAttributes, torch.nn.Module):
    """Base class for lattice elements representing physical components.

    Parameters
    ----------
    l : Number
        Length [meter].
    beam : dict
        Beam configuration containing both `beta` and `gamma`.
    label : str, optional
        Label of the element.
    aperture : :class:`Aperture`
        The object representing the element's aperture.

    Attributes
    ----------
    makethin_min_length : float
        Minimal required length of an element to be sliced when via `makethin`. If the element's length is below that
        threshold it is considered to be a thin element already.
    makethin_slicing_style : str
        Default slicing style when calling `makethin`. For more options see :meth:`makethin`.
    transfer_map_order : int
        The order up to which transfer map coefficients are considered. For linear optics, setting ``transfer_map_order = 1``
        can save memory and compute time since second order coefficients won't be computed.
    field_errors : dict
        Maps the names of field coefficients to the names of corresponding field errors.

    Notes
    -----
    For an explanation of the coordinates see [1]_. For an explanation of the various aperture types see [2]_.

    .. [1] F. Christoph Iselin, "The MAD program (Methodical Accelerator Design) Version 8.13 -
           Physical Methods Manual", 1994
    .. [2] Hans Grote, Frank Schmidt, Laurent Deniau and Ghislain Roy, "The MAD-X Program (Methodical Accelerator
           Design) Version 5.02.08 - User's Reference Manual, 2016
    """
    l: Tensor

    makethin_min_length = 1e-6
    makethin_slicing_style = 'teapot'

    transfer_map_order = 2

    field_errors = {}

    def __init__(self, l: Number = 0, *,
                 aperture: Optional[Aperture] = None, beam: Optional[dict] = None, label: Optional[str] = None,
                 **kwargs):
        super().__init__()
        self.l = prepare_attribute_value(l)
        self.beam = beam
        self.label = label
        self.aperture = aperture
        kwargs.pop('nst', None)  # Remove optional PTC parameters.
        if kwargs:
            warnings.warn(f'Unknown parameters for element of type {type(self)}: {kwargs}')
        self.d = torch.zeros(6, 1)
        self.R = torch.eye(6)
        self.T = torch.zeros(6, 6, 6) if self.transfer_map_order >= 2 else None

    def __call__(self, x: Tensor, *, method: str) -> Tensor:
        return super().__call__(x, method=method)

    def __repr__(self):
        attributes = list(get_type_hints(type(self))) + list(self.field_errors.values()) + ['label']
        if self.aperture is not None and torch.all(torch.isfinite(self.aperture.aperture)):
            attributes.insert(-1, 'aperture')
        return (f'{type(self).__name__}('
                f'{", ".join(f"{x}={repr(getattr(self, x))}" for x in attributes)}'
                f')'.replace('\n', ' '))

    @property
    def element(self) -> Element:
        """Return the element itself (this method exists for convenience compatibility with :class:`AlignmentError`."""
        return self

    @property
    def transfer_map(self) -> TransferMap:
        return self.d, self.R, self.T

    def update_transfer_map(self, *, reset=False) -> None:
        if reset:
            self.reset_transfer_map()

    def reset_transfer_map(self):
        self.d = torch.zeros(6, 1)
        self.R = torch.eye(6)
        if self.transfer_map_order >= 2:
            self.T = torch.zeros(6, 6, 6)

    def forward(self, x: Tensor, *, method: str) -> Tensor:
        return getattr(self, method)(x)

    def exact(self, x: Tensor) -> Tensor:
        raise NotImplementedError

    def linear(self, x: Tensor) -> Tensor:
        return self.d + self.R @ x

    def second_order(self, x: Tensor) -> Tensor:
        return self.linear(x) + torch.einsum('ijk,jl,kl->il', self.T, x, x)

    def loss(self, x: Tensor) -> Tensor:
        if self.aperture is None:
            return torch.zeros(x.shape[1])
        return self.aperture(x[[0, 2]])

    def makethin(self, n: int, *, style: Optional[str] = None) -> Union[Element, ThinElement]:
        """
        See Also
        --------
        :meth:`ThinElement.create_thin_sequence` - For available slicing styles.
        """
        if n == 0 or self.l < self.makethin_min_length:
            return self
        attributes = {k: getattr(self, k) / n for k in type(self).__annotations__}
        thick_cls = partial(Drift, beam=self.beam)
        thin_cls = partial(type(self), **attributes, l=0., beam=self.beam)
        slices = ThinElement.create_thin_sequence(n, self.l.item(), thick_cls, thin_cls, self.label,
                                                  style or self.makethin_slicing_style)
        return ThinElement(self, slices)


class Marker(Element):
    """Marker element."""

    def __init__(self, **kwargs):
        if kwargs.pop('l', 0) > 0:
            raise ValueError('Marker with non-zero length is not allowed')
        super().__init__(l=0, **kwargs)

    def linear(self, x: Tensor) -> Tensor:
        return x

    def exact(self, x: Tensor) -> Tensor:
        return x


class Drift(Element):
    """Drift space.

    .. Note:: Unlike in MADX, drift spaces feature aperture checks here.

    Parameters
    ----------
    l : Number
        Length of the drift [m].
    """

    def __init__(self, l: Number, *, beam: dict, **kwargs):
        super().__init__(l, beam=beam, **kwargs)
        self.update_transfer_map()

    def update_transfer_map(self, *, reset=False) -> None:
        super().update_transfer_map(reset=reset)
        beta, gamma = self.beam['beta'], self.beam['gamma']

        self.R[0, 1] = self.R[2, 3] = self.l
        self.R[4, 5] = self.l / (beta * gamma) ** 2

        if self.transfer_map_order >= 2:
            self.T[0, 1, 5] = self.T[0, 5, 1] = -0.5 * self.l / beta
            self.T[2, 3, 5] = self.T[2, 5, 3] = -0.5 * self.l / beta
            self.T[4, 1, 1] = self.T[4, 3, 3] = -0.5 * self.l / beta
            self.T[4, 5, 5] = -1.5 * self.l / beta / (beta * gamma) ** 2

    # noinspection PyTypeChecker
    def exact(self, x):
        beta = self.beam['beta']
        x, px, y, py, z, pt = x
        pz = torch.sqrt(1 + 2*pt/beta + pt**2 - px**2 - py**2)
        return torch.stack([
            x + px * self.l / pz,
            px,
            y + py * self.l / pz,
            py,
            z + (1/beta - (1/beta + pt) / pz) * self.l,
            pt
        ])

    def makethin(self, n: int, *, style: str = None) -> Drift:
        """Drift spaces are not affected by `makethin`."""
        return self


class Instrument(Drift):
    """A place holder for any type of beam instrumentation."""
    pass


class Placeholder(Drift):
    """A place holder for any type of element."""
    pass


class Monitor(Drift):
    """Beam position monitor."""

    def readout(self, x):
        """Return BPM readings for the given coordinates.

        Parameters
        ----------
        x : Tensor
            6D phase-space coordinates of shape (6, N).

        Returns
        -------
        xy : Tensor
            BPM readings in x- and y-dimension of shape (2, N).
        """
        return x[[0, 2]]


class HMonitor(Monitor):
    """Beam position monitor for measuring horizontal beam position."""
    pass


class VMonitor(Monitor):
    """Beam position monitor for measuring horizontal beam position."""
    pass


class Kicker(Element):
    """Combined horizontal and vertical kicker magnet.

    Parameters
    ----------
    hkick : Number or Parameter
        Horizontal kick [rad].
    vkick : Number or Parameter
        Vertical kick [rad].
    dkh : Number or Parameter
        Horizontal absolute dipolar field error [rad].
    dkv : Number or Parameter
        Vertical absolute dipolar field error [rad].
    """
    hkick : Union[Tensor, Parameter]
    vkick : Union[Tensor, Parameter]

    field_errors = {'hkick': 'dkh', 'vkick': 'dkv'}

    def __init__(self,
                 hkick: Parameterizable[Number] = 0, vkick: Parameterizable[Number] = 0,
                 l: Number = 0,
                 *,
                 beam: Optional[dict] = None,
                 dkh: Parameterizable[Number] = 0, dkv: Parameterizable[Number] = 0,
                 **kwargs):
        super().__init__(l=l, beam=beam, **kwargs)
        self.hkick = prepare_attribute_value(hkick)
        self.vkick = prepare_attribute_value(vkick)
        self.dkh = prepare_attribute_value(dkh)
        self.dkv = prepare_attribute_value(dkv)
        if self.l > 0:
            if self.beam is None:
                raise ValueError("'beam' must not be None if 'length' is greater than zero")
            drift = Drift(self.l, beam=self.beam)
            self.R[:] = drift.R
            if self.transfer_map_order >= 2:
                self.T[:] = drift.T

    @property
    def d(self) -> Tensor:
        d = torch.zeros(6, 1)
        d[1, 0] = self.hkick + self.dkh
        d[3, 0] = self.vkick + self.dkv
        return d

    @d.setter
    def d(self, value):
        pass

    @property
    @safeguard_thick
    def transfer_map(self) -> TransferMap:
        return super().transfer_map

    def reset_transfer_map(self):
        super().reset_transfer_map()
        if self.l > 0:
            drift = Drift(self.l, beam=self.beam)
            self.R[:] = drift.R
            if self.transfer_map_order >= 2:
                self.T[:] = drift.T

    @safeguard_thick
    def linear(self, x: Tensor) -> Tensor:
        return super().linear(x)

    @safeguard_thick
    def second_order(self, x: Tensor) -> Tensor:
        return super().second_order(x)


class HKicker(Kicker):
    """Horizontal kicker magnet."""
    kick : Union[Tensor, Parameter]

    def __init__(self, kick: Parameterizable[Number], l: Number = 0, *, beam: Optional[dict] = None, **kwargs):
        super().__init__(kick, 0, l=l, beam=beam, **kwargs)

    @property
    def kick(self) -> Tensor:
        return self.hkick

    @kick.setter
    def kick(self, val) -> None:
        self.hkick = val


class VKicker(Kicker):
    """Vertical kicker magnet."""
    kick : Union[Tensor, Parameter]

    def __init__(self, kick: Parameterizable[Number], l: Number = 0, *, beam: Optional[dict] = None, **kwargs):
        super().__init__(0, kick, l=l, beam=beam, **kwargs)

    @property
    def kick(self) -> Tensor:
        return self.vkick

    @kick.setter
    def kick(self, val) -> None:
        self.vkick = val


class TKicker(Kicker):
    """Similar to `Kicker` (see Chapter 10.12, MADX User's Guide)."""
    pass


class Quadrupole(Element):
    """Quadrupole magnet.

    Whether this is a (horizontally) focusing or defocusing magnet is determined from the value of `k1`
    (k1 > 0 indicates a horizontally focusing quadrupole).
    Hence, in case `k1` is a Parameter, it always must be non-zero. For that reason it is convenient to use boundaries
    e.g. `[eps, k1_max]` with a small number `eps` (e.g. `1e-16`) and clip the value of `k1` accordingly.
    If `k1` is not a Parameter it can be zero and a corresponding `Drift` transformation will be used.

    Parameters
    ----------
    k1 : Number or Parameter
        Normalized quadrupole gradient strength [1/m^2].
    dk1 : Number or Parameter
        Absolute error of `k1` [1/m^2].
    """
    k1 : Union[Tensor, Parameter]

    field_errors = {'k1': 'dk1'}

    def __init__(self, k1: Parameterizable[Number], l: Number,
                 *, beam: dict, dk1: Parameterizable[Number] = 0, **kwargs):
        super().__init__(l, beam=beam, **kwargs)
        self.k1 = prepare_attribute_value(k1)
        self.dk1 = prepare_attribute_value(dk1)
        self.update_transfer_map()

    def update_transfer_map(self, *, reset=False) -> None:
        super().update_transfer_map(reset=reset)

        k1 = self.k1 + self.dk1
        if k1 == 0 and k1.requires_grad:
            raise ValueError('k1 must not be zero; use value clipping and an epsilon boundary instead of zero.')
        elif k1 == 0:
            drift = Drift(self.l, beam=self.beam)
            self.R[:] = drift.R
            if self.transfer_map_order >= 2:
                self.T[:] = drift.T
        else:
            beta, gamma = self.beam['beta'], self.beam['gamma']

            w = torch.sqrt(torch.abs(k1))
            wl = w * self.l
            cx = torch.cos(wl)
            sx = torch.sin(wl) / w
            cy = torch.cosh(wl)
            sy = torch.sinh(wl) / w
            if k1 < 0:  # Horizontally defocusing.
                cx, sx, cy, sy = cy, sy, cx, sx

            self.R[0, 0] = self.R[1, 1] = cx
            self.R[0, 1] = sx
            self.R[1, 0] = -k1 * sx
            self.R[2, 2] = self.R[3, 3] = cy
            self.R[2, 3] = sy
            self.R[3, 2] = k1 * sy
            self.R[4, 5] = self.l / (beta * gamma)**2

            if self.transfer_map_order >= 2:
                one_over_four_beta = 0.25 / beta
                coef_005 =  k1 * self.l * sx * one_over_four_beta
                coef_225 = -k1 * self.l * sy * one_over_four_beta

                self.T[0, 0, 5] = self.T[0, 5, 0] = coef_005
                self.T[0, 1, 5] = self.T[0, 5, 1] = -(sx + self.l * cx) * one_over_four_beta

                self.T[1, 0, 5] = self.T[1, 5, 0] = -k1 * (sx - self.l * cx) * one_over_four_beta
                self.T[1, 1, 5] = self.T[1, 5, 1] = coef_005

                self.T[2, 2, 5] = self.T[2, 5, 2] = coef_225
                self.T[2, 3, 5] = self.T[2, 5, 3] = -(sy + self.l * cy) * one_over_four_beta

                self.T[3, 2, 5] = self.T[3, 5, 2] = k1 * (sy - self.l * cy) * one_over_four_beta
                self.T[3, 3, 5] = self.T[3, 5, 3] = coef_225

                self.T[4, 0, 0]                   = -k1 * (self.l - sx * cx) * one_over_four_beta
                self.T[4, 0, 1] = self.T[4, 1, 0] =  k1 * sx ** 2 * one_over_four_beta
                self.T[4, 1, 1]                   = -(self.l + sx * cx) * one_over_four_beta
                self.T[4, 2, 2]                   =  k1 * (self.l - sy * cy) * one_over_four_beta
                self.T[4, 2, 3] = self.T[4, 3, 2] = -k1 * sy ** 2 * one_over_four_beta
                self.T[4, 3, 3]                   = -(self.l + sy * cy) * one_over_four_beta
                self.T[4, 5, 5]                   = -1.5 * self.l / beta / (beta * gamma)**2

    def makethin(self, n: int, *, style: str = None) -> Union[Quadrupole, ThinElement]:
        if n == 0 or self.l < self.makethin_min_length:
            return self
        thick_cls = partial(Drift, beam=self.beam)
        thin_cls = partial(ThinQuadrupole, self.k1*self.l/n, dk1l=self.dk1*self.l/n)
        slices = ThinElement.create_thin_sequence(n, self.l.item(), thick_cls, thin_cls, self.label,
                                                  style or self.makethin_slicing_style)
        return ThinElement(self, slices)


class ThinQuadrupole(Element):
    """Thin lens representation of a quadrupole magnet.

    Parameters
    ----------
    k1l : Number or Parameter
        Integrated quadrupole gradient strength [1/m].
    dk1l : Number or Parameter
        Absolute error of `k1l` [1/m].
    """
    k1l : Union[Tensor, Parameter]

    field_errors = {'k1l': 'dk1l'}

    def __init__(self, k1l: Parameterizable[Number], *, dk1l: Parameterizable[Number] = 0, **kwargs):
        super().__init__(**kwargs)
        self.k1l = prepare_attribute_value(k1l)
        self.dk1l = prepare_attribute_value(dk1l)
        self.update_transfer_map()

    def update_transfer_map(self, *, reset=False) -> None:
        super().update_transfer_map(reset=reset)
        k1l = self.k1l + self.dk1l
        self.R[1, 0] = -k1l
        self.R[3, 2] =  k1l

    def makethin(self, n: int, *, style: str = None) -> NoReturn:
        raise NotImplementedError


class Sextupole(Element):
    """Sextupole magnet.

    Parameters
    ----------
    k2 : Number or Parameter
        Normalized sextupole coefficient [1/m^3].
    dk2 : Number or Parameter
        Absolute error of `k2` [1/m^3].
    """
    k2 : Union[Tensor, Parameter]

    field_errors = {'k2': 'dk2'}

    def __init__(self, k2: Parameterizable[Number], l: Number,
                 *, beam: dict, dk2: Parameterizable[Number] = 0, **kwargs):
        super().__init__(l, beam=beam, **kwargs)
        self.k2 = prepare_attribute_value(k2)
        self.dk2 = prepare_attribute_value(dk2)
        self.update_transfer_map()

    def update_transfer_map(self, *, reset=False) -> None:
        super().update_transfer_map(reset=reset)
        drift = Drift(self.l, beam=self.beam)
        self.R[:] = drift.R
        if self.transfer_map_order >= 2:
            self.T[:] = drift.T
            k2l = (self.k2 + self.dk2) * self.l
            coef_1 = k2l / 2
            coef_2 = coef_1 * self.l / 2
            coef_3 = coef_2 * self.l / 3
            coef_4 = coef_3 * self.l / 4
            self.T[0, 0, 0]                   = -coef_2
            self.T[0, 0, 1] = self.T[0, 1, 0] = -coef_3
            self.T[0, 1, 1]                   = -coef_4 * 2
            self.T[0, 2, 2]                   =  coef_2
            self.T[0, 2, 3] = self.T[0, 3, 2] =  coef_3
            self.T[0, 3, 3]                   =  coef_4 * 2
            self.T[1, 0, 0]                   = -coef_1
            self.T[1, 0, 1] = self.T[1, 1, 0] = -coef_2
            self.T[1, 1, 1]                   = -coef_3 * 2
            self.T[1, 2, 2]                   =  coef_1
            self.T[1, 2, 3] = self.T[1, 3, 2] =  coef_2
            self.T[1, 3, 3]                   =  coef_3 * 2
            self.T[2, 0, 2] = self.T[2, 2, 0] =  coef_2
            self.T[2, 0, 3] = self.T[2, 3, 0] =  coef_3
            self.T[2, 1, 2] = self.T[2, 2, 1] =  coef_3
            self.T[2, 1, 3] = self.T[2, 3, 1] =  coef_4 * 2
            self.T[3, 0, 2] = self.T[3, 2, 0] =  coef_1
            self.T[3, 0, 3] = self.T[3, 3, 0] =  coef_2
            self.T[3, 1, 2] = self.T[3, 2, 1] =  coef_2
            self.T[3, 1, 3] = self.T[3, 3, 1] =  coef_3 * 2

    def makethin(self, n: int, *, style: str = None) -> Union[Sextupole, ThinElement]:
        if n == 0 or self.l < self.makethin_min_length:
            return self
        thick_cls = partial(Drift, beam=self.beam)
        thin_cls = partial(ThinSextupole, self.k2*self.l/n, dk2l=self.dk2*self.l/n)
        slices = ThinElement.create_thin_sequence(n, self.l.item(), thick_cls, thin_cls, self.label,
                                                  style or self.makethin_slicing_style)
        return ThinElement(self, slices)


class ThinSextupole(Element):
    """Thin lens representation of a sextupole magnet.

    Parameters
    ----------
    k2l : Number or Parameter
        Integrated sextupole coefficient [1/m^2].
    dk2l : Number or Parameter
        Absolute error of `k2l` [1/m^2].
    """
    k2l : Union[Tensor, Parameter]

    field_errors = {'k2l': 'dk2l'}

    def __init__(self, k2l: Parameterizable[Number], *, dk2l: Parameterizable[Number] = 0, **kwargs):
        super().__init__(**kwargs)
        self.k2l = prepare_attribute_value(k2l)
        self.dk2l = prepare_attribute_value(dk2l)
        self.update_transfer_map()

    def update_transfer_map(self, *, reset=False) -> None:
        super().update_transfer_map(reset=reset)
        if self.transfer_map_order >= 2:
            k2l_over_2 = (self.k2l + self.dk2l) / 2
            self.T[1, 0, 0]                   = -k2l_over_2
            self.T[1, 2, 2]                   =  k2l_over_2
            self.T[3, 0, 2] = self.T[3, 2, 0] =  k2l_over_2

    def makethin(self, n: int, *, style: str = None) -> NoReturn:
        raise NotImplementedError


class SBendBody(Element):
    """The body of a sector bending magnet.

    Parameters
    ----------
    angle : Number
        Bending angle of the dipole [rad].
    dk0 : Number
        Normalized dipole field error [rad/m].
    """
    angle : Tensor

    field_errors = {'k0': 'dk0'}

    def __init__(self, angle: Number, l: Number, *, beam: dict, dk0: Number = 0, **kwargs):
        super().__init__(l, beam=beam, **kwargs)
        self.angle = prepare_attribute_value(angle)
        self.dk0 = prepare_attribute_value(dk0)
        self.update_transfer_map()

    @property
    def k0(self) -> Tensor:
        return self.angle / self.l

    @k0.setter
    def k0(self, value: Tensor):
        self.angle = value * self.l

    def update_transfer_map(self, *, reset=False) -> None:
        super().update_transfer_map(reset=reset)
        beta, gamma = self.beam['beta'], self.beam['gamma']

        angle, l = self.angle, self.l
        dh = self.dk0

        if angle == 0:
            drift = Drift(self.l.item(), beam=self.beam)
            self.R[:] = drift.R
            if self.transfer_map_order >= 2:
                self.T[:] = drift.T
        else:
            k0 = angle / l
            cx = torch.cos(angle)
            sx = torch.sin(angle)
            bg_sq = (beta * gamma) ** 2

            self.R[0, 0] = cx
            self.R[0, 1] = sx / k0
            self.R[0, 5] = (1 - cx) / (k0 * beta)
            self.R[1, 0] = -k0 * sx
            self.R[1, 1] = cx
            self.R[1, 5] = sx / beta
            self.R[2, 3] = l
            self.R[4, 0] = -sx / beta
            self.R[4, 1] = (cx - 1) / (k0 * beta)
            self.R[4, 5] = l / bg_sq - (k0*l - sx) / (k0 * beta**2)

            if self.transfer_map_order >= 2:
                self.T[0, 0, 0] = -0.5 * k0 * sx ** 2
                self.T[0, 0, 1] = self.T[0, 1, 0] = 0.5 * cx * sx
                self.T[0, 0, 5] = self.T[0, 5, 0] = 0.5 * sx ** 2 / beta
                self.T[0, 1, 1] = 0.5 * cx * (1 - cx) / k0
                self.T[0, 1, 5] = self.T[0, 5, 1] = -0.5 * sx * cx / k0 / beta
                self.T[0, 3, 3] = -0.5 * (1 - cx) / k0
                self.T[0, 5, 5] = -0.5 * sx**2 / k0 / beta**2 - 0.5 * (1 - cx) / k0 / bg_sq
                self.T[1, 1, 1] = -0.5 * sx
                self.T[1, 3, 3] = -0.5 * sx
                self.T[1, 5, 5] = -0.5 * sx / bg_sq
                self.T[2, 0, 3] = self.T[2, 3, 0] = 0.5 * sx
                self.T[2, 1, 3] = self.T[2, 3, 1] = 0.5 * (1 - cx) / k0
                self.T[2, 3, 5] = self.T[2, 5, 3] = -0.5 * sx / k0 / beta
                self.T[4, 0, 5] = self.T[4, 5, 0] = 0.5 * sx / bg_sq
                self.T[4, 1, 1] = -0.5 * sx / beta / k0
                self.T[4, 1, 5] = self.T[4, 5, 1] = 0.5 * (1 - cx) / k0 / bg_sq
                self.T[4, 3, 3] = -0.5 * sx / k0 / beta
                self.T[4, 5, 5] = -1.5 * sx / k0 / bg_sq / beta

        if dh != 0:
            if angle == 0:
                self.d[0, 0] = -0.5 * dh * l**2
                self.d[1, 0] = -dh * l

                if self.transfer_map_order >= 2:
                    self.d[4, 0] = self.d[4, 0] - dh**2 * l**3 / 6 / beta

                    self.R[0, 5] = self.R[0, 5] + 0.5 * dh * l ** 2 / beta
                    self.R[4, 1] = self.R[4, 1] + 0.5 * dh * l ** 2 / beta
            else:
                self.d[0, 0] = -dh * (1 - cx) / k0**2
                self.d[1, 0] = -dh * sx / k0
                self.d[4, 0] = -dh * (sx/k0 - l) / k0 / beta

                if self.transfer_map_order >= 2:
                    self.d[0, 0] = self.d[0, 0] + 0.5 * dh**2 * (1 - cx)**2 / k0**3
                    self.d[4, 0] = self.d[4, 0] +       dh**2 * (sx/k0 - l) / k0**2 / beta

                    self.R[0, 0] = self.R[0, 0] - dh * sx**2 / k0
                    self.R[0, 1] = self.R[0, 1] - dh * sx * (1 - cx) / k0**2
                    self.R[0, 5] = self.R[0, 5] + dh * (cx - cx**2) / k0**2 / beta
                    self.R[1, 0] = self.R[1, 0] - dh * sx
                    self.R[4, 1] = self.R[4, 1] + dh * (1 - cx) / k0**2 / beta
                    self.R[4, 5] = self.R[4, 5] - dh * (sx/k0 - l) / k0
                    self.R[2, 3] = self.R[2, 3] + dh * (sx/k0 - l) / k0

    def makethin(self, n: int, *, style: str = None) -> Union[Element, ThinElement]:
        raise NotImplementedError


class Dipedge(Element):
    """Fringing fields at the entrance and exit of dipole magnets.

    Parameters
    ----------
    h : Number
        Curvature of the associated dipole magnet body.
    e1 : Number
        The rotation angle of the pole face.
    fint : Number
        The fringing field integral.
    hgap : Number
        The half gap height of the associated dipole magnet.
    he : Number
        The curvature of the pole face.
    """
    h : Tensor
    e1 : Tensor
    fint : Tensor
    hgap : Tensor

    def __init__(self, h: Number, e1: Number, fint: Number, hgap: Number, he: Number = 0,
                 *, entrance: bool = True, **kwargs):
        super().__init__(**kwargs)
        setattr_multi(self, ['h', 'e1', 'fint', 'hgap'], locals())  # __setattr__ takes care of attribute value preparation.
        self.he = prepare_attribute_value(he)
        self.entrance = entrance
        self.update_transfer_map()

    def update_transfer_map(self, *, reset=False) -> None:
        super().update_transfer_map(reset=reset)
        h, e1, fint, hgap = self.h, self.e1, self.fint, self.hgap
        he = self.he

        self.R[1, 0] =  h * torch.tan(e1)
        self.R[3, 2] = -h * torch.tan(e1 - 2*hgap*h*fint * (1 + torch.sin(e1)**2) / torch.cos(e1))

        if self.transfer_map_order >= 2:
            sign = 1 if self.entrance else -1
            t000 = -sign * 0.5 * h * torch.tan(e1)**2
            t022 =  sign * 0.5 * h / torch.cos(e1)**2
            t100 = 0.5 * h * he / torch.cos(e1)**3
            t122 = sign * 0.5 * h**2 * torch.tan(e1)**3 - t100
            self.T[0, 0, 0] =                    t000
            self.T[0, 2, 2] =                    t022
            self.T[1, 0, 0] =                    t100
            self.T[1, 0, 1] = self.T[1, 1, 0] = -t000
            self.T[1, 2, 2] =                    t122
            self.T[1, 2, 3] = self.T[1, 3, 2] =  t000
            self.T[2, 0, 2] = self.T[2, 2, 0] = -t000
            self.T[3, 0, 2] = self.T[3, 2, 0] = -t100
            self.T[3, 0, 3] = self.T[3, 3, 0] =  t000
            self.T[3, 1, 2] = self.T[3, 2, 1] = -t022
            if self.entrance:
                self.T[1, 2, 2] += 0.5 * h**2 * torch.tan(e1) / torch.cos(e1)**2
            else:
                self.T[1, 0, 0] -= 0.5 * h**2 * torch.tan(e1)**3
                self.T[3, 0, 2] += 0.5 * h**2 * torch.tan(e1) / torch.cos(e1)**2
                self.T[3, 2, 0] += 0.5 * h**2 * torch.tan(e1) / torch.cos(e1)**2

    def makethin(self, n: int, *, style: str = None) -> Union[Element, ThinElement]:
        raise NotImplementedError


@PartitionedElement.register
class AlignmentError(AnnotationTypedAttributes, torch.nn.Module):
    """Wrapper class representing coordinate transformations due to alignment errors or tilts.
       Do not instantiate directly, use one of the subclasses instead.

    Attributes
    ----------
    target : :data:`LatticeElement` or AlignmentError
        Target of the alignment error can be a lattice element or another alignment error.
    """
    triggers = tuple()  # Attribute names that trigger the usage of a particular `AlignmentError`.

    def __init__(self, target: Union[LatticeElement, AlignmentError]):
        super().__init__()
        self.target = target
        self.d_enter = torch.zeros(6, 1)
        self.R_enter = torch.eye(6)
        self.T_enter = torch.zeros(6, 6, 6)
        self.d_exit = torch.zeros(6, 1)
        self.R_exit = torch.eye(6)
        self.T_exit = torch.zeros(6, 6, 6)

    def __call__(self, x: Tensor, *, method: str) -> Tensor:
        return super().__call__(x, method=method)

    def __repr__(self):
        return (f'{type(self).__name__}('
                f'{", ".join(f"{x}={repr(getattr(self, x))}" for x in get_type_hints(type(self)))},\n'
                f'{" " * (len(type(self).__name__) + 1)}'
                f'target={self.target!r})')

    @property
    def aperture(self) -> Optional[Aperture]:
        return self.target.aperture

    @property
    def l(self) -> Tensor:
        return self.target.l

    @property
    def label(self) -> str:
        return self.target.label

    @property
    def element(self) -> LatticeElement:
        """The underlying lattice element to which the alignment error(s) is (are) applied."""
        return list(self.unwrap())[-1]

    @property
    def transfer_map_enter(self) -> TransferMap:
        """Transfer map at entrance of the element."""
        return self.d_enter, self.R_enter, self.T_enter

    @property
    def transfer_map_exit(self) -> TransferMap:
        """Transfer map at exit of the element."""
        return self.d_exit, self.R_exit, self.T_exit

    @property
    def transfer_maps(self) -> List[Union[TransferMap, List]]:
        """Return the single transfer maps for entrance transformation, actual element and exit transformation."""
        try:
            target_map = self.target.transfer_map  # Try 'transfer_map' first in case 'target' is a CompoundElement.
        except AttributeError:
            target_map = self.target.transfer_maps
        return [self.transfer_map_enter, target_map, self.transfer_map_exit]

    def update_transfer_map(self, *, reset=False) -> None:
        """Update the transfer map of the `target` lattice element that this alignment error instance refers to
           (see :meth:`CompactElement.update_transfer_map`)"""
        self.target.update_transfer_map(reset=reset)

    def linear(self, x: Tensor) -> Tensor:
        """Linear tracking through the element with alignment error transformations at entrance and exit."""
        return self(x, method='linear')

    def second_order(self, x: Tensor) -> Tensor:
        """Second order tracking through the element with alignment error transformations at entrance and exit."""
        return self(x, method='second_order')

    def exact(self, x: Tensor) -> Tensor:
        """Exact tracking through the element with alignment error transformations at entrance and exit."""
        return self(x, method='exact')

    def forward(self, x: Tensor, *, method: str) -> Tensor:
        return self.exit(self.target(self.enter(x), method=method))

    def enter(self, x: Tensor) -> Tensor:
        """Applies linear coordinate transformation at the entrance of the wrapped element."""
        return self.R_enter @ x + self.d_enter

    def exit(self, x: Tensor) -> Tensor:
        """Applies linear coordinate transformation at the exit of the wrapped element."""
        return self.R_exit @ x + self.d_exit

    def loss(self, x: Tensor) -> Tensor:
        return self.target.loss(x)

    def makethin(self, n: int, *, style: Optional[str] = None) -> AlignmentError:
        copied = copy.copy(self)
        copied._modules = copy.copy(copied._modules)  # Copy _modules because __setattr__ puts the value there if it is a Module.
        copied.target = self.target.makethin(n, style=style)
        return copied

    def unwrap(self) -> Iterator[Union[AlignmentError, LatticeElement]]:
        """Returns an iterator over the alignment error hierarchy eventually yielding the underlying lattice element."""
        yield self
        if isinstance(self.target, AlignmentError):
            yield from self.target.unwrap()
        else:
            yield self.target


class Offset(AlignmentError):
    """AlignmentError representing the xy-offset of an element.

    Attributes
    ----------
    dx : Number or Parameter
        Horizontal offset.
    dy : Number or Parameter
        Vertical offset.
    """
    dx : Union[Tensor, Parameter]
    dy : Union[Tensor, Parameter]
    triggers = ('dx', 'dy')

    def __init__(self, target: Union[LatticeElement, AlignmentError],
                 dx: Parameterizable[Number] = 0, dy: Parameterizable[Number] = 0):
        super().__init__(target)
        self.dx = prepare_attribute_value(dx)
        self.dy = prepare_attribute_value(dy)

    @property
    def d_enter(self) -> Tensor:
        d_inv = torch.zeros(6, 1)
        d_inv[0] -= self.dx
        d_inv[2] -= self.dy
        return d_inv

    @property
    def d_exit(self) -> Tensor:
        d = torch.zeros(6, 1)
        d[0] += self.dx
        d[2] += self.dy
        return d

    @d_enter.setter
    def d_enter(self, value):
        pass

    @d_exit.setter
    def d_exit(self, value):
        pass


class LongitudinalRoll(AlignmentError):
    """AlignmentError representing the roll about the longitudinal axis of an element.

    .. Note::
       MADX uses a right-handed coordinate system (see Fig. 1.1, MADX User's Guide), therefore
       ``x = x*cos(psi) - y*sin(psi)`` describes a clockwise rotation of the trajectory.

    Attributes
    ----------
    psi : Number or Parameter
        Rotation angle about s-axis.
    """
    psi : Union[Tensor, Parameter]
    triggers = ('dpsi',)

    def __init__(self, target: Union[LatticeElement, AlignmentError], psi: Parameterizable[Number] = 0):
        super().__init__(target)
        self.psi = prepare_attribute_value(psi)

    @property
    def R_enter(self) -> Tensor:
        cos = torch.cos(self.psi)
        sin = torch.sin(self.psi)
        R_inv = torch.eye(6)
        R_inv[0, 0] = R_inv[1, 1] = R_inv[2, 2] = R_inv[3, 3] = cos
        R_inv[0, 2] = R_inv[1, 3] = sin
        R_inv[2, 0] = R_inv[3, 1] = -sin
        return R_inv

    @property
    def R_exit(self) -> Tensor:
        cos = torch.cos(self.psi)
        sin = torch.sin(self.psi)
        R = torch.eye(6)
        R[0, 0] = R[1, 1] = R[2, 2] = R[3, 3] = cos
        R[0, 2] = R[1, 3] = -sin
        R[2, 0] = R[3, 1] = sin
        return R

    @R_enter.setter
    def R_enter(self, value):
        pass

    @R_exit.setter
    def R_exit(self, value):
        pass


class Tilt(LongitudinalRoll):
    """The tilt of an element represents the roll about the longitudinal axis.

    .. Note::
       MADX uses a right-handed coordinate system (see Fig. 1.1, MADX User's Guide), therefore
       ``x = x*cos(psi) - y*sin(psi)`` describes a clockwise rotation of the trajectory.

    Attributes
    ----------
    psi : Number or Parameter
        Rotation angle about s-axis.

    Notes
    -----
    `Tilt` is only a subclass of `AlignmentError` for technical reasons and has no meaning beyond that.
    A `Tilt` is not considered an alignment error from the simulation point of view.
    """
    triggers = ('tilt',)


class BPMError(AlignmentError):
    """BPM readout errors.

    The actual BPM reading is computed as (for both horizontal and vertical plane separately): ``rx * (x + ax)``.

    Attributes
    ----------
    ax : Tensor or :data:`Parameter`
        Horizontal absolute read error.
    ay : Tensor or :data:`Parameter`
        Vertical absolute read error.
    rx : Tensor or :data:`Parameter`
        Horizontal relative read error.
    ry : Tensor or :data:`Parameter`
        Vertical relative read error.
    """
    ax : Union[Tensor, Parameter]
    ay : Union[Tensor, Parameter]
    rx : Union[Tensor, Parameter]
    ry : Union[Tensor, Parameter]
    triggers = ('mrex', 'mrey', 'mscalx', 'mscaly')

    def __init__(self, target: Monitor,
                 ax: Parameterizable[Number] = 0, ay: Parameterizable[Number] = 0,
                 rx: Parameterizable[Number] = 0, ry: Parameterizable[Number] = 0):
        super().__init__(target)
        setattr_multi(self, ['ax', 'ay', 'rx', 'ry'], locals())  # __setattr__ takes care of attribute value preparation.

    def enter(self, x: Tensor) -> Tensor:
        return x

    def exit(self, x: Tensor) -> Tensor:
        return x

    def readout(self, x: Tensor) -> Tensor:
        """Return BPM readings subject to absolute and relative readout errors.

        Parameters
        ----------
        x : Tensor
            6D phase-space coordinates of shape (6, N).

        Returns
        -------
        xy : Tensor
            BPM readings in x- and y-dimension of shape (2, N).

        See Also
        --------
        :meth:`Monitor.readout`
        """
        a = torch.zeros(2, 1)
        r = torch.zeros(2, 1)
        a[0, 0] = self.ax
        a[1, 0] = self.ay
        r[0, 0] = 1. + self.rx
        r[1, 0] = 1. + self.ry
        return r * (x[[0, 2]] + a)


class Segment(torch.nn.Module):
    """Wrapper class representing a sequence of elements (possibly a segment of the lattice).

    Elements or sub-segments can be selected via `__getitem__`, i.e. ``segment[item]`` notation. Here `item` can be
    one of the following:

    * int - indicating the index position in the segment.
    * str - will be compared for equality against element labels; if a single element with that label is found it is
      returned otherwise all elements with that label are returned as a list. An exception are strings containing an
      asterisk which will be interpreted as a shell-style wildcard and converted to a corresponding regex Pattern.
    * re.Pattern - will be matched against element labels; a list of all matching elements is returned.
    * instance of :class:`Element` or :class:`AlignmentError` - the element itself (possibly wrapped by other
      AlignmentError instances is returned.
    * subclass of :class:`Element` or :class:`AlignmentError` - a list of elements of that type (possibly wrapped by
      AlignmentError instances) is returned.
    * tuple - must contain two elements, the first being one of the above types and the second an integer; the first
      element is used to select a list of matching elements and the second integer element is used to select the
      corresponding element from the resulting list.
    * slice - start and stop indices can be any of the above types that selects exactly a single element or None;
      a corresponding sub-Segment is returned. The `step` parameter of the slice is ignored. In case the stop marker
      is not None, the corresponding element is included in the selection.
      
    An element of a segment can be updated by using `__setitem__`, i.e. ``segment[item] = ...`` notation, where `item`
    can be any of the above types that selects exactly a single element.

    Attributes
    ----------
    elements : list of :data:`LatticeElement`
    """

    # noinspection PyShadowingNames
    def __init__(self, elements: Sequence[LatticeElement]):
        super().__init__()
        self.elements = list(elements)
        for i, element in enumerate(elements):
            self._set_element_as_attribute(element, i)

    # Workaround for https://youtrack.jetbrains.com/issue/PY-37601#focus=streamItem-27-3719045.0-0
    def __call__(self, *args, **kwargs) -> Tensor:
        return super().__call__(*args, **kwargs)

    @singledispatchmethod
    def __getitem__(self, item) -> NoReturn:
        raise TypeError(f'Illegal type for element selection: {type(item)}')

    @__getitem__.register(int)
    def _(self, item: int) -> LatticeElement:
        return self.elements[item]

    @__getitem__.register(str)
    def _(self, item: str) -> Union[LatticeElement, List[LatticeElement]]:
        selection = [x for x in self.elements if match_element(item, x)]
        if len(selection) == 1 and '*' not in item:
            selection = selection[0]
        return selection

    @__getitem__.register(re.Pattern)
    @__getitem__.register(type)
    def _(self, item: Union[Pattern, Type[LatticeElement]]) -> List[LatticeElement]:
        return [x for x in self.elements if match_element(item, x)]

    # noinspection PyTypeChecker
    @__getitem__.register(slice)
    def _(self, item: SubSegmentSelector) -> Segment:
        start, stop = item.start, item.stop
        if not isinstance(start, int) and start is not None:
            start = self.get_element_index(start)
        if not isinstance(stop, int) and stop is not None:
            stop = self.get_element_index(stop) + 1
        return Segment(self.elements[start:stop])

    @__getitem__.register(tuple)
    def _(self, item: Tuple[MultiElementSelector, int]) -> LatticeElement:
        selection = self[item[0]]
        if isinstance(selection, list):
            try:
                return selection[item[1]]
            except IndexError:
                raise IndexError(f'{item[1]} (only {len(selection)} elements with characteristic '
                                 f'{repr(item[0])} were found)') from None
        else:
            if item[1] != 0:
                raise IndexError(f'{item[1]} (only 1 element with label {repr(item[0])} was found')
            return selection

    del _

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return f'{type(self).__name__}(elements={pformat(self.elements)})'

    def __setitem__(self, index: SingleElementSelector, value: LatticeElement):
        if not isinstance(index, int):
            index = self.get_element_index(index)
        self.elements[index] = value
        self._set_element_as_attribute(value, index)

    @property
    def l(self) -> Tensor:
        return sum(e.l for e in self.elements)

    def apply_unique_labels(self) -> None:
        """Ensure that every element in the lattice has a unique label.

        If an element's label is `None` it will be replaced by a string indicating its position, e.g. ``e5`` for the
        fifth element. If an element's label already appeared before then it will be augmented by ``_{i+1}`` where
        ``i`` is the number of times this label has appeared already.

        This method modifies the element labels in-place.

        Raises
        ------
        RuntimeError
            If the algorithm cannot find a unique labeling, e.g. if labels are ``['a', 'a_2', 'a']`` then for the
            last element the algorithm attempts to use ``a_2`` however this label appeared already one element before.
        """
        seen = Counter()
        for i, element in enumerate(self.elements, start=1):
            label = element.label
            if label is None:
                label = f'e{i}'
            if label in seen:
                seen[label] += 1
                label = f'{label}_{seen[label]}'
                if label in seen:
                    raise RuntimeError(f'Augmented label already appeared before: {label!r} (cannot find unique labeling)')
            seen[label] += 1
            element.label = label

    def transfer_maps(self, method: Literal['accumulate', 'reduce', 'local'], *,
                      order: Literal[1, 2] = 2,
                      indices: Optional[Union[Literal[0, 1, 2], Tuple[Literal[0, 1, 2], ...]]] = None,
                      symplectify: bool = True,
                      labels: bool = False,
                      unfold_alignment_errors: bool = False,
                      d0: Optional[Tensor] = None,
                      R0: Optional[Tensor] = None,
                      T0: Optional[Tensor] = None
                      ) -> Union[Tensor, TransferMap, List[Tensor], List[TransferMap], List[Tuple[str, Tensor]], List[Tuple[str, TransferMap]]]:
        """Process the transfer maps of the segment's elements according to the specified method.

        .. Note::
           This does not automatically compute the closed orbit first in order to use it as a starting value for `d0`.
           In that case, the closed orbit has to be provided manually in form of the parameter `d0`.

        Parameters
        ----------
        method : str in {'accumulate', 'reduce', 'local'}
            If "accumulate" then the transfer maps are accumulated by contracting subsequent transfer maps.
            If "reduce" then the contracted transfer map for the complete segment is returned (this is identical to the last
            transfer map for "accumulate").
            If "local" then the local transfer map of each element is computed, taking into consideration the value of the
            local closed orbit. The result contains the closed orbit at the exit of each element as the zeroth order coefficient.
        order : int
            The order up to which transfer map coefficients (d, R, T) are taken into account for the contraction of two
            subsequent transfer maps.
        indices : int or tuple of int
            Indicates the indices of the processed transfer maps which should be stored in the results. If a single number
            is given, all indices up to the specified number (inclusive) are considered.
            E.g. if ``indices = 0`` and ``method = 'reduce'`` then the result will be just ``d`` where ``d`` is the
            orbit computed to second order but the resulting first and second order coefficients of the reduced transfer
            maps are discarded. Discarding coefficients of higher orders in the (intermediary) results can save memory
            and compute time. Note that ``max(indices) <= order`` must be fulfilled.
        symplectify : bool
            Specifies whether the linear term (the transfer matrix) of lattice elements should be symplectified after
            the addition of second-order feed-down terms. This is only relevant for ``order >= 2``.
        labels : bool
            If True then the element's labels are returned alongside their transfer maps as 2-tuples (for ``method = "reduce"``
            this parameter is ignored).
            In case `unfold_alignment_errors` is True as well, an element's label is repeated for each alignment error
            map (at entrance and exit), e.g. for an offset element "e1" it will be
            ``[..., ("e1", entrance_map), ("e1", element_map), ("e1", exit_map), ...]``.
        unfold_alignment_errors : bool
            If True then the entrance and exit transformations of alignment errors are considered as separate transfer maps
            rather than being contracted with their wrapped element's map. This increases the number of transfer maps as
            compared to the length of the segment.
        d0 : Tensor, optional
            The value of the closed orbit at the beginning of the segment.
        R0 : Tensor, optional
            Initial value for the first order terms.
        T0 : Tensor, optional
            Initial value for the second order terms.

        Returns
        -------
        transfer_maps : :class:`TransferMap` or list of :class:`TransferMap`
            Depending on the value of `method` either of the following is returned:
                * "accumulate" -- a list of the accumulated transfer maps along the lattice is returned.
                * "reduce" -- the single transfer map, corresponding to the whole segment, is returned.
                * "local" -- a list of the element-local transfer maps is returned.
        """
        if indices is None:
            indices = range(order + 1)
        elif isinstance(indices, int):
            indices = (indices,)
        if max(indices) > order:
            raise ValueError(f'Requested indices exceed the specified order: {indices} > {order}')

        result = self.compute_transfer_maps(method, order=order, index=max(indices), symplectify=symplectify,
                                            unfold_alignment_errors=unfold_alignment_errors, d0=d0, R0=R0, T0=T0)

        if len(indices) == 1:
            result = (m[indices[0]] for m in result)
        else:
            result = (tuple(m[i] for i in indices) for m in result)
        if method == 'reduce':
            return next(result)
        elif labels:
            if unfold_alignment_errors:
                labels = it.chain.from_iterable(it.repeat(e.label,
                                                          2*len(tuple(e.unwrap()))-1 if isinstance(e, AlignmentError) else 1)
                                                for e in self.elements)
            else:
                labels = (e.label for e in self.elements)
            result = zip(labels, result)
        return list(result)

    @copy_doc(PartitionedElement)
    def compute_transfer_maps(self, method: Literal['accumulate', 'reduce', 'local'], *,
                              order: Literal[1, 2] = 2,
                              index: Optional[Literal[0, 1, 2]] = None,
                              symplectify: bool = True,
                              unfold_alignment_errors: bool = False,
                              d0: Optional[Tensor] = None,
                              R0: Optional[Tensor] = None,
                              T0: Optional[Tensor] = None) -> Iterator[TransferMap]:

        def handle(x: TransferMap, y: LatticeElement) -> Iterator[TransferMap]:
            """Handle the given element `y` by producing a corresponding stream of transfer maps starting from `x`."""
            if isinstance(y, AlignmentError):
                x = process(x, y.transfer_map_enter)
                if unfold_alignment_errors:
                    yield x
                for x in handle(x, y.target):
                    if unfold_alignment_errors:
                        yield x
                yield process(x, y.transfer_map_exit)
            else:
                try:
                    y_map = y.transfer_map
                except AttributeError:
                    initial = dict(d0=x[0])
                    if method != 'local':
                        initial['R0'] = x[1]
                        initial['T0'] = x[2]
                    yield from y.compute_transfer_maps('reduce', order=order, index=index, symplectify=symplectify,
                                                       **initial)
                else:
                    yield process(x, y_map)

        def process(x: TransferMap, y: TransferMap) -> TransferMap:
            """Process the given transfer maps by producing a new transfer map starting from `x`."""
            if method == 'local':
                return (_contract_transfer_maps(x, y, order=order, index=0)[0],
                        *_update_transfer_matrix_reference(x, y, order=order, symplectify=symplectify)[1:])
            else:
                return _contract_transfer_maps(x, y, order=order, symplectify=symplectify, index=index)

        if index is None:
            index = order

        transfer_maps = it.chain([[(torch.zeros(6, 1)    if d0 is None                else d0,  # Wrap in extra list since the handler
                                    torch.eye(6)         if R0 is None and index >= 1 else R0,  # expects a stream of maps per element.
                                    torch.zeros(6, 6, 6) if T0 is None and index >= 2 else T0)]],
                                 self.elements)
        if method in {'accumulate', 'local'}:
            result = it.islice(it.accumulate(transfer_maps, lambda x, y: tuple(handle(x[-1], y))), 1, None)
            yield from it.chain.from_iterable(result)
        elif method == 'reduce':
            yield reduce(lambda x, y: tuple(handle(x[-1], y)), transfer_maps)[-1]
        else:
            raise ValueError(f'method must be one of {{"accumulate", "reduce", "local"}} (got {method!r})')

    def update_transfer_maps(self, *, reset=False) -> None:
        """Update the transfer map of each element (see :meth:`CompactElement.update_transfer_map`)."""
        for element in self.elements:
            element.update_transfer_map(reset=reset)

    def get_element_index(self, marker: SingleElementSelector) -> int:
        label, count = marker if isinstance(marker, tuple) else (marker, None)
        indices = [i for i, x in enumerate(self.elements) if match_element(label, x)]
        if not indices:
            raise IndexError(f'No element with label "{label}" found')
        elif len(indices) > 1 and count is None:
            raise IndexError(f'{len(indices)} elements with label "{label}" found; without an occurrence count this '
                             f'selection is ambiguous. An occurrence count can be provided via (label, count).')
        if count is None:
            count = 0
        try:
            return indices[count]
        except IndexError:
            raise IndexError(f'Cannot select element "{label}" #{count} ({len(indices)} were found)') from None

    def linear(self, x: Tensor, **kwargs) -> Union[Tensor, Tuple]:
        """Linear tracking through the segment."""
        return self(x, method='linear', **kwargs)

    def second_order(self, x: Tensor, **kwargs) -> Union[Tensor, Tuple]:
        """Second order tracking through the segment."""
        return self(x, method='second_order', **kwargs)

    def exact(self, x: Tensor, **kwargs) -> Union[Tensor, Tuple]:
        """Exact tracking through the segment."""
        return self(x, method='exact', **kwargs)

    def forward(self, x: Tensor, *,
                method: SelectionCriteria[Union[str, Callable[[Tensor], Tensor]]],
                aperture: bool = False, exact_drift: bool = True,
                observe: Optional[Union[bool, MatchingCriteria]] = None,
                recloss: Optional[Union[bool, MatchingCriteria]] = None,
                loss_func: Callable[[Tensor], Tensor] = None) -> Union[Tensor, Tuple]:
        """Track the given particles through the segment.

        Parameters
        ----------
        x : Tensor
            Shape `(6, N)` where `N` is the number of particles.
        method : :data:`SelectionCriteria` of str or callable
            Method name which will be used for the lattice elements to perform tracking.
        aperture : bool
            Determines whether aperture checks are performed (and thus particles marked lost / excluded from tracking).
        exact_drift : bool
            If true (default) then `Drift`s will always be tracked through via `exact`, no matter what `method` is.
        observe : sequence of {str or re.Pattern or subclass of `Element`}
            Indicates relevant observation points; the (intermediary) positions at these places will be returned.
            Items are matched against element labels (see function `match_element`).
        recloss : bool or "sum" or {str or re.Pattern or subclass of `Element`} or a sequence thereof
            If "sum" then the particle loss at each element will be recorded and summed into a single variable which
            will be returned. If a sequence is given it must contain element labels or regex patterns and the loss will
            be recorded only at the corresponding elements (similar to `observe` for positions). If `True` then the loss
            will be recorded at all elements; if `False` the loss is not recorded at all. A true value for this
            parameter will automatically set `aperture` to `True`.
        loss_func : callable
            This parameter can be used to supply a function for transforming the returned loss at each element. This
            can be useful if some variation of the loss is to be accumulated into a single tensor. The function
            receives the loss tensor as returned by `Aperture.loss` as an input and should return a tensor of any shape.
            If not supplied this function defaults to `torch.sum` if `recloss == "accumulate"` and the identity if
            ``recloss == "history"``. Note that if a function is supplied it needs to cover all the steps, also the
            summation in case ``recloss == "accumulate"`` (the default only applies if no function is given).

        Returns
        -------
        x : Tensor
            Shape `(6, M)` where `M` is the number of particles that reached the end of the segment (`M` can be
            different from `N` in case aperture checks are performed).
        history : dict
            The (intermediary) positions at the specified observation points. Keys are element labels and values are
            positions of shape `(6, M_i)` where `M_i` is the number of particles that reached that element.
            This is only returned if `observe` is true.
        loss : Tensor or dict
            If ``recloss == "accumulate"`` the loss value accumulated for each element (i.e. the sum of all individual
            loss values) is returned. Otherwise, if `recloss` is true, a dict mapping element labels to recorded loss
            values is returned.
        """
        method = setup_matching_criteria(method, str)

        def _get_method(_element):
            if isinstance(_element, Drift) and exact_drift:
                return 'exact'
            try:
                return find_matching_criterion(_element, method)
            except KeyError:
                if isinstance(_element, Segment):
                    return method
                else:
                    raise TrackingError(f'The following element did not match any tracking method specification: {_element}') from None

        def _forward(_x, _element):
            _method = _get_method(_element)
            _kwargs = {}
            if isinstance(_element, Segment):
                _kwargs.update(aperture=aperture, exact_drift=exact_drift)
            if callable(_method):
                return _method(_element, _x, **_kwargs)
            else:
                return _element(_x, method=_method, **_kwargs)

        if not (aperture or observe or recloss):
            return reduce(_forward, self.elements, x)

        if observe is None or isinstance(observe, bool):
            observe = observe or []
        elif not isinstance(observe, list):
            observe = [observe]

        if recloss:
            aperture = True
        accumulate = recloss == 'sum'
        if accumulate:
            if loss_func is None:
                loss_func = torch.sum
            recloss = True
        elif recloss is False or recloss is None:
            recloss = []
        elif recloss is not True and not isinstance(recloss, list):
            recloss = [recloss]

        acc_loss = tensor(0.)
        loss_history = {}
        history = {}
        for element in self.elements:
            if aperture:  # Check aperture at entrance of element.
                if x.shape[1] > 0:
                    loss = element.loss(x)
                else:
                    loss = x.sum(dim=0)  # Produces zero.
                if recloss is True or any(match_element(place, element) for place in recloss):
                    custom_loss_val = loss_func(loss) if loss_func is not None else loss
                    if accumulate:
                        acc_loss.add_(custom_loss_val)
                    else:
                        loss_history[element.label] = custom_loss_val
                x = x[:, loss == 0]  # Particles with `loss > 0` are lost.
            if x.shape[1] > 0:
                x = _forward(x, element)
            if observe is True or any(match_element(place, element) for place in observe):
                history[element.label] = x
        ret_val = [x]
        if observe:
            ret_val.append(history)
        if accumulate:
            ret_val.append(acc_loss)
        elif recloss:
            ret_val.append(loss_history)
        return tuple(ret_val) if len(ret_val) > 1 else ret_val[0]

    def makethin(self, n: SelectionCriteria[int], *, style: Optional[SelectionCriteria[str]] = None) -> Segment:
        """Retrieve a thin representation for each element of the segment except for those indicated by `exclude`.

        Parameters
        ----------
        n : :data:`SelectionCriteria` of int
            Number of thin slices. If `int` this applies to all elements. Otherwise must key-value pairs. Keys should be
            element selectors (see :data:`SingleElementSelector` and :data:`MultiElementSelector`) or `None` for
            providing a default. Values should be the corresponding number of slices that are applied to the elements
            that match the key selector. Only the first matching key is considered.
            If a default value is desired it can be provided in various ways:

                1. Using ``{None: default_value}``.
                2. Using a regex that matches any label (given that all elements have a `label` different from `None`).
                3. Using the class `Element`.

            Note that for all options these should appear at the very end of the list of criteria, otherwise they will
            override any subsequent definitions.
        style : :data:`SelectionCriteria` of str
            Slicing style per element. Works similar to the `n` parameter. See :meth:`Element.makethin` for more
            information about available slicing styles.

        Returns
        -------
        Segment
            Containing thin elements.

        See Also
        --------
        :func:`find_matching_criterion`
            For details about how keys in `n` can be used to fine-tune the slice number per element.
        :meth:`Element.makethin`
            For available slicing styles.
        """
        n = setup_matching_criteria(n, int)
        style = setup_matching_criteria(style, str, optional=True)
        segment = []
        for element in self.elements:
            try:
                val = find_matching_criterion(element, n)
            except KeyError:
                logger.debug('The following element did not match any slice number definition and remains thick: '
                             '%s', element)
                val = 0
            segment.append(element.makethin(val, style=find_matching_criterion(element, style)) if val > 0 else element)
        return Segment(segment)

    def flatten(self) -> Iterator[Union[LatticeElement, AlignmentError]]:
        """Retrieve a flat representation of the segment (with sub-segments flattened as well)."""
        for item in self.elements:
            if isinstance(item, Segment):
                yield from item.flatten()
            else:
                yield item

    def flat(self) -> Segment:
        """Convenience function wrapping `Segment.flatten`."""
        return Segment(list(self.flatten()))

    def _set_element_as_attribute(self, element: LatticeElement, index: int):
        setattr(self, f'_e{index}_{getattr(element, "label", None)}', element)


@CompactElement.register
class CompoundElement(AnnotationTypedAttributes, Segment):
    """Represents an element which is composed of multiple interdependent parts.

    Attributes
    ----------
    transfer_map_order : int
        The order of truncation used for contracting the successive transfer maps into a single transfer map (see also
        :class:`Element`).
    """
    l: Tensor

    transfer_map_order = 2

    field_errors = {}

    def __init__(self, parts: Sequence[LatticeElement],
                 *, aperture: Optional[Aperture] = None, beam: Optional[dict] = None, label: Optional[str] = None,
                 **kwargs):
        super().__init__(parts)
        self.aperture = aperture
        self.beam = beam
        self.label = label
        kwargs.pop('nst', None)  # Remove optional PTC parameters.
        if kwargs:
            warnings.warn(f'Unknown parameters for element of type {type(self)}: {kwargs}')

    def __repr__(self):
        base = Element.__repr__(self)
        sep = '\n    > '
        return base + sep + sep.join(repr(e) for e in self.elements)

    @property
    def element(self) -> CompoundElement:
        """Return the element itself (this property exists for compatibility with :class:`Element`."""
        return self

    @property
    def d(self) -> Tensor:
        """Zeroth order coefficients of the overall transfer map of the compound element."""
        return self.transfer_map[0]

    @property
    def R(self) -> Tensor:
        """First order coefficients of the overall transfer map of the compound element."""
        return self.transfer_map[1]

    @property
    def T(self) -> Tensor:
        """Second order coefficients of the overall transfer map of the compound element."""
        return self.transfer_map[2]

    @property
    def transfer_map(self) -> TransferMap:
        """Return the overall transfer map of the compound element."""
        return next(self.compute_transfer_maps('reduce', order=self.transfer_map_order, symplectify=False))

    def update_transfer_map(self, *, reset=False) -> None:
        """Update the transfer map of each part of the compound element (see :meth:`CompactElement.update_transfer_map`)."""
        return self.update_transfer_maps(reset=reset)

    def loss(self, x: Tensor) -> Tensor:
        return self.aperture(x[[0, 2]])


class SBend(CompoundElement):
    """Sector bending magnet.

    Parameters
    ----------
    angle : Number
        Bending angle of the dipole [rad].
    e1 : Number
        Rotation angle for the entrance pole face [rad]. ``e1 = e2 = angle/2`` turns an `SBEND` into a `RBEND`.
    e2 : Number
        Rotation angle for the exit pole face [rad].
    fint : Number
        Fringing field integral at entrance. If `fintx` is not specified then `fint` is also used at the exit.
    fintx : Number
        Fringing field integral at exit.
    hgap : Number
        Half gap of the magnet [m].
    h1 : Number
        Curvature of the entrance pole face [1/m].
    h2 : Number
        Curvature of the exit pole face [1/m].
    """
    angle: Tensor
    e1: Tensor
    e2: Tensor
    fint: Tensor
    fintx: Tensor
    hgap: Tensor
    h1: Tensor
    h2: Tensor

    field_errors = {'k0': 'dk0'}

    def __init__(self,
                 angle: Number,
                 l: Number,
                 e1: Number = 0,
                 e2: Number = 0,
                 fint: Union[Number, bool] = 0.,
                 fintx: Optional[Number] = None,
                 hgap: Number = 0,
                 h1: Number = 0,
                 h2: Number = 0,
                 *,
                 beam: dict,
                 dk0: Number = 0,
                 aperture: Optional[Aperture] = None,
                 label: Optional[str] = None,
                 **kwargs):
        if fint is True:
            fint = 0.5
        if fintx is None:
            fintx = fint
        entrance = Dipedge(angle / l, e1, fint, hgap, h1, entrance=True, **kwargs.copy())
        body = SBendBody(angle, l, beam=beam, dk0=dk0, **kwargs.copy())
        exit = Dipedge(angle / l, e2, fintx, hgap, h2, entrance=False, **kwargs.copy())
        super().__init__([entrance, body, exit], aperture=aperture, beam=beam, label=label, **kwargs)
        self.entrance = entrance
        self.body = body
        self.exit = exit
        self._hgap = prepare_attribute_value(hgap)

    @property
    def angle(self) -> Tensor:
        return self.body.angle

    @angle.setter
    def angle(self, value: Number):
        self.body.angle = value

    @property
    def e1(self) -> Tensor:
        return self.entrance.e1

    @e1.setter
    def e1(self, value: Number):
        self.entrance.e1 = value

    @property
    def e2(self) -> Tensor:
        return self.exit.e1

    @e2.setter
    def e2(self, value: Number):
        self.exit.e1 = value

    @property
    def fint(self) -> Tensor:
        return self.entrance.fint

    @fint.setter
    def fint(self, value: Number):
        self.entrance.fint = value

    @property
    def fintx(self) -> Tensor:
        return self.exit.fint

    @fintx.setter
    def fintx(self, value: Number):
        self.exit.fint = value

    @property
    def h1(self) -> Tensor:
        return self.entrance.he

    @h1.setter
    def h1(self, value: Number):
        self.entrance.he = value

    @property
    def h2(self) -> Tensor:
        return self.exit.he

    @h2.setter
    def h2(self, value: Number):
        self.exit.he = value

    @property
    def hgap(self) -> Tensor:
        return self._hgap

    @hgap.setter
    def hgap(self, value: Number):
        self.entrance.hgap = value
        self.exit.hgap = value
        self._hgap = value

    @property
    def k0(self) -> Tensor:
        return self.body.k0

    @k0.setter
    def k0(self, value: Number):
        self.body.k0 = value

    @property
    def dk0(self) -> Tensor:
        return self.body.dk0

    @dk0.setter
    def dk0(self, value: Number):
        self.body.dk0 = value

    def flatten(self) -> Iterator[SBend]:
        yield self


class RBend(SBend):
    """Sector bending magnet with parallel pole faces (see :class:`SBend`)."""

    def __init__(self,
                 angle: Number,
                 l: Number,
                 e1: Number = 0,
                 e2: Number = 0,
                 fint: Union[Number, bool] = 0.,
                 fintx: Optional[Number] = None,
                 hgap: Number = 0,
                 h1: Number = 0,
                 h2: Number = 0,
                 *,
                 beam: dict,
                 dk0: Number = 0,
                 aperture: Optional[Aperture] = None,
                 label: Optional[str] = None,
                 **kwargs):
        super().__init__(angle, l, e1 + angle/2, e2 + angle/2, fint, fintx, hgap, h1, h2,
                         dk0=dk0, beam=beam, aperture=aperture, label=label, **kwargs)


@PartitionedElement.register
class ThinElement(Segment):
    """Thin version of an element (containing thin slices separated by drift spaces; see :meth:`Element.makethin`).
    
    Attributes
    ----------
    makethin_deltas : dict
        Contains functions to compute the distances between slices for the various slicing styles. The functions
        expect the number of slices as an argument and return the distance between element boundaries and first/last
        slice and the distance between slices as a 2-tuple.
    """
    makethin_deltas = {'edge':   lambda n: (0.,            1 / (n - 1)     ),
                       'simple': lambda n: (0.5 / n,       1 / n           ),
                       'teapot': lambda n: (0.5 / (n + 1), n / (n ** 2 - 1))}

    # noinspection PyShadowingNames
    def __init__(self, base: LatticeElement, elements: Sequence[LatticeElement]):
        super().__init__(elements)
        self.base = base

    def __repr__(self):
        sep = '\n    > '
        return repr(self.base) + sep + sep.join(repr(e) for e in self.elements)

    @property
    def aperture(self) -> Aperture:
        return self.base.aperture

    @property
    def l(self) -> Tensor:
        return self.base.l

    @property
    def label(self) -> str:
        return self.base.label

    def loss(self, x: Tensor) -> Tensor:
        return self.base.loss(x)

    @classmethod
    def create_thin_sequence(cls, n: int, l: Number, thick_cls: partial, thin_cls: partial, base_label: str,
                             style: str) -> List[LatticeElement]:
        """Create a sequence of `n` thin elements given by `thin_cls` using the requested slicing style.

        Parameters
        ----------
        n : int
            Number of slices (i.e. number of thin elements in the segment).
        l : Number
            Length of the segment (usually the length of the original lattice element).
        thick_cls : partial of Element
            Partial type which should inherit from `Element`. Thick elements will be created as
            ``thick_cls(l=..., label=...)``.
        thin_cls : partial of Element
            Partial type which should inherit from `Element`. Thin elements will be created as ``thin_cls(label=...)``.
        base_label : str
            Base label of the segment's elements. Drifts will have suffix ``__d{i}`` and thin elements ``__{i}`` where
            `i` is the position in the segment.
        style : str
            Slicing style. Available styles are ``{"teapot", "simple", "edge"}``. See Notes for more details.

        Returns
        -------
        thin_sequence : list of :data:`LatticeElement`

        Notes
        -----
        All slicing styles imply equidistant slices, the difference is the offset to the entrance and exit of the
        element as well as the distance between slices. Let :math:`\\delta` be the distance from the entrance of the
        element to the first slice (and likewise, due to symmetry reasons, the distance from the last slice to the exit
        of the element) and :math:`\\Delta` is the distance between two slices (:math:`\\delta, \\Delta` are normalized
        to the length of the element). If :math:`n` is the number of slices then the following condition must hold:

        .. math:: 2\\delta + (n - 1)\\Delta = 1

        The different styles choose :math:`\\delta, \\Delta` as follows:

        +--------+---------------------------+--------------------------+
        |        | :math:`\\delta`           | :math:`\\Delta`          |
        +========+===========================+==========================+
        | teapot | :math:`\\frac{1}{2(n+1)}` | :math:`\\frac{n}{n^2-1}` |
        +--------+---------------------------+--------------------------+
        | simple | :math:`\\frac{1}{2n}`     | :math:`\\frac{1}{n}`     |
        +--------+---------------------------+--------------------------+
        | edge   | :math:`0`                 | :math:`\\frac{1}{n-1}`   |
        +--------+---------------------------+--------------------------+

        For example for :math:`n = 3` this gives the following:

        .. code::
           thick    ===========================
           edge     |------------|------------|
           simple   ----|--------|--------|----
           teapot   ---|---------|---------|---
                     ^       ^             ^
                   delta   Delta         slice

        For details about the TEAPOT algorithm see [1]_.

        .. [1] H. Burkhardt, R. De Maria, M. Giovannozzi, and T. Risselada, "Improved TEAPOT Method and Tracking with
               Thick Quadrupoles for the LHC and its Upgrade", in Proc. IPAC'13, Shanghai, China, May 2013,
               paper MOPWO027, pp. 945-947.
        """
        if n < 1:
            raise ValueError('Number of thin slices must be at least 1')
        if n == 1:
            delta = 0.5
            Delta = 0.
        else:
            try:
                delta, Delta = cls.makethin_deltas[style](n)
            except KeyError:
                raise ValueError(f'Invalid style: {style} (must be one of {set(cls.makethin_deltas)!r})')
        slices = [thick_cls(l=l*delta, label=f'{base_label}__d0')]
        for i in range(n - 1):
            slices.append(thin_cls(label=f'{base_label}__{i}'))
            slices.append(thick_cls(l=l * Delta, label=f'{base_label}__d{i + 1}'))
        slices.append(thin_cls(label=f'{base_label}__{n - 1}'))
        slices.append(thick_cls(l=l * delta, label=f'{base_label}__d{n}'))
        return slices


def setup_matching_criteria(criteria: SelectionCriteria, dtype, *, optional: bool = False, default: Any = None) \
        -> List[Tuple[SelectionKey, SelectionValue]]:
    """Create a common format for matching criteria from a variety of input options."""
    if criteria is None and optional:
        return [(None, default)]
    if isinstance(criteria, dtype):
        return [(None, criteria)]
    if isinstance(criteria, tuple):
        return [criteria]
    if isinstance(criteria, list):
        if optional:
            criteria = criteria + [(None, default)]  # If a default is already specified via None it will match first.
        return criteria
    if isinstance(criteria, dict):
        if optional:
            criteria.setdefault(None, default)
        return list(criteria.items())
    raise TypeError(f'Invalid type for criteria specification: {type(criteria)} (value: {criteria})')


def find_matching_criterion(element: Union[LatticeElement, AlignmentError],
                            criteria: List[Tuple[SelectionKey, SelectionValue]]) -> SelectionValue:
    """Match the given element to the selection keys in `criteria` and return the value corresponding to the first match.

    .. Note::
       ``None`` serves as a default kay and matches every element. For that reason it should appear at the end of the
       `criteria` list.

    Parameters
    ----------
    element : :class:`Element` or :class:`AlignmentError`
        The element for which the criterion is matched (and the corresponding value selected).
    criteria : list of (criterion, value)
        List containing the criteria to be considered as tuples together with the corresponding values.

    Returns
    -------
    value : Any
        The value corresponding to the first matching key.

    Raises
    ------
    KeyError
        If no criteria was met.
    """
    for criterion, value in criteria:
        if criterion is None or match_element(criterion, element):
            return value
    raise KeyError('No matching criterion was found')


# noinspection PyUnusedLocal
@singledispatch
def match_element(criterion: Any, element: Union[LatticeElement, AlignmentError]) -> NoReturn:
    raise TypeError(f'Illegal type for matching an element: {type(criterion)}')


# noinspection PyUnusedLocal
@match_element.register(type(None))
def _(criterion: type(None), element: LatticeElement) -> bool:
    return True


@match_element.register(str)
@match_element.register(re.Pattern)
def _(criterion: LabelSelector, element: LatticeElement) -> bool:
    if isinstance(criterion, str):
        if '*' in criterion:
            criterion = re.compile('^' + re.escape(criterion).replace('\\*', '.*?') + '$')
        else:
            return element.label == criterion
    return isinstance(element.label, str) and re.match(criterion, element.label)


@match_element.register(type)
def _(criterion: Type[LatticeElement], element: LatticeElement) -> bool:
    return (isinstance(element, criterion)
            or isinstance(element, AlignmentError) and any(isinstance(x, criterion) for x in element.unwrap()))


@match_element.register(Element)
@match_element.register(AlignmentError)
def _(criterion: LatticeElement, element: LatticeElement) -> bool:
    return element is criterion


del _


def _contract_transfer_maps(x: TransferMap, y: TransferMap, *,
                            order: Literal[1, 2] = 2, symplectify: bool = True,
                            index: Literal[0, 1, 2] = 2) -> TransferMap:
    """Contract the given transfer maps into a new transfer map."""
    d = y[0] + y[1] @ x[0]
    if index >= 1:
        y = _update_transfer_matrix_reference(x, y, order=order, symplectify=symplectify)
        R = y[1] @ x[1]
    else:
        R = None
    T = None
    if order >= 2:
        d = d + torch.einsum('ijk,jl,kl->il', y[2], x[0], x[0])
        if index >= 2:
            T = torch.einsum('il,ljk->ijk', y[1], x[2]) + torch.einsum('ilm,lj,mk->ijk', y[2], x[1], x[1])
    return d, R, T


def _update_transfer_matrix_reference(x: TransferMap, y: TransferMap, *,
                                      order: Literal[1, 2] = 2, symplectify: bool = True) -> TransferMap:
    """Change the reference of the `y` transfer matrix taking into account the closed orbit value provided by `x`."""
    d, R, T = y
    if order >= 2:
        R = R + 2 * torch.einsum('ikl,l->ik', y[2], x[0].squeeze())
        if symplectify:
            R = Utilities.symplectify(R)
    return d, R, T


class Utilities:
    S2 = np.array([[ 0, 1],
                   [-1, 0]], dtype=float)
    S = scipy.linalg.block_diag(S2, S2, S2)

    I = torch.eye(6)
    S2 = torch.from_numpy(S2)
    S = torch.from_numpy(S)

    @classmethod
    def symplectify(cls, R: Tensor) -> Tensor:
        """Symplectify the given matrix.

        Notes
        -----
        For details see [1]_.

        [1] Liam Healy, Lie Algebraic Methods for Treating Lattice Parameter Errors in Particle Accelerators,
            University of Maryland, PhD Thesis, 1986 (chapter 5 "Symplectification of Matrices").
        """
        I, S = cls.I, cls.S
        V = (I - R) @ torch.inverse(I + R)  # Skip the multiplication with S here, this is incorporated into SW (next line).
        SW = 0.5 * (S @ torch.t(V) @ S + V)  # Inverse sign here (also inverted on the next line).
        return (I - SW) @ torch.inverse(I + SW)


def configure(*, transfer_map_order: Optional[Literal[1, 2]] = None) -> None:
    """Configure element classes globally.

    Parameters
    ----------
    transfer_map_order : int
        Set the order of truncation for transfer map coefficients (see :class:`Element`).
    """
    if transfer_map_order is not None:
        Element.transfer_map_order = transfer_map_order
        CompoundElement.transfer_map_order = transfer_map_order


aperture_types = {  # type: Dict[str, Aperture]
    k.lower().replace('aperture', '', 1): v for k, v in sorted(globals().items())
    if inspect.isclass(v) and issubclass(v, Aperture) and v is not Aperture
}
elements = {  # type: Dict[str, Element]
    k.lower(): v for k, v in sorted(globals().items())
    if inspect.isclass(v) and issubclass(v, (Element, CompoundElement)) and v is not Element and v is not CompoundElement
       and not k.startswith('Thin')
}
alignment_errors = {  # type: Dict[str, AlignmentError]
    k: v for v in (t[1] for t in sorted(globals().items()))
    if inspect.isclass(v) and issubclass(v, AlignmentError) and v is not AlignmentError
    for k in v.triggers
}
