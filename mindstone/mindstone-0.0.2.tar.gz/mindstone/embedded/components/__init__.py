""" components sub-package

"""

from mindstone.embedded.components.led import LEDComponent
from mindstone.embedded.components.servo import ServoComponent
from mindstone.embedded.components.ultrasonic import UltrasonicSensorComponent

COMPONENT_REGISTER = {
    "servo": ServoComponent,
    "led": LEDComponent,
    "ultrasonic": UltrasonicSensorComponent
}
