from sage.all import cached_function, PermutationGroup, Partitions, prod
from admcycles import psiclass, lambdaclass, list_strata

# ASV forks before running a benchmark so all caches are empty when a benchmark
# function is first run. However, asv does not fork between repetitions of a
# benchmark so make sure to always run asv with --quick. We could fix this by
# decorating each benchmark or suite such that it forks again; wouldn't be hard
# if we believe that this makes sense.
@cached_function
def nothing_is_cached():
    return None

def to_exp_dict(p):
    d = {}
    for i in p:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    return d

class NoProduct:
    r"""
    When a list of .params starts with this entry, not all combinations of the
    entries are processed but each entry is understood as a list of parameters.
    """
    def __init__(self, names):
        self._names = names

    def __repr__(self):
        return self._names

class Benchmark:
    r"""
    Base class for benchmarks that understand the NoProduct marker defined above.
    """
    def setup(self, *args):
        if args and isinstance(args[0], NoProduct):
            raise NotImplementedError("this marker input will be ignored by ASV because we are throwing a NotImplementedError in setup()")

class StrataGeneration(Benchmark):
    def time_list_strata(self, gn):
        g, n = gn
        list_strata(g, n, 3*g-3+n)

    time_list_strata.params = [NoProduct('g, n'), (0, 7), (1, 5), (2, 3), (3, 2), (4, 0)] # (2, 4) times out

class Evaluation(Benchmark):
    def time_psi_classes(self, gn):
        g, n = gn
        for p in Partitions(3*g-3+n, max_length=n):
            prod(psiclass(i+1, g, n)**j for i,j in enumerate(p)).evaluate()

    time_psi_classes.params = [NoProduct('g, n'), (0, 33), (1, 18), (2, 16), (6, 10), (9, 7), (13, 5), (20, 4)]

class AlgebraInTautologicalRing(Benchmark):
    def time_lambda_and_psi_product1(self):
        # from https://gitlab.com/jo314schmitt/admcycles/issues/28
        lambdaclass(3,3,3) * psiclass(1,3,3)**2 * psiclass(2,3,3)**2 * psiclass(3,3,3)**2

    def time_lambda_power(self, dgnp):
        d, g, n, p = dgnp
        lambdaclass(d,g,n)**p

    time_lambda_power.params = [NoProduct('d, g, p, n'), (1, 3, 2, 3), (2, 4, 0, 2)]
