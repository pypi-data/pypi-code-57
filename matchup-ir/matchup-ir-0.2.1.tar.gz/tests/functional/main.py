import unittest

from tests.functional import boolean_test, extended_boolean_test, probabilistic_test, vector_test,\
    generalized_vector_test, belief_network_test


def create_suite(t_lst, t_load):
    t_lst.append(t_load.loadTestsFromTestCase(boolean_test.BooleanTest))
    t_lst.append(t_load.loadTestsFromTestCase(extended_boolean_test.ExtendedBooleanTest))
    t_lst.append(t_load.loadTestsFromTestCase(probabilistic_test.ProbabilisticTest))
    t_lst.append(t_load.loadTestsFromTestCase(vector_test.VectorTest))
    t_lst.append(t_load.loadTestsFromTestCase(generalized_vector_test.GeneralizedVectorTest))
    t_lst.append(t_load.loadTestsFromTestCase(belief_network_test.BeliefNetworkTest))


test_list = []
test_loader = unittest.TestLoader()

# add test suites
create_suite(test_list, test_loader)

suite = unittest.TestSuite(test_list)
runner = unittest.TextTestRunner()
runner.run(suite)
