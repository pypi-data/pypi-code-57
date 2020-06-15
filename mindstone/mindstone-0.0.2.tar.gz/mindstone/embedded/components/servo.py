""" servo component module.

"""

from mindstone.embedded.channels.pwm import PWMChannelABC
from mindstone.embedded.components.component import ComponentABC
from mindstone.embedded.components.mutable import MutableComponentABC
from mindstone.embedded.components.observable import ObservableComponentABC


class ServoComponent(ComponentABC, MutableComponentABC, ObservableComponentABC):
    """ servo component class.

    """

    def __init__(self, model: str, trigger: int):
        super().__init__(model)

        self.is_active = False
        self.angle = None

        self.new_channel("trigger", trigger, "pwm", frequency=self.properties["pwm_frequency"])

    def update(self, angle: float = None, is_active: bool = None):
        if is_active is not None:
            if is_active != self.is_active:
                if is_active:
                    self.start()
                else:
                    self.stop()
        if angle is not None:
            if self.is_active:
                self.change_angle(float(angle))
            else:
                raise NotImplementedError("Could not set angle. Servo can't be used without first being activated.")

    def observe(self) -> dict:
        return {
            "angle": self.angle,
            "is_active": self.is_active
        }

    def change_angle(self, angle):
        lower_bound, upper_bound = tuple(self.properties["rotation"])
        if not lower_bound <= angle <= upper_bound:
            raise ValueError("Servo angle should be between {} and {}".format(lower_bound, upper_bound))
        self.angle = angle
        channel = self.channels["trigger"]
        assert isinstance(channel, PWMChannelABC)
        channel.change_duty_cycle(self._angle_to_duty_cycle(angle))

    def start(self, angle: float = 90):
        dc = self._angle_to_duty_cycle(angle)
        channel = self.channels["trigger"]
        assert isinstance(channel, PWMChannelABC)
        channel.start(dc)
        self.is_active = True

    def stop(self):
        channel = self.channels["trigger"]
        assert isinstance(channel, PWMChannelABC)
        channel.stop()
        self.is_active = False

    def _angle_to_duty_cycle(self, angle: float) -> float:
        start_on_time = self.properties["start_on_time"]
        end_on_time = self.properties["end_on_time"]
        pwm_frequency = self.properties["pwm_frequency"]
        rotation = self.properties["rotation"]
        start_dc = start_on_time * pwm_frequency * 100
        end_dc = end_on_time * pwm_frequency * 100
        difference = end_dc - start_dc
        return round(start_dc + difference * angle / rotation[1], 1)
