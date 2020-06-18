from .sandbox_check import SandboxCheck


class SandboxLivenessCheck(SandboxCheck):
    def __init__(self, result, liveness_type):
        SandboxCheck.__init__(self, result)
        self.__liveness_type = liveness_type

    @property
    def liveness_type(self):
        return self.__liveness_type

    def to_json(self):
        parent = SandboxCheck.to_json(self)
        parent["liveness_type"] = self.liveness_type
        return parent
