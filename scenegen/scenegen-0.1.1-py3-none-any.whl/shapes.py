"""Primitive shapes"""

from dataclasses import dataclass, field
from typing import Tuple

from PIL import Image, ImageDraw  # type: ignore


@dataclass
class Shape:
    """A base shape"""

    shape: str = field(default="rectangle")
    center: Tuple[int, int] = field(default=(0, 0))
    size: Tuple[int, int] = field(default=(0, 0))
    color: Tuple[int, int, int] = field(default=(0, 0, 0))
    _half_size: Tuple[int, int] = field(default=(0, 0))

    def __post_init__(self) -> None:
        """Compute values depending on input"""
        self._half_size = (int(self.size[0] / 2), int(self.size[1] / 2))

    def draw(self, image: Image) -> Tuple[int, int, int, int]:
        """Draw shape on image"""
        raise NotImplementedError


@dataclass
class Rectangle(Shape):  # pylint: disable=R0903
    """A rectangular shape"""

    def draw(self, image: Image) -> Tuple[int, int, int, int]:
        """Draw a rectangle on an image"""
        rect_xy = (
            self.center[0] - self._half_size[0],
            self.center[1] - self._half_size[1],
            self.center[0] + self._half_size[0] - 1,
            self.center[1] + self._half_size[1] - 1,
        )
        draw = ImageDraw.Draw(image)
        draw.rectangle(xy=rect_xy, fill=self.color)
        return rect_xy


@dataclass
class Checkers(Shape):  # pylint: disable=R0903
    """A checkers pattern"""

    spacing: int = field(default=32)

    def draw(self, image: Image) -> Tuple[int, int, int, int]:
        """Draw a checkers pattern on an image"""
        is_on: bool = False
        for _y in range(0, self.size[1], self.spacing):
            for _x in range(0, self.size[0], self.spacing):
                is_on ^= True
                if not is_on:
                    continue
                rectangle = Rectangle(
                    center=(_x + int(self.spacing / 2), _y + int(self.spacing / 2)),
                    size=(self.spacing, self.spacing),
                    color=self.color,
                )
                rectangle.draw(image)
            is_on ^= True

        return (
            self.center[0] - self._half_size[0],
            self.center[1] - self._half_size[1],
            self.center[0] + self._half_size[0] - 1,
            self.center[1] + self._half_size[1] - 1,
        )


@dataclass
class Circle(Shape):  # pylint: disable=R0903
    """A circular shape"""

    def draw(self, image: Image) -> Tuple[int, int, int, int]:
        """Draw a circle on an image"""
        circ_xy = (
            self.center[0] - self._half_size[0],
            self.center[1] - self._half_size[1],
            self.center[0] + self._half_size[0] - 1,
            self.center[1] + self._half_size[1] - 1,
        )
        draw = ImageDraw.Draw(image)
        draw.ellipse(xy=circ_xy, fill=self.color)
        return circ_xy


SHAPES = {
    "rectangle": Rectangle,
    "checkers": Checkers,
    "circle": Circle,
}
