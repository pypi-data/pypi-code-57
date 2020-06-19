#
# MIT License
#
# Copyright (c) 2020 Keisuke Sehara
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from collections import namedtuple as _namedtuple
import math as _math
from scipy.optimize import least_squares as _least_squares
import numpy as _np

VERSION_STR = "1.0.0a5"

class FittingMixin:
    """a mix-in class for enabling fitting.

    - the object for the class must be initialized from a set of parameters
    (e.g. as a named tuple).
    - the class must have the following methods:
        - `bounds(**kwargs)`
        - `init(xp, yp, **kwargs)`
        - `deviation(x, xp, yp, **kwargs)`
    """
    @classmethod
    def fit(cls, xp, yp, **kwargs):
        """performs fitting from a set of x- and y-coordinates, xp and yp."""
        if "max_nfev" in kwargs.keys():
            nfev = kwargs.pop("max_nfev")
        else:
            nfev = None
        opt = _least_squares(cls.deviation, x0=cls.init(xp, yp, **kwargs), args=(xp, yp),
                             kwargs=kwargs, bounds=cls.bounds(**kwargs), max_nfev=nfev)
        if opt["success"] == False:
            msg = opt["message"]
            raise RuntimeError(f"fitting of {cls.__name__} failed ({msg})")
        return cls(*opt["x"])

    @classmethod
    def bounds(cls, **kwargs):
        return (0, _np.inf)

    @classmethod
    def init(cls, xp, yp, **kwargs):
        raise NotImplementedError(f"{cls.__name__}.init()")

    @classmethod
    def deviation(cls, x, xp, yp, **kwargs):
        return cls(*x).transform(xp) - yp

class Parabola(_namedtuple("_Parabola", ("xf", "yf", "phi", "L")),
                    FittingMixin):
    """a 2D parabola model.

    from xp and yp: `model = Parabola2D.fit(xp, yp)`
    """

    @classmethod
    def init(cls, xp, yp, **kwargs):
        init_phi = kwargs.get("init_phi", _math.pi/2)
        return (_np.nanmean(xp), _np.nanmean(yp), init_phi, 1.0)

    @classmethod
    def bounds(cls, **kwargs):
        xrng = kwargs.get("xrange", (-_np.inf, _np.inf))
        yrng = kwargs.get("yrange", (-_np.inf, _np.inf))
        return ((xrng[0], yrng[0], -_np.inf, 0),
                (xrng[1], yrng[1], _np.inf, _np.inf)) # (lower, upper)

    @classmethod
    def deviation(cls, x, xp, yp, **kwargs):
        parabola = cls(*x)
        p = _np.stack([xp,yp],axis=0)
        f = parabola.focus.reshape((2,1))
        u = parabola.axis.reshape((2,1))
        r = p - f
        return _np.linalg.norm(r, axis=0) - (r * u).sum(axis=0) - parabola.L

    @property
    def focus(self):
        """returns the coordinates of the focus."""
        return _np.array([self.xf, self.yf])

    @property
    def axis(self):
        """returns a unit vector along the axis of symmetry."""
        return _np.array([_math.cos(self.phi), _math.sin(self.phi)])

    @property
    def rotation(self):
        """returns the rotation matrix for obtaining the rotation of this parabola
        from the "normal" parabola."""
        c, s = _math.cos(self.phi), _math.sin(self.phi)
        return _np.array([[s,c], [-c,s]])

    def draw(self, t):
        """`t` must be the coordinate parameter that is used as the x-coordinate
        to draw the "normal" parabola."""
        # draw the "normal" parabola
        xp = t
        yp = (1/(2*self.L)) * (t**2) - self.L/2
        p  = _np.stack([xp,yp],axis=0)
        f  = self.focus.reshape((2,1))
        # translate/rotate to what it should be
        # [0,:] and [1,:] should contain the x- and y- coordinates
        return _np.matmul(self.rotation, p) + f

class Circle(_namedtuple("_Circle", ("xc", "yc", "radius")),
             FittingMixin):
    @classmethod
    def init(cls, xp, yp, **kwargs):
        xc = xp.mean()
        yc = yp.mean()
        r  = _np.sqrt((xp - xc)**2 + (yp - yc)**2).mean()
        return (xc, yc, r)

    @classmethod
    def bounds(cls, **kwargs):
        return ((-_np.inf, -_np.inf, 0.0),
                (_np.inf, _np.inf, _np.inf))

    @classmethod
    def deviation(cls, x, xp, yp, **kwargs):
        circle = cls(*x)
        return (xp - circle.xc)**2 + (yp - circle.yc)**2 - circle.radius**2

    def compute_radius(self, xp, yp):
        return _np.sqrt((xp - self.xc)**2 + (yp - self.yc)**2)

    def compute_angles(self, xp, yp):
        return _np.arctan2(yp - self.yc, xp - self.xc)

    @property
    def center(self):
        return _np.array([self.xc, self.yc])

    def draw(self, angles):
        """angles in radians"""
        return _np.stack([_np.cos(angles), _np.sin(angles)],
                         axis=0) * self.radius + self.center.reshape((2,1))

class Ellipse(_namedtuple("_Ellipse", ("xc", "yc", "A", "B", "phi")),
                    FittingMixin):
    EPSILON = _np.array([[1e-3, 0],[0, 1e-3]]) # to avoid singularity of the matrix

    @classmethod
    def init(cls, xp, yp, **kwargs):
        xc    = xp.mean()
        yc    = yp.mean()
        xsize = xp.max() - xp.min()
        ysize = yp.max() - yp.min()
        if xsize >= ysize:
            phi = 0.0
        else:
            phi = _math.pi / 2
        return (xc, yc, 1.0, 1.0, phi)

    @classmethod
    def bounds(cls, **kwargs):
        return ((-_np.inf, -_np.inf, 0, 0, -_np.inf),
                (_np.inf, _np.inf, _np.inf, _np.inf, _np.inf)) # (lower, upper)

    @classmethod
    def deviation(cls, x, xp, yp, **kwargs):
        return (_np.linalg.norm(cls(*x).transform(xp, yp), axis=0) - 1)**2

    @property
    def center(self):
        return _np.array([self.xc, self.yc])

    @property
    def matrix(self):
        """returns a matrix M^{-1}, consisting of the
        semi-major and -minor axis vectors."""
        c, s = _math.cos(self.phi), _math.sin(self.phi)
        return _np.array([[self.A * c, -self.B * s],
                         [self.A * s, self.B * c]])

    @property
    def transformation(self):
        """returns a matrix that is used to 'standardize'
        the x- and y-coordinates, into a set of circular coordinates."""
        M = self.matrix
        try:
            return _np.linalg.inv(M)
        except _np.linalg.LinAlgError:
            return _np.linalg.inv(M + self.EPSILON)

    def transform(self, xp, yp):
        """returns a set of circular-standardized coordinates."""
        if _np.ndim(xp) == 0:
            xp = (xp,)
            yp = (yp,)
        p = _np.stack([xp, yp], axis=0)
        c = self.center.reshape((2,1))
        return _np.matmul(self.transformation, p-c)

    def compute_phases(self, xp, yp):
        """compute angular parameters for given (xp, yp)"""
        transformed = self.transform(xp, yp)
        out = _np.arctan2(transformed[1], transformed[0])
        if _np.ndim(xp) == 0:
            return out[0]
        else:
            return out

    def draw(self, angles):
        u = _np.stack([_np.cos(angles), _np.sin(angles)], axis=0)
        return _np.matmul(self.matrix, u) + self.center.reshape((2,1))
