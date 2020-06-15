""" component data module.

"""

component_data = {
    "ServoComponent": {
        "SG90": {
            "weight": 14.7,
            "torque": 2.5,
            "speed": 0.3,
            "rotation": [0, 180],
            "pwm_frequency": 50,
            "start_on_time": 0.0005,
            "end_on_time": 0.0024
        },
        "Corona939MG": {
            "weight": 12.5,
            "torque": 2.5,
            "speed": 0.42,
            "rotation": [0, 180],
            "pwm_frequency": 400,
            "start_on_time": 0.0005,
            "end_on_time": 0.0024
        }
    },

    "UltrasonicComponent": {
        "HCSR04": {
            "accuracy": 3,
            "range": [0.02, 4],
            "trigger_pw": 0.00001
        }
    }
}
