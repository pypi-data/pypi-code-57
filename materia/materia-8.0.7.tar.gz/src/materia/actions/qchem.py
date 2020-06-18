from .core import Modify

__all__ = [
    "QChemModifyRSHParameter",
    "QChemIncreaseResponseIterations",
    "QChemIncreaseSCFIterations",
]


class QChemIncreaseResponseIterations(Modify):
    def __init__(self, increase_factor):
        self.increase_factor = increase_factor

    def modify(self, task):
        try:
            task.settings["response", "maxiter"] *= self.increase_factor
        except KeyError:
            task.settings["response", "maxiter"] = (
                60 * self.increase_factor
            )  # FIXME: 60 is the default value in QChem v5.2.1 - can this be changed to be version-independent?

        return task


class QChemIncreaseSCFIterations(Modify):
    def __init__(self, increase_factor):
        self.increase_factor = increase_factor

    def modify(self, task):
        try:
            task.settings["rem", "max_scf_cycles"] *= self.increase_factor
        except KeyError:
            task.settings["rem", "max_scf_cycles"] = (
                50 * self.increase_factor
            )  # FIXME: 50 is the default value in QChem v5.2.1 - can this be changed to be version-independent?

        return task


class QChemModifyRSHParameter(Modify):
    def __init__(self, omega):
        self.omega = omega

    def modify(self, task):
        task.settings["rem", "omega"] = self.omega
        task.settings["rem", "omega2"] = self.omega

        return task
