"""A scene"""
# pylint: disable=C0330
from dataclasses import dataclass, field
from typing import cast, Any, Tuple, List, Dict, Generator

from PIL import Image  # type: ignore

from scenegen.walk import walk
from scenegen.shapes import SHAPES, Rectangle  # pylint: disable=W0611


@dataclass
class Scene:
    """A Scene"""

    width: int = field(default=1024)
    height: int = field(default=768)
    description: Any = field(default_factory=dict)
    _layers: Dict[int, Any] = field(default_factory=dict)

    def play(
        self, beginning: int = 0, end: int = 0
    ) -> Generator[Tuple[bytes, List[Tuple[int, int, int, int]]], None, None]:
        """Play scene for each clock step"""
        clock: int = beginning
        for clock in range(beginning, end, 1):
            yield self.render(clock)

    def flatten(self, description: Dict[str, Any]) -> None:
        """Flatten a scene description to layers by zindex"""

        def walk_shapes(tree: Dict[str, Any]) -> None:
            """Walk through the scene description"""
            if "shape" in tree:
                # this looks like a shape, add it to a layer
                zindex = tree.pop("zindex", 0)
                if not zindex in self._layers:
                    self._layers[zindex] = []
                self._layers[zindex].append(tree)
            else:
                for value in tree.values():
                    if isinstance(value, dict):
                        walk_shapes(value)

        walk_shapes(description)

    def render(self, clock: int) -> Tuple[bytes, List[Tuple[int, int, int, int]]]:
        """Render scene for a clock step"""
        image: Image = Image.new("RGB", (self.width, self.height))
        self._layers = dict()
        description: Dict[str, Any] = walk(clock, self.description)
        self.flatten(description)
        boundingboxes: List[Tuple[int, int, int, int]] = []

        for layer in sorted(self._layers):
            for element in self._layers[layer]:
                shape = SHAPES[element.pop("shape")](**element)
                _boundingboxes = shape.draw(image)
                if not (
                    _boundingboxes[0] == 0
                    and _boundingboxes[1] == 0
                    and _boundingboxes[2] == self.width - 1
                    and _boundingboxes[3] == self.height - 1
                ):
                    # an element doesn't span the whole image, record its bounding box
                    boundingboxes.append(_boundingboxes)

        return (cast(bytes, image.tobytes()), boundingboxes)
