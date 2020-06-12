import pystencils as ps
import sympy as sp
from pystencils.fd.derivation import FiniteDifferenceStaggeredStencilDerivation as FDS, \
    FiniteDifferenceStencilDerivation as FD
import itertools
from collections import defaultdict
from collections.abc import Iterable


class FVM1stOrder:
    """Finite-volume discretization

    Args:
        field: the field with the quantity to calculate, e.g. a concentration
        flux: a list of sympy expressions that specify the flux, one for each cartesian direction
        source: a list of sympy expressions that specify the source
    """
    def __init__(self, field: ps.field.Field, flux=0, source=0):
        def normalize(f, shape):
            shape = tuple(s for s in shape if s != 1)
            if not shape:
                shape = None

            if isinstance(f, sp.Array) or isinstance(f, Iterable) or isinstance(f, sp.Matrix):
                return sp.Array(f, shape)
            else:
                return sp.Array([f] * (sp.Mul(*shape) if shape else 1))

        self.c = field
        self.dim = self.c.spatial_dimensions
        self.j = normalize(flux, (self.dim, ) + self.c.index_shape)
        self.q = normalize(source, self.c.index_shape)

    def discrete_flux(self, flux_field: ps.field.Field):
        """Return a list of assignments for the discrete fluxes

        Args:
            flux_field: a staggered field to which the fluxes should be assigned
        """

        assert ps.FieldType.is_staggered(flux_field)

        def discretize(term, neighbor):
            if isinstance(term, sp.Matrix):
                nw = term.applyfunc(lambda t: discretize(t, neighbor))
                return nw
            elif isinstance(term, ps.field.Field.Access):
                avg = (term.get_shifted(*neighbor) + term) * sp.Rational(1, 2)
                return avg
            elif isinstance(term, ps.fd.Diff):
                direction1 = term.args[1]
                if isinstance(term.args[0], ps.Field.Access):  # first derivative
                    access = term.args[0]
                    direction = (direction1,)
                elif isinstance(term.args[0], ps.fd.Diff):  # nested derivative
                    if isinstance(term.args[0].args[0], ps.fd.Diff):  # third or higher derivative
                        raise ValueError("can only handle first and second derivatives")
                    elif not isinstance(term.args[0].args[0], ps.Field.Access):
                        raise ValueError("can only handle derivatives of field accesses")

                    access, direction2 = term.args[0].args[:2]
                    direction = (direction1, direction2)
                else:
                    raise NotImplementedError("can only deal with derivatives of field accesses, "
                                              "but not {}; expansion of derivatives probably failed"
                                              .format(type(term.args[0])))

                fds = FDS(neighbor, access.field.spatial_dimensions, direction)
                return fds.apply(access)

            if term.args:
                new_args = [discretize(a, neighbor) for a in term.args]
                return term.func(*new_args)
            else:
                return term

        fluxes = self.j.applyfunc(ps.fd.derivative.expand_diff_full)
        fluxes = [sp.Matrix(fluxes.tolist()[i]) if flux_field.index_dimensions > 1 else fluxes.tolist()[i] 
                  for i in range(self.dim)]

        discrete_fluxes = []
        for neighbor in flux_field.staggered_stencil:
            neighbor = ps.stencil.direction_string_to_offset(neighbor)
            directional_flux = fluxes[0] * int(neighbor[0])
            for i in range(1, self.dim):
                directional_flux += fluxes[i] * int(neighbor[i])
            discrete_flux = discretize(directional_flux, neighbor)
            discrete_fluxes.append(discrete_flux)

        if flux_field.index_dimensions > 1:
            return [ps.Assignment(lhs, rhs)
                    for i, d in enumerate(flux_field.staggered_stencil) if discrete_fluxes[i]
                    for lhs, rhs in zip(flux_field.staggered_vector_access(d), sp.simplify(discrete_fluxes[i]))]
        else:
            return [ps.Assignment(flux_field.staggered_access(d), sp.simplify(discrete_fluxes[i]))
                    for i, d in enumerate(flux_field.staggered_stencil)]

    def discrete_source(self):
        """Return a list of assignments for the discrete source term"""

        def discretize(term):
            if isinstance(term, ps.fd.Diff):
                direction1 = term.args[1]
                if isinstance(term.args[0], ps.Field.Access):  # first derivative
                    access = term.args[0]
                    direction = (direction1,)
                elif isinstance(term.args[0], ps.fd.Diff):  # nested derivative
                    if isinstance(term.args[0].args[0], ps.fd.Diff):  # third or higher derivative
                        raise ValueError("can only handle first and second derivatives")
                    elif not isinstance(term.args[0].args[0], ps.Field.Access):
                        raise ValueError("can only handle derivatives of field accesses")

                    access, direction2 = term.args[0].args[:2]
                    direction = (direction1, direction2)
                else:
                    raise NotImplementedError("can only deal with derivatives of field accesses, "
                                              "but not {}; expansion of derivatives probably failed"
                                              .format(type(term.args[0])))

                if self.dim == 2:
                    stencil = ["".join(a).replace(" ", "") for a in itertools.product("NS ", "EW ")
                               if "".join(a).strip()]
                else:
                    stencil = ["".join(a).replace(" ", "") for a in itertools.product("NS ", "EW ", "TB ")
                               if "".join(a).strip()]
                weights = None
                for stencil in [["N", "S", "E", "W", "T", "B"][:2 * self.dim], stencil]:
                    stencil = [tuple(ps.stencil.direction_string_to_offset(d, self.dim)) for d in stencil]

                    derivation = FD(direction, stencil).get_stencil()
                    if not derivation.accuracy:
                        continue
                    weights = derivation.weights

                    # if the weights are underdefined, we can choose the free symbols to find the sparsest stencil
                    free_weights = set(itertools.chain(*[w.free_symbols for w in weights]))
                    if len(free_weights) > 0:
                        zero_counts = defaultdict(list)
                        for values in itertools.product([-1, -sp.Rational(1, 2), 0, 1, sp.Rational(1, 2)],
                                                        repeat=len(free_weights)):
                            subs = {free_weight: value for free_weight, value in zip(free_weights, values)}
                            weights = [w.subs(subs) for w in derivation.weights]
                            if not all(a == 0 for a in weights):
                                zero_count = sum([1 for w in weights if w == 0])
                                zero_counts[zero_count].append(weights)
                        best = zero_counts[max(zero_counts.keys())]
                        if len(best) > 1:
                            raise NotImplementedError("more than one suitable set of weights found, "
                                                      "don't know how to proceed")
                        weights = best[0]
                    break
                if not weights:
                    raise Exception('the requested derivative cannot be performed with the available neighbors')
                assert weights

                if access._field.index_dimensions == 0:
                    return sum([access._field.__getitem__(point) * weight for point, weight in zip(stencil, weights)])
                else:
                    total = access.get_shifted(*stencil[0]).at_index(*access.index) * weights[0]
                    for point, weight in zip(stencil[1:], weights[1:]):
                        addl = access.get_shifted(*point).at_index(*access.index) * weight
                        total += addl
                    return total

            if term.args:
                new_args = [discretize(a) for a in term.args]
                return term.func(*new_args)
            else:
                return term

        source = self.q.applyfunc(ps.fd.derivative.expand_diff_full)
        source = source.applyfunc(discretize)

        return [ps.Assignment(lhs, rhs) for lhs, rhs in zip(self.c.center_vector, sp.flatten(source)) if rhs]

    def discrete_continuity(self, flux_field: ps.field.Field):
        """Return a list of assignments for the continuity equation, which includes the source term

        Args:
            flux_field: a staggered field from which the fluxes are taken
        """

        assert ps.FieldType.is_staggered(flux_field)

        neighbors = flux_field.staggered_stencil + [ps.stencil.inverse_direction_string(d)
                                                    for d in flux_field.staggered_stencil]
        divergence = flux_field.staggered_vector_access(neighbors[0]) / \
            sp.Matrix(ps.stencil.direction_string_to_offset(neighbors[0])).norm()
        for d in neighbors[1:]:
            divergence += flux_field.staggered_vector_access(d) / \
                sp.Matrix(ps.stencil.direction_string_to_offset(d)).norm()
        A0 = sum([sp.Matrix(ps.stencil.direction_string_to_offset(d)).norm()
                  for d in flux_field.staggered_stencil]) / self.dim
        divergence /= A0

        source = self.discrete_source()
        source = {s.lhs: s.rhs for s in source}

        return [ps.Assignment(lhs, (lhs - rhs + source[lhs]) if lhs in source else (lhs - rhs))
                for lhs, rhs in zip(self.c.center_vector, divergence)]


