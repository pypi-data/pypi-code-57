from base_normalisation_unit import NormaliserTester

from netcdf_scm.normalisation import NormaliserRunningMeanDedrift


class TestRunningMean(NormaliserTester):
    tclass = NormaliserRunningMeanDedrift

    def test_method_name(self):
        assert self.tclass().method_name == "21-yr-running-mean-dedrift"
