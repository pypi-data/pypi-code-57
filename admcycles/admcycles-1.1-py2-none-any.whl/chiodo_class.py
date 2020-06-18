r"""
Chiodo class from JPPZ - Corollary 4
"""
from __future__ import absolute_import, print_function

import itertools

from six.moves import range

from admcycles.admcycles import Tautv_to_tautclass, Tautvb_to_tautclass, Tautvecttobasis, tautgens, psiclass, tautclass, list_strata
from admcycles.stable_graph import StableGraph
from admcycles.graph_sum import graph_sum, divbyaut
from admcycles.double_ramification_cycle
import admcycles.DR as DR

from sage.combinat.subset import Subsets
from sage.arith.all import factorial
from sage.functions.other import floor, ceil
from sage.misc.misc_c import prod
from sage.rings.all import PolynomialRing, QQ, ZZ
from sage.modules.free_module_element import vector
from sage.rings.polynomial.polynomial_ring import polygen
from sage.rings.polynomial.multi_polynomial_element import MPolynomial

def chiodo_class(g, Avector, d=None, k=None, rpoly=False, tautout=True, basis=False):
    if d is None:
        d = g
    n = len(Avector)

    if any(isinstance(ai, MPolynomial) for ai in Avector):
        # compute DRpoly and substitute the ai in there
        pol, gens = DRpoly(g, d, n, tautout=tautout, basis=basis, gensout=True)
        subsdict = {gens[i]: Avector[i] for i in range(n)}

        if tautout:
            pol.coeff_subs(subsdict)
            pol.simplify()
            return pol
        return pol.apply_map(lambda x: x.subs(subsdict))

    if k is None:
        k = floor(sum(Avector)/(2*g-2+n))
    if sum(Avector) != k*(2*g-2+n):
        raise ValueError('2g-2+n must divide the sum of entries of Avector.')

    gens = tautgens(g, n, d, decst=True)
    v = vector([DR_coeff_new(decs, g, n, d, Avector, k, rpoly) for decs in gens]) / ZZ(2)**d
    #v1=vector([QQ(a) for a in DR.convert_vector_to_monomial_basis(v,g,d,tuple(range(1, n+1)),DR.MODULI_ST)])

    if basis:
        v1 = Tautvecttobasis(v, g, n, d)
        if tautout:
            return Tautvb_to_tautclass(v1, g, n, d)
        return v1
    else:
        if tautout:
            return Tautv_to_tautclass(v, g, n, d)
        return v


def DR_coeff_setup(G, g, n, d, Avector, k):
    gamma = G.gamma
    kappa, psi = G.poly.monom[0]
    exp_list = []
    scalar_factor = QQ((1, G.automorphism_number()))
    given_weights = [-k * (2 * gv - 2 + len(gamma._legs[i]))
                     for i, gv in enumerate(gamma._genera)]

    # contributions to scalar_factor from kappa-classes
    for v in range(gamma.num_verts()):
        if len(kappa[v]) == 1: # some kappa_1^e at this vertex
            scalar_factor *= (-k**2)**(kappa[v][0]) / factorial(kappa[v][0])

    # contributions to scalar_factor and given_weights from markings
    for i in range(1, n + 1):
        v = gamma.vertex(i)
        psipow = psi.get(i, 0) # if i in dictionary, have psi_i^(psi[i]), otherwise have psi_i^0
        given_weights[v] += Avector[i - 1]
        scalar_factor *= (Avector[i - 1])**(2 * psipow) / factorial(psipow)

    # contributions to scalar_factor and explist from edges
    for (lu, lv) in gamma._edges:
        psipowu = psi.get(lu, 0)
        psipowv = psi.get(lv, 0)
        exp_list.append(psipowu + psipowv + 1)
        scalar_factor *= ((-1)**(psipowu+psipowv)) / factorial(psipowv) / factorial(psipowu) / (psipowu+psipowv+1)

    return exp_list, given_weights, scalar_factor


def DR_coeff_new(G, g, n, d, Avector, k, rpoly):
    gamma = G.gamma # underlying stable graph of decstratum G
    kappa, _ = G.poly.monom[0]
    # kappa is a list of lenght = # vertices, of entries like [3,0,2] meaning that at this vertex there is a kappa_1^3 * kappa_3^2
    # _ = psi is a dictionary and psi[3]=4 means there is a decoration psi^4 at marking/half-edge 3

    if any(len(kalist) > 1 for kalist in kappa):
        return 0  # vertices can only carry powers of kappa_1, no higher kappas allowed

    m0 = ceil(sum([abs(i) for i in Avector]) / ZZ(2)) + g*abs(k) # value from which on the Pixton-sum below will be polynomial in m
    h0 = gamma.num_edges() - gamma.num_verts() + 1 # first Betti number of the graph Gamma
    exp_list, given_weights, scalar_factor = DR_coeff_setup(G, g, n, d, Avector, k)

    deg = 2 * sum(exp_list)  # degree of polynomial in m
    # R = PolynomialRing(QQ, len(gamma.edges) + 1, 'd')
    # P=prod([(di*(d0-di))**exp_list[i] for i,di in enumerate(R.gens()[1:])])/(d0**h0)
    u = gamma.flow_solve(given_weights)
    Vbasis = gamma.cycle_basis()

    #mpoly = mpoly_affine_sum(P, u, Vbasis,m0+1,deg)
    mpoly = mpoly_special(exp_list, h0, u, Vbasis, m0+1, deg)

    # mpoly = interpolate(mrange, mvalues)
    if rpoly:
        return mpoly * scalar_factor
    return mpoly.subs(r=0) * scalar_factor


def mpoly_special(exp_list, h0, u, Vbasis, start, degr):
    r"""
    Return the sum of the rational function in DR_coeff_new over the
    affine space u + V modulo r in ZZ^n as a univariate polynomial in r.
    V is the lattice with basis Vbasis.
    Use that this sum is polynomial in r starting from r=start and the polynomial has
    degree degr (for now).
    """
    mrange = list(range(start, start + degr + 2))
    mvalues = []
    rank = len(Vbasis)
    ulen = len(u)

    for m in mrange:
        total = 0
        for coeff in itertools.product(*[list(range(m)) for i in range(rank)]):
            v = u + sum([coeff[i]*Vbasis[i] for i in range(rank)])
            v = [vi % m for vi in v]
            total += prod([(v[i]*(m-v[i]))**exp_list[i] for i in range(ulen)])
        mvalues.append(total/QQ(m**h0))

    return interpolate(mrange, mvalues)



"""
def chiodo_class(g, Avector, d=None, k=None, r=None, rpoly=False, tautout=True, basis=False):
    r"""Returns the formula epsilon_* c(- R* pi_* L) from [JPPZ, Corollary 4]."""
    if d is None:
        d = g
    n = len(Avector)
    if k is None:
        k = floor(sum(Avector)/(2*g-2+n))
    if sum(Avector) != k*(2*g-2+n):
        raise ValueError('2g-2+n must divide the sum of entries of Avector.')
    if r == None and not rpoly:
        raise ValueError('Either r must be specified or rpoly must be set to True.')        
    
    if not r is None:
        GWlist = GammaWlist(g, Avector, d, k, r)
        GF = GFactor(r)
        
        return graph_sum(g,n,decgraphs=GWlist,globalfact=GF, vertterm=None,legterm=None,edgeterm=None,maxdeg=None,deg=None,termsout=False)
                

def GammaWlist(g, Avector, d, k, r):
    n = len(Avector)
    for e in range(d+1): # number of edges"""
        for gamma in list_strata(g, n, e):
            
