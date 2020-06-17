"""A scene test generator"""
from copy import deepcopy
from functools import partial
from typing import cast, Any, Tuple, List, Dict, Generator
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image  # type: ignore

from scenegen.scene import Scene


@dataclass
class TestScene:
    """A test scene generator implementation"""

    scene: str = field(default="default")
    width: int = field(default=512)
    height: int = field(default=512)
    length: int = field(default=512)
    output: Path = field(default=Path("/dev/null"))
    _scene: Scene = field(default=Scene(width=512, height=512), repr=False)

    def __post_init__(self) -> None:
        """Set up the scene"""
        self._scene.description = self.scene_description(self.scene)
        self._scene.width = self.width
        self._scene.height = self.height

    def frames(self) -> Generator[Tuple[bytes, List[Tuple[int, int, int, int]]], None, None]:
        """The frames"""
        for (rawframe, boundingboxes) in self._scene.play(end=self.length):
            yield (rawframe, boundingboxes)

    def save(self) -> None:
        """Generate a test scene"""
        for index, (rawframe, _) in enumerate(self.frames()):
            image = Image.frombytes("RGB", (self._scene.width, self._scene.height), rawframe,)
            image.save(self.output / f"{index:010}.png")

    def scene_description(self, scene_name: str) -> Dict[str, Any]:
        """A specific test scene"""
        return cast(Dict[str, Any], TestScene.scene_descriptions()[scene_name](width=self.width, height=self.height))

    @staticmethod
    def scene_descriptions() -> Dict[str, Any]:
        """The test scenes"""

        def scene_default(width: int, height: int) -> Dict[str, Any]:
            """The default"""

            def update_color_rectangle(clock: int = 0) -> Tuple[int, int, int]:
                """The rectangle color update function"""
                return (clock % 256, clock % 256, clock % 256)

            return {
                "box": {
                    "zindex": 1,
                    "shape": "rectangle",
                    "center": (width * 0.5, height * 0.5),
                    "size": (width * 0.5, height * 0.5),
                    "color": update_color_rectangle,
                },
            }

        def scene_boxes(width: int, height: int) -> Dict[str, Any]:
            """A scene with moving boxes"""
            boxsize = int(min(width, height) * 0.1)
            margin = boxsize * 2
            corners: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]] = (
                (margin, margin),
                (width - margin, margin),
                (width - margin, height - margin),
                (margin, height - margin),
            )
            travel = int(min(width, height) * 0.0125)
            direction: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]] = (
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
            )
            boxes: List[Dict[str, Any]] = [
                {"position": list(corners[0]), "direction": 0},
                {"position": list(corners[1]), "direction": 1},
                {"position": list(corners[2]), "direction": 2},
                {"position": list(corners[3]), "direction": 3},
            ]

            def update_position(clock: int = 0, boxid: int = 0) -> Tuple[int, int]:  # pylint: disable=W0613
                """Update a box's position"""
                box = deepcopy(boxes[boxid])

                boxes[boxid]["position"][0] += travel * direction[boxes[boxid]["direction"]][0]
                boxes[boxid]["position"][1] += travel * direction[boxes[boxid]["direction"]][1]

                if boxes[boxid]["direction"] == 0 and boxes[boxid]["position"][0] >= corners[1][0]:
                    boxes[boxid]["direction"] = 1
                elif boxes[boxid]["direction"] == 1 and boxes[boxid]["position"][1] >= corners[2][1]:
                    boxes[boxid]["direction"] = 2
                elif boxes[boxid]["direction"] == 2 and boxes[boxid]["position"][0] <= corners[3][0]:
                    boxes[boxid]["direction"] = 3
                elif boxes[boxid]["direction"] == 3 and boxes[boxid]["position"][1] <= corners[0][1]:
                    boxes[boxid]["direction"] = 0

                return cast(Tuple[int, int], box["position"])

            return {
                "background": {
                    "zindex": 0,
                    "shape": "rectangle",
                    "size": (width, height),
                    "color": (255, 255, 255),
                    "center": (width * 0.5, height * 0.5),
                },
                "boxes": {
                    f"box-{_id}": {
                        "zindex": 1,
                        "shape": "rectangle",
                        "size": (boxsize, boxsize),
                        "color": (0, 0, 0),
                        "center": partial(update_position, boxid=_id),
                    }
                    for _id in range(4)
                },
            }

        def scene_balls(width: int, height: int) -> Dict[str, Any]:
            """A scene with moving, colored balls"""

            ballsize: int = int(min(width, height) * 0.4)
            frames_per_ball: int = 64
            startpos: Tuple[int, int] = (int(width * 0.25), int(height / 2))
            endpos: Tuple[int, int] = (int(width * 0.75), int(height / 2))
            stepping: Tuple[int, int] = (
                int((endpos[0] - startpos[0]) / frames_per_ball),
                int((endpos[1] - startpos[1]) / frames_per_ball),
            )

            balls: Dict[str, Dict[str, Any]] = {
                "red": {
                    "start": frames_per_ball,
                    "end": frames_per_ball * 2,
                    "position": list(startpos),
                    "color": (255, 0, 0),
                },
                "green": {
                    "start": frames_per_ball * 2,
                    "end": frames_per_ball * 3,
                    "position": list(startpos),
                    "color": (0, 255, 0),
                },
                "blue": {
                    "start": frames_per_ball * 3,
                    "end": frames_per_ball * 4,
                    "position": list(startpos),
                    "color": (0, 0, 255),
                },
            }

            def ball(clock: int = 0) -> Dict[str, Any]:
                """Generate a ball"""
                _balls = {}
                for _ball in balls:
                    if clock < balls[_ball]["start"] or clock >= balls[_ball]["end"]:
                        continue
                    _balls[_ball] = {
                        "zindex": 2,
                        "shape": "circle",
                        "size": (ballsize, ballsize),
                        "color": balls[_ball]["color"],
                        "center": balls[_ball]["position"],
                    }
                    balls[_ball]["position"][0] += stepping[0]
                    balls[_ball]["position"][1] += stepping[1]

                return _balls

            return {
                "background": {
                    "zindex": 0,
                    "shape": "rectangle",
                    "size": (width, height),
                    "color": (64, 64, 64),
                    "center": (width * 0.5, height * 0.5),
                },
                "checkers": {
                    "zindex": 1,
                    "shape": "checkers",
                    "size": (width, height),
                    "color": (192, 192, 192),
                    "center": (width * 0.5, height * 0.5),
                },
                "ball": ball,
            }

        return {
            "default": scene_default,
            "boxes": scene_boxes,
            "balls": scene_balls,
        }
