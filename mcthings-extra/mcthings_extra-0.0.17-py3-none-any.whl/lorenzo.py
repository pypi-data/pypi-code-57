# Licensed under the terms of http://www.apache.org/licenses/LICENSE-2.0
# Author/s (©): Familia de Lorenzo

from mcpi import block
from mcpi.vec3 import Vec3
from mcthings.scene import Scene
from mcthings.thing import Thing


class Stairs(Thing):

    def build(self):
        mc = Scene.server



        self._end_position = Vec3(end_x, self.position.y, self.position.z)