from typing import Dict
from .systems import System, TF


class BasicSystem(System):
    def __init__(self, g: TF, k: TF = 1, h: TF = 1):
        super().__init__(g, k, h, 0, 0)


class BasicExperiment:
    def __init__(self, system: BasicSystem):
        self.system = system

    def render_step(self) -> Dict:
        t, y = self.system.step()
        return {
            "data": [
                {"x": t, "y": y, "type": "line"}
            ],
            "layout": {
                "title": "Step Response of System"
            }
        }

    def render_bode(self) -> Dict:
        mag, phase, omega = self.system.bode_close()
        return {
            "data": [
                {"x": omega, "y": mag, "type": "line", "name": "Magnitude"},
                {"x": omega, "y": phase, "type": "line", "name": "Phase"}
            ],
            "layout": {
                "xaxis": {"type": "log", "title": "Frequency"},
                # "yaxis": {"domain": [0, 0.5]},
                # "yaxis2": {"domain": [0.5, 1]},
                # "grid": {"rows": 2, "columns": 1, "pattern": 'independent'},
                "title": "Bode Plot"
            }
        }