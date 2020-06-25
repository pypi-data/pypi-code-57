"""A Python package for using complex numbers as vectors."""
from __future__ import annotations

import math
import cmath


def convert_angle(angle, unit: str):
    """Convert an angle to radians."""
    unit = unit.lower()
    if unit in {"d", "deg", "degrees", "degree", "°"}:
        return angle * math.tau / 360
    if unit in {"r", "", None, "rad", "radian", "radians"}:
        return angle
    if unit in {
        "g",
        "grad",
        "gradians",
        "gradian",
        "gons",
        "gon",
        "grades",
        "grade",
    }:
        return angle * math.tau / 400
    if unit in {"mins", "min", "minutes", "minute", "'", "′"}:
        return angle * math.tau / 21600
    if unit in {"secs", "sec", "seconds", "seconds", '"', "″"}:
        return angle * math.tau / 1296000
    if unit in {"turn", "turns"}:
        return angle * math.tau
    raise ValueError(f"Invalid angle unit: '{unit}'")


def _object_to_xy(obj) -> tuple:
    """Convert an object to an (x, y) tuple."""
    # Deal with objects with x and y attributes
    try:
        x = obj.x
        y = obj.y
    except AttributeError:
        # Deal with iterables
        try:
            iterable = iter(obj)
            try:
                x = next(iterable)
                y = next(iterable)
            except StopIteration:
                raise ValueError("Iterable is too short to create Vector")
            try:
                next(iterable)
                raise ValueError("Iterable is too long to create Vector")
            except StopIteration:
                pass
        except TypeError:
            raise TypeError(
                "Single argument Vector must be Vector, complex, iterable or have x and y attributes"
            )
    return (x, y)


class Vector(complex):
    """A two-dimensional vector."""

    def __new__(cls, x=None, y=None, r=None, theta=None, angle_unit="rad"):
        if r is None and theta is None:
            if x is None:
                raise ValueError("Invalid arguments to create Vector")
            # Create Vector from x and y
            if y is not None:
                try:
                    return super().__new__(cls, x, y)
                except TypeError:
                    raise TypeError("x and y values must be numeric to create Vector")
            else:
                # Create Vector from a single argument using
                # the implementation complex provides
                try:
                    return super().__new__(cls, x)
                except TypeError:
                    # Create Vector from a single-argument using our
                    # implementation
                    x, y = *_object_to_xy(x)
                    try:
                        return super().__new__(cls, x, y)
                    except TypeError:
                        raise TypeError(
                            "x and y values must be numeric to create Vector"
                        )
        # Create Vector from polar arguments
        elif all((x is None, y is None, r is not None, theta is not None)):
            return super().__new__(cls, cmath.rect(r, convert_angle(theta, angle_unit)))

        raise ValueError("Invalid arguments to create Vector")

    def dot(self, other: Vector) -> float:
        """Return the dot product of self and other."""
        return self.x * other.x + self.y * other.y

    def perpdot(self, other: Vector) -> float:
        """
        Get the perpendicular dot product of self and other.

        This is the signed area of the parallelogram they define. It is
        also one of the 'cross products' that can be defined on 2d
        vectors.
        """
        return self.x * other.y - self.y * other.x

    def perp(self) -> Vector:
        """
        Get the vector, rotated anticlockwise by pi / 2.

        This is one of the 'cross products' that can be defined on 2d
        vectors. Use -Vector.perp() for a clockwise rotation.
        """
        return Vector(-self.y, self.x)

    def rotate(self, angle, unit="rad") -> Vector:
        """
        Return a self, rotated by angle anticlockwise.

        Use negative angles for a clockwise rotation.
        """
        angle = convert_angle(angle, unit)
        return Vector(r=self.r, theta=self.theta + angle)

    def rec(self) -> tuple:
        """Get the vector as (x, y)."""
        return (self.x, self.y)

    def pol(self) -> tuple:
        """Get the vector as (r, theta)."""
        return cmath.polar(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x} {self.y})"

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if isinstance(key, int):
            if key in {0, -2}:
                return self.x
            if key in {1, -1}:
                return self.y
            raise IndexError("Vector index out of range")

        if isinstance(key, slice):
            return self.rec()[key]

        raise TypeError(
            f"Vector indices must be integers or slices, not {key.__class__.__name__}"
        )

    def __iter__(self):
        yield self.x
        yield self.y

    def __reversed__(self):
        yield self.y
        yield self.x

    def __round__(self, ndigits=0) -> tuple:
        return (round(self.x, ndigits), round(self.y, ndigits))

    @property
    def x(self) -> float:
        """Return the horizontal component of the vector."""
        return self.real

    @property
    def y(self) -> float:
        """Return the vertical component of the vector."""
        return self.imag

    @property
    def r(self) -> float:
        """Return the radius of the vector."""
        return abs(self)

    @property
    def theta(self) -> float:
        """
        Return the angle of the vector, anticlockwise from the horizontal.

        Negative values are clockwise. Returns values in the range
        [-pi, pi]. See documentation of cmath.phase for details.
        """
        return cmath.phase(self)