def VOF(j: ps.field.Field, v: ps.field.Field, ρ: ps.field.Field):
    """Volume-of-fluid discretization of advection

    Args:
        j: the staggeredfield to write the fluxes to
        v: the flow velocity field
        ρ: the quantity to advect
    """
    assert ps.FieldType.is_staggered(j)

    fluxes = [[] for i in range(j.index_shape[0])]

    v0 = v.center_vector
    for d, neighbor in enumerate(j.staggered_stencil):
        c = ps.stencil.direction_string_to_offset(neighbor)
        v1 = v.neighbor_vector(c)

        # going out
        cond = sp.And(*[sp.Or(c[i] * v0[i] > 0, c[i] == 0) for i in range(len(v0))])
        overlap1 = [1 - sp.Abs(v0[i]) for i in range(len(v0))]
        overlap2 = [c[i] * v0[i] for i in range(len(v0))]
        overlap = sp.Mul(*[(overlap1[i] if c[i] == 0 else overlap2[i]) for i in range(len(v0))])
        fluxes[d].append(ρ.center_vector * overlap * sp.Piecewise((1, cond), (0, True)))

        # coming in
        cond = sp.And(*[sp.Or(c[i] * v1[i] < 0, c[i] == 0) for i in range(len(v1))])
        overlap1 = [1 - sp.Abs(v1[i]) for i in range(len(v1))]
        overlap2 = [v1[i] for i in range(len(v1))]
        overlap = sp.Mul(*[(overlap1[i] if c[i] == 0 else overlap2[i]) for i in range(len(v1))])
        fluxes[d].append(ρ.neighbor_vector(c) * overlap * sp.Piecewise((1, cond), (0, True)))

    for i, ff in enumerate(fluxes):
        fluxes[i] = ff[0]
        for f in ff[1:]:
            fluxes[i] += f

    assignments = []
    for i, d in enumerate(j.staggered_stencil):
        for lhs, rhs in zip(j.staggered_vector_access(d).values(), fluxes[i].values()):
            assignments.append(ps.Assignment(lhs, rhs))
    return assignments
