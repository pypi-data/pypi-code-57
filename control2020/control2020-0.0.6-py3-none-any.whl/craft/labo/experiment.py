from .systems import System, TF


class BasicSystem(System):
    def __init__(self, g: TF, k: TF = 1, h: TF = 1):
        super().__init__(g, k, h, 0, 0)


class BasicExperiment:
    def __init__(self, system: BasicSystem):
        self.system = system

