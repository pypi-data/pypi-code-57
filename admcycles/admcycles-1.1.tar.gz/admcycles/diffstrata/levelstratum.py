from __future__ import absolute_import
from __future__ import print_function

import itertools
import sys
from collections import Counter, defaultdict
from sympy.utilities.iterables import partitions
from ast import literal_eval

# pylint does not know sage
from sage.structure.sage_object import SageObject # pylint: disable=import-error
from sage.matrix.constructor import matrix # pylint: disable=import-error
from sage.misc.flatten import flatten # pylint: disable=import-error
from sage.misc.cachefunc import cached_method # pylint: disable=import-error
from sage.structure.formal_sum import FormalSum, FormalSums # pylint: disable=import-error
from sage.rings.rational_field import QQ # pylint: disable=import-error
from sage.arith.functions import lcm # pylint: disable=import-error
from sage.functions.other import factorial # pylint: disable=import-error
from sage.symbolic.ring import SR # pylint: disable=import-error
from sage.combinat.integer_vector_weighted import WeightedIntegerVectors  # pylint: disable=import-error
from sage.functions.other import binomial  # pylint: disable=import-error

import sage.misc.persist

from copy import deepcopy

import admcycles.admcycles

import admcycles.diffstrata.levelgraph
import admcycles.diffstrata.bic
import admcycles.diffstrata.sig
import admcycles.stratarecursion
import admcycles.diffstrata.stratatautring

ADM_EVALS = {}
TOP_XIS = {}
FILENAME = 'adm_evals.sobj'
XI_FILENAME = 'top_xis.sobj'

#######################################################################
#######################################################################
###### Recursive Calculations and Degeneration Graphs
#######################################################################
## The idea is to do all calculations recursively.
## In particular, the Degeneration Graph is itself a recursive object.
##
## The key observation is that:
## * Each 3-level graph arises by either clutching a top component of
##      a BIC to a BIC of its bottom component of a BIC of the top
##      component to the bottom component.
## * On the other hand, each 3-level graph is the intersection of
##      two (different) BICs of the Stratum.
## * Therefore, for each BIC B of the Stratum, every BIC Bt in the top
##      component corresponds to a unique BIC B' of the stratum, so
##      that the 3-level graph (Bt clutched to the bottom component of B)
##      is B*B' (i.e. delta_1 of this graph is B', delta_2 is B).
##      The same is true for the BICs of the bottom component.
## * We thus obtain two maps, for each BIC B of the stratum:
##      * top_to_bic mapping BICs of the top component to BICs of
##          the stratum
##      * bot_to_bic mapping BICs of the bottom component to BICs of
##          the stratum
## * These maps have disjoint images.
## * These maps fail to be embeddings precisely when the intersection
##      of two BICs is not irreducible (i.e. clutching different BICs
##      to a component results in the intersection with the same divisor)
##      or when there are automorphisms involved (i.e. several ways of
##      undegenerating to the same BIC).
## We can thereby express the clutching of a product of BICs in the top
## and bottom components of a BIC in our stratum as a product of BICs of
## our stratum. Hence the procedure is recursive.
##
## Therefore, the GenDegenerationGraph needs to remember only the BICs
## together with, for each BIC, top and bottom components and the two maps.
##
## More precisely, the Degeneration Graph of a GeneralisedStratum
## consists of the following information:
## * The BICs inside the Stratum.
## * For each BIC, its top and bottom component (GeneralisedStratum
##      together with a dictionary Stratum points -> LevelGraph points)
## * For each BIC, the BICs of its top and bottom component, together
##      with the maps top_to_bic and bot_to_bic.
##
## We can now calculate the GenDegenerationGraph:
## * Step 1: Calculate all BICs in a GeneralisedStratum.
## * Step 2: Separate these into top an bottom component.
## * Step 3: Calculate all BICs in every top and bottom component.
## * Step 4: Calculate top_to_bic and bot_to_bic for each BIC in the
##      Stratum (as dictionaries: index of BIC in top/bottom ->
##      index of BIC in stratum)
##
## In particular, we this implies the following recursive algorithm for
## the EmbeddedLevelGraph of an arbitrary product of BICs in the stratum:
## INPUT: Product of BICs.
## OUTPUT: EmbeddedLevelGraph.
## * Step 1: Choose a BIC B from the product (e.g. the first).
## * Step 2: Find the preimages of the other BICs in the product under
##      top_to_bic and bot_to_bic of B.
## * This gives (possibly multiple) products of BICs in the top and bottom
##      stratum of B.
## * Step 3: Apply to product in top an bottom to get two EmbeddedLevelGraphs
## * Step 4: Return the clutching of the top and bottom graph.
##
## Moreover, we can generate the "lookup list", consisting of the non-empty
## products of BICs in each stratum.
## For this, we record all intersections that give 3-level graphs in each
## GenDegenerationGraph (i.e. (2,1) means that there exists a 3-level graph
## C such that delta(1) of C is bics[2] and delta(2) of C is bics[1]).
## Note that this is equivalent to 2 being in the image of top_to_bic(1).
##
## The key observation here is that any profile (i_1,...,i_n) can be
## written as a "domino" of 3-level graphs, i.e. (i_1,i_2)(i_2,_3)...(i_n-1,i_n).
##
## However, for the recursive generation of the lookup list, it is enough
## to take a profile and add the top generations of the first bic and the
## bottom degenerations of the last bic to obtain a profile with length
## increased by one (see the implementation below for more details.)
##
#######################################################################
#######################################################################

class GeneralisedStratum(SageObject):
    """
    A union of (meromorphic) strata with residue conditions.

    A GeneralisedStratum is uniquely identified by the following information:

    * sig_list : list of signatures [sig_1,...,sig_n], where sig_i is the Signature 
        of the component i,

    * res_cond : list of residue conditions, i.e. [R_1,...,R_n] where each R_l is 
        a list of tuples (i,j), corresponding to the j-th component of sig_i, that 
        share a residue condition (i.e. the residues at these poles add up to 0).
    Note that the residue theorem for each component will be added automatically.
    """
    def __init__(self,sig_list,res_cond=None):
        self._h0 = len(sig_list)
        self._sig_list = sig_list
        self._n = sum([sig.n for sig in sig_list]) # total number of points
        self._g = [sig.g for sig in sig_list]
        # remember poles as (i,j) where i is the component and j is the index in sig_i
        self._polelist = [(i,j) for i,sig in enumerate(sig_list) for j in sig.pole_ind]
        self._p = len(self._polelist)
        if res_cond is None:
            res_cond = []
        self._res_cond = res_cond
        self.init_more()
    
    def init_more(self):
        self._bics = None
        self._smooth_LG = None
        self._all_graphs = None
        self._lookup_list = None
        self._lookup = {}
        if not self.is_empty():
            self.DG = admcycles.diffstrata.stratatautring.GenDegenerationGraph(self)
        # cache AdditiveGenerators:
        self._AGs = {}
        # tautological class of self:
        one = self.additive_generator((tuple(),0))
        self.ONE = one.as_taut()
        # tautological class of zero:
        self.ZERO = ELGTautClass(self,[])
    
    def __repr__(self):
        return "GeneralisedStratum(sig_list=%r,res_cond=%r)" % (self._sig_list,self._res_cond)
    def __str__(self):
        rep = ''
        if self._h0 > 1:
            rep += 'Product of Strata:\n'
        else:
            rep += 'Stratum: '
        for sig in self._sig_list:
            rep += repr(sig.sig) + '\n'
        rep += 'with residue conditions: '
        if not self._res_cond:
            rep += repr([]) + '\n'
        for res in self._res_cond:
            rep += repr(res) + '\n'
        return rep
    
    def info(self):
        """
        Print facts about self.

        This calculates everything, so could take long(!)

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((1,1))])
            sage: X.info()
            Stratum: (1, 1)
            with residue conditions: []
            Genus: [2]
            Dimension: 4
            Boundary Graphs (without horizontal edges):
            Codimension 0: 1 graph
            Codimension 1: 4 graphs
            Codimension 2: 4 graphs
            Codimension 3: 1 graph
            Total graphs: 10

            sage: X=GeneralisedStratum([Signature((4,))])
            sage: X.info()
            Stratum: (4,)
            with residue conditions: []
            Genus: [3]
            Dimension: 5
            Boundary Graphs (without horizontal edges):
            Codimension 0: 1 graph
            Codimension 1: 8 graphs
            Codimension 2: 19 graphs
            Codimension 3: 16 graphs
            Codimension 4: 4 graphs
            Total graphs: 48
        """
        print(self)
        print("Genus: %s" % self._g)
        print("Dimension: %s" % self.dim())
        print("Boundary Graphs (without horizontal edges):")
        tot = 0
        for c, graphs in enumerate(self.all_graphs):
            n = len(graphs)
            print("Codimension %s: %s %s" % (c,n,_graph_word(n)))
            tot += n
        print("Total graphs: %s" % tot)

    def additive_generator(self,enh_profile,leg_dict=None):
        """
        The AdditiveGenerator for the psi-polynomial given by leg_dict on enh_profile.

        For example, if psi_2 is the psi-class at leg 2 of enh_profile,
        the polynomial psi_2^3 would be encoded by the leg_dict {2 : 3}.

        This method should always be used instead of generating AdditiveGenerators
        directly, as the objects are cached here, i.e. the _same_ object is returned
        on every call.
        
        Args:
            enh_profile (tuple): enhanced profile
            leg_dict (dict, optional): Dictionary mapping legs of the underlying
                graph of enh_profile to positive integers, corresponding to 
                the power of the psi class associated to this leg. Defaults to None.
        
        Returns:
            AdditiveGenerator: the (cached) AdditiveGenerator

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: a = X.additive_generator(((0,),0))
            sage: a is X.additive_generator(((0,),0))
            True
            sage: a is AdditiveGenerator(X,((0,),0))
            False
        """
        ag_hash = hash_AG(leg_dict, enh_profile)
        return self.additive_generator_from_hash(ag_hash)
    
    def additive_generator_from_hash(self,ag_hash):
        if not ag_hash in self._AGs:
            self._AGs[ag_hash] = AdditiveGenerator.from_hash(self,ag_hash) 
        return self._AGs[ag_hash]

    def simple_poles(self):
        simple_poles = [p for p in self._polelist if self.stratum_point_order(p) == -1]
        return simple_poles        

    @cached_method
    def is_empty(self):
        """
        Checks if self fails to exist for residue reasons (simple pole with residue forced zero).
        
        Returns:
            bool: existence of simple pole with residue zero.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((1,-1))
            sage: X.is_empty()
            True
        """
        for p in self.simple_poles():
            if self.smooth_LG.residue_zero(p):
                return True
        return False                

    def is_disconnected(self):
        return self._h0 > 1

    def stratum_point_order(self,p):
        """
        The pole order at the stratum point p.
        
        Args:
            p (tuple): Point (i,j) of self.
        
        Returns:
            int: Pole order of p.
        """
        i, j = p
        return self._sig_list[i].sig[j]

    @property
    def bics(self):
        """
        Initialise BIC list on first call.
        
        Note that _bics is a list of tuples of EmbeddedLevelGraphs
        (each tuple consists of one EmbeddedLevelGraph for every
        connected component).
        """
        if self.is_empty():
            return []
        if self._bics is None:
            return self.gen_bic()
        return self._bics

    @property
    def res_cond(self):
        return self._res_cond

    @property
    def lookup_list(self):
        """
        The list of all (ordered) profiles.

        Note that starting with SAGE 9.0 profile numbering is no longer deterministic.
        
        Returns:
            list: Nested list of tuples.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: assert len(X.lookup_list) == 3
            sage: X.lookup_list[0]
            [()]
            sage: X.lookup_list[1]
            [(0,), (1,)]
            sage: assert len(X.lookup_list[2]) == 1
        """
        if self.is_empty():
            return []
        if self._lookup_list is None:
            # First, we build the "lookup-list", i.e. the list of all profiles:
            # the non-empty profiles can be found recursively:
            # given a profile, we create new profiles by adding top and bottom
            # degenerations of the corresponding bic to the begining and end.
            self._lookup_list = [[tuple()]]  # only one with 0 levels
            n = len(self.bics)
            self._lookup_list += [[(i,) for i in range(n)]]  # bics
            new_profiles = n
            while new_profiles:
                # we temporarily work with a set to avoid duplicates
                self._lookup_list.append(set())
                for profile in self._lookup_list[-2]:
                    first = profile[0]
                    for i in self.DG.top_to_bic(first).values():
                        self._lookup_list[-1].add((i,)+profile)
                    if len(profile) > 1:
                        last = profile[-1]
                        for i in self.DG.bot_to_bic(last).values():
                            self._lookup_list[-1].add(profile+(i,))
                self._lookup_list[-1] = list(self._lookup_list[-1])
                new_profiles = len(self._lookup_list[-1])
            self._lookup_list.pop()
        return self._lookup_list

    @property
    def all_graphs(self):
        """
        Nested list of all EmbeddedLevelGraphs in self.

        This list is built on first call.

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((1,1))])
            sage: assert comp_list(X.all_graphs[0], [EmbeddedLevelGraph(X, LG=LevelGraph([2],[[1, 2]],[],{1: 1, 2: 1},[0],True),dmp={1: (0, 0), 2: (0, 1)},dlevels={0: 0})])
            sage: assert comp_list(X.all_graphs[1], \
            [EmbeddedLevelGraph(X, LG=LevelGraph([1, 0],[[1, 2], [3, 4, 5, 6]],[(1, 5), (2, 6)],{1: 0, 2: 0, 3: 1, 4: 1, 5: -2, 6: -2},[0, -1],True),dmp={3: (0, 0), 4: (0, 1)},dlevels={0: 0, -1: -1}),\
            EmbeddedLevelGraph(X, LG=LevelGraph([1, 1, 0],[[1], [2], [3, 4, 5, 6]],[(2, 5), (1, 6)],{1: 0, 2: 0, 3: 1, 4: 1, 5: -2, 6: -2},[0, 0, -1],True),dmp={3: (0, 0), 4: (0, 1)},dlevels={0: 0, -1: -1}),\
            EmbeddedLevelGraph(X, LG=LevelGraph([1, 1],[[1], [2, 3, 4]],[(1, 4)],{1: 0, 2: 1, 3: 1, 4: -2},[0, -1],True),dmp={2: (0, 0), 3: (0, 1)},dlevels={0: 0, -1: -1}),\
            EmbeddedLevelGraph(X, LG=LevelGraph([2, 0],[[1], [2, 3, 4]],[(1, 4)],{1: 2, 2: 1, 3: 1, 4: -4},[0, -1],True),dmp={2: (0, 0), 3: (0, 1)},dlevels={0: 0, -1: -1})])
            sage: assert comp_list(X.all_graphs[2],\
            [EmbeddedLevelGraph(X, LG=LevelGraph([1, 0, 0],[[1], [2, 3, 4], [5, 6, 7, 8]],[(1, 4), (3, 8), (2, 7)],{1: 0, 2: 0, 3: 0, 4: -2, 5: 1, 6: 1, 7: -2, 8: -2},[0, -1, -2],True),dmp={5: (0, 0), 6: (0, 1)},dlevels={0: 0, -2: -2, -1: -1}),\
            EmbeddedLevelGraph(X, LG=LevelGraph([1, 0, 0],[[1, 2], [3, 4, 5], [6, 7, 8]],[(1, 4), (2, 5), (3, 8)],{1: 0, 2: 0, 3: 2, 4: -2, 5: -2, 6: 1, 7: 1, 8: -4},[0, -1, -2],True),dmp={6: (0, 0), 7: (0, 1)},dlevels={0: 0, -2: -2, -1: -1}),\
            EmbeddedLevelGraph(X, LG=LevelGraph([1, 1, 0],[[1], [2, 3], [4, 5, 6]],[(1, 3), (2, 6)],{1: 0, 2: 2, 3: -2, 4: 1, 5: 1, 6: -4},[0, -1, -2],True),dmp={4: (0, 0), 5: (0, 1)},dlevels={0: 0, -2: -2, -1: -1}),\
            EmbeddedLevelGraph(X, LG=LevelGraph([1, 1, 0],[[1], [2], [3, 4, 5, 6]],[(2, 5), (1, 6)],{1: 0, 2: 0, 3: 1, 4: 1, 5: -2, 6: -2},[0, -1, -2],True),dmp={3: (0, 0), 4: (0, 1)},dlevels={0: 0, -2: -2, -1: -1})])
            sage: assert comp_list(X.all_graphs[2], [EmbeddedLevelGraph(X, LG=LevelGraph([1, 0, 0, 0],[[1], [2, 3, 4], [5, 6, 7], [8, 9, 10]],[(1, 4), (3, 7), (2, 6), (5, 10)],{1: 0, 2: 0, 3: 0, 4: -2, 5: 2, 6: -2, 7: -2, 8: 1, 9: 1, 10: -4},[0, -1, -2, -3],True),dmp={8: (0, 0), 9: (0, 1)},dlevels={0: 0, -2: -2, -1: -1, -3: -3})])
        """
        if self.is_empty():
            return []
        if self._all_graphs is None:
            # We build the graph list from the lookup list:
            # Note that lookup returns a list of graphs.
            self._all_graphs = []
            for l in self.lookup_list:
                self._all_graphs.append(
                    list(itertools.chain.from_iterable(self.lookup(g) 
                        for g in l))
                )
            # Ensure that degenerations of top and bottom match up:
            assert all(k in self.DG.bot_to_bic(j).values() 
                            for k in range(self.DG.n) 
                            for j in self.DG.top_to_bic(k).values())
        return self._all_graphs

    @property
    def smooth_LG(self):
        """
        The smooth EmbeddedLevelGraph inside a LevelStratum.

        Note that the graph might be disconnected!

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((1,1))])
            sage: assert X.smooth_LG.is_isomorphic(EmbeddedLevelGraph(X,LG=LevelGraph([2],[[1, 2]],[],{1: 1, 2: 1},[0],True),dmp={1: (0, 0), 2: (0, 1)},dlevels={0: 0}))
            
            Note that we get a single disconnected graph if the stratum is
            disconnected.

            sage: X=GeneralisedStratum([Signature((0,)), Signature((0,))])
            sage: X.smooth_LG
            EmbeddedLevelGraph(LG=LevelGraph([1, 1],[[1], [2]],[],{1: 0, 2: 0},[0, 0],True),dmp={1: (0, 0), 2: (1, 0)},dlevels={0: 0})
        
        Returns:
            EmbeddedLevelGraph: The output of unite_embedded_graphs applied to
                the (embedded) smooth_LGs of each component of self.
        """
        if not self._smooth_LG:
            graph_list = []
            for i,sig in enumerate(self._sig_list):
                g = admcycles.diffstrata.levelgraph.smooth_LG(sig)
                dmp = {j:(i,j-1) for j in range(1,sig.n+1)}
                graph_list.append((self,g,dmp,{0:0}))
            self._smooth_LG = unite_embedded_graphs(tuple(graph_list))
        return self._smooth_LG

    @cached_method
    def residue_matrix(self):
        """
        Calculate the matrix associated to the residue space, 
        i.e. a matrix with a line for every residue condition and a column for every pole of self.

        The residue conditions consist ONLY of the ones coming from the GRC (in _res_cond) 
        For inclusion of the residue theorem on each component, use smooth_LG.full_residue_matrix!
        """
        return self.matrix_from_res_conditions(self._res_cond)
    
    def matrix_from_res_conditions(self,res_conds):
        """
        Calculate the matrix for a list of residue conditions, i.e.
        a matrix with one line for every residue condition and a column for each pole of self.
        
        Args:
            res_conds (list): list of residue conditions, i.e. a nested list R
                R = [R_1,R_2,...] where each R_i is a list of poles (stratum points)
                whose residues add up to zero.
        
        Returns:
            SAGE matrix: residue matrix (with QQ coefficients)

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((2,-2,-2)),Signature((2,-2,-2))])
            sage: X.matrix_from_res_conditions([[(0,1),(0,2),(1,2)],[(0,1),(1,1)],[(1,1),(1,2)]])
            [1 1 0 1]
            [1 0 1 0]
            [0 0 1 1]
        """
        res_vec = []
        for res_c in res_conds:
            # note: int(True)=1, int(False)=0
            res_vec += [[int(p in res_c) for p in self._polelist]]
        return matrix(QQ,res_vec)
    
    @cached_method
    def residue_matrix_rank(self):
        return self.residue_matrix().rank()
    
    @cached_method
    def dim(self):
        """
        Return the dimension of the stratum, that is the sum of 2g_i + n_i - 1 - residue conditions -1 for projective.

        The residue conditions are given by the rank of the (full!) residue matrix.

        Empty strata return -1.

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((4,))])
            sage: all(B.top.dim() + B.bot.dim() == X.dim()-1 for B in X.bics)
            True
        """
        if self.is_empty():
            return -1
        # add residue conditions from RT for every connected component:
        M = self.smooth_LG.full_residue_matrix
        return (sum([2*sig.g + sig.n - 1 for sig in self._sig_list])
                    - M.rank() - 1)

    def gen_bic(self):
        """
        Generates all BICs (using bic) as EmbeddedLevelGraphs.
        
        Returns:
            list: self._bics i.e. a list of (possibly disconnected) 
                EmbeddedLevelGraphs.
                (More precisely, each one is a tuple consisting of one 
                EmbeddedLevelGraph for every connected component that has
                been fed to unite_embedded_graphs).
        """
        self._bics = []
        if self.is_empty():
            return 
        ## The BICs are the products of BICs for each connected component
        ## (satisfying the residue condition).
        ## Moreover, if there are several connected components, we also need
        ## to include the smooth stratum on each level.
        emb_bic_list = []

        ## First, we establish the dictionaries for the EmbeddedLevelGraphs:
        ## * the marked points of the stratum are numbered (i,j) where (i,j)
        ##      is the j-th point on the i-th connected component.
        ##      Note that j is the index in sig, i.e. starts at 0.
        ## * on each BIC, the i-th point of the signature is the point i+1
        ## mp_dict maps the points on the BIC to the points of the stratum
        for i, sig in enumerate(self._sig_list):
            mp_dict = {j : (i,j-1) for j in range(1,sig.n+1)}
            # We can't build the EmbeddedLevelGraph until we have the data for all
            # components (otherwise we mess up the legality check, etc.)
            # So for now, we just store the generating info for each connected component seperately.
            emb_bic_list_cur = []
            for g in admcycles.diffstrata.bic.bic_alt_noiso(sig.sig): # TODO: Adjust for Signature!!
                level_dict = {g.internal_level_number(0): 0,
                              g.internal_level_number(-1): -1}
                EG = (self,g,mp_dict,level_dict)
                emb_bic_list_cur.append(EG)
            if self._h0 > 1:
                # we need the smooth component on each level
                for l in [0,-1]:
                    emb_bic_list_cur.append((self, admcycles.diffstrata.levelgraph.smooth_LG(sig), mp_dict,
                            {0 : l},  # one for each level
                        )
                    )
            emb_bic_list.append(emb_bic_list_cur)
        # The elements of _bics are now products of the (embedded) bics of the components
        # Careful: The only ones that are not allowed are those, where all
        #       components are on one level!!
        prod_bics = itertools.product(*emb_bic_list)
        for prod_graph in prod_bics:
            # levels are stored in values of the dict in component 3 of each tuple:
            if (any(0 in g[3].values() for g in prod_graph) and
                any(-1 in g[3].values() for g in prod_graph)
            ):
                # NOTE: This actually builds the EmbeddedLevelGraphs!
                pg = unite_embedded_graphs(prod_graph)
                if pg.is_legal():  # check r-GRC
                    self._bics.append(pg)
        # isomorphism classes:  (possibly figure out how to check earlier?)
        self._bics = admcycles.diffstrata.bic.isom_rep(self._bics)
        return self._bics

    #### Ideally, we could always work with enhanced profiles, never with graphs.
    #### Then edge maps could work like this:
    ## Def: A leg is a tuple consisting of:
    ## * an enhanced profile (of a levelgraph)
    ## * the levelstratum inside the profile (e.g. for the profile (1,2,3) this would
    ##   be either 1^top, 3^bot, (12) or (23)). These were computed for the stratum anyway.
    ## * an orbit of a marked point of this gen levelstratum, which corresponds to an edge
    ##   of the corresponding graph
    ##   i.e. an ordered tuple of marked points equivalent by automorphisms of the corresponding
    ##   BIC or 3-level graph (which should be also an automorphism of the full graph??!!)
    ##
    ## Then:
    ## INPUT: (leg, enhanced profile)
    ## The enhanced profile should be that of a degeneration of the graph of leg (!)
    ##
    ## OUTPUT: leg (on the second profile)
    ##
    ## Case 1:
    ##   The levelstratum of the leg is unchanged by the degeneration.
    ##   i.e.: (1,2) and (1,2,3) for an edge on (1,2).
    ##   In this case the output is trivially the same edge embedded into (1,2,3)
    ##   (because (1,2) is still a level of (1,2,3)).
    ##
    ## Case 2:
    ##   The levelstratum is degenerated,
    ##   i.e.: (1,2) and (1,3,2) for an leg e on (1,2).
    ##   In this case we know that e (by checking the sign of the order) is either
    ##   a leg on 1^bot or 2^top and the degeneration is given by top_to_bic_inv (or
    ##   bot_to_bic_inv) of 3, where we can then track the marked point associated to e.
    ####

    # TODO: This should work "smarter", see above.
    @cached_method
    def explicit_leg_maps(self,enh_profile,enh_deg_profile,only_one=False):
        """
        Provide explicit leg maps (as list of dictionaries: legs of LG to legs of LG), from
        the graph associated to enh_profile to the one associated to enh_deg_profile.

        If enh_deg_profile is not a degeneration (on the level of profiles), None is
        returned.
        
        Args:
            enh_profile (enhanced profile): tuple (profile, index).
            enh_deg_profile (enhanced profile): tuple (profile, index).
            only_one (bool, optional): Give only one (the 'first') map (or None if none exist). 
                Defaults to False.

        Raises:
            RuntimeError: If enh_profile is empty.
            UserWarning: If there are no degenerations in the appropriate profile.

        Returns:
            list of dicts: List of the leg isomorphisms, None if not a degeneration, 
                only one dict if only_one=True.
        
        EXAMPLES ::

        """
        profile = enh_profile[0]
        deg_profile = enh_deg_profile[0]
        # check if deg_profile is actually a (profile) degeneration:
        if not set(profile).issubset(set(deg_profile)):
            return None
        g = self.lookup_graph(*enh_profile)
        degen = self.lookup_graph(*enh_deg_profile)
        if not degen:
            raise RuntimeError ("%r is not a graph in %r!" % (enh_deg_profile,self))
        # To obtain g, we have to squish degen at the places in the profile
        # of degen that are not in the profile of g.
        # We work from right to left to avoid confusion with the level numbering.
        degen_squish = degen
        for level, bic_index in list(enumerate(deg_profile))[::-1]:
            if bic_index in profile:
                continue
            degen_squish = degen_squish.squish_vertical(level)
        isoms = (l_iso for v_iso, l_iso in g.isomorphisms(degen_squish))
        try:
            first_isom = next(isoms)
        except StopIteration:
            # No isomorphisms found
            raise UserWarning("Squish of %r not isomorphic to %r!" % (enh_deg_profile, enh_profile))
        if only_one:
            return first_isom
        else:
            return [first_isom] + list(isoms)

    #####
    ### Common degenerations:
    ## This should eat two graphs, given by their "enhanced profile" i.e. things we can 
    ## feed to graph_lookup (a list of BICs and an index) and also return a list of
    ## enhanced profiles.

    ### Naive approach:
    ## do a (set-wise) degeneration of the profile and just go through the list
    ## checking which ones are actually degenerations:
    ## INPUT: Profile + index
    ## OUTPUT: List of profiles + indices

    ## TODO: There should be a smart way! For that one has to understand
    ## how to correctly encode the irreducible components of the profiles.

    @cached_method
    def common_degenerations(self,s_enh_profile,o_enh_profile):
        """
        Find common degenerations of two graphs.
        
        Args:
            s_enh_profile (tuple): Enhanced profile, i.e. a tuple (p,k) consisting of
                * a sorted (!) profile p
                * an index in self.lookup(p)
                thus giving the information of an EmbeddedLevelGraph in self.
            o_enh_profile (tuple): Enhanced profile.
        
        Returns:
            list: list of enhanced profiles, i.e. entries of type [tuple profile, index] 
                    (that undegenerate to the two given graphs).

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((4,))])

            To retrieve the actual EmbeddedLevelGraphs, we must use lookup_graph.  
            (Because of BIC renumbering between different SAGE versions we can't provide any concrete examples :/)

            Note that the number of components can also go down.

            Providing common graphs works:

            sage: X.common_degenerations(((2,),0),((2,),0))
            [((2,), 0)]

            Empty intersection gives empty list.

        """
        s_profile = s_enh_profile[0]
        o_profile = o_enh_profile[0]
        try:
            # merge_profiles returns None if there aren't any...
            deg_profile = tuple(self.merge_profiles(s_profile,o_profile))
        except TypeError:
            return []
        return_list = []
        # careful with reducible profiles:
        for i in range(len(self.lookup(deg_profile))):
            if self.is_degeneration((deg_profile,i),s_enh_profile) and self.is_degeneration((deg_profile,i),o_enh_profile):
                return_list.append((deg_profile,i))
        return return_list
    
    # Excess intersection of two additive generators in an ambient graph
    def intersection(self,s_taut_class,o_taut_class,amb_enh_profile=None):
        """
        Excess intersection of two tautological classes in Chow of ambient_enh_profile.
        
        Args:
            s_taut_class (ELGTautClass): tautological class
            o_taut_class (ELGTautClass): tautological class
            amb_enh_profile (tuple, optional): enhanced profile of ambient graph. 
                    Defaults to None.

        Raises:
            RuntimeError: raised if any summand of any tautological class is not on
                    a degeneration of ambient_enh_profile.
        
        Returns:
            ELGTautClass: Tautological class on common degenerations
        """
        # check input:
        if amb_enh_profile is None:
            amb_enh_profile = ((),0)
        if s_taut_class == 0 or s_taut_class == self.ZERO:
            return self.ZERO
        if s_taut_class == 1 or s_taut_class == self.ONE:
            return o_taut_class
        if o_taut_class == 0 or o_taut_class == self.ZERO:
            return self.ZERO
        if o_taut_class == 1 or o_taut_class == self.ONE:
            return s_taut_class
        return_list = []
        # unpack tautological classes:
        for s_coeff, s_add_gen in s_taut_class.psi_list:
            for o_coeff, o_add_gen in o_taut_class.psi_list:
                prod = self.intersection_AG(s_add_gen, o_add_gen, amb_enh_profile)
                if prod == 0 or prod == self.ZERO:
                    continue
                return_list.append(s_coeff*o_coeff * prod)
        return_value = self.ELGsum(return_list)
        if return_value == 0:
            return self.ZERO
        if s_taut_class.is_equidimensional() and o_taut_class.is_equidimensional():
            assert return_value.is_equidimensional(),\
                "Product of equidimensional classes is not equidimensional! %s * %s = %s"\
                    % (s_taut_class, o_taut_class, return_value)
        return return_value

    @cached_method
    def intersection_AG(self, s_add_gen, o_add_gen, amb_enh_profile=None):
        """
        Excess intersection formula for two AdditiveGenerators in Chow of amb_enh_profile.

        Note that as AdditiveGenerators and enhanced profiles are hashable,
        this method can (and will) be cached (in contrast with intersection).
        
        Args:
            s_add_gen (AdditiveGenerator): first AG
            o_add_gen (AdditiveGenerator): second AG
            amb_enh_profile (tuple, optional): enhanced profile of ambient graph. 
                    Defaults to None.
        
        Raises:
            RuntimeError: raised if any of the AdditiveGenerators is not on
                    a degeneration of ambient_enh_profile.
        
        Returns:
            ELGTautClass: Tautological class on common degenerations
        """
        if amb_enh_profile is None:
            amb_enh_profile = ((),0)
        s_enh_profile = s_add_gen.enh_profile
        o_enh_profile = o_add_gen.enh_profile
        if not self.is_degeneration(s_enh_profile,amb_enh_profile):
            raise RuntimeError("%r is not a degeneration of %r" % (s_enh_profile,amb_enh_profile))
        if not self.is_degeneration(o_enh_profile,amb_enh_profile):
            raise RuntimeError("%r is not a degeneration of %r" % (o_enh_profile,amb_enh_profile))
        # Degree check: 
        # * the degree of the product is the sum of the degreees
        # * the product is supported on a set of codim >= max(codim(s),codim(o))
        # => if the sum of the degrees is > (dim(self) - max(codim(s),codim(o)))
        #   the product will be 0 in any case
        # NOTE: degree = codim + psi-degree
        deg_sum = s_add_gen.psi_degree + o_add_gen.psi_degree
        if deg_sum > self.dim() - max(len(s_enh_profile[0]),len(o_enh_profile[0])):
            return self.ZERO
        degenerations = self.common_degenerations(s_enh_profile,o_enh_profile)
        if not degenerations:
            return self.ZERO
        NB = self.cnb(s_enh_profile,o_enh_profile,amb_enh_profile)
        if NB == 1:
            # Intersection is transversal, in this case we are done:
            # the pullback of an additive generator is a taut class
            # where all classes live on the same graph:
            prod = [(_cs * _co, s_pb * o_pb)
                        for L in degenerations
                            for _cs, s_pb in s_add_gen.pull_back(L).psi_list
                            for _co, o_pb in o_add_gen.pull_back(L).psi_list]
            return ELGTautClass(self,[(c, AG) for c, AG in prod])
        elif NB == 0 or NB == self.ZERO:
            # product with 0 is 0 ...
            return NB
        else:
            # intersect the pullback to L with the normal bundle pulled back to L (in L):
            summands = [self.intersection(
                            self.intersection(
                                    s_add_gen.pull_back(L),
                                    o_add_gen.pull_back(L),
                                    L),
                            self.gen_pullback_taut(
                                    NB,
                                    L,
                                    self.minimal_common_undegeneration(s_enh_profile,o_enh_profile)
                                ),
                            L)
                                        for L in degenerations]
            return self.ELGsum([tcls for tcls in summands])

    def normal_bundle(self, enh_profile, ambient=None):
        """
        Normal bundle of enh_profile in ambient.

        Note that this is equivalent to cnb(enh_profile, enh_profile, ambient).
        
        Args:
            enh_profile (tuple): enhanced profile
            ambient (tuple, optional): enhanced profile. Defaults to None.
        
        Raises:
            ValueError: Raised if enh_profile is not a codim 1 degeneration of ambient
        
        Returns:
            ELGTautClass: Normal bundle N_{enh_profile, ambient}
        """
        if ambient is None:
            ambient = ((),0)
        else:
            ambient = (tuple(ambient[0]),ambient[1])
        if len(enh_profile[0]) != len(ambient[0]) + 1 or not self.is_degeneration(enh_profile,ambient):
            raise ValueError("%r is not a codim 1 degeneration of %r" % (enh_profile,ambient))
        return self.cnb(enh_profile, enh_profile, ambient)

    # This is an element of CH^s(ambient) where s is the cardinality of the intersection of profiles
    # or equivalently in CH^(c+s)(B) where c is the codimension of ambient.
    @cached_method
    def cnb(self,s_enh_profile,o_enh_profile,amb_enh_profile=None):
        """
        Common Normal bundle of two graphs in an ambient graph.

        Note that for a trivial normal bundle (transversal intersection)
        we return 1 (int) and NOT self.ONE !!

        The reason is that the ``correct'' ONE would be the ambient graph and that
        is a pain to keep track of in intersection....
        
        Args:
            s_enh_profile (tuple): enhanced profile
            o_enh_profile (tuple): enhanced profile
            amb_enh_profile (tuple, optional): enhanced profile. Defaults to None.

        Raises:
            RuntimeError: Raised if s_enh_profile or o_enh_profile do not degenerate 
                from amb_enh_profile.
        
        Returns:
            ELGTautClass: Product of normal bundles appearing.
            1 if the intersection is transversal.
        """
        # check/normalise input:
        if amb_enh_profile is None:
            amb_enh_profile = ((),0)
        else:
            amb_enh_profile = (tuple(amb_enh_profile[0]),amb_enh_profile[1])
        if not self.is_degeneration(s_enh_profile,amb_enh_profile):
            raise RuntimeError("%r is not a degeneration of %r" % (s_enh_profile,amb_enh_profile))
        if not self.is_degeneration(o_enh_profile,amb_enh_profile):
            raise RuntimeError("%r is not a degeneration of %r" % (o_enh_profile,amb_enh_profile))
        min_com = self.minimal_common_undegeneration(s_enh_profile,o_enh_profile)
        if min_com == amb_enh_profile:
            return 1  # terminating condition, transversal
        else:
            assert self.codim_one_common_undegenerations(s_enh_profile,o_enh_profile,amb_enh_profile),\
                "minimal common undegeneration is %r, ambient profile is %r, but there aren't codim one common undegenerations!"\
                    % (min_com,amb_enh_profile)
        return_list = []
        for ep in self.codim_one_common_undegenerations(s_enh_profile,o_enh_profile,amb_enh_profile):
            G = self.lookup_graph(*ep)
            p, i = ep
            AGG = self.additive_generator(ep,None)
            # This is the "difference" between ep and amb_enh_profile:
            # i.e. the inserted level, i in paper notation
            squished_level = get_squished_level(ep,amb_enh_profile)
            ll = self.bics[p[squished_level]].ell
            xi_top = self.xi_at_level(squished_level,ep,quiet=True)
            xi_bot = self.xi_at_level(squished_level+1,ep,quiet=True)
            xis = -xi_top + xi_bot
            summand = 1/QQ(ll) * self.gen_pullback_taut(xis,min_com,ep)
            # calL pulled back to min_com:
            summand -= 1/QQ(ll) * self.gen_pullback_taut(self.calL(ep, squished_level),min_com,ep)
            if summand == 0:
                # product is zero!
                return self.ZERO
            assert summand.is_equidimensional(),\
                "Not all summands in %s of same degree!" % summand
            return_list.append(summand)
        # product over normal bundles:
        if not return_list:
            return 1  # empty product => transversal
        NBprod = return_list[0]
        for nb in return_list[1:]:
            NBprod = self.intersection(NBprod,nb,min_com)
        assert NBprod.is_equidimensional(), "Not all summands in %s of same degree!" % NBprod
        return NBprod

    @cached_method
    def gen_pullback(self,add_gen,o_enh_profile,amb_enh_profile=None):
        """
        Generalised pullback of additive generator to o_enh_profile in amb_enh_profile.
        
        Args:
            add_gen (AdditiveGenerator): additive generator on a degeneration of amb_enh_profile.
            o_enh_profile (tuple): enhanced profile (degeneration of amb_enh_profile)
            amb_enh_profile (tuple, optional): enhanced profile. Defaults to None.

        Raises:
            RuntimeError: If one of the above is not actually a degeneration of amb_enh_profile.
        
        Returns:
            ELGTautClass: Tautological class on common degenerations of AdditiveGenerator profile and o_enh_profile.
        """
        # check input:
        if amb_enh_profile is None:
            amb_enh_profile = ((),0)
        if not self.is_degeneration(o_enh_profile,amb_enh_profile):
            raise RuntimeError("%r is not a degeneration of %r" % (o_enh_profile,amb_enh_profile))
        s_enh_profile = add_gen.enh_profile
        if not self.is_degeneration(s_enh_profile,amb_enh_profile):
            raise RuntimeError("%r is not a degeneration of %r" % (s_enh_profile,amb_enh_profile))
        degenerations = self.common_degenerations(s_enh_profile,o_enh_profile)
        # if there are no common degenerations, pullback is 0
        if not degenerations:
            return self.ZERO
        NB = self.cnb(s_enh_profile,o_enh_profile,amb_enh_profile)
        # stop condition
        if NB == 0 or NB == self.ZERO:
            return 0
        return_list = []
        for L in degenerations:
            if NB == 1:
                # transversal
                return_list.append(add_gen.pull_back(L))
            else:
                return_list.append(
                    self.intersection(
                        self.gen_pullback_taut(NB, L, self.minimal_common_undegeneration(s_enh_profile,o_enh_profile)),
                        add_gen.pull_back(L),
                        L
                    )
                )
        return_value = self.ELGsum(return_list)
        if return_value != 0:
            return return_value
        else:
            return self.ZERO

    def gen_pullback_taut(self, taut_class, o_enh_profile,amb_enh_profile=None):
        """
        Generalised pullback of tautological class to o_enh_profile in amb_enh_profile.

        This simply returns the ELGSum of gen_pullback of all AdditiveGenerators.
        
        Args:
            taut_class (ELGTautClass): tautological class each summand on a degeneration of amb_enh_profile.
            o_enh_profile (tuple): enhanced profile (degeneration of amb_enh_profile)
            amb_enh_profile (tuple, optional): enhanced profile. Defaults to None.

        Raises:
            RuntimeError: If one of the above is not actually a degeneration of amb_enh_profile.
        
        Returns:
            ELGTautClass: Tautological class on common degenerations of AdditiveGenerator profile and o_enh_profile.
        """
        return_list = []
        for c, AG in taut_class.psi_list:
            return_list.append(c * self.gen_pullback(AG, o_enh_profile, amb_enh_profile))
        return self.ELGsum(return_list)

    ## TODO: There should be a better way for this, using just BICs and where
    ## marked points go ... (see discussion above)
    @cached_method
    def explicit_edge_becomes_long(self,enh_profile,edge):
        """
        A list of enhanced profiles where the (explicit) edge 'edge' became long.

        We go through the codim one degenerations of enh_profile and check
        each graph, if edge became long (under any degeneration).

        However, we count each graph only once, even if there are several ways
        to undegenerate (see examples).
        
        Args:
            enh_profile (tuple): enhanced profile: (profile, index).
            edge (tuple): edge of the LevelGraph associated to enh_profile: 
                (start leg, end leg).
        
        Raises:
            RuntimeError: Raised if the leg is not a leg of the graph of enh_profile.
        
        Returns:
            list: list of enhanced profiles.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((1,1))
            sage: V=[ep for ep in X.enhanced_profiles_of_length(1) if X.lookup_graph(*ep).level(0)._h0 == 2]
            sage: epV=V[0]
            sage: VLG=X.lookup_graph(*epV).LG
            sage: assert len(X.explicit_edge_becomes_long(epV, VLG.edges[1])) == 1
            sage: assert X.explicit_edge_becomes_long(epV, VLG.edges[1]) == X.explicit_edge_becomes_long(epV, VLG.edges[1])

        """
        ep_list = []
        for ep in self.codim_one_degenerations(enh_profile):
            g = self.lookup_graph(*ep)
            if g.LG.has_long_edge:
                for leg_map in self.explicit_leg_maps(enh_profile,ep):
                    try:
                        if g.LG.is_long((leg_map[edge[0]],leg_map[edge[1]])):
                            ep_list.append(ep)
                            break  # Not sure, if we want to record several occurences...
                    except KeyError:
                        raise RuntimeError("%r does not seem to be an edge of %r"
                            % (edge, enh_profile))
        return ep_list

    @cached_method
    def explicit_edges_between_levels(self,enh_profile,start_level,stop_level):
        """
        Edges going from (relative) level start_level to (relative) level stop_level.

        Note that we assume here that edges respect the level structure, i.e.
        start on start_level and end on end_level!
        
        Args:
            enh_profile (tuple): enhanced profile
            start_level (int): relative level number (0...codim)
            stop_level (int): relative level number (0...codim)
        
        Returns:
            list: list of edges, i.e. tuples (start_point,end_point)
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))

            Compact type:

            sage: assert len([ep for ep in X.enhanced_profiles_of_length(1) if len(X.explicit_edges_between_levels(ep,0,1)) == 1]) == 1

            Banana:

            sage: assert len([ep for ep in X.enhanced_profiles_of_length(1) if len(X.explicit_edges_between_levels(ep,0,1)) == 2]) == 1

        """
        G = self.lookup_graph(*enh_profile)
        # TODO: There should be a way smarter way for doing this...
        edges = [e for e in G.LG.edges 
                    if (G.LG.level_number(G.LG.levelofleg(e[0])) == start_level and
                        G.LG.level_number(G.LG.levelofleg(e[1])) == stop_level)]
        return edges

    ### Finding codimension one degenerations:
    # This is not very fancy yet.
    # At the moment, we take a profile and check at which places we can compatibly
    # insert a BIC (similarly to creating the lookup_list).
    # We then check "by hand", if this is ok with the enhanced structure, i.e.
    # on connected components.
    # Note that this check is bypassed if the input profile is irreducible.
    @cached_method
    def codim_one_degenerations(self,enh_profile):
        """
        Degenerations of enh_profile with one more level.
        
        Args:
            enh_profile (enhanced profile): tuple (profile, index)
        
        Raises:
            RuntimeError: Error if we find a degeneration that doesn't squish
                back to the graph we started with.
        
        Returns:
            list: list of enhanced profiles.

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((4,))])
            sage: assert all(len(p) == 2 for p, _ in X.codim_one_degenerations(((2,),0)))

            Empty profile gives all bics:

            sage: assert X.codim_one_degenerations(((),0)) == [((0,), 0), ((1,), 0), ((2,), 0), ((3,), 0), ((4,), 0), ((5,), 0), ((6,), 0), ((7,), 0)]
        """
        profile = list(enh_profile[0])
        # empty profile gives all bics:
        if not profile:
            return [((b,),0) for b in range(len(self.bics))]
        deg_list = []
        # build all length 1 profile extensions:
        # The first and last entry don't have any compatibility conditions:
        # add all top degenerations of the first guy
        for bic in self.DG.top_to_bic(profile[0]).values():
            deg_list.append(tuple([bic] + profile[:]))
        # and all bottom degenerations of the last guy
        for bic in self.DG.bot_to_bic(profile[-1]).values():
            deg_list.append(tuple(profile[:] + [bic]))
        # For the "middle" entries of the profile, we have to check compatibility
        for i in range(len(profile)-1):
            for bic in self.DG.bot_to_bic(profile[i]).values():  # candidates
                if bic in self.DG.top_to_bic(profile[i+1]).values():
                    deg_list.append(tuple(profile[:i+1] + [bic] + profile[i+1:]))
        deg_list = list(set(deg_list))  # remove duplicates
        # We now build the list of enhanced profiles:
        enh_list = []
        for p in deg_list:
            for i in range(len(self.lookup(p))):
                if self.is_degeneration((p,i),enh_profile):
                    enh_list.append((p,i))
        return enh_list

    @cached_method
    def codim_one_common_undegenerations(self,s_enh_profile,o_enh_profile,amb_enh_profile=None):
        """
        Profiles that are 1-level degenerations of amb_enh_profile and include
        s_enh_profile and o_enh_profile.
        
        Args:
            s_enh_profile (tuple): enhanced profile
            o_enh_profile (tuple): enhanced profile
            amb_enh_profile (tuple): enhanced profile
        
        Returns:
            list: list of enhanced profiles
        
        EXAMPLES ::

        """
        if amb_enh_profile is None:
            amb_enh_profile = ((),0)
        profile_list = []
        for ep in self.codim_one_degenerations(amb_enh_profile):
            if self.is_degeneration(s_enh_profile,ep) and self.is_degeneration(o_enh_profile,ep):
                profile_list.append(ep)
        return profile_list

    @cached_method
    def minimal_common_undegeneration(self,s_enh_profile,o_enh_profile):
        """
        The minimal dimension graph that is undegeneration of both s_enh_profile
        and o_enh_profile.
        
        Args:
            s_enh_profile (tuple): enhanced profile
            o_enh_profile (tuple): enhanced profile

        Raises:
            RuntimeError: If there are no common undgenerations in the intersection profile.

        Returns:
            tuple: enhanced profile
        
        EXAMPLES ::

        """
        s_profile = s_enh_profile[0]
        o_profile = o_enh_profile[0]
        # build "sorted" intersection
        intersection = []
        for b in s_profile:
            if b in o_profile:
                intersection.append(b)
        # make hashable
        intersection = tuple(intersection)
        # if the intersection profile is irreducible, we are done:
        if len(self.lookup(intersection)) == 1:
            return (intersection, 0)
        else:
            for i in range(len(self.lookup(intersection))):
                if (self.is_degeneration(s_enh_profile,(intersection,i)) and
                                self.is_degeneration(o_enh_profile,(intersection,i))):
                    return (intersection, i)
            else:
                raise RuntimeError("No common undegeneration in profile %r" % intersection)
                            
    @cached_method
    def is_degeneration(self,s_enh_profile,o_enh_profile):
        """
        Check if s_enh_profile is a degeneration of o_enh_profile.
        
        Args:
            s_enh_profile (tuple): enhanced profile
            o_enh_profile (tuple): enhanced profile
        
        Returns:
            bool: True if the graph associated to s_enh_profile is a degeneration
                of the graph associated to o_enh_profile, False otherwise.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((4,))])
            sage: assert X.is_degeneration(((7,),0),((7,),0))

            The empty tuple corresponds to the stratum:

            sage: assert X.is_degeneration(((2,),0),((),0))
        """
        s_profile = s_enh_profile[0]
        o_profile = o_enh_profile[0]
        # first check: subset:
        if not set(o_profile) <= set(s_profile):
            return False
        # in the irreducible case, we are done:
        if len(self.lookup(s_profile)) == len(self.lookup(o_profile)) == 1:
            assert self.explicit_leg_maps(o_enh_profile,s_enh_profile),\
                "%r and %r contain only one graph, but these are not degenerations!"\
                    % (o_enh_profile,s_enh_profile)
            return True
        else:
            # otherwise: check if an undegeneration map exists:
            try:
                if self.explicit_leg_maps(o_enh_profile,s_enh_profile,only_one=True) is None:
                    return False
                else:
                    return True
            except UserWarning:
                # This is raised if there is no undegeneration inside the expected profile...
                return False

    @cached_method
    def squish(self, enh_profile, l):
        """
        Squish level l of the graph associated to enh_profile. Returns the enhanced profile
        associated to the squished graph.
        
        Args:
            enh_profile (tuple): enhanced profile
            l (int): level of graph associated to enhanced profile
        
        Raises:
            RuntimeError: Raised if a BIC is squished at a level other than 0.
            RuntimeError: Raised if the squished graph is not found in the squished profile.
        
        Returns:
            tuple: enhanced profile.

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: assert all(X.squish(ep,0) == ((),0) for ep in X.enhanced_profiles_of_length(1))
            sage: assert all(X.squish((p,i),1-l) == ((p[l],),0) for p, i in X.enhanced_profiles_of_length(2) for l in range(2))
        """
        p, i = enh_profile
        if len(p) == 1:
            if l != 0:
                raise RuntimeError("BIC can only be squished at level 0!" % (enh_profile, l))
            return ((), 0)
        new_p = list(p)
        new_p.pop(l)
        new_p = tuple(new_p)
        enhancements = []
        for j in range(len(self.lookup(new_p))):
            if self.is_degeneration(enh_profile, (new_p,j)):
                enhancements.append(j)
        if len(enhancements) != 1:
            raise RuntimeError("Cannot squish %r at level %r! No unique graph found in %r!" % (enh_profile, l, new_p))
        return (new_p, enhancements[0])

    ### Partial order
    ## The lookup graph gives a partial order on the BICs (the 3-level graph (i,j)
    ## implies i > j).
    @cached_method
    def lies_over (self,i,j):
        """
        Determine if (i,j) is a 3-level graph.
        
        Args:
            i (int): Index of BIC.
            j (int): Index of BIC.
        
        Returns:
            bool: True if (i,j) is a 3-level graph, False otherwise.
        
        EXAMPLES ::

        """
        if j in self.DG.bot_to_bic(i).values():
            assert i in self.DG.top_to_bic(j).values(),\
                "%r is a bottom degeneration of %r, but %r is not a top degeneration of %r!"\
                    % (j,i,i,j)
            return True
        else:
            assert i not in self.DG.top_to_bic(j).values(),\
                "%r is not a bottom degeneration of %r, but %r is a top degeneration of %r!"\
                    % (j,i,i,j)
            return False

    ### Merging profiles (with respect to lies_over)
    @cached_method
    def merge_profiles(self,p,q):
        """
        Merge profiles with respect to the ordering "lies_over".
        
        Args:
            p (iterable): sorted profile
            q (iterable): sorted profile
        
        Returns:
            tuple: sorted profile or None if no such sorted profile exists.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((4,))])
            sage: X.merge_profiles((5,),(5,))
            (5,)
        """
        # input profiles should be sorted:
        assert all(self.lies_over(p[i],p[i+1]) for i in range(len(p)-1)),\
            "Profile %r not sorted!" % (p,)
        assert all(self.lies_over(q[i],q[i+1]) for i in range(len(q)-1)),\
            "Profile %r not sorted!" % (q,)
        new_profile = []
        next_p = 0
        next_q = 0
        while next_p < len(p) and next_q < len(q):
            if p[next_p] == q[next_q]:
                new_profile.append(p[next_p])
                next_p += 1
                next_q += 1
            else:
                if self.lies_over(p[next_p],q[next_q]):
                    new_profile.append(p[next_p])
                    next_p += 1
                else:
                    if self.lies_over(q[next_q],p[next_p]):
                        new_profile.append(q[next_q])
                    else:
                        return None
                    next_q += 1
        # pick up rest (one of these is empty!):
        new_profile += p[next_p:]
        new_profile += q[next_q:]
        return tuple(new_profile)

    ### Better graph lookup:
    ## Here we should really work with "enhanced dominos", because
    ## otherwise it's not clear how the list indices of degenerations are related
    ## to each other.
    ## Therefore, arguments are:
    ##   * a sorted(!) list of BICs, i.e. an element of the lookup_list
    ##   * a (consistent) choice of components of the involved 3-level graph (i.e.
    ##      enhanced dominos)
    ## This can consistently produce a graph.
    ##
    ## For now, we use the workaround to forcably only work with sorted profiles
    ## where the indexing is at least consistent.
    ###

    def lookup_graph(self,bic_list,index=0):
        """
        Return the graph associated to an enhanced profile.

        Note that starting in SAGE 9.0 profile numbering will change between sessions!
        
        Args:
            bic_list (iterable): (sorted!) tuple/list of indices of bics.
            index (int, optional): Index in lookup list. Defaults to 0.

        Returns:
            EmbeddedLevelGraph: graph associated to the enhanced (sorted) profile
                (None if empty).

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: X.lookup_graph(())
            EmbeddedLevelGraph(LG=LevelGraph([2],[[1]],[],{1: 2},[0],True),dmp={1: (0, 0)},dlevels={0: 0})

            Note that an enhanced profile needs to be unpacked with *:

            sage: X.lookup_graph(*X.enhanced_profiles_of_length(2)[0])  # 'unsafe' (edge ordering may change)  # doctest:+SKIP
            EmbeddedLevelGraph(LG=LevelGraph([1, 0, 0],[[1], [2, 3, 4], [5, 6, 7]],[(1, 4), (2, 6), (3, 7)],{1: 0, 2: 0, 3: 0, 4: -2, 5: 2, 6: -2, 7: -2},[0, -1, -2],True),dmp={5: (0, 0)},dlevels={0: 0, -1: -1, -2: -2})

        """
        # this is a bit stupid, but whatever...
        if all(self.lies_over(bic_list[i],bic_list[i+1]) for i in range(len(bic_list)-1)):
            return self.lookup(bic_list)[index]
        else:
            return None
    
    def lookup(self,bic_list, quiet=True):
        """
        Take a profile (i.e. a list of indices of BIC) and return the corresponding
        EmbeddedLevelGraphs (i.e. the product of these BICs).

        Note that this will be a one element list "most of the time", but
        it can happen that this is not irreducible:

        This implementation is not dependent on the order (!) (we look in top and
        bottom degenerations and clutch...)

        However, for caching purposes, it makes sense to use only the sorted profiles...

        NOTE THAT IN PYTHON3 PROFILES ARE NO LONGER DETERMINISTIC!!!!!

        (they typically change with every python session...)

        Args:
            bic_list (iterable): list of indices of bics
        
        Returns:
            list: The list of EmbeddedLevelGraphs corresponding to the profile.

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((4,))])

            This is independent of the order.

            sage: p, _ = X.enhanced_profiles_of_length(2)[0]
            sage: assert any(X.lookup(p)[0].is_isomorphic(G) for G in X.lookup((p[1],p[0])))

            Note that the profile can be empty or reducible.

        """
        if not quiet:
            print("Looking up enhanced profiles in %r..." % (bic_list,))
            sys.stdout.flush()  # MPI computer has congestion issues...
        lookup_key = tuple(bic_list)
        if not bic_list:  # empty
            if not  quiet:
                print("Empty profile, returning smooth_LG. Done.")
                sys.stdout.flush()
            return [self.smooth_LG]
        if len(bic_list) == 1:
            if not  quiet:
                print("BIC, profile irreducible by definition. Done.")
                sys.stdout.flush()
            return [self.bics[bic_list[0]]]
        try:
            cached_list = self._lookup[lookup_key]
            if not quiet:
                print("Using cached lookup. Done.")
                sys.stdout.flush()
            return cached_list
        except KeyError:
            bic_list = list(bic_list)  # in case we are passed a tuple...
            # otherwise, making a copy if we're about to manipulate is also not
            # such a bad idea...
            i = bic_list.pop()  # index in self.bics
            B = self.bics[i]  # this might build bics (!)
            # We split the remainder of bic_list into those coming from
            # degenerations of the top component and those from bottom.
            # Note that these lists will contain their indices in B.top
            # and B.bot, respectively.
            # Moreover, they have to be nested in case there are multiple components.
            top_lists = [[]]
            bot_lists = [[]]
            for j in bic_list:
                if not quiet:
                    print("Looking at BIC %r:" % j, end=' ')
                    sys.stdout.flush()
                # a bic is either in the image of top_to_bic
                # or bot_to_bic.
                # If it isn't in any image, the intersection is empty
                # and we return None.
                # Note that again this might build the maps.
                try:
                    top_bics = self.DG.top_to_bic_inv(i)[j]
                    if not quiet:
                        print("Adding %r BICs from top component to top_lists..." % len(top_bics))
                        sys.stdout.flush()
                    # if there are several components, we "branch out":
                    new_top_lists = []
                    for b in top_bics:
                        for top_list in top_lists:
                            new_top_lists.append(top_list + [b])
                    top_lists = new_top_lists
                except KeyError:
                    try:
                        bot_bics = self.DG.bot_to_bic_inv(i)[j]
                        if not quiet:
                            print("Adding %r BICs from bottom component to bot_lists..." % len(bot_bics))
                            sys.stdout.flush()
                        # if there are several components, we "branch out":
                        new_bot_lists = []
                        for b in bot_bics:
                            for bot_list in bot_lists:
                                new_bot_lists.append(bot_list + [b])
                        bot_lists = new_bot_lists
                    except KeyError:
                        # Intersection empty.
                        return []
            if not quiet:
                print("Done building top_lists and bot_lists.")
                print("This gives us %r profiles in %s and %r profiles in %s that we will now clutch pairwise and recursively." % \
                        (len(top_lists), B.top, len(bot_lists), B.bot))
                sys.stdout.flush()
            graph_list = [admcycles.diffstrata.stratatautring.clutch(
                    self,
                    top,
                    bot,
                    B.clutch_dict,
                    B.emb_top,
                    B.emb_bot
                )   
                for top_list, bot_list in itertools.product(top_lists,bot_lists)
                for top in B.top.lookup(top_list, quiet=quiet)
                for bot in B.bot.lookup(bot_list, quiet=quiet)
            ]
            # we might have picked up isomorphic guys (e.g. v-graph)
            if not quiet:
                print("For profile %r in %s, we have thus obtained %r graphs." %\
                    (bic_list, self, len(graph_list)))
                print("Sorting these by isomorphism class...", end=' ')
                sys.stdout.flush()
            rep_list = admcycles.diffstrata.bic.isom_rep(graph_list)
            self._lookup[lookup_key] = rep_list
            if not quiet:
                print("Done. Found %r isomorphism classes." % len(rep_list))
                sys.stdout.flush()  # MPI computer has congestion issues...
            return rep_list

    @cached_method
    def sub_graph_from_level(self,enh_profile,l,direction='below',return_split_edges=False):
        """
        Extract an EmbeddedLevelGraph from the subgraph of enh_profile that is either 
        above or below level l.

        This is embedded into the top/bottom component of the bic at profile[l-1].
        In particular, this is a 'true' sub graph, i.e. the names of the vertices and
        legs are the same as in enh_profile.

        Note: For l==0 or l==number_of_levels we just return enh_profile.
        
        Args:
            l (int): (relative) level number.
            direction (str, optional): 'above' or 'below'. Defaults to 'below'.
            return_split_edges (bool, optional. Defaults to False): also return a tuple
                of the edges split across level l.
        
        Returns:
            EmbeddedLevelGraph: Subgraph of top/bottom component of the bic at profile[l-1].

            If return_split_edges=True: Returns tuple (G,e) where
                * G is the EmbeddedLevelGraph
                * e is a tuple of edges of enh_profile that connect legs above level
                    l with those below (i.e. those edges needed for clutching!)
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: ep = X.enhanced_profiles_of_length(2)[0]
            sage: X.sub_graph_from_level(ep, 1, 'above') 
            EmbeddedLevelGraph(LG=LevelGraph([1],[[1]],[],{1: 0},[0],True),dmp={1: (0, 0)},dlevels={0: 0})
            sage: X.sub_graph_from_level(ep, 1, 'below')  # 'unsafe' (edge order might change)  # doctest:+SKIP
            EmbeddedLevelGraph(LG=LevelGraph([0, 0],[[2, 3, 4], [5, 6, 7]],[(2, 6), (3, 7)],{2: 0, 3: 0, 4: -2, 5: 2, 6: -2, 7: -2},[-1, -2],True),dmp={5: (0, 0), 4: (0, 1)},dlevels={-1: -1, -2: -2})
            sage: X.bics[ep[0][0]].top
            LevelStratum(sig_list=[Signature((0,))],res_cond=[],leg_dict={1: (0, 0)})
            sage: X.bics[ep[0][1]].bot
            LevelStratum(sig_list=[Signature((2, -2, -2))],res_cond=[[(0, 1), (0, 2)]],leg_dict={3: (0, 0), 4: (0, 1), 5: (0, 2)})
        """
        G = self.lookup_graph(*enh_profile)
        if l == 0:
            if direction == 'below':
                if return_split_edges:
                    return (G,tuple())
                return G
            if return_split_edges:
                return (None,tuple())
            return None
        if l == G.number_of_levels:
            if direction == 'above':
                if return_split_edges:
                    return (G,tuple())
                return G
            if return_split_edges:
                return (None,tuple())
            return None
        profile, _i = enh_profile
        # The BIC that will give us the level is BIC l-1 in the profile:
        bic_number = profile[l-1]
        B = self.bics[bic_number]
        # We extract the subgraph from the underlying LevelGraph, so we have
        # to work with the internal level numbering:
        internal_l = G.LG.internal_level_number(l)
        # Actually only three things depend on above/below:
        # * The choice of vertices in the subgraph.
        # * The choice of level to embed into (top/bottom of B).
        # * The new level dictionary (as extracting does not change the levels,
        #   this just consists of the releveant part of G.dlevels)
        # Note that in the 'below' case we consider levels <= l, while in 'above'
        # we consider > l (we want to cut level passage l!)
        if direction == 'below':
            new_vertices = [v for v in range(len(G.LG.genera)) 
                                if G.LG.levelofvertex(v) <= internal_l]
            # in this case, the level we want to embed into is the bottom of B
            L = B.bot
            # the levels <= internal_l survive into dlevels
            new_dlevels = {k:v for k,v in G.dlevels.items() if k <= internal_l}
        else:
            assert direction == 'above'
            new_vertices = [v for v in range(len(G.LG.genera)) 
                                if G.LG.levelofvertex(v) > internal_l]
            # in this case, the level we want to embed into is the top of B
            L = B.top
            # the levels >= internal_l survive into dlevels
            new_dlevels = {k:v for k,v in G.dlevels.items() if k > internal_l}
        vertex_set = set(new_vertices)
        new_edges = [e for e in G.LG.edges 
                        if G.LG.vertex(e[0]) in vertex_set and \
                            G.LG.vertex(e[1]) in vertex_set]
        new_LG = G.LG.extract(new_vertices,new_edges)
        leg_set = set(flatten(new_LG.legs))
        # Next, we take the part of dmp that we still need:
        # Note that G.dmp maps legs of G to points of X, but we want is a map
        # to points of L.
        # We get this from the following observation:
        # We have
        # * L.leg_dict: points of B -> points of L
        # * B.dmp_inv: points of X -> points of B
        # Therefore the composition gives the desired map
        #   points of G -> points of L
        new_dmp = {k : L.leg_dict[B.dmp_inv[v]]
                    for k, v in G.dmp.items() if k in leg_set}
        # The only thing missing is to add the marked points of the edges
        # that we have cut:
        # We do this in no particular order, as the clutching information will
        # have to be retrieved anyways when actually splitting the graph.
        # Note that != is boolean xor (!)
        split_edges = [e for e in G.LG.edges 
                            if (e[0] in leg_set) != (e[1] in leg_set)]
        split_half_edges = [e[0] if e[0] in leg_set else e[1]
                                for e in split_edges]
        # To place these into new_dmp, we pick an undegeneration map G -> B
        # Note that the choice of map *should* not matter, as they should differ
        # only by an automorphism of B... (except for psi classes, where we have
        # to be careful with xi_on_level!!!)
        B_to_G = self.explicit_leg_maps(((bic_number,),0),enh_profile,only_one=True)
        assert B_to_G  # G is actually a degeneration of B!
        G_to_B = {v : k for k, v in B_to_G.items()}
        # check the points we already placed are consistent:
        assert all(L.leg_dict[G_to_B[leg]] == new_dmp[leg] for leg in new_dmp)
        while split_half_edges:
            leg = split_half_edges.pop()
            new_dmp[leg] = L.leg_dict[G_to_B[leg]]
        # some more checks:
        legs_in_new_edges = set(flatten(new_edges))
        marked_points = set(new_dmp.keys())
        assert legs_in_new_edges.isdisjoint(marked_points)
        assert leg_set == (legs_in_new_edges | marked_points)
        sub_graph = EmbeddedLevelGraph(L,new_LG,new_dmp,new_dlevels)
        if return_split_edges:
            return (sub_graph, tuple(split_edges))
        return sub_graph

    # @cached_method
    def split_graph_at_level(self,enh_profile,l):
        """
        Splits enh_profile self into top and bottom component at level l.

        (Note that the 'cut' occurs right above level l, i.e. to get the top level
        and the rest, l should be 1! (not 0))

        The top and bottom components are EmbeddedLevelGraphs, embedded into
        top and bottom of the corresponding BIC (obtained via sub_graph_from_level).

        The result is made so that it can be fed into clutch.
        
        Args:
            enh_profile (tuple): enhanced profile.
            l (int): (relative) level of enh_profile.

        Returns:
            dict: dictionary consising of
                * X:            GeneralisedStratum self.X
                * top:          EmbeddedLevelGraph: top component
                * bottom:       EmbeddedLevelGraph: bottom component
                * clutch_dict:  clutching dictionary mapping ex-half-edges on 
                        top to their partners on bottom (both as points in the 
                        respective strata via dmp!)
                * emb_dict_top: a dictionary embedding top into the stratum of self
                * emb_dict_bot: a dictionary embedding bot into the stratum of self
                * leg_dict:     a dictionary legs of enh_profile -> legs of top/bottom
        
        Note that clutch_dict, emb_top and emb_bot are dictionaries between 
        points of strata, i.e. after applying dmp to the points!

        EXAMPLES ::

            In particular, we can use this to "glue" the BICs of 10^top into (10,9,6) and
            obtain all components of the profile.

        """
        # Split the graph into top and bottom components at level l:
        top_graph, se_top = self.sub_graph_from_level(enh_profile,l,direction='above',return_split_edges=True)
        bot_graph, se_bot = self.sub_graph_from_level(enh_profile,l,direction='below',return_split_edges=True)
        assert se_top == se_bot
        split_edges = se_top
        # We construct the clutching info by splitting the BIC that corresponds
        # to level l:
        p, _i = enh_profile
        # TODO: edge cases
        B = self.bics[p[l-1]]
        clutching_info = B.split()
        # we simply replace the top and bottom components of B by our graphs:
        assert clutching_info['top'] == top_graph.X == B.top
        clutching_info['top'] = top_graph
        assert clutching_info['bottom'] == bot_graph.X == B.bot
        clutching_info['bottom'] = bot_graph
        # the clutch_dict has to be replaced by the split_edges:
        # Note that these are currently edges of enh_profile, so they need to be
        # translated to points on the corresponding stratum via the embedding
        # of top_graph/bot_graph:
        # WARNING: We use here (once again) implicitly that e[0] is above e[1]!
        clutching_info['clutch_dict'] = {top_graph.dmp[e[0]] : bot_graph.dmp[e[1]]
                                            for e in split_edges}
        return clutching_info

    # @cached_method
    def doublesplit(self,enh_profile):
        """
        Splits embedded 3-level graph into top, middle and bottom component, along with
        all the information required (by clutch) to reconstruct self.

        We return a dictionary so that the result can be fed into clutch (naming of 
        optional arguments...)

        This is mainly a technical backend for doublesplit_graph_before_and_after_level.

        Note that in contrast to EmbeddedLevelGraph.split, we want to feed a length-2-profile 
        so that we can really split into the top and bottom of the associated BICs (the only
        strata we can control!)
        
        This method is mainly intended for being fed into clutch.

        Args:
            enh_profile (tuple): enhanced profile.

        Raises:
            ValueError: Raised if self is not a 3-level graph.
        
        Returns:
            dict: A dictionary consisting of:
                X:                  GeneralisedStratum self,
                top:                LevelStratum top level of top BIC, 
                bottom:             LevelStratum bottom level of bottom BIC, 
                middle:             LevelStratum level -1 of enh_profile,
                emb_dict_top:       dict: points of top stratum -> points of X, 
                emb_dict_bot:       dict: points of bottom stratum -> points of X, 
                emb_dict_mid:       dict: points of middle stratum -> points of X,
                clutch_dict:        dict: points of top stratum -> points of middle stratum, 
                clutch_dict_lower:  dict: points of middle stratum -> points of bottom stratum,
                clutch_dict_long:   dict: points of top stratum -> points of bottom stratum.

        EXAMPLES ::


        Long edges work.

        """
        p, i = enh_profile
        if not len(p) == 2:
            raise ValueError("Error: Not a 3-level graph! %r" % self)
        G = self.lookup_graph(p,i)
        # Here it is important that we pick top and bot of the corresponding BICs and identify them with
        # level(0) and level(2) of G (as these might not be the same (e.g. switched components!)!)
        top = self.bics[p[0]].top  
        middle = G.level(1)
        bottom = self.bics[p[1]].bot
        # To construct the embedding dictionaries, we have to identify legs of G
        # with (stratum) points of top/middle/bottom as keys and points on self as
        # values.
        #
        # The values (points on self) are given by G.dmp.
        #
        # The keys for middle are given via leg_dict.
        # 
        # For top and bottom, we have to first fix a map from G to 
        # p[0] and p[1] and then combine self.dmp with the leg_dicts of the LevelStrata.
        # It *shouldn't* matter, which undegeneration we take:
        top_to_G = self.explicit_leg_maps(((p[0],),0),enh_profile,only_one=True)
        G_to_top = {v : k for k, v in top_to_G.items()}
        bot_to_G = self.explicit_leg_maps(((p[1],),0),enh_profile,only_one=True)     
        G_to_bot = {v : k for k, v in bot_to_G.items()}   
        # More precisely: We now have the following maps (e.g. for top):
        # 
        #   G_to_top: points in G -> points in p[0]
        #   top.leg_dict: points in p[0] -> stratum points of top
        #
        # and
        #
        #   top.leg_dict_inv: stratum points of top -> points in p[0]
        #   top_to_G: points in p[0] -> points in G
        #   G.dmp: points in G -> stratum points on self
        # 
        # i.e. emb_top is the composition of the inverse of the leg_dict
        # of top, i.e. top.stratum_number, with top_to_G and G.dmp
        # (giving a map from the points of top to the points of self)
        # and the same for middle and bottom.
        #
        # We implement this by iterating over the marked points of G on top level,
        # which are exactly the keys of G.dmp that are on top level.
        #
        # For this, we have to compose with G_to_top and top.leg_dict again.
        #
        # Note that we make extra sure that we didn't mess up the level numbering by
        # using the relative level numbering (where the top level is guaranteed to be 0,
        # the middle is 1 and the bottom level is 2 (positive!)).
        emb_dict_top = {top.leg_dict[G_to_top[l]] : G.dmp[l]
                            for l in iter(G.dmp)
                                if G.LG.level_number(G.LG.levelofleg(l)) == 0}
        emb_dict_mid = {middle.leg_dict[l] : G.dmp[l]
                            for l in iter(G.dmp)
                                if G.LG.level_number(G.LG.levelofleg(l)) == 1}
        emb_dict_bot = {bottom.leg_dict[G_to_bot[l]] : G.dmp[l]
                            for l in iter(G.dmp)
                                if G.LG.level_number(G.LG.levelofleg(l)) == 2}
        # Because this is a 3-level graph, all edges of self are cut in this process
        # and this gives us exactly the dictionary we must remember:
        # Note however, that we have to check if the edge connects top - middle, middle - bottom
        # or top - bottom.
        # Note that all these dictionaries map points of GeneralisedStrata to each
        # other so we must take the corresponding stratum_number!
        clutch_dict = {}
        clutch_dict_lower = {}
        clutch_dict_long = {}
        # If the edges are not sorted with e[0] above e[1], we complain.
        for e in G.LG.edges:
            if G.LG.level_number(G.LG.levelofleg(e[0])) == 0:
                if G.LG.level_number(G.LG.levelofleg(e[1])) == 1:
                    clutch_dict[top.stratum_number(G_to_top[e[0]])] = middle.stratum_number(e[1])
                else:
                    assert G.LG.level_number(G.LG.levelofleg(e[1])) == 2
                    clutch_dict_long[top.stratum_number(G_to_top[e[0]])] = bottom.stratum_number(G_to_bot[e[1]])
            else:
                assert G.LG.level_number(G.LG.levelofleg(e[0])) == 1
                assert G.LG.level_number(G.LG.levelofleg(e[1])) == 2
                clutch_dict_lower[middle.stratum_number(e[0])] = bottom.stratum_number(G_to_bot[e[1]])
        return {'X': self, 'top': top, 'bottom': bottom, 'middle': middle,
                'emb_dict_top': emb_dict_top, 'emb_dict_mid': emb_dict_mid, 'emb_dict_bot': emb_dict_bot,
                'clutch_dict': clutch_dict, 'clutch_dict_lower': clutch_dict_lower, 'clutch_dict_long': clutch_dict_long}

    @cached_method
    def three_level_profile_for_level(self,enh_profile,l):
        """
        Find the 3-level graph that has level l of enh_profile as its middle level.
        
        Args:
            enh_profile (tuple): enhanced profile
            l (int): (relative) level number
        
        Raises:
            RuntimeError: raised if no unique (or no) 3-level graph is found.
        
        Returns:
            tuple: enhanced profile of the 3-level graph.
        
        EXAMPLES ::

        """
        profile, _ = enh_profile
        three_level_profile = (profile[l-1],profile[l])
        # in case this is reducible, we have to find the correct enhanced profile:
        possible_enhancements = len(self.lookup(three_level_profile))
        assert possible_enhancements > 0, "No 3-level graph for subprofile %r of %r found!" % (three_level_profile, profile)
        enhancements = []
        for i in range(possible_enhancements):
            if self.is_degeneration(enh_profile,(three_level_profile,i)):
                enhancements.append(i)
        if len(enhancements) != 1:
            raise RuntimeError("No unique 3-level undegeneration in %r around level %r! %r" % (three_level_profile, l, enhancements))
        return (three_level_profile,enhancements[0])

    # @cached_method
    def doublesplit_graph_before_and_after_level(self,enh_profile,l):
        """
        Split the graph enh_profile directly above and below level l.

        This can be used for gluing an arbitrary degeneration of level l into enh_profile.

        The result is made so that it can be fed into clutch.
        
        To ensure compatibility with top/bot/middle_to_bic when gluing, we have
        to make sure that everything is embedded into the "correct" generalised strata.

        We denote the 3-level graph around level l by H.

        Then the top part will be embedded into the top of the top BIC of H,
        the bottom part will be embedded into the bot of the bottom BIC of H
        and the middle will be the middle level of H.

        For a 3-level graph is (almost) equivalent to doublesplit(), the only difference
        being that here we return the 0-level graph for each level.

        Args:
            enh_profile (tuple): enhanced profile.
            l (int): (relative) level of enh_profile.

        Raises:
            ValueError: Raised if l is 0 or lowest level.
            RuntimeError: Raised if we don't find a unique 3-level graph around l.
        
        Returns:
            dict: A dictionary consisting of:
                X:                  GeneralisedStratum self.X,
                top:                LevelStratum top level of top BIC of H, 
                bottom:             LevelStratum bottom level of bottom BIC of H, 
                middle:             LevelStratum middle level of H,
                emb_dict_top:       dict: points of top stratum -> points of X, 
                emb_dict_bot:       dict: points of bottom stratum -> points of X, 
                emb_dict_mid:       dict: points of middle stratum -> points of X,
                clutch_dict:        dict: points of top stratum -> points of middle stratum, 
                clutch_dict_lower:  dict: points of middle stratum -> points of bottom stratum,
                clutch_dict_long:   dict: points of top stratum -> points of bottom stratum.

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((4,))])
            sage: assert all(clutch(**X.doublesplit_graph_before_and_after_level(ep,l)).is_isomorphic(X.lookup_graph(*ep)) for levels in range(3,X.dim()+1) for ep in X.enhanced_profiles_of_length(levels-1) for l in range(1,levels-1))
            sage: X=GeneralisedStratum([Signature((2,2,-2))])
            sage: assert all(clutch(**X.doublesplit_graph_before_and_after_level(ep,l)).is_isomorphic(X.lookup_graph(*ep)) for levels in range(3,X.dim()+2) for ep in X.enhanced_profiles_of_length(levels-1) for l in range(1,levels-1))  # long time
        """
        p, i = enh_profile
        if l == 0 or l == len(p) + 1:
            raise ValueError("Doublesplit must occur at 'inner' level! %r" % l)
        G = self.lookup_graph(p,i)
        # Split the graph into top and bottom components around level l:
        top_graph, se_top = self.sub_graph_from_level(enh_profile,l,direction='above',return_split_edges=True)
        bot_graph, se_bot = self.sub_graph_from_level(enh_profile,l+1,direction='below',return_split_edges=True)
        # We construct the clutching info by splitting the 3-level graph around l
        # Note that the middle level is really the same as that of enh_profile (that's 
        # why we have to care about components of the profile here), but the leg
        # numbering might be different, so we still have to work with an undegeneration map:
        t_l_enh_profile = self.three_level_profile_for_level(enh_profile,l)
        clutching_info = self.doublesplit(t_l_enh_profile)
        assert top_graph.X == clutching_info['top']
        assert bot_graph.X == clutching_info['bottom']
        L = clutching_info['middle']
        assert L == self.lookup_graph(*t_l_enh_profile).level(1)
        # we simply replace the top and bottom components of B by our graphs:
        clutching_info['top'] = top_graph
        clutching_info['bottom'] = bot_graph
        # Now we have to match up the edges:
        # Note that se_top consists of the edges connecting top_graph to any vertex
        # on or below level l
        # We therefore start by distinguishing those edges ending on level l from the others
        # (long edges):
        # WARNING: We use here (once again) implicitly that e[0] is above e[1]!
        top_to_l = []
        top_to_bot = []
        for e in se_top:
            if G.LG.level_number(G.LG.levelofleg(e[1])) == l:
                top_to_l.append(e)
            else:
                top_to_bot.append(e)
        # the same for se_bot:
        bot_to_l = []
        bot_to_top = []
        for e in se_bot:
            if G.LG.level_number(G.LG.levelofleg(e[0])) == l:
                bot_to_l.append(e)
            else:
                bot_to_top.append(e)
        assert set(top_to_bot) == set(bot_to_top)
        # Translating the edges into points on the strata immediately gives the
        # three clutching dictionaries:
        # Note that instead of directly using leg_dict for the middle level, 
        # we first pick an undegeneration map to the 3-level graph and compose
        # with (the inverse of) that:
        middle_leg_map = self.explicit_leg_maps(t_l_enh_profile,enh_profile,only_one=True)
        ep_to_m = {v : k for k, v in middle_leg_map.items()}
        # WARNING: We use here (once again) implicitly that e[0] is above e[1]!
        clutching_info['clutch_dict'] = {top_graph.dmp[e[0]] : L.leg_dict[ep_to_m[e[1]]]
                                            for e in top_to_l}
        clutching_info['clutch_dict_lower'] = {L.leg_dict[ep_to_m[e[0]]] : bot_graph.dmp[e[1]]
                                            for e in bot_to_l}
        clutching_info['clutch_dict_long'] = {top_graph.dmp[e[0]] : bot_graph.dmp[e[1]]
                                            for e in top_to_bot}
        return clutching_info

    # @cached_method
    def splitting_info_at_level(self,enh_profile,l):
        """
        Retrieve the splitting and embedding dictionaries for splitting at level l,
        as well as the level in 'standard form', i.e. as either:
            * a top of a BIC
            * a bot of a BIC
            * a middle of a 3-level graph

        This is essentially only a frontend for split_graph_at_level and
        doublesplit_graph_before_and_after_level and saves us the annoying
        case distinction.

        This is important, because when we glue we should *always* use the
        dmp's of the splitting dictionary, which can (and will) be different
        from leg_dict of the level!
        
        Args:
            enh_profile (tuple): enhanced profile
            l (int): (relative) level number
        
        Returns:
            tuple: (splitting dict, leg_dict, level) where
                splitting dict is the splitting dictionary:
                * X:            GeneralisedStratum self.X
                * top:          EmbeddedLevelGraph: top component
                * bottom:       EmbeddedLevelGraph: bottom component
                * clutch_dict:  clutching dictionary mapping ex-half-edges on 
                        top to their partners on bottom (both as points in the 
                        respective strata via dmp!)
                * emb_dict_top: a dictionary embedding top into the stratum of self
                * emb_dict_bot: a dictionary embedding bot into the stratum of self

                leg_dict is the dmp at the current level (to be used instead
                of leg_dict of G.level(l)!!!)

                and level is the 'standardised' LevelStratum at l (as described above).
        
        Note that clutch_dict, emb_top and emb_bot are dictionaries between 
        points of strata, i.e. after applying dmp to the points!

        """
        profile, _ = enh_profile
        # For this, we have to distinguish again, if we're gluing into the middle 
        # (two cuts) or at one end of the profile (1 cut):
        if l == 0:
            d = self.split_graph_at_level(enh_profile,1)
            assert d['top'].is_isomorphic(d['top'].X.smooth_LG)
            return d, d['top'].dmp, d['top'].X
        if l == len(profile):
            d = self.split_graph_at_level(enh_profile,l)
            assert d['bottom'].is_isomorphic(d['bottom'].X.smooth_LG)
            return d, d['bottom'].dmp, d['bottom'].X
        d = self.doublesplit_graph_before_and_after_level(enh_profile,l)
        three_level_profile = self.three_level_profile_for_level(enh_profile,l)
        assert self.lookup_graph(*three_level_profile).level(1) == d['middle']
        # for the middle level, we have to use the undegeneration map to
        # the 3-level graph:
        middle_leg_map = self.explicit_leg_maps(three_level_profile,enh_profile,only_one=True)
        L_to_m = {v : d['middle'].leg_dict[k] for k, v in middle_leg_map.items() 
                            if k in d['middle'].leg_dict}
        return d, L_to_m, d['middle']

    @cached_method
    def enhanced_profiles_of_length(self,l,quiet=True):
        """
        A little helper for generating all enhanced profiles in self of a given length.
        
        Args:
            l (int): length (codim) of profiles to be generated.
        
        Returns:
            tuple: tuple of enhanced profiles
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((4,))
            sage: len(X.lookup_list[2])
            17
            sage: len(X.enhanced_profiles_of_length(2))
            19

        """
        if not quiet:
            print('Generating enhanced profiles of length %r...' % l)
            sys.stdout.flush()
        if l >= len(self.lookup_list):
            return tuple()
        ep_list = []
        for c, p in enumerate(self.lookup_list[l]):
            if not quiet:
                print('Building all graphs in %r (%r/%r)...' % (p, c+1, len(self.lookup_list[l])))
                sys.stdout.flush()
            for i in range(len(self.lookup(p, quiet=True))):  # quiet=False gives A LOT of output here...
                ep_list.append((p,i))
        return tuple(ep_list)

    #########################################################
    #### Checks
    #########################################################

    def check_dims(self,codim=None,quiet=False):
        """
        Check if, for each non-horizontal level graph of codimension codim 
        the dimensions of the levels add up to the dimension of the level graph 
        (dim of stratum - codim).

        If codim is ommitted, check the entire stratum.

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((1,1))])
            sage: X.check_dims()
            Codimension 0 Graph 0: Level sums ok!
            Codimension 1 Graph 0: Level sums ok!
            Codimension 1 Graph 1: Level sums ok!
            Codimension 1 Graph 2: Level sums ok!
            Codimension 1 Graph 3: Level sums ok!
            Codimension 2 Graph 0: Level sums ok!
            Codimension 2 Graph 1: Level sums ok!
            Codimension 2 Graph 2: Level sums ok!
            Codimension 2 Graph 3: Level sums ok!
            Codimension 3 Graph 0: Level sums ok!
            True

            sage: X=GeneralisedStratum([Signature((4,))])
            sage: X.check_dims(quiet=True)
            True

            sage: X=GeneralisedStratum([Signature((10,0,-10))])
            sage: X.check_dims()
            Codimension 0 Graph 0: Level sums ok!
            Codimension 1 Graph 0: Level sums ok!
            Codimension 1 Graph 1: Level sums ok!
            Codimension 1 Graph 2: Level sums ok!
            Codimension 1 Graph 3: Level sums ok!
            Codimension 1 Graph 4: Level sums ok!
            Codimension 1 Graph 5: Level sums ok!
            Codimension 1 Graph 6: Level sums ok!
            Codimension 1 Graph 7: Level sums ok!
            Codimension 1 Graph 8: Level sums ok!
            Codimension 1 Graph 9: Level sums ok!
            Codimension 1 Graph 10: Level sums ok!
            Codimension 1 Graph 11: Level sums ok!
            True

            sage: X=GeneralisedStratum([Signature((2,2,-2))])
            sage: X.check_dims(quiet=True)  # long time (3 seconds)
            True
        """
        return_value = True
        if codim is None:
            codims = range(self.dim())
        else:
            codims = [codim]
        for c in codims:
            for i,emb_g in enumerate(self.all_graphs[c]):
                g = emb_g.LG
                dimsum = 0
                if not quiet:
                    print("Codimension", c, "Graph", repr(i) + ":", end=" ")
                for l in range(g.numberoflevels()):
                    L = g.stratum_from_level(l)
                    if L.dim() == -1:
                        if quiet:
                            print("Codimension", c, "Graph", repr(i) + ":", end=" ")
                        print("Error: Level", l, "is of dimension -1!")
                        return_value = False
                    dimsum += L.dim()
                if dimsum != self.dim() - c:
                    if quiet:
                        print("Codimension", c, "Graph", repr(i) + ":", end=" ")
                    print("Error: Level dimensions add up to", dimsum, "not", self.dim() - c, "!")
                    return_value = False
                else:
                    if not quiet:
                        print("Level sums ok!")
        return return_value

    ###########
    ### Chern class calculation:
    def psi(self,leg):
        """
        CURRENTLY ONLY ALLOWED FOR CONNECTED STRATA!!!!

        The psi class on the open stratum at leg.
        
        Args:
            leg (int): leg number (as index of signature, not point of stratum!!!)
        
        Returns:
            ELGTautClass: Tautological class associated to psi.
        """
        psi = self.additive_generator([tuple(),0],{leg:1})
        return psi.as_taut()

    # @cached_method
    def taut_from_graph(self,profile,index=0):
        """
        Tautological class from the graph with enhanced profile (profile, index).
        
        Args:
            profile (iterable): profile
            index (int, optional): Index of profile. Defaults to 0.
        
        Returns:
            ELGTautClass: Tautological class consisting just of this one graph.
        
        EXAMPLES ::

        """
        return self.additive_generator((tuple(profile),index)).as_taut()

    def ELGsum(self, L):
        """
        Sum of tautological classes.

        This is generally faster than += (i.e. sum()), because reduce is only called
        once at the end and not at every step.
        
        Args:
            L (iterable): Iterable of ELGTautClasses on self.
        
        Returns:
            ELGTautClass: Sum over input classes.
        """
        new_psi_list = []
        for T in L:
            if T == 0:
                continue
            new_psi_list.extend(T.psi_list)
        return ELGTautClass(self, new_psi_list)

    def pow(self, T, k, amb=None):
        """
        Calculate T^k with ambient amb.
        
        Args:
            T (ELGTautClass): Tautological class on self.
            k (int): positive integer.
            amb (tuple, optional): enhanced profile. Defaults to None.
        
        Returns:
            ELGTautClass: T^k in CH(amb).
        """
        if amb is None:
            amb = ((), 0)
            ONE = self.ONE
        else:
            ONE = self.taut_from_graph(*amb)
        prod = ONE
        for _ in range(k):
            prod = self.intersection(prod, T, amb)
        return prod

    def exp(self,T,amb=None,quiet=True,prod=True,stop=None):
        """
        (Formal) exp of a Tautological Class.

        This is done (by default) by calculating exp of every AdditiveGenerator
        (which is cached) and calculating the product of these.

        Alternatively, prod=False computes sums of powers of T.
        
        Args:
            T (ELGTautClass): Tautological Class on X.
        
        Returns:
            ELGTautClass: Tautological Class on X.
        """
        N = self.dim()
        if amb is None:
            amb = ((), 0)
        if not prod:
            if not quiet:
                print("Calculating exp of %s..." % T)
            def _status(i):
                # primitive, but whatever
                if not quiet:
                    print("Calculating power %r..." % i)
                return 1
            return self.ELGsum([_status(i) * QQ(1)/QQ(factorial(i)) * self.pow(T,i,amb) for i in range(N+1)])
        # Calculate instead product of exp(AG):
        e = self.taut_from_graph(*amb)
        if not quiet:
            print("Calculating exp as product of %r factors..." % len(T.psi_list), end=' ')
            sys.stdout.flush()
        for c, AG in T.psi_list:
            f = AG.exp(c, amb, stop)
            if f == 0 or f == self.ZERO:
                return self.ZERO
            e = self.intersection(e, f, amb)
        if not quiet:
            print('Done!')
        return e

    @cached_method
    def exp_bic(self, i):
        l = self.bics[i].ell
        AG = self.additive_generator(((i,),0))
        return AG.exp(l, amb=None) - self.ONE

    def td_contrib(self,l,T,amb=None):
        """
        (Formal) td^-1 contribution, i.e. (1-exp(-l*T))/T.
        
        Args:
            l (int): weight
            T (ELGTautClass): Tautological class on self.
        
        Returns:
            ELGTautClass: Tautological class on self.
        """
        N = self.dim()
        if amb is None:
            amb = ((), 0)
        return self.ELGsum([QQ(-l)**k/QQ(factorial(k+1)) * self.pow(T,k,amb) for k in range(N+1)])
    
    @property
    def xi(self):
        """
        xi of self in terms of psi and BICs according to Sauvaget's formula.

        Note that we first find an "optimal" leg.

        Returns:
            ELGTautClass: psi class on smooth stratum + BIC contributions (all
                    with multiplicities...)

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: print(X.xi)  # 'unsafe' (order of summands might change) # doctest:+SKIP
            Tautological class on Stratum: (2,)
            with residue conditions: []
            <BLANKLINE>
            3 * Psi class 1 with exponent 1 on level 0 * Graph ((), 0) +
            -1 * Graph ((0,), 0) +
            -1 * Graph ((1,), 0) +
            <BLANKLINE>
        """
        try:
            return self._xi 
        except AttributeError:
            self._xi = self.xi_with_leg(quiet=True)
            return self._xi

    @cached_method
    def xi_pow(self,n):
        """
        Cached method for calculating powers of xi.
        
        Args:
            n (int): non-negative integer (exponent)
        
        Returns:
            ELGTautClass: xi^n
        """
        if n == 0:
            return self.ONE
        return self.xi * self.xi_pow(n-1)

    @cached_method
    def xi_with_leg(self,leg=None,quiet=True,with_leg=False):
        """
        xi class of self expressed using Sauvaget's relation (with optionally a choice of leg)
        
        Args:
            leg (tuple, optional): leg on self, i.e. tuple (i,j) for the j-th element 
                of the signature of the i-th component. Defaults to None. In this case,
                an optimal leg is chosen.
            quiet (bool, optional): No output. Defaults to False.
            with_leg (bool, optional): Return choice of leg. Defaults to False.
        
        Returns:
            ELGTautClass: xi in terms of psi and bics according to Sauvaget.
            (ELGTautClass, tuple): if with_leg=True, where tuple is the corresponding
                leg on the level i.e. (component, signature index) used.
        
        EXAMPLES ::

            In the stratum (2,-2) the pole is chosen by default (there is no 'error term'):

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,-2))
            sage: print(X.xi)
            Tautological class on Stratum: (2, -2)
            with residue conditions: []
            <BLANKLINE>
            -1 * Psi class 2 with exponent 1 on level 0 * Graph ((), 0) +
            <BLANKLINE>
            sage: print(X.xi_with_leg(leg=(0,1)))
            Tautological class on Stratum: (2, -2)
            with residue conditions: []
            <BLANKLINE>
            -1 * Psi class 2 with exponent 1 on level 0 * Graph ((), 0) +
            <BLANKLINE>

            We can specify the zero instead and pick up the extra divisor:

            sage: print(X.xi_with_leg(leg=(0,0)))  # 'unsafe' (order of summands might change) # doctest:+SKIP
            Tautological class on Stratum: (2, -2)
            with residue conditions: []
            <BLANKLINE>
            3 * Psi class 1 with exponent 1 on level 0 * Graph ((), 0) +
            -1 * Graph ((0,), 0) +
            <BLANKLINE>
        """
        if not quiet:
            print("Applying Sauvaget's relation to express xi for %r..." % self)
        if leg is None:
            # choose a "good" leg:
            l, k, bot_bic_list = self._choose_leg_for_sauvaget_relation(quiet)
        else:
            l = leg
            k = self._sig_list[l[0]].sig[l[1]]
            bot_bic_list = self.bics_with_leg_on_bottom(l)
        # find internal leg number on smooth graph correspoding to l:
        G = self.lookup_graph(tuple())
        internal_leg = G.dmp_inv[l]  # leg number on graph
        xi = (k+1) * self.psi(internal_leg)
        add_gens = [self.additive_generator([(b,),0]) for b in bot_bic_list]
        self._xi = xi + ELGTautClass(self, [(-self.bics[bot_bic_list[i]].ell, AG) \
                                for i, AG in enumerate(add_gens)])
        # self._xi = xi + sum([QQ(1)/QQ(AG.stack_factor)*AG.as_taut() \
        #                         for i, AG in enumerate(add_gens)])
        if with_leg:
            return (self._xi,l)
        else:
            return self._xi

    def _choose_leg_for_sauvaget_relation(self,quiet=True):
        """
        Choose the best leg for Sauvaget's relation, i.e. the one that appears on bottom
        level for the fewest BICs.

        Returns:
            tuple: tuple (leg, order, bic_list) where:
                * leg (tuple), as a tuple (number of conn. comp., index of the signature tuple),
                * order (int) the order at leg, and
                * bic_list (list of int) is a list of indices of self.bics where leg
                    is on bottom level.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,-2))
            sage: X._choose_leg_for_sauvaget_relation()
            ((0, 1), -2, [])

            In the minimal stratum, we always find all BICS:

            sage: X=Stratum((2,))
            sage: X._choose_leg_for_sauvaget_relation()
            ((0, 0), 2, [0, 1])
        """
        best_case = len(self.bics)
        best_leg = -1
        # points of the stratum are best accessed through the embedding of the smooth graph:
        # (we sort for better testing...)
        leg_list = sorted(list(self.smooth_LG.dmp_inv.keys()), key=lambda x:x[1])
        for l in leg_list:
            bot_list = self.bics_with_leg_on_bottom(l)
            # none is best we can do:
            if not bot_list:
                order = self._sig_list[l[0]].sig[l[1]]
                if not quiet:
                    print("Choosing leg %r (of order %r) because it never appears on bottom level." 
                            % (l, order))
                return (l,order,[])
            on_bottom = len(bot_list)
            if on_bottom <= best_case:
                best_case = on_bottom
                best_leg = l
                best_bot_list = bot_list[:]  # copy!
        assert best_leg != -1, "No best leg found for %r!" % self
        order = self._sig_list[best_leg[0]].sig[best_leg[1]]
        if not quiet:
            print("Choosing leg %r (of order %r), because it only appears on bottom %r out of %r times."\
                % (best_leg, order, best_case, len(self.bics)))
        return (best_leg, order, best_bot_list)

    def bics_with_leg_on_bottom(self,l):
        """
        A list of BICs where l is on bottom level.
        
        Args:
            l (tuple): leg on self (i.e. (i,j) for the j-th element of the signature 
                of the i-th component)
        
        Returns:
            list: list of indices self.bics
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((2,))])
            sage: X.bics_with_leg_on_bottom((0,0))
            [0, 1]
        """
        bot_list = []
        # the corresponding point on each EmbeddedLevelGraph is leg
        for i, B in enumerate(self.bics):
            # reminder: l is leg on stratum, i.e. (i,j)
            # dmp_inv maps this to a leg on a graph (integer)
            leg = B.dmp_inv[l]
            leg_level = B.dlevels[B.LG.levelofleg(leg)]
            assert leg_level in [0,-1], "Leg %r of BIC %r is not on level 0 or -1!"\
                % (leg, B)
            if leg_level == -1:
                bot_list.append(i)
        return bot_list

    @cached_method
    def xi_at_level(self,l,enh_profile,leg=None,quiet=True):
        """
        Pullback of xi on level l to enh_profile.

        This corresponds to xi_Gamma^[i] in the paper.

        Args:
            l (int): level number (0,...,codim)
            enh_profile (tuple): enhanced profile
            leg (int, optional): leg (as a leg of enh_profile!!!), to be used
                in Sauvaget's relation. Defaults to None, i.e. optimal choice.
        
        Raises:
            RuntimeError: raised if classes produced by xi on the level have
                unexpected codimension.
            ValueError: if the leg provided is not found on the level.
        
        Returns:
            ELGTautClass: tautological class consisting of psi classes on
                enh_profile and graphs with oner more level.

        EXAMPLES ::

            Compare multiplication with xi to xi_at_level (for top-degree):

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,-2,0))
            sage: assert all(X.xi_at_level(0, ((i,),0)) == X.xi*X.taut_from_graph((i,)) for i in range(len(X.bics)))

        """
        if enh_profile == ((),0):
            assert l == 0
            if leg:
                level_leg = self.smooth_LG.dmp[leg]
                return self.xi_with_leg(level_leg)
            return self.xi
        G = self.lookup_graph(*enh_profile)
        GAG = self.additive_generator(enh_profile)
        # we need to use splitting info instead of direct level extraction,
        # because the embeddings might differ by an automorphism!
        d, leg_dict, L = self.splitting_info_at_level(enh_profile,l)
        inv_leg_dict = {v : k for k, v in leg_dict.items()}
        assert set(leg_dict.values()) == set(L.leg_dict.values())
        if leg is None:
            l_xi, level_leg = L.xi_with_leg(with_leg=True,quiet=quiet)
        else:
            if not (leg in leg_dict):
                raise ValueError('Leg %r is not on level %r of %r!' % (leg, l, enh_profile))
            level_leg = leg_dict[leg]
            l_xi = L.xi_with_leg(level_leg,quiet=quiet)
        taut_list = []
        if l_xi == 0:
            return self.ZERO
        for c, AG in l_xi.psi_list:
            if AG.codim == 0:
                # psi class on L:
                new_leg_dict = {}
                for AGleg in AG.leg_dict:
                    leg_on_G = inv_leg_dict[L.smooth_LG.dmp[AGleg]]
                    new_leg_dict[leg_on_G] = AG.leg_dict[AGleg]
                next_taut = (c, self.additive_generator(enh_profile,leg_dict=new_leg_dict))
            elif AG.codim == 1:
                coeff, glued_AG = self.glue_AG_at_level(AG,enh_profile,l)
                next_taut = (c*coeff,glued_AG)
            else:
                raise RuntimeError("Classes in xi should all be of codim 0 or 1! %s" % l_xi)
            taut_list.append(next_taut)
        return ELGTautClass(self,taut_list)

    @cached_method
    def glue_AG_at_level(self,AG,enh_profile,l):
        """
        Glue an AdditiveGenerator into level l of enh_profile.

        Note that AG must be an AdditiveGenerator on the level obtained via
        self.splitting_info_at_level!

        Currently this is only implemented for graphs (and only really tested
        for BICs!!!)

        TODO: Test for AGs that are not BICs and psi classes.
        
        Args:
            AG (AdditiveGenerator): AdditiveGenerator on level
            enh_profile (tuple): enhanced profile of self.
            l (int): level number of enh_profile.
        
        Raises:
            RuntimeError: raised if the new profile is empty.
        
        Returns:
            tuple: A tuple consisting of the stackfactor (QQ) and the
                AdditiveGenerator of the glued graph.
        """
        # TODO: Check if longer profiles work + psis!
        #
        # First, we figure out the profile of the new graph of self.
        # For this, we must translate the profile (inside L) of the AG
        # into an extended profile (of self) as a degeneration of enh_profile:
        profile, _comp = enh_profile
        AGprofile, AGcomp = AG.enh_profile
        # We start by deciding where something must be inserted into enh_profile:
        # 
        # We observe that level l is either:
        # * B^top of the first BIC in profile (level 0),
        # * B^bot of the last BIC in profile (lowest level), or
        # * the middle of the 3-level graph (profile[l-1],profile[l]).
        #
        # There is also the "degenerate case" of an empty profile that
        # we should exclude first:
        if len(profile) == 0:
            assert l == 0
            # level stratum == stratum
            # stack_factor = QQ(AG.stack_factor)
            return (1, self.additive_generator((AGprofile,AGcomp)))
        elif l == 0:
            new_bics = [self.DG.top_to_bic(profile[l])[bic_index] for bic_index in AGprofile]
        elif l == len(profile):
            new_bics = [self.DG.bot_to_bic(profile[l-1])[bic_index] for bic_index in AGprofile]
        else:  # we are in the middle of the corresponding 3-level graph:
            three_level_profile, enhancement = self.three_level_profile_for_level(enh_profile,l)
            new_bics = [self.DG.middle_to_bic((three_level_profile,enhancement))[bic_index]
                            for bic_index in AGprofile]
        p = list(profile)
        p = tuple(p[:l] + new_bics + p[l:])
        # Now we know the profile, we have to figure out, which component
        # we're on.
        # For this, we split the enh_profile apart, replace one part by the BIC and 
        # and glue it back together again.
        comp_list = []
        assert len(self.lookup(p)) > 0, "Error: Glued into empty profile %r" % p
        # The splitting information and the level in 'standard form' (i.e. one
        # of the three above possibilities), is given by splitting_info_at_level:
        d, leg_dict, L = self.splitting_info_at_level(enh_profile,l)
        if not AG._X is L:
            print("Warning! Additive Generator should live on level %r of %r! I hope you know what you're doing...." % (l,enh_profile))
        # We first build the "big" graph, i.e. glue in the AG.
        # For this, we have to distinguish again, if we're gluing into the middle 
        # (two cuts) or at one end of the profile (1 cut):
        if l == 0:
            assert d['top'].X is L
            # we glue into top:
            d['top'] = d['top'].X.lookup_graph(*AG.enh_profile)
        elif l == len(profile):
            assert d['bottom'].X is L
            # we glue into bottom:
            d['bottom'] = d['bottom'].X.lookup_graph(*AG.enh_profile)
        else:
            assert d['middle'] is L
            # we glue into middle:
            d['middle'] = d['middle'].lookup_graph(*AG.enh_profile)
        glued_graph = admcycles.diffstrata.stratatautring.clutch(**d)
        # Now we check the components of p for glued_graph:
        for i, H in enumerate(self.lookup(p)):
            if glued_graph.is_isomorphic(H):
                comp_list.append(i)
        if len(comp_list) != 1:
            raise RuntimeError("%r is not a unique degeneration of %r! %r" % (p,enh_profile,comp_list))
        i = comp_list[0]
        glued_AG = self.additive_generator((p,i))
        GAG = self.additive_generator(enh_profile)
        stack_factor = 1
        for i in range(len(AGprofile)):
            stack_factor *= QQ(self.bics[new_bics[i]].ell) / QQ(L.bics[AGprofile[i]].ell)
        stack_factor *= QQ(len(glued_graph.automorphisms)) / QQ(len(AG._G.automorphisms)*len(GAG._G.automorphisms))
        return (stack_factor, glued_AG)

    def calL(self, enh_profile=None, l=0):
        """
        The error term of the normal bundle on level l of enh_profile * -ll
        (pulled back to enh_profile)
        
        Args:
            enh_profile (tuple, optional): enhanced profile. Defaults to None.
            l (int, optional): level. Defaults to 0.
        
        Returns:
            ELGTautClass: Tautological class on self
        """
        result = []
        if enh_profile is None or enh_profile == ((), 0):
            for i, B in enumerate(self.bics):
                ll = self.bics[i].ell
                result.append(ll*self.taut_from_graph((i,)))
        else:
            # Morally, L = G.level(squished_level)
            # but we have to use splitting_info_at_level to glue in safely!
            d, leg_dict, L = self.splitting_info_at_level(enh_profile, l)
            for i, B in enumerate(L.bics):
                BAG = L.additive_generator(((i,),0))
                sf, glued_AG = self.glue_AG_at_level(BAG, enh_profile, l)
                coeff = QQ(sf*B.ell)
                result.append(coeff * glued_AG.as_taut())
        if not result:
            return self.ZERO
        return self.ELGsum(result)

    ################################################################
    ############ SEC 9 FORMULAS ####################################
    ################################################################
    ## The following formulas check various identities used in    ##
    ## and around sec 9 of the paper. They also serve as examples ##
    ## for the methods introduced above.                          ##
    ################################################################

    @property
    def c1_E(self):
        """
        The first chern class of Omega^1(log) (Thm 1.1).
        
        Returns:
            ELGTautClass: c_1(E) according to Thm 1.1.
        
        EXAMPLES ::

        """
        N = self.dim() + 1
        c1E = [N*self.xi]
        for i, B in enumerate(self.bics):
            Ntop = B.top.dim() + 1
            l = B.ell
            c1E.append(((N-Ntop)*l)*self.taut_from_graph((i,)))
        return self.ELGsum(c1E)
    
    @property
    def c2_E(self):
        """
        A direct formula for the second Chern class.
        
        Returns:
            ELGTautClass: c_2 of the Tangent bundle of self.
        """
        N = QQ(self.dim() + 1)
        c2E = [N*(N-1)/QQ(2) * (self.xi_pow(2))]
        for i, B in enumerate(self.bics):
            Ntop = B.top.dim() + 1
            Nbot = B.bot.dim() + 1
            xitop = self.xi_at_level(0, ((i,),0))
            xibot = self.xi_at_level(1, ((i,),0))
            l = QQ(B.ell)
            c2E.append(l/2 * ((N*(N-1) - Ntop*(Ntop-1))*xitop +
                              ((N-Ntop)**2 + Ntop - N)*xibot))
        for ep in self.enhanced_profiles_of_length(2):
            p, _ = ep
            delta0 = self.bics[p[0]]
            delta1 = self.bics[p[1]]
            Nd0 = delta0.top.dim() + 1
            Nd1 = delta1.top.dim() + 1
            ld0 = QQ(delta0.ell)
            ld1 = QQ(delta1.ell)
            factor = QQ(1)/QQ(2) * ld0 * ld1 * (N*(N-2*Nd0)-Nd1*(Nd1-2*Nd0)-N+Nd1)
            c2E.append(factor * self.taut_from_graph(*ep))
        return self.ELGsum(c2E)
    
    @cached_method
    def ch1_pow(self, n):
        """
        A direct formula for powers of ch_1
        
        Args:
            n (int): exponent
        
        Returns:
            ELGTautClass: ch_1(T)^n
        """
        N = QQ(self.dim() + 1)
        chpow = [QQ(N**n)/QQ(factorial(n)) * self.xi_pow(n)]
        for L in range(1,n+1):
            summand = []
            for ep in self.enhanced_profiles_of_length(L):
                p, _ = ep
                delta = [self.bics[b] for b in p]
                ld = [B.ell for B in delta]
                Nd = [B.top.dim() + 1 for B in delta]
                exi = self.exp(N*self.xi_at_level(0,ep), amb=ep)
                factor = 1
                td_prod = self.taut_from_graph(*ep)
                for i in range(L):
                    factor *= (N - Nd[i])*ld[i]
                    td_prod = self.intersection(td_prod, 
                        self.td_contrib(-ld[i]*(N-Nd[i]), 
                            self.cnb(ep, ep, self.squish(ep, i)), ep),
                                ep)
                prod = self.intersection(exi, td_prod, ep)
                summand.append(factor * prod.degree(n))
            chpow.append(self.ELGsum(summand))
        return factorial(n) * self.ELGsum(chpow)

    @property
    def ch2_E(self):
        """
        A direct formula for ch_2.
        
        Returns:
            ELGTautClass: ch_2
        """
        N = QQ(self.dim() + 1)
        ch2E = [N/QQ(2) * (self.xi_pow(2))]
        for i, B in enumerate(self.bics):
            Ntop = B.top.dim() + 1
            Nbot = B.bot.dim() + 1
            xitop = self.xi_at_level(0, ((i,),0))
            xibot = self.xi_at_level(1, ((i,),0))
            l = QQ(B.ell)
            ch2E.append(l/2 * ((N - Ntop)*(xitop + xibot)))
        for ep in self.enhanced_profiles_of_length(2):
            p, _ = ep
            delta0 = self.bics[p[0]]
            delta1 = self.bics[p[1]]
            Nd0 = delta0.top.dim() + 1
            Nd1 = delta1.top.dim() + 1
            ld0 = QQ(delta0.ell)
            ld1 = QQ(delta1.ell)
            factor = QQ(1)/QQ(2) * ld0 * ld1 * (N - Nd1)
            ch2E.append(factor * self.taut_from_graph(*ep))
        return self.ELGsum(ch2E)

    def ch_E_alt(self, d):
        """
        A formula for the Chern character.
        
        Args:
            d (int): cut-off degree
        
        Returns:
            ELGTautClass: sum of ch_0 to ch_d.
        """
        N = QQ(self.dim() + 1)
        ch_E = [N/QQ(factorial(d)) * self.xi_pow(d)]
        for L in range(1, d+1):
            summand = []
            for ep in self.enhanced_profiles_of_length(L):
                p, _ = ep 
                ld = [self.bics[b].ell for b in p]
                Nd = self.bics[p[-1]].top.dim() + 1
                ld_prod = 1
                for l in ld:
                    ld_prod *= l
                factor = ld_prod * (N - Nd)
                td_prod = self.ONE
                for i in range(L):
                    td_prod = self.intersection(td_prod, self.td_contrib(-ld[i], self.cnb(ep, ep, self.squish(ep, i)), ep), ep)
                inner_sum = []
                for j in range(d-L+1):
                    pr = self.intersection(self.pow(self.xi_at_level(0, ep), j, ep), td_prod.degree(d-j), ep)
                    inner_sum.append(QQ(1)/QQ(factorial(j)) * pr)
                summand.append(factor * self.ELGsum(inner_sum))
            ch_E.append(self.ELGsum(summand))
        return self.ELGsum(ch_E)

    @cached_method
    def exp_xi(self, quiet=True):
        """
        Calculate exp(xi) using that no powers higher than 2g appear for connected
        holomorphic strata.
        
        Args:
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            ELGTautClass: exp(xi)
        """
        if not self._polelist and len(self._g) == 1:
            stop = 2*self._g[0]
        else:
            stop = None
        if not quiet:
            if stop:
                stop_str = stop - 1
            else:
                stop_str = stop
            print('Stoping exp(xi) at degree %r' % stop_str)
        return self.exp(self.xi, quiet=quiet, stop=stop)
    
    def xi_at_level_pow(self, level, enh_profile, exponent):
        """
        Calculate powers of xi_at_level (using ambient enh_profile).

        Note that when working with xi_at_level on enh_profile, multiplication
        should always take place in CH(enh_profile), i.e. using intersection
        instead of *. This is simplified for powers by this method.

        Moreover, by Sauvaget, xi^n = 0 for n >= 2g for connected holomorphic
        strata, so we check this before calculating.
        
        Args:
            level (int): level of enh_profile.
            enh_profile (tuple): enhanced profile of self.
            exponent (int): exponent
        
        Returns:
            ELGTautClass: Pushforward of (xi_{enh_profile}^[l])^n to self.
        """
        G = self.lookup_graph(*enh_profile)
        L = G.level(level)
        if not L._polelist and len(L._g) == 1:
            if exponent >= 2*L._g[0]:
                return self.ZERO
        if enh_profile == ((), 0):
            assert level == 0
            return self.xi_pow(exponent)
        # ambient!
        power = self.taut_from_graph(*enh_profile)
        # maybe consecutive squaring is better? Seems that it isn't :/
        # xi = self.xi_at_level(level, enh_profile)
        # def _rec(x, n):
        #     if n == 0:
        #         return self.taut_from_graph(*enh_profile)
        #     if n == 1:
        #         return x
        #     if n % 2 == 0:
        #         return _rec(self.intersection(x, x, enh_profile), n // 2)
        #     return self.intersection(x, _rec(self.intersection(x, x, enh_profile), (n - 1) // 2), enh_profile)
        # return _rec(xi, exponent)
        xi = self.xi_at_level(level, enh_profile)
        for _ in range(exponent):
            power = self.intersection(power, xi, enh_profile)
        return power
    
    @cached_method
    def exp_L(self, quiet=True):
        """
        exp(calL)
        
        Args:
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            ELGTautClass: exp(calL)
        """
        return self.exp(self.calL(), quiet=quiet)

    @property
    def P_B(self):
        """
        The twisted Chern character of self, see sec 9 of the paper.
        
        Returns:
            ELGTautClass: class of P_B
        """
        # Prop. 9.2
        N = QQ(self.dim() + 1)
        PB = [N*self.exp_xi() + (-1)*self.ONE]
        for L in range(1,N):
            inner = []
            for enh_profile in self.enhanced_profiles_of_length(L):
                p, _ = enh_profile
                B = self.bics[p[0]]
                Ntop = B.top.dim() + 1
                summand = (-1)**L * (Ntop*self.exp_xi() + (-1)*self.ONE)
                prod_list = []
                for i in range(L):
                    ll = self.bics[p[i]].ell
                    squish = self.squish(enh_profile, i)  
                    td_NB = ll * self.td_contrib(ll, self.cnb(enh_profile, enh_profile, squish), enh_profile)
                    prod_list.append(td_NB)
                if prod_list:
                    prod = prod_list[0]
                    for f in prod_list[1:]:
                        # multiply with ambient Gamma (=enh_profile)!
                        prod = self.intersection(prod, f, enh_profile)
                    const = prod.degree(0)
                    prod += (-1) * const
                    summand *= (prod + const*self.taut_from_graph(*enh_profile))
                inner.append(summand)
            PB.append(self.ELGsum(inner))
        return self.ELGsum(PB)

    def charToPol(self, ch, upto=None, quiet=True):
        """
        Newton's identity to recursively translate the Chern character into the
        Chern polynomial.
        
        Args:
            ch (ELGTautClass): Chern character
            upto (int, optional): Calculate polynomial only up to this degree. Defaults to None (full polynomial).
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            list: Chern polynomial as list of ELGTautClasses (indexed by degree)
        """
        if not quiet:
            print('Starting charToPol...')
        C = ch.list_by_degree()
        # throw out factorials:
        p = [factorial(k)*c for k, c in enumerate(C)]
        # calculate recursively using Newton's identity:
        E = [self.ONE]
        if upto is None:
            upto = self.dim()
        for k in range(1, upto + 1):
            if not quiet:
                print('Calculating c_%r...' % k)
            ek = []
            for i in range(1, k+1):
                ek.append((-1)**(i-1) * E[k-i]*p[i])
            E.append(QQ(1)/QQ(k) * self.ELGsum(ek))
        return E
    
    def top_chern_class_alt(self, quiet=True):
        """
        Top chern class from Chern polynomial.
        
        Args:
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            ELGTautClass: c_top of the tangent bundle of self.
        """
        ch = self.ch_E_fast(quiet=quiet).list_by_degree()
        top_c = []
        N = self.dim()
        for p in partitions(N):
            l = sum(p.values())
            factor = (-1)**(N-l)
            # for r, n in enumerate(p.values()):
                # factor *= QQ(factorial(r)**n)/QQ(factorial(n))
            ch_prod = self.ONE
            for i, n in p.items():
                factor *= QQ(factorial(i-1)**n)/QQ(factorial(n))
                if i == 1:
                    ch_prod *= self.ch1_pow(n)
                else:
                    ch_prod *= ch[i]**n
            top_c.append(factor*ch_prod)
        return self.ELGsum(top_c)
    
    def top_chern_class_direct(self, quiet=True):
        """
        A direct formula for the top Chern class using only xi_at_level.
        
        Args:
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            ELGTautClass: c_top of the Tangent bundle of self.
        """
        N = self.dim()
        top_c = []
        for L in range(N+1):
            if not quiet:
                print('Going through %r profiles of length %r...' % (len(self.enhanced_profiles_of_length(L)), L))
            summand = []
            for ep in self.enhanced_profiles_of_length(L):
                p, _ = ep
                ld = [self.bics[b].ell for b in p]
                ld_prod = 1
                for l in ld:
                    ld_prod *= l
                inner = []
                for K in WeightedIntegerVectors(N-L, [1]*(L+1)):
                    xi_prod = self.taut_from_graph(*ep)
                    for i, k in enumerate(K):
                        xi_prod = self.intersection(xi_prod, self.xi_at_level_pow(i, ep, k), ep)
                    inner.append((K[0] + 1) * xi_prod)
                summand.append(ld_prod * self.ELGsum(inner))
            top_c.append(self.ELGsum(summand))
        return self.ELGsum(top_c)

    def top_xi_at_level_comparison(self, ep, quiet=False):
        """
        Comparison of level-wise computation vs xi_at_level.
        
        Args:
            ep (tuple): enhanced profile
            quiet (bool, optional): no output. Defaults to False.
        
        Returns:
            bool: Should always be True.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: assert all(X.top_xi_at_level_comparison(ep, quiet=True) for l in range(len(X.lookup_list)) for ep in X.enhanced_profiles_of_length(l))
        """
        N = self.dim()
        p, _ = ep
        L = len(p)
        ld   = [self.bics[b].ell           for b in p]
        Nvec = [self.bics[b].top.dim() + 1 for b in p]
        Nvec.append(N+1)
        ld_prod = 1
        for l in ld:
            ld_prod *= l
        inner = []
        xi_prod = self.xi_at_level_pow(0, ep, Nvec[0]-1)
        for i in range(1,L+1):
            xi_prod = self.intersection(xi_prod, self.xi_at_level_pow(i, ep, Nvec[i]-Nvec[i-1]-1), ep)
        xi_at_level_prod = (Nvec[0] * xi_prod).evaluate(quiet=True)
        if not quiet:
            print("Product of xis at levels: %r" % xi_at_level_prod)
        G = self.lookup_graph(*ep)
        AG = self.additive_generator(ep)
        top_xi_at_level = [(G.level(i).xi_at_level_pow(0,((),0),G.level(i).dim())).evaluate(quiet=True) for i in range(L+1)]
        if not quiet:
            print(top_xi_at_level)
        prod = Nvec[0]
        for x in top_xi_at_level:
            prod *= x
        tot_prod = AG.stack_factor*prod
        if not quiet:
            print("Stack factor: %r" % AG.stack_factor)
            print("Product: %r" % prod)
            print("Total product: %r" % tot_prod)
        return tot_prod == xi_at_level_prod
    
    def top_xi_at_level(self, ep, level, quiet=True):
        """
        Evaluate the top xi power on a level.

        Note that this is _not_ computed on self but on the GeneralisedStratum
        corresponding to level l of ep (the result is a number!).

        Moreover, all results are cached and the cache is synchronised with
        XI_FILENAME.

        The key for the cache is L.dict_key (where L is the LevelStratum).
        
        Args:
            ep (tuple): enhanced profile
            level (int): level number of ep
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            QQ: integral of the top xi power against level l of ep.

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: X.top_xi_at_level(((),0), 0)
            -1/640
        """
        G = self.lookup_graph(*ep)
        L = G.level(level)
        key = L.dict_key()
        cache = load_xis()
        if not (key in cache):            
            N = L.dim()
            if not quiet:
                print('(calc)', end=' ')
                sys.stdout.flush()
            top_xi = L.xi_at_level_pow(0, ((),0), N)
            cache[key] = top_xi.evaluate(quiet=True)
            # write to file
            sage.misc.persist.save(cache,XI_FILENAME)
            # os.fsync()
        else:
            if not quiet:
                print ('(cache)', end=' ')
                sys.stdout.flush()
        if not quiet:
            print(cache[key], end=' ')
            sys.stdout.flush()
        assert QQ(cache[key]) == cache[key]
        return cache[key]

    def euler_char_immediate_evaluation(self, quiet=True):
        """
        Calculate the (Orbifold) Euler characteristic of self by evaluating top xi
        powers on levels.

        This is (by far) the fastest way of computing Euler characteristics.

        Note that only combinatorial information about the degeneration graph
        of self is used (enhanced_profiles_of_length(L)) and top_xi_at_level
        the values of which are cached and synched with XI_FILENAME.
        
        Args:
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            QQ: (Orbifold) Euler characteristic of self.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: X.euler_char_immediate_evaluation()
            -1/40
        """
        N = self.dim()
        ec = 0
        for L in range(N+1):
            if not quiet:
                total=len(self.enhanced_profiles_of_length(L, quiet=False))
                print('Going through %r profiles of length %r...' % (total, L))
            for i, ep in enumerate(self.enhanced_profiles_of_length(L)):
                if not quiet:
                    print('%r / %r, %r:' % (i+1, total, ep), end=' ')
                    sys.stdout.flush()
                p, _ = ep
                ld = [self.bics[b].ell for b in p]
                if p:
                    NGammaTop = self.bics[p[0]].top.dim() + 1
                else:
                    NGammaTop = N + 1
                ld_prod = 1
                for l in ld:
                    ld_prod *= l
                AG = self.additive_generator(ep)
                prod = ld_prod * NGammaTop * AG.stack_factor
                if not quiet:
                    print("Calculating xi at", end=' ')
                    sys.stdout.flush()
                for i in range(L+1):
                    if not quiet:
                        print('level %r' % i, end=' ')
                        sys.stdout.flush()
                    prod *= self.top_xi_at_level(ep, i, quiet=quiet)
                    if prod == 0:
                        if not quiet:
                            print("Product 0.", end=' ')
                            sys.stdout.flush()
                        break
                if not quiet:
                    print('Done.')
                    sys.stdout.flush()
                ec += prod
        return (-1)**N * ec
    
    def euler_characteristic(self):
        """
        Calculate the (Orbifold) Euler characteristic of self by evaluating top xi
        powers on levels. See also euler_char_immediate_evaluation.
        
        Returns:
            QQ: (Orbifold) Euler characteristic of self.

        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: X.euler_characteristic()
            -1/40
        """
        return self.euler_char_immediate_evaluation()

    def euler_char(self,quiet=True, alg='direct'):
        """
        Calculate the (Orbifold) Euler characteristic of self by computing the top
        Chern class and evaluating this.

        Note that this is significantly slower than using self.euler_characteristic!

        The optional keyword argument alg determines how the top Chern class
        is computed and can be either:
        * direct (default): using top_chern_class_direct
        * alt: using top_chern_class_alt
        * other: using top_chern_class

        Args:
            quiet (bool, optional): no ouput. Defaults to True.
            alg (str, optional): algorithm (see above). Defaults to 'direct'.
        
        Returns:
            QQ: (Orbifold) Euler characteristic of self.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=Stratum((2,))
            sage: X.euler_char()
            -1/40
            sage: X.euler_char(alg='alt')
            -1/40
            sage: X.euler_char(alg='other')
            -1/40
        """
        if alg == 'direct':
            tcc = self.top_chern_class_direct(quiet=quiet)
        elif alg == 'alt':
            tcc = self.top_chern_class_alt(quiet=quiet)
        else:
            tcc = self.top_chern_class(quiet=quiet, alg=alg)
        if not quiet:
            print('Evaluating...')
        return (-1)**self.dim() * tcc.evaluate(quiet=True)

    def top_chern_class(self, inside=True, prod=True, top=False, quiet=True, alg='fast'):
        """
        Compute the top Chern class from the Chern polynomial via the Chern character.

        This uses chern_poly.
        
        Args:
            inside (bool, optional): passed to chern_poly. Defaults to True.
            prod (bool, optional): passed to chern_poly. Defaults to True.
            top (bool, optional): passed to chern_poly. Defaults to False.
            quiet (bool, optional): passed to chern_poly. Defaults to True.
            alg (str, optional): passed to chern_poly. Defaults to 'fast'.
        
        Returns:
            ELGTautClass: c_top(T) of self.
        """
        return self.chern_poly(inside=inside, prod=prod, top=top, quiet=quiet, alg=alg)[-1]

    def chern_poly(self, inside=True, prod=True, top=False, quiet=True, alg='fast', upto=None):
        """
        The Chern polynomial calculated from the Chern character.
        
        The optional keyword argument alg determines how the Chern character
        is computed and can be either:
            * fast (default): use ch_E_fast
            * bic_prod: use ch_E_prod
            * other: use ch_E

        Args:
            inside (bool, optional): passed to ch_E. Defaults to True.
            prod (bool, optional): passed to ch_E. Defaults to True.
            top (bool, optional): passed to ch_E. Defaults to False.
            quiet (bool, optional): no output. Defaults to True.
            alg (str, optional): algorithm used (see above). Defaults to 'fast'.
            upto (int, optional): highest degree of polynomial to calculate. Defaults to None (i.e. dim so the whole polynomial).
        
        Returns:
            list: Chern polynomial as list of ELGTautClasses (indexed by degree)
        """
        if alg == 'bic_prod':
            ch = self.ch_E_prod(quiet=quiet)
        elif alg == 'fast':
            ch = self.ch_E_fast(quiet=quiet)
        else:
            ch = self.ch_E(inside=inside, prod=prod, top=top, quiet=quiet)
        return self.charToPol(ch, quiet=quiet, upto=upto)

    def chern_class(self, n, quiet=True):
        """
        A direct formula for the n-th Chern class of the tangent bundle of self.
        
        Args:
            n (int): degree
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            ELGTautClass: c_n(T) of self.
        """
        N = self.dim() + 1
        c_n = []
        for L in range(N):
            if not quiet:
                print('Going through %r profiles of length %r...' % (len(self.enhanced_profiles_of_length(L)), L))
            summand = []
            for ep in self.enhanced_profiles_of_length(L):
                if not quiet:
                    print("Profile: %r" % (ep,), end=' ')
                p, _ = ep
                delta = [self.bics[b] for b in p]
                ld = [B.ell for B in delta]
                Nd = [B.top.dim() + 1 for B in delta]
                ld_prod = 1
                for l in ld:
                    ld_prod *= l
                inner = []
                for K in WeightedIntegerVectors(n-L, [1]*(L+1)):
                    if not quiet:
                        print('xi coefficient: k_0:', K[0], end=' ')
                        print('N-L-sum:', N-L-sum(K[1:]), end=' ')
                        print('Binomial:', binomial(N-L-sum(K[1:]), K[0]))
                    factor = binomial(N-L-sum(K[1:]), K[0])
                    prod = self.xi_at_level_pow(0, ep, K[0])
                    for i, k in list(enumerate(K))[1:]:
                        if not quiet:
                            print('k_%r: %r' % (i, k), end=' ')
                            print('r_Gamma,i:', (N-Nd[i-1]), end=' ')
                            print('L-i: %r, sum: %r' % (L-i, sum(K[i+1:])), end=' ')
                            print('Binomial:', binomial((N-Nd[i-1]) - (L-i) - sum(K[i+1:]), k+1))
                        factor *= binomial((N-Nd[i-1]) - (L-i) - sum(K[i+1:]), k+1)
                        squish = self.squish(ep, i-1)
                        X_pow = self.pow(ld[i-1] * self.cnb(ep, ep, squish), k, ep)
                        prod = self.intersection(prod, X_pow, ep)
                    inner.append(factor * prod)
                summand.append(ld_prod * self.ELGsum(inner))
            c_n.append(self.ELGsum(summand))
        return self.ELGsum(c_n)

    def ch_E_prod(self,quiet=True):
        """
        The product version of the Chern character formula.
        
        Args:
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            ELGTautClass: Chern character of the tangent bundle.
        """
        N = QQ(self.dim() + 1)
        ch_E = [N*self.ONE]
        for L, profiles in enumerate(self.lookup_list):
            if not quiet:
                print('Going through %r profiles of length %r...' % (len(profiles), L))
            summand = []
            for p in profiles:
                if not p:
                    continue
                Nd = self.bics[p[-1]].top.dim() + 1
                if N == Nd:  # factor == 0
                    continue
                factor = (N - Nd)
                bic_prod = self.ONE
                for Di in p:
                    bic_prod *= self.exp_bic(Di)
                summand.append(factor*bic_prod)
            ch_E.append(self.ELGsum(summand))
        return self.exp_xi(quiet=quiet) * self.ELGsum(ch_E)

    def ch_E_fast(self,quiet=True):
        """
        A more direct (and faster) formula for the Chern character (see sec 9 of the paper).
        
        Args:
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            ELGTautClass: Chern character of the tangent bundle.
        """
        N = QQ(self.dim() + 1)
        ch_E = [N*self.exp_xi(quiet=quiet)]
        for L in range(1, N):
            if not quiet:
                print('Going through %r profiles of length %r...' % (len(self.enhanced_profiles_of_length(L)), L))
            summand = []
            for ep in self.enhanced_profiles_of_length(L):
                p, _ = ep
                ld = [self.bics[b].ell for b in p]
                Nd = self.bics[p[-1]].top.dim() + 1
                if N == Nd:  # factor == 0
                    continue
                ld_prod = 1
                for l in ld:
                    ld_prod *= l
                factor = ld_prod * (N - Nd)
                td_prod = self.ONE
                for i in range(L):
                    td_prod = self.intersection(td_prod, self.td_contrib(-ld[i], self.cnb(ep, ep, self.squish(ep, i)), ep), ep)
                exi = self.exp(self.xi_at_level(0, ep), ep)
                pr = self.intersection(exi, td_prod, ep)
                summand.append(factor*pr)
            ch_E.append(self.ELGsum(summand))
        return self.ELGsum(ch_E)

    def top_chern_alt(self):
        """
        The top Chern class of self, computed by calulating the Chern polynomial
        from the Chern character as P_B*exp(L) and taking the top-degree part.
        
        Returns:
            ELGTautClass: top Chern class of the tangent bundle.
        """
        return self.charToPol(self.P_B*self.exp_L())[-1]

    def first_term(self, top=False, quiet=True):
        """
        The calculation of (N*self.exp_xi() - self.ONE)*self.exp_L() split into
        pieces with more debugging outputs (calculation can take a LONG time!)
        
        Args:
            top (bool, optional): Do calculations on level. Defaults to False.
            quiet (bool, optional): No output. Defaults to True.
        
        Returns:
            ELGTautClass: First term of ch.
        """
        if not quiet:
            print('Calculating first term...')
        N = QQ(self.dim() + 1)
        BICs = []
        for i, B in enumerate(self.bics):
            BICs.append((B.ell, self.additive_generator(((i,),0))))
        L = ELGTautClass(self, BICs, reduce=False)
        if top:
            if not quiet:
                print('Calculating exp_xi_L...')
            exp_xi_L = self.ELGsum([N*B.ell*self.exp(self.xi_at_level(0,((i,),0)), ((i,),0),quiet=quiet) for i, B in enumerate(self.bics)] + [(-1)*L])
            last = exp_xi_L
            if not quiet:
                print('Calculating recursive exponential factors: ', end=' ')
            for k in range(1, N-1):
                if not quiet:
                    print(k, end=' ')
                last = QQ(1)/QQ(k+1) * L * last
                if last == self.ZERO:
                    break
                exp_xi_L._psi_list.extend(last.psi_list)
            if not quiet:
                print('Done!')
                print('Adding exp_xi...')
            res = self.ELGsum([N*self.exp_xi(quiet=quiet), -self.ONE, exp_xi_L])
        else:
            if not quiet:
                print('Calculating exp(xi+L)...')
            res = N * self.exp(self.xi + L, quiet=quiet)
            if not quiet:
                print('Subtracting exp_L...')
            res -= self.exp_L(quiet=quiet)
        if not quiet:
            print('Done calculating first term!')
        return res

    def ch_E(self, inside=True, prod=True, top=False, quiet=True):
        """
        The Chern character (accoring to sec. 9 of the paper)
        
        Args:
            inside (bool, optional): work with ambient. Defaults to True.
            prod (bool, optional): product instead of sum. Defaults to True.
            top (bool, optional): work on level. Defaults to False.
            quiet (bool, optional): no output. Defaults to True.
        
        Returns:
            ELGTautClass: Chern character of the tangent bundle of self.
        """
        # Prop. 9.2
        N = QQ(self.dim() + 1)
        # ch = [(N*self.exp_xi() + (-1)*self.ONE)*self.exp_L()]
        ch = [self.first_term(top=top,quiet=quiet)]
        for L in range(1,N):
            inner = []
            if not quiet:
                print('Going through profiles of length %r...' % L)
            for enh_profile in self.enhanced_profiles_of_length(L):
                p, _ = enh_profile
                B = self.bics[p[0]]
                Ntop = B.top.dim() + 1
                if not inside:
                    summand = (-1)**L * (Ntop*self.exp_xi() - self.ONE)
                else:
                    if not quiet:
                        print('Calculating inner exp(xi): ', end=' ')
                    summand = (-1)**L * (Ntop*self.exp(self.xi_at_level(0, enh_profile), enh_profile, quiet=quiet) - self.taut_from_graph(*enh_profile))
                prod_list = []
                for i in range(L):
                    ll = self.bics[p[i]].ell
                    squish = self.squish(enh_profile, i)  
                    td_NB = ll * self.td_contrib(-ll, self.cnb(enh_profile, enh_profile, squish), enh_profile)
                    prod_list.append(td_NB)
                if prod_list:
                    prod = prod_list[0]
                    for f in prod_list[1:]:
                        # multiply with ambient Gamma (=enh_profile)!
                        prod = self.intersection(prod, f, enh_profile)
                    if prod:
                        for l in range(len(p) + 1):
                            prod = self.intersection(prod,\
                                        self.exp(self.calL(enh_profile, l), enh_profile),\
                                    enh_profile)
                    else:
                        prod = self.intersection(prod,\
                                        self.exp(
                                            self.ELGsum(self.calL(enh_profile, l) for l in range(len(p)+1)),\
                                         enh_profile),
                                        enh_profile)
                    if inside:
                        prod = self.intersection(prod, summand, enh_profile)
                    # multiply constant term with Gamma (for i_*)
                    const = prod.degree(0)
                    prod += (-1) * const
                    if inside:
                        summand = prod
                    else:
                        summand *= (prod + const*self.taut_from_graph(*enh_profile))
                inner.append(summand)
            ch.append(self.ELGsum(inner))
        return self.ELGsum(ch)

    ################################################################
    ############ END OF SEC 9 FORMULAS #############################
    ################################################################

    def res_stratum_class(self,cond,debug=False):
        """
        The class of the stratum cut out by cond inside self.
        
        Args:
            cond (list): list of a residue condition, i.e. a list of poles of self.
        
        Returns:
            ELGTautClass: Tautological class of Prop. 9.3
        
        EXAMPLES ::


        """
        st_class = -1 * self.xi_with_leg(quiet=True)
        bic_list = []
        if debug:
            print("Calculating the class of the stratum cut out by %r in %r..." % (cond,self))
            print("-xi = %s" % st_class)
        for i, B in enumerate(self.bics):
            if debug:
                print("Checking BIC %r:" % i)
            top = B.top
            # we restrict/translate cond to top:
            poles_on_bic = [B.dmp_inv[p] for p in cond]
            cond_on_top = [top.leg_dict[leg] for leg in poles_on_bic if leg in top.leg_dict]
            # if there are RCs on top, we must check that they don't change the rank
            if cond_on_top:
                MT = top.matrix_from_res_conditions([cond_on_top])
                top_G = top.smooth_LG
                RT = top_G.full_residue_matrix
                if (MT.stack(RT)).rank() != RT.rank():
                    assert (MT.stack(RT)).rank() > RT.rank()
                    if debug:
                        print("Discarding (because of top).")
                    continue
            l = B.ell
            if debug:
                print("Appending with coefficient -%r" % l)
            bic_list.append((l,i))
        st_class += self.ELGsum([-l*self.taut_from_graph((i,),0) for l, i in bic_list])
        return st_class

    def adm_evaluate(self,stgraph,psis,sig,g,quiet=False,admcycles_output=False):
        """
        Evaluate the psi monomial on a (connected) stratum without residue conditions
        using admcycles.

        stgraph should be the one-vertex graph associated to the stratum sig.

        We use admcycles Strataclass to calculate the class of the stratum inside
        Mbar_{g,n} and multiply this with psis (in admcycles) and evaluate the product.

        The result is cached and synched with FILENAME.
        
        Args:
            stgraph (stgraph): admcycles stgraph
            psis (dict): psi polynomial on stgraph
            sig (tuple): signature tuple
            g (int): genus of sig
            quiet (bool, optional): No output. Defaults to False.
            admcycles_output (bool, optional): Print the admcycles classes. Defaults to False.
        
        Returns:
            QQ: integral of psis on stgraph.
        """
        # key = (tuple(sorted(psis.items())), tuple(sig))
        key = adm_key(sig, psis)
        cache = load_adm_evals()
        if not key in cache:
            DS = admcycles.admcycles.decstratum(stgraph,psi=psis)
            Stratum_class = admcycles.stratarecursion.Strataclass(g,1,sig)
            if not quiet or admcycles_output:
                print("DS: %r\n Stratum_class: %r" % (DS,Stratum_class))
            product = Stratum_class*DS  # in admcycles!
            if not quiet or admcycles_output:
                print("Product: %r" % product.evaluate())
            cache[key] = product.evaluate()  # in admcycles!
            # write to file
            sage.misc.persist.save(cache,FILENAME)
        return cache[key]

    def evaluate(self,psis={},quiet=False,warnings_only=False,admcycles_output=False):
        """
        Evaluate the psi monomial psis on self.

        Psis is a dictionary legs of self.smooth_LG -> exponents encoding a psi monomial.

        We translate residue conditions of self into intersections of simpler classes
        and feed the final pieces into admcycles for actual evaluation.
        
        Args:
            psis (dict, optional): Psi monomial (as legs of smooth_LG -> exponent). Defaults to {}.
            quiet (bool, optional): No output. Defaults to False.
            warnings_only (bool, optional): Only warnings. Defaults to False.
            admcycles_output (bool, optional): adm_eval output. Defaults to False.
        
        Raises:
            RuntimeError: raised if a required residue condition is not found.
        
        Returns:
            QQ: integral of psis against self.
        """
        G = self.smooth_LG
        LG = G.LG
        # Check if the rGRC doesn't cut down the dimension:
        # Recall:
        # * residue_matrix_from_RT has the RT on each component of G as rows
        # * full_residue_matrix is this + the res_cond of self
        if G.full_residue_matrix.rank() == G.residue_matrix_from_RT.rank():
            if self._h0 > 1:
                if not quiet or warnings_only:
                    print("----------------------------------------------------")                       
                    print("Level %r disconnected." % self)
                    print("----------------------------------------------------")
                    print("No residue conditions: contribution is 0.")
                return 0
            # stratum is connected!
            # 0 dimensional strata contribute 1
            if self.dim() == 0:
                return 1
            # We can just use admcycles to evaluate:
            return self.adm_evaluate(LG.stgraph,psis,self._sig_list[0].sig,LG.g(),quiet=quiet,admcycles_output=admcycles_output)
        # There *are* non-trivial residue conditions!
        if self._h0 > 1:
            if not quiet or warnings_only:
                print("----------------------------------------------------")                       
                print("Level %r disconnected." % self)
                print("----------------------------------------------------")
            # Check if graph of residue conditions is disconnected:
            if not LG.underlying_graph.is_connected():
                if not quiet or warnings_only:
                    print("Level is product: contribution is 0.")
                return 0
        # Create new stratum with one residue condition less:
        new_rc = deepcopy(self._res_cond)
        # conditions from RT:
        RT_M = G.residue_matrix_from_RT
        # we remove conditions until the rank drops:
        while new_rc:
            lost_cond = new_rc.pop()
            new_M = self.matrix_from_res_conditions(new_rc)
            if new_M:
                full_M = new_M.stack(RT_M)
            else:
                full_M = RT_M
            if full_M.rank() == G.full_residue_matrix.rank() - 1:
                # rank dropped
                break
        else:
            raise RuntimeError("No Conditions cause dimension to drop in %r!" % self._res_cond)
        try:
            new_leg_dict = deepcopy(self._leg_dict)
        except AttributeError:
            new_leg_dict = {}
        new_stratum = LevelStratum(self._sig_list,new_rc,new_leg_dict)
        assert new_stratum.dim() == self.dim() + 1
        # Because only the RCs changed, G still lives inside this stratum
        # so we can use it to build our new AdditiveGenerator:
        new_AG = new_stratum.additive_generator(((),0),psis)
        new_class = new_AG.as_taut()*new_stratum.res_stratum_class(lost_cond)
        result = new_class.evaluate(quiet=quiet)
        return result

#################################################################
#################################################################
#################################################################
#################################################################

class Stratum(GeneralisedStratum):
    """
    A simpler frontend for a GeneralisedStratum with one component and
    no residue conditions.
    """
    def __init__(self,sig):
        super(Stratum, self).__init__([admcycles.diffstrata.sig.Signature(sig)])

#################################################################
#################################################################
#################################################################
#################################################################

class LevelStratum(GeneralisedStratum):
    """
    A stratum that appears as a level of a levelgraph.

    This is a GeneralisedStratum together with a dictionary mapping the
    leg numbers of the (big) graph to the legs of the Generalisedstratum.

    Note that if this is initialised from an EmbeddedLevelGraph, we also
    have the attribute leg_orbits, a nested list giving the orbits of
    the points under the automorphism group of the graph.

    * leg_dict : a (bijective!) dictionary mapping the leg numbers of a graph 
        to the corresponing tuple (i,j), i.e. the point j on the component i.

    * res_cond : a (nested) list of residue conditions given by the r-GRC when
        extracting a level.

    """
    def __init__(self,sig_list,res_cond=None,leg_dict=None):
        super(LevelStratum,self).__init__(sig_list,res_cond)
        if leg_dict is None:
            # assume the points were numbered 1...n
            self._leg_dict = {}
            for i in range(len(sig_list)):
                for j in range(sig_list[i].n):
                    self._leg_dict[i+j+1] = (i,j)
        else:
            self._leg_dict = leg_dict
        # build inverse dictonary
        self._inv_leg_dict = dict([(v,k) for k,v in self._leg_dict.items()])

    def __repr__(self):
        return "LevelStratum(sig_list=%r,res_cond=%r,leg_dict=%r)" % (self._sig_list,self._res_cond,self.leg_dict)
    def __str__(self):
        rep = ''
        if self._h0 > 1:
            rep += 'Product of Strata:\n'
        else:
            rep += 'Stratum: '
        for sig in self._sig_list:
            rep += repr(sig) + '\n'
        rep += 'with residue conditions: '
        for res in self._res_cond:
            rep += repr(res) + ' '
        rep += '\n'
        rep += 'dimension: ' + repr(self.dim()) + '\n'
        rep += 'leg dictionary: ' + repr(self._leg_dict) + '\n'
        try:
            rep += 'leg orbits: ' + repr(self.leg_orbits) + '\n'
        except AttributeError:
            pass
        return rep

    @cached_method
    def dict_key(self):
        """
        The hash-key for the cache of top-xi-powers.

        More precisely, we sort each signature, sort this list and renumber
        the residue conditions accordingly. Finally, everything is made into a tuple.
        
        Returns:
            tuple: nested tuple.
        """
        rc_dict = {}
        sig = []
        for new_i, new_sign in enumerate(sorted(enumerate(self._sig_list), key=lambda k: k[1].sig)):
            i, sign = new_sign
            curr_sig = []
            for new_j, s in enumerate(sorted(enumerate(sign.sig), key=lambda k: k[1])):
                j, a = s
                curr_sig.append(a)
                rc_dict[(i,j)] = (new_i, new_j)
            sig.append(tuple(curr_sig))
        sig = tuple(sig)
        rc = sorted([sorted([rc_dict[cond] for cond in conds]) for conds in self._res_cond])
        rc = tuple(tuple(c) for c in rc)
        return (sig, rc)

    @property
    def leg_dict(self):
        return self._leg_dict

    @property
    def inv_leg_dict(self):
        return self._inv_leg_dict

    ## Psi classes are numbered according to the points of the stratum, but we want 
    ## to use them for the points of the graph. The leg_dicts translate between these, 
    ## we make this a little more user friendly.
    def stratum_number(self,n):
        """
        Returns a tuple (i,j) for the point j on the component i that corresponds 
        to the leg n of the graph.
        """
        return self._leg_dict[n]

    def leg_number(self,n):
        """
        Returns the leg number (of the graph G) that corresponds to the psi class
        number n.
        """
        return self._inv_leg_dict[n]

#################################################################
#################################################################
#################################################################
#################################################################

class EmbeddedLevelGraph(object):
    """
    LevelGraph inside a generalised stratum.

    Note that the points of the enveloping GeneralisedStratum are of the form
    (i,j) where i is the component and j the index of sig of that component,
    while the points of the level graph are numbers 1,...,n.

    Thus, dmp is a dictionary mapping integers to tuples of integers.

    Attributes:
        LG (LevelGraph): underlying LevelGraph
        X (GeneralisedStratum): enveloping stratum
        dmp (dict): (bijective!) dictionary marked points of LG -> points of stratum
        dmp_inv (dict): inverse of dmp
        dlevels (dict): (bijective!) dictionary levels of LG -> new level numbering
        dlevels_inv (dict): inverse of dlevels
        top (GeneralisedStratum): (if self is a BIC) top component
        bot (GeneralisedStratum): (if self is a BIC) bottom component
        clutch_dict (dict): (if self is a BIC) dictionary mapping points of top
            stratum to points of bottom stratum where there is an edge in self.
        emb_top (dict): (if self is a BIC) dictionary mapping points of stratum top
            to the corresponding points of the enveloping stratum.
        emb_bot (dict): (if self is a BIC) dictionary mapping points of stratum bot
            to the corresponding points of the enveloping stratum.
        automorphisms (list of list of dicts): automorphisms
        codim (int): codimension of LevelGraph in stratum
        number_of_levels (int): Number of levels of self.
    
    Note that attempting to access any of the attributes top, bot, clutch_dict,
    emb_top or emb_bot will raise a ValueError if self is not a BIC.
    """
    def __init__(self,X,LG,dmp,dlevels):
        """
        Initialises EmbeddedLevelGraph.
        
        Args:
            LG (LevelGraph): underlying LevelGraph
            X (GeneralisedStratum): enveloping stratum
            dmp (dictionary): (bijective!) dictionary marked points of LG -> points of stratum
            dlevels (dictionary): (bijective!) dictionary levels of LG -> new level numbering
        """
        self.LG = LG
        self.X = X
        self.dmp = dmp
        self.dmp_inv = {value: key for key, value in dmp.items()}
        self.add_vertices_at_infinity()
        self.dlevels = dlevels
        self.dlevels_inv = {value: key for key, value in dlevels.items()}
        self._top = None
        self._bot = None
        self._clutch_dict = None
        self._emb_top = None
        self._emb_bot = None
        self._automorphisms = None
        self._level = {}
        self._ell = None
        self.codim = self.LG.codim()
        self.number_of_levels = len(set(self.dlevels.keys()))

    def __repr__(self):
        return "EmbeddedLevelGraph(LG=%r,dmp=%r,dlevels=%r)" % (self.LG, self.dmp, self.dlevels)
    def __str__(self):
        return ("Embedded Level Graph consisting of %s with point dictionary %s and level dictionary %s"
                    % (self.LG, self.dmp, self.dlevels))

    def explain(self):
        """
        A more user-friendly display of __str__ :-)

        EXAMPLES ::

        """
        def _list_print(L):
            if len(L) > 1:
                s = ['s ']
                for x in L[:-2]:
                    s.append('%r, ' % x)
                s.append('%r ' % L[-2])
                s.append('and %r.' % L[-1])
                return ''.join(s)
            else:
                return ' %r.' % L[0]
        def _num(i):
            if i == 1:
                return 'one edge'
            else:
                return '%r edges' % i
        print("LevelGraph embedded into stratum %s with:" % self.X)
        LG = self.LG
        for l in range(LG.numberoflevels()):
            internal_l = LG.internal_level_number(l)
            print("On level %r:" % l)
            for v in LG.verticesonlevel(internal_l):
                print("* A vertex (number %r) of genus %r" % (v, LG.genus(v)))
        levels_of_mps = list(set([LG.level_number(LG.levelofleg(leg)) for leg in self.dmp]))
        print("The marked points are on level%s" % _list_print(sorted(levels_of_mps)))
        print("More precisely, we have:")
        for leg in self.dmp:
            print("* Marked point %r of order %r on vertex %r on level %r" % \
                    (self.dmp[leg], LG.orderatleg(leg), LG.vertex(leg), LG.level_number(LG.levelofleg(leg))))
        print("Finally, we have %s. More precisely:" % _num(len(LG.edges)))
        edge_dict = {e : (LG.vertex(e[0]), LG.vertex(e[1])) for e in LG.edges}
        edge_dict_inv = {}
        for k, v in edge_dict.items():
            if v in edge_dict_inv:
                edge_dict_inv[v].append(k)
            else:
                edge_dict_inv[v] = [k]
        for e in edge_dict_inv:
            print("* %s between vertex %r (on level %r) and vertex %r (on level %r) with prong%s" %
                    (_num(len(edge_dict_inv[e])), 
                    e[0], LG.level_number(LG.levelofvertex(e[0])),
                    e[1], LG.level_number(LG.levelofvertex(e[1])),
                    # _write_prongs()
                    _list_print([LG.prong(ee) for ee in edge_dict_inv[e]])))

    def __eq__(self,other):
        if not isinstance(other, EmbeddedLevelGraph):
            return False
        return self.LG == other.LG and self.dmp == other.dmp and self.dlevels == other.dlevels

    @cached_method
    def is_bic(self):
        return self.LG.is_bic()

    @property
    def ell(self):
        """
        If self is a BIC: the lcm of the prongs.
        
        Raises:
            RuntimeError: raised if self is not a BIC.
        
        Returns:
            int: lcm of the prongs.
        """
        if self._ell is None:
            if not self.is_bic():
                raise RuntimeError("ell only defined for BICs!")
            self._ell = lcm(self.LG.prongs.values())
        return self._ell

    @property
    def top(self):
        if self._top is None:
            self.split()
        return self._top

    @property
    def bot(self):
        if self._bot is None:
            self.split()
        return self._bot

    @property
    def clutch_dict(self):
        if self._clutch_dict is None:
            self.split()
        return self._clutch_dict

    @property
    def emb_bot(self):
        if self._emb_bot is None:
            self.split()
        return self._emb_bot

    @property
    def emb_top(self):
        if self._emb_top is None:
            self.split()
        return self._emb_top

    def add_vertices_at_infinity(self):
        """
        We add the vertices at infinity to the underlying_graph of self.LG.

        These are given by the residue conditions.

        More precisely: Recall that the underlying_graph of self.LG has vertices
        and edges of self.LG stored in the form UG_vertex = (vertex number, genus, 'LG')
        and edges of the underlying graph are of the form:
                (UG_vertex, UG_vertex, edge name)
        We now add vertices 'at level infinity' by adding, for each res_cond of self.X
            * a UG_vertex calles (i, 0, 'res') (where i is the index of the condition in res_cond
                we are currently considering)
        and edges so that each residue condition corresponds to an edge from the corresponding
        pole to some residue at 'level infinity'. We store these in the form:
            * (res_vertex, UG_vertex, resiedgej) 
        Here UG_vertex is the vertex of self.LG, in the form (vertex number, genus, 'LG'),
        that res_vertex is attached to and j is the leg of that vertex (as a leg of self.LG!)
        corresponding to the pole that resi should be attached to.
        """
        # remove any that might already be there:
        existing_residues = [v for v in self.LG.underlying_graph.vertices()
                                    if v[2] == 'res']
        for v in existing_residues:
            self.LG.underlying_graph.delete_vertex(v)
        # add a vertex for every residue condition:
        # TODO: remove duplicates?
        edges = []
        for i, rc in enumerate(self.X.res_cond):
            v_name = (i, 0, 'res')
            for p in rc:
                e_name = 'res%redge%r' % (i,self.dmp_inv[p])
                v_on_graph = self.LG.vertex(self.dmp_inv[p])
                edges.append((self.LG.UG_vertex(v_on_graph),v_name,e_name))
        self.LG.underlying_graph.add_edges(edges)

    @property
    @cached_method
    def residue_matrix_from_RT(self):
        """
        The matrix associated to the residue conditions imposed by the residue theorem
        on each vertex of self.
        
        Returns:
            SAGE Matrix: matrix of residue conditions given by RT
        """
        poles_by_vertex = {}
        for p in self.X._polelist:
            vertex = self.LG.vertex(self.dmp_inv[p])
            try:
                poles_by_vertex[vertex].append(p)
            except KeyError:
                poles_by_vertex[vertex] = [p]
        rows = []
        for v in poles_by_vertex:
            rows.append([int(p in poles_by_vertex[v]) for p in self.X._polelist])
        return matrix(QQ,rows)
    
    @property
    @cached_method
    def full_residue_matrix(self):
        """
        Residue matrix with GRC conditions and RT conditions (for each vertex).
        
        Returns:
            matrix: Matrix with # of poles columns and a row for each condition.
        """
        M = self.X.residue_matrix()
        if M:
            M = M.stack(self.residue_matrix_from_RT)
        else:
            M = self.residue_matrix_from_RT
        return M

    def residue_zero(self,pole):
        """
        Check if the residue at pole is forced zero by residue conditions.

        NOTE: We DO include the RT on the vertices in this check!
        
        Args:
            pole (tuple): pole (as a point (i,j) of self.X)
        
        Returns:
            bool: True if forced zero, False otherwise.
        """
        # add the equation corresponding to the residue at pole to the residue matrix
        # and see if the rank changes:
        i = self.X._polelist.index(pole)
        res_vec = [[int(i==j) for j in range(len(self.X._polelist))]]
        RM = self.full_residue_matrix
        # RM = self.X.residue_matrix()
        if RM:
            stacked = RM.stack(matrix(res_vec))
            return stacked.rank() == self.full_residue_matrix.rank()
            # return stacked.rank() == self.X.residue_matrix().rank()
        else:
            return False
                
    def level(self,l):
        """
        The generalised stratum on level l.

        Note that this is cached, i.e. on first call, it is stored in the dictionary
        _level.
        
        Args:
            l (int): relative level number (0,...,codim)
        
        Returns:
            LevelStratum: the LevelStratum, i.e. 
                * a list of Signatures (one for each vertex on the level)
                * a list of residue conditions, i.e. a list [res_1,...,res_r]
                    where each res_k is a list of tuples [(i_1,j_1),...,(i_n,j_n)]
                    where each tuple (i,j) refers to the point j (i.e. index) on the
                    component i and such that the residues at these points add up
                    to 0.
                * a dictionary of legs, i.e. n -> (i,j) where n is the original
                    number of the point (on the LevelGraph self) and i is the 
                    number of the component, j the index of the point in the signature tuple.
                Note that LevelStratum is a GeneralisedStratum together with
                a leg dictionary.
                Here, we provide an additional attribute:
                * leg_orbits, a nested list giving the orbits of the points on the level
                    under the automorphism group of self.
        
        EXAMPLES ::


            For the banana graph, the automorphisms fix the marked points but permute
            the edges. (ALL CONCRETE EXAMPLES REMOVED DUE TO INCONSISTENT BIC NUMBERING BETWEEN SAGE VERSIONS!!!)


            For the V-graph, the automorphisms permute edges on different components.


            In the stratum (4), there are more complicated examples.

        """
        try:
            LS = self._level[l]
        except KeyError:
            # for the residue conditions: We add the residue conditions from
            # the enveloping stratum:
            # We do this by passing those poles with residue forced zero
            # as those to be ignored in the residue calcuations performed by the
            # LevelGraph:
            # We have to translate them to points on self:
            # Note that self.LG knows the "level at infinity"
            excluded_poles = tuple(self.dmp_inv[p] for p in flatten(self.X.res_cond,max_level=1))
            LS = self.LG.stratum_from_level(l,excluded_poles=excluded_poles)
            # add automorphism info
            LS.leg_orbits = []
            seen = set()
            for leg in LS._leg_dict:
                if leg in seen:
                    continue
                curr_orbit = [LS._leg_dict[leg]]
                for _v_map, l_map in self.automorphisms:
                    curr_orbit.append(LS._leg_dict[l_map[leg]])
                    seen.update([l_map[leg]])
                LS.leg_orbits.append(list(set(curr_orbit)))  # remove duplicates
            self._level[l] = LS
        return LS
    
    def legs_are_isomorphic(self,leg,other_leg):
        """
        Check if leg and other_leg are in the same Aut-orbit of self.
        
        Args:
            leg (int): leg on self.LG
            other_leg (int): leg on self.LG
        
        Raises:
            RuntimeError: If leg is not in any aut-orbit of the level it should be on.
        
        Returns:
            bool: True if they are in the same orbit of self.level(levelofleg),
                    False, otherwise.

        EXAMPLES ::


            Note the assymetric banana graph.


            The symmetric one has isomorphisms.


            Legs are isomorphic to themselves.

            It's symmetric.

        """
        level = self.LG.level_number(self.LG.levelofleg(leg))
        other_level = self.LG.level_number(self.LG.levelofleg(other_leg))
        if level != other_level:
            return False
        assert(level == other_level)
        emb_leg = self.level(level)._leg_dict[leg]
        emb_other_leg = self.level(level)._leg_dict[other_leg]
        for orbit in self.level(level).leg_orbits:
            if emb_leg in orbit:
                if emb_other_leg in orbit:
                    return True
                else:
                    return False
        else:
            raise RuntimeError ("leg %r not in any orbit %r of %r" %
                                (leg,self.level(level).leg_orbits,self.level(level)))

    @cached_method
    def edge_orbit(self,edge):
        """
        The edge orbit of edge in self.
        
        Args:
            edge (tuple): edge of self.LG, i.e. tuple (start leg, end leg), where
                start leg should not be on a lower level than end leg.
        
        Raises:
            ValueError: if edge is not an edge of self.LG
        
        Returns:
            set: set of edges in aut-orbit of edge.
        
        EXAMPLES ::

        """
        if not edge in self.LG.edges:
            raise ValueError("%r is not an edge of %r!" % (edge, self))
        s = set([edge])
        for v_map, l_map in self.automorphisms:
            new_edge = (l_map[edge[0]], l_map[edge[1]])
            s.add(new_edge)
        return s

    def len_edge_orbit(self,edge):
        """
        Length of the edge orbit of edge in self.
        
        Args:
            edge (tuple): edge of self.LG, i.e. tuple (start leg, end leg), where
                start leg should not be on a lower level than end leg.
        
        Raises:
            ValueError: if edge is not an edge of self.LG
        
        Returns:
            int: length of the aut-orbit of edge.
        
        EXAMPLES ::


            Prongs influence the orbit length.

        """
        return len(self.edge_orbit(edge))

    def automorphisms_stabilising_legs(self,leg_tuple):
        stabs = []
        for v_map, l_map in self.automorphisms:
            for l in leg_tuple:
                if l_map[l] != l:
                    break
            else:  # no break
                stabs.append(l_map)
        return stabs

    def delta(self,i):
        """
        Squish all levels except for i.
        
        Note that delta(1) contracts everything except top-level and that the 
        argument is interpreted via internal_level_number (i.e. a relative level number).

        Moreover, dlevels is set to map to 0 and -1(!).

        Args:
            i (int): Level not to be squished.
        
        Returns:
            EmbeddedLevelGraph: Embedded BIC (result of applying delta to the 
                underlying LevelGraph)
        """
        newLG = self.LG.delta(i,quiet=True)
        newdmp = self.dmp.copy()
        # level_number is (positive!) relative level number.
        newdlevels = {l:-newLG.level_number(l) for l in newLG.levels}
        return EmbeddedLevelGraph(self.X,newLG,newdmp,newdlevels)
    
    def squish_vertical(self,level):
        """
        Squish level crossing below level 'level'.

        Note that in contrast to the levelgraph method, we work with relative
        level numbers here!
        
        Args:
            level (int): relative (!) level number.
        
        Returns:
            EmbeddedLevelGraph: Result of squishing.
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((4,))])
            sage: p = X.enhanced_profiles_of_length(4)[0][0]
            sage: g = X.lookup_graph(p)

            lookup_graph uses the sorted profile (note that these do not have to be reduced!):

            sage: assert any(g.squish_vertical(0).is_isomorphic(G) for G in X.lookup(p[1:]))
            sage: assert any(g.squish_vertical(1).is_isomorphic(G) for G in X.lookup(p[:1]+p[2:]))
            sage: assert any(g.squish_vertical(2).is_isomorphic(G) for G in X.lookup(p[:2]+p[3:]))
            sage: assert any(g.squish_vertical(3).is_isomorphic(G) for G in X.lookup(p[:3]))

            Squishing outside the range of levels does nothing:

            sage: assert g.squish_vertical(4) == g

            Recursive squishing removes larger parts of the profile:

            sage: assert any(g.squish_vertical(3).squish_vertical(2).is_isomorphic(G) for G in X.lookup(p[:2]))
        """
        newLG = self.LG.squish_vertical(self.LG.internal_level_number(level),quiet=True)
        newdmp = self.dmp.copy()
        # level_number is (positive!) relative level number.
        newdlevels = {l:-newLG.level_number(l) for l in newLG.levels}
        return EmbeddedLevelGraph(self.X,newLG,newdmp,newdlevels)

    def split(self):
        """
        Splits embedded BIC self into top and bottom component.
        
        Raises:
            ValueError: Raised if self is not a BIC.

        Returns:
            dict: dictionary consising of
                * X:            GeneralisedStratum self.X
                * top:          LevelStratum: top component
                * bottom:       LevelStratum: bottom component
                * clutch_dict:  clutching dictionary mapping ex-half-edges on 
                        top to their partners on bottom (both as points in the 
                        respective strata!)
                * emb_dict_top: a dictionary embedding top into the stratum of self
                * emb_dict_bot: a dictionary embedding bot into the stratum of self
        
        Note that clutch_dict, emb_top and emb_bot are dictionaries between 
        points of strata, i.e. after applying dmp to the points!

        EXAMPLES ::

        """
        if not self.is_bic():
            raise ValueError(
                    "Error: %s is not a BIC! Cannot be split into Top and Bottom component!"
                    % self)
        self._top = self.level(0)
        self._bot = self.level(1)
        # To construct emb_top and emb_bot, we have to combine self.dmp with the
        # the leg_dicts of top and bot.
        # More precisely: emb_top is the composition of the inverse of the leg_dict
        # of top, i.e. top.stratum_number, and self.dmp
        # (giving a map from the points of top to the points of the enveloping
        # stratum of self) and the same for bot.
        # We implement this by iterating over the marked points of self on top level,
        # which are exactly the keys of self.dmp that are on top level.
        # Note that we make extra sure that we didn't mess up the level numbering by
        # using the relative level numbering (where the top level is guaranteed to be 0
        # and the bottom level is 1 (positive!)).
        self._emb_top = {self._top.stratum_number(l) : self.dmp[l]
                            for l in iter(self.dmp)
                                if self.LG.level_number(self.LG.levelofleg(l)) == 0}
        self._emb_bot = {self._bot.stratum_number(l) : self.dmp[l]
                            for l in iter(self.dmp)
                                if self.LG.level_number(self.LG.levelofleg(l)) == 1}
        # Because this is a BIC, all edges of self are cut in this process
        # and this is exactly the dictionary we must remember
        # WARNING: Here we assume that e[0] is on top level and e[1] is on bottom
        #   This is assured by tidy_up, e.g. after initialisation!
        # Note that all these dictionaries map points of GeneralisedStrata to each
        # other so we must take the corresponding stratum_number!
        self._clutch_dict = {self._top.stratum_number(e[0]) : self._bot.stratum_number(e[1])
                                    for e in self.LG.edges}
        return {'X': self.X, 'top': self._top, 'bottom': self._bot,
                'clutch_dict': self._clutch_dict, 
                'emb_dict_top': self._emb_top, 'emb_dict_bot': self._emb_bot,}

    def is_legal(self):
        """
        Check the R-GRC for self.
        
        Returns:
            bool: result of R-GRC.
        """
        # Check if any levels are empty:
        # Note that this can only happen if self.X has simple poles (as we never
        # have horizontal edges)
        if self.X.simple_poles():
            if any(self.level(l).is_empty() for l in range(self.number_of_levels)):
                return False
        # poles are excluded if they are contained in _any_ residue condition of the stratum.
        # In particular, they are _not_ excluded if they are only restrained by the RT on some component!
        poles_in_rc_stratum = flatten(self.X.res_cond, max_level=1)
        poles_in_rc_graph = tuple(self.dmp_inv[p] for p in poles_in_rc_stratum)
        return self.LG.is_legal(excluded_poles=poles_in_rc_graph, quiet=True)

    def is_isomorphic(self,other):
        """
        Check if self and other are isomorphic (as EmbeddedLevelGraphs).
        
        Args:
            other (EmbeddedLevelGraph): Graph to check isomorphism.
        
        Returns:
            bool: True if there exists at least one isomorphism.
        """
        # TODO: Maybe include a way to check against unembedded LGs
        # TODO: Check embedding!
        if not isinstance(other, EmbeddedLevelGraph):
            return False
        try:
            next(self.isomorphisms(other))
            return True
        except StopIteration:
            return False
    
    @property
    def automorphisms(self):
        """
        The automorphisms of self (as automorphisms of the underlying LevelGraph,
        respecting the embedding, see doc of isomorphisms).
        
        Returns:
            list: list of tuples:
                dict: map of vertices
                dict: map of legs
        
        EXAMPLES ::

        """
        if not self._automorphisms:
            self._automorphisms = list(self.isomorphisms(self))
        return self._automorphisms

    def isomorphisms(self,other):
        """
        Generator yielding the "next" isomorphism of self and other.

        Note that while this gives an "isomorphism" from self.LG to other.LG, this
        is not necessarily an isomorphism of the LevelGraphs (the numbered points may
        be permuted if this is "fixed" by the embedding).
        
        Args:
            other (EmbeddedLevelGraph): The (potentially) isomorphic EmbeddedLevelGraph.
        
        Yields:
            tuple: The next compatible isomorphism:
                dict: vertices of self.LG -> vertices of other.LG
                dict: legs of self.LG -> legs of other.LG
        """
        #### Isomorphisms of EmbeddedLevelGraphs:
        ## An isomorphism of EmbeddedLevelGraph is a set of compatible level isomorphisms.
        ## We iterate through the isomorphisms on each level and yield whenever we find
        ## compatible levelisomorphisms for all levels.
        ## Note that we use dlevels for this, as these should be compatible.
        # There are (at least) two ways in which this can be optimised:
        # * don't go through the entire product before checking edge compatibility!
        # * choose a smart ordering of levels (e.g. number of vertices)
        isom_vertices = {}
        isom_legs = {}
        for level_isos in itertools.product(*[self._level_iso(other,l) for l in self.dlevels.values()]):
            for level_iso_v, level_iso_l in level_isos:
                isom_vertices.update(level_iso_v)
                isom_legs.update(level_iso_l)
            # check edge compatibility
            for e in self.LG.edges:
                if (isom_legs[e[0]],isom_legs[e[1]]) not in other.LG.edges:
                    break
            else:  # no break
                yield isom_vertices.copy(), isom_legs.copy()

    def _level_iso(self,other,l):
        """
        Generator yielding the "next" isomorphism of level l of self and other.

        Here, l is a value of dlevels (this should be compatible).

        Note that we require the graph to have no horizontal edges, i.e. the level
        contains no edges!

        TODO: * Maybe add future horizontal support?
              * Maybe use relative level number instead? (this seems to give weird behaviour
                right now...)
        
        Args:
            other (EmbeddedLevelGraph): The embedded graph we are checking for isomorphism.
            l (int): Level number (embedded into the stratum, i.e. value of dlevels).
        
        Yields:
            tuple: the next isomorphism of levels:
                dict: vertices of self.LG -> vertices of other.LG
                dict: legs of self.LG -> legs of other.LG
        """
        #### Isomorphisms of levels:
        ## An isomorphism of levels consist of
        ## * a map: vertices to vertices
        ## * a map: legs to legs
        ## respecting:
        ## * the genus,
        ## * the number of legs on every vertex,
        ## * the order at every leg,
        ## * the marked points of the stratum (via dmp).
        ####
        # First, we extract the data for level l from self and other.
        # Note that we do not use stratum_from_level to avoid all the overhead.
        # TODO: All this should be cached!!
        l_self = self.LG.internal_level_number(l)
        l_other = other.LG.internal_level_number(l)
        # we need to be careful to distinguish the indices in the list of genera
        # of the LevelGraph from the actual genera.
        vv_self_idx = self.LG.verticesonlevel(l_self)  # list of indices
        vv_other_idx = other.LG.verticesonlevel(l_other)  # list of indices
        if len(vv_self_idx) != len(vv_other_idx):
            return
        vv_self = [self.LG.genus(i) for i in vv_self_idx]  # list of genera
        vv_other = [other.LG.genus(i) for i in vv_other_idx]  # list of genera
        # extract the legs: (nested lists)
        legs_self = [self.LG.legsatvertex(v) for v in vv_self_idx]
        legs_other = [other.LG.legsatvertex(v) for v in vv_other_idx]
        # build dictionary: leg -> index in vv
        leg_dict_self = {l:i for i,legs in enumerate(legs_self) for l in legs}
        leg_dict_other = {l:i for i, legs in enumerate(legs_other) for l in legs}
        if len(leg_dict_self) != len(leg_dict_other):
            return
        # for quick checks, we create sorted lists of the orders at each vertex
        order_sorted_self = [sorted([self.LG.orderatleg(l) for l in legs]) 
                                for legs in legs_self]
        order_sorted_other = [sorted([other.LG.orderatleg(l) for l in legs]) 
                                for legs in legs_other]
        # We create the two maps as dictionaries:
        # index of vv_self -> index of vv_other
        isom_vert = {}
        # leg number (on self.LG) -> leg number (on other.LG)
        isom_legs = {}
        # We also want to keep track of whom we've already mapped:
        # source is a dictionary: genus -> list of indices of vv_self
        source = {}
        for i, g in enumerate(vv_self):
            try:
                source[g].append(i)
            except KeyError:
                source[g] = [i]
        # target is a dictionary: genus -> list of indices of vv_other
        target = {}
        for i, g in enumerate(vv_other):
            try:
                target[g].append(i)
            except KeyError:
                target[g] = [i]
        # for the legs we build copies of the nested lists to manipulate
        legs_source = [legs[:] for legs in legs_self]
        legs_target = [legs[:] for legs in legs_other]
        # Next, we exclude some deal-breakers:
        # * The same genera must appear.
        if sorted(vv_self) != sorted(vv_other):
            return
        # * The same embedded points have to be on this level (they have to be
        # mapped to each other!)
        # In particular, this gives a part of the leg map (and thus also of the
        # vertex map).
        for p_self, p in self.dmp.items():  # p is the "shared" point of the stratum
            p_other = other.dmp_inv[p]
            # If neither point is on this level, we continue:
            if not (p_self in leg_dict_self or p_other in leg_dict_other):
                continue
            # The vertex of p_self must map to that of p_other.
            # Three things can fail here:
            # * only one of the two points is on this level.
            if ((p_self in leg_dict_self and p_other not in leg_dict_other) or
                (p_self not in leg_dict_self and p_other in leg_dict_other)):
                return
            v_self = leg_dict_self[p_self]
            v_other = leg_dict_other[p_other]
            # * the points are on incompatible vertices (genus or numbers/orders of legs!)
            if (vv_self[v_self] != vv_other[v_other] or
                len(legs_self[v_self]) != len(legs_other[v_other]) or
                order_sorted_self[v_self] != order_sorted_other[v_other]):
                return
            # * two points are on the same vertex in one case, but on different vertices
            #   in the other. I.e. v_self is already being mapped somewhere other than v_other
            #   or v_other is already being mapped to (by someone else)
            try:
                if isom_vert[v_self] != v_other:
                    return
            except KeyError:  # v_self not being mapped yet, i.e. still in source
                g = vv_other[v_other]
                if v_other in target[g]:  # make sure v_other is still a possible target
                    isom_vert[v_self] = v_other
                    source[g].remove(v_self)
                    target[g].remove(v_other)
                else:
                    return
            # now we can safely map the legs:
            isom_legs[p_self] = p_other
            # and remove them from source and target (so they won't be reassigned later)
            legs_source[v_self].remove(p_self)
            legs_target[v_other].remove(p_other)
        # Next, we construct maps of the remaining vertices.
        # For this, we use a small recursive function:
        curr_v_map = {}
        legal_v_maps = []
        def vertex_maps(sl,tl):
            if not sl:
                # all entries of tl should be None at this point:
                assert(all(tv is None for tv in tl))
                legal_v_maps.append(curr_v_map.copy())
                return
            curr_v = sl.pop()
            curr_legs = len(legs_self[curr_v])
            # try to map curr_v to tl:
            for i,tv in enumerate(tl):
                # we temporarily set "hit" targets to None so we don't have to worry
                # about indexing...
                if tv is None:  
                    continue
                # check if legs _can_ be compatible:
                if (curr_legs != len(legs_other[tv]) or 
                    order_sorted_self[curr_v] != order_sorted_other[tv]):
                    continue
                tl[i] = None
                curr_v_map[curr_v] = tv
                vertex_maps(sl,tl)
                # undo
                del curr_v_map[curr_v]
                tl[i] = tv
            # undo
            sl.append(curr_v)
        # the function for the legs is almost the same, just the condition is different:
        curr_l_map = {}
        legal_l_maps = []
        def leg_maps(sl,tl):
            if not sl:
                # all entries of tl should be None at this point:
                assert(all(tleg is None for tleg in tl))
                legal_l_maps.append(curr_l_map.copy())
                return
            curr_l = sl.pop()
            # try to map curr_l to tl:
            for i, tleg in enumerate(tl):
                # we temporarily set "hit" targets to None so we don't have to worry
                # about indexing...
                if tleg is None:
                    continue
                # check if orders are compatible:
                if self.LG.orderatleg(curr_l) == other.LG.orderatleg(tleg):
                    tl[i] = None
                    curr_l_map[curr_l] = tleg
                    leg_maps(sl,tl)
                    # undo
                    del curr_l_map[curr_l]
                    tl[i] = tleg
            # undo
            sl.append(curr_l)
        # Now we build the list of all vertex isomorphisms going through the vertices by genus
        v_isom_list = []
        for g in source:
            legal_v_maps = []  # will get filled by vertex_maps
            vertex_maps(source[g],target[g])
            v_isom_list.append(legal_v_maps[:])  # copy!
        # v_isom_list is now a nested list of maps for each genus.
        # the product consists of tuples, one map for every genus.
        for v_maps in itertools.product(*v_isom_list):
            for v_map in v_maps:
                # this overwrites exactly the vertices in source.
                isom_vert.update(v_map)
            # Finally, the returned vertex map should use the indexing of the
            # LevelGraph, not of the level:
            return_isom_vert = {vv_self_idx[k] : vv_other_idx[v]
                                    for k,v in isom_vert.items()}
            # Now we build all leg maps, again as a product of all maps at vertices.
            # Note: This also included the previously assigned vertices (with marked points...)
            l_isom_list = []
            for v in isom_vert:  
                # Construct leg maps:
                # We work with legs_source and legs_target, i.e. the list
                # of legs with the marked points removed.
                legal_l_maps = []
                leg_maps(legs_source[v],legs_target[isom_vert[v]])
                l_isom_list.append(legal_l_maps[:])  # copy!
            for l_maps in itertools.product(*l_isom_list):
                for l_map in l_maps:
                    isom_legs.update(l_map)
                yield return_isom_vert.copy(), isom_legs.copy()

#################################################################
#################################################################
#################################################################
#################################################################

class AdditiveGenerator (SageObject):
    """
    Product of Psi classes on an EmbeddedLevelGraph (of a stratum X).

    The information of a product of psi-class on an EmbeddedLevelGraph, i.e. a
    leg_dict and an enhanced_profile, where leg_dict is a dictionary on the legs
    leg -> exponent of the LevelGraph associated to the enhanced profile, i.e. 
    (profile,index) or None if we refer to the class of the graph.

    We (implicitly) work inside some stratum X, where the enhanced profile
    makes sense.

    This class should be considered constant (hashable)!
    """
    def __init__ (self,X,enh_profile,leg_dict=None):
        """
        AdditiveGenerator for psi polynomial given by leg_dict on graph
        corresponding to enh_profile in X.
        
        Args:
            X (GeneralisedStrataum): enveloping stratum
            enh_profile (tuple): enhanced profile (in X)
            leg_dict (dict, optional): dictionary leg of enh_profile -> exponent
                encoding a psi monomial. Defaults to None.
        """
        self._X = X
        self._hash = hash_AG(leg_dict, enh_profile)
        self._enh_profile = (tuple(enh_profile[0]),enh_profile[1])
        self._leg_dict = leg_dict
        self._G = self._X.lookup_graph(*enh_profile)
        # dictionary leg -> level
        # Careful! These are leg numbers on the whole graph, not on
        # the graphs inside the LevelStrata!!
        self._level_dict = {}
        if not leg_dict is None:
            for l in leg_dict:
                self._level_dict[l] = self._G.LG.level_number(self._G.LG.levelofleg(l))
        self._inv_level_dict = {}
        for leg in self._level_dict:
            try:
                self._inv_level_dict[self._level_dict[leg]].append(leg)
            except KeyError:
                self._inv_level_dict[self._level_dict[leg]] = [leg]

    @classmethod
    def from_hash(cls,X,hash):
        """
        AdditiveGenerator from a hash generated with hash_AG.
        
        Args:
            X (GeneralisedStratum): Enveloping stratum.
            hash (tuple): hash from hash_AG
        
        Returns:
            AdditiveGenerator: AG from hash.
        """
        if hash[0] is None:
            leg_dict = None
        else:
            leg_dict = dict(hash[0])
        return cls(X,(hash[1],hash[2]),leg_dict)

    def __hash__(self):
        return hash(self._hash)
    def __eq__(self,other):
        try:
            return self._hash == other._hash
        except AttributeError:
            return NotImplemented

    def __repr__(self):
        return "AdditiveGenerator(X=%r,enh_profile=%r,leg_dict=%r)"\
             % (self._X, self._enh_profile, self._leg_dict)
        # Better, but destroys tests:
        # return "AdditiveGenerator(enh_profile=%r,leg_dict=%r)"\
        #      % (self._enh_profile, self._leg_dict)
    def __str__(self):
        str = ""
        if not self._leg_dict is None:
            for l in self._leg_dict:
                str += "Psi class %r with exponent %r on level %r * "\
                            % (l, self._leg_dict[l], self._level_dict[l])
        str += "Graph %r" % (self._enh_profile,)
        return str
    
    def __mul__(self,other):
        """
        Multiply to psi products on the same graph (add dictioaries).
        
        Args:
            other (AdditiveGenerator): Product of psi classes on same graph.
        
        Returns:
            AdditiveGenerator: Product of psi classes on same graph.
        
        EXAMPLES ::


            Also works without legs.
    
        """
        # Check that other is an AdditiveGenerator for the same graph:
        try:
            if self._X != other._X or self._enh_profile != other._enh_profile:
                return NotImplemented
            other_leg_dict = other._leg_dict
        except AttributeError:
            return NotImplemented
        # "unite" the leg_dicts:
        if self._leg_dict is None:
            self_leg_dict = {}
        else:
            self_leg_dict = self._leg_dict
        if other_leg_dict is None:
            other_leg_dict = {}
        new_leg_dict = {l:self_leg_dict.get(l,0) + other_leg_dict.get(l,0)
                            for l in set(self_leg_dict) | set(other_leg_dict)}
        return self._X.additive_generator(self._enh_profile,new_leg_dict)
    def __rmul__(self,other):
        self.__mul__(other)
    def __pow__(self, n):
        return self.pow(n)

    @property
    def enh_profile(self):
        return self._enh_profile

    @property
    def psi_degree(self):
        """
        Sum of powers of psi classes of self.
        """
        if self._leg_dict is None:
            return 0
        else:
            return sum(self._leg_dict.values())

    @cached_method
    def dim_check(self):
        """
        Check if, on any level, the psi degree is higher than the dimension.
        
        Returns:
            bool: False if the class is 0 for dim reasons, True otherwise.
        """
        # remove if degree > dim(X)
        if self.degree > self._X.dim():
            return False
        if self.codim == 0:
            # Avoid crazy infinite recursion for smooth graph :-)
            return True
        # for each level, check if psi product on level exceeds level dimension
        for level_number in range(self.codim + 1):
            assert self.level_dim(level_number) >= 0
            if self.degree_on_level(level_number) > self.level_dim(level_number):
                return False
        return True

    @property
    def codim(self):
        """
        The codimension of the graph (number of levels)
        
        Returns:
            int: length of the profile
        """
        return len(self._enh_profile[0])

    @property
    def degree(self):
        """
        Degree of class, i.e. codimension of graph + psi-degree
        
        Returns:
            int: codim + psi_degree
        """
        # degree = codim of graph + powers of psi classes
        return self.codim + self.psi_degree

    @property
    def leg_dict(self):
        return self._leg_dict

    @property
    def level_dict(self):
        """
        The dictionary mapping leg -> level
        """
        return self._level_dict

    @property
    def inv_level_dict(self):
        """
        The dictionary mapping level -> list of legs on level.
        
        Returns:
            dict: level -> list of legs.
        """
        return self._inv_level_dict

    @cached_method
    def degree_on_level(self,level):
        """
        Total degree of psi classes on level.
        
        Args:
            level (int): (relative) level number (i.e. 0...codim)
        
        Raises:
            RuntimeError: Raised for level number out of range.
        
        Returns:
            int: sum of exponents of psis appearing on this level.
        """
        if level not in range(self.codim + 1):
            raise RuntimeError("Illegal level number: %r on %r" % (level, self))
        try:
            return sum(self._leg_dict[leg] for leg in self._inv_level_dict[level])
        except KeyError:
            # no psis on this level
            return 0
    
    def level(self,level_number):
        """
        Level of underlying graph.
        
        Args:
            level_number (int): (relative) level number (0...codim)
        
        Returns:
            LevelStratum: Stratum at level level_number of self._G.
        """
        return self._G.level(level_number)

    @cached_method
    def level_dim(self,level_number):
        """
        Dimension of level level_number.
        
        Args:
            level_number (int): (relative) level number (i.e. 0...codim)
        
        Returns:
            int: dimension of GeneralisedLevelStratum
        """
        level = self._G.level(level_number)
        return level.dim()

    @property
    def stack_factor(self):
        """
        The stack factor, that is the product of the prongs of the underlying graph
        divided by the product of the ells of the BICs and the automorphisms.
        
        Returns:
            QQ: stack factor
        """
        try:
            return self._stack_factor
        except AttributeError:
            # to get g_Gamma, we have to take the product of prongs/lcm for each bic:
            prod = 1
            for k in self._G.LG.prongs.values():
                prod *= k

            p, _ = self.enh_profile

            bic_contr = 1
            for i in p:
                bic_contr *= self._X.bics[i].ell

            stack_factor = QQ(prod) / QQ(bic_contr * len(self._G.automorphisms))

            self._stack_factor = stack_factor
            return self._stack_factor

    @cached_method
    def as_taut(self):
        """
        Helper method, returns [(1,self)] as default input to ELGTautClass.
        """
        return ELGTautClass(self._X,[(1,self)])
    
    @cached_method
    def is_in_ambient(self,ambient_enh_profile):
        """
        Check if ambient_enh_profile is an ambient graph, i.e. self is a degeneration
        of ambient_enh_profile.
        
        Args:
            ambient_enh_profile (tuple): enhanced profile.
        
        Returns:
            bool: True if there exists a leg map, False otherwise.
        
        EXAMPLES ::

        """
        return self._X.is_degeneration(self._enh_profile,ambient_enh_profile)

    @cached_method
    def pow(self, n, amb=None):
        """
        Recursively calculate the n-th power of self (in amb), caching all results.
        
        Args:
            n (int): exponent
            amb (tuple, optional): enhanced profile. Defaults to None.
        
        Returns:
            ELGTautClass: self^n in CH(amb)
        """
        if amb is None:
            ONE = self._X.ONE
            amb = ((),0)
        else:
            ONE = self._X.taut_from_graph(*amb)
        if n == 0:
            return ONE
        return self._X.intersection(self.as_taut(), self.pow(n-1, amb), amb)

    @cached_method
    def exp(self, c, amb=None, stop=None):
        """
        exp(c * self) in CH(amb), calculated via exp_list.
        
        Args:
            c (QQ): coefficient
            amb (tuple, optional): enhanced profile. Defaults to None.
            stop (int, optional): cut-off. Defaults to None.
        
        Returns:
            ELGTautClass: the tautological class associated to the
                graded list exp_list.
        """
        # graded pieces are already reduced:
        new_taut_list = []
        for T in self.exp_list(c, amb, stop):
            new_taut_list.extend(T.psi_list)
        return ELGTautClass(self._X, new_taut_list, reduce=False)

    @cached_method
    def exp_list(self, c, amb=None, stop=None):
        """
        Calculate exp(c * self) in CH(amb).

        We calculate exp as a sum of powers (using self.pow, i.e. cached)
        and check at each step if the power vanishes (if yes, we obviously stop).

        The result is returned as a list consisting of the graded pieces.

        Optionally, one may specify the cut-off degree using stop (by
        default this is dim + 1).
        
        Args:
            c (QQ): coefficient
            amb (tuple, optional): enhanced profile. Defaults to None.
            stop (int, optional): cut-off. Defaults to None.
        
        Returns:
            list: list of ELGTautClasses
        """
        c = QQ(c)
        if amb is None:
            ONE = self._X.ONE
            amb = ((),0)
        else:
            ONE = self._X.taut_from_graph(*amb)
        e = [ONE]
        f = ONE
        coeff = QQ(1)
        k = QQ(0)
        if stop is None:
            stop = self._X.dim() + 1
        while k < stop and f != self._X.ZERO:
            k += 1
            coeff *= c/k
            f = self.pow(k, amb)
            e.append(coeff * f)
        return e

    def pull_back(self,deg_enh_profile):
        """
        Pull back self to the graph associated to deg_enh_profile.

        Note that this returns an ELGTautClass as there could be several maps.

        More precisely, we return the sum over the pulled back classes divided
        by the number of undegeneration maps.

        Args:
            deg_enh_profile (tuple): enhanced profile of graph to pull back to.
        
        Raises:
            RuntimeError: raised if deg_enh_profile is not a degeneration of the 
                underlying graph of self.
        
        Returns:
            ELGTautClass: sum of pullbacks of self to deg_enh_profile for each
                undegeneration map divided by the number of such maps.

        """
        if self._leg_dict is None:
            # trivial pullback
            return ELGTautClass(self._X,[(1,self._X.additive_generator(deg_enh_profile))])
        else:
            leg_maps = self._X.explicit_leg_maps(self._enh_profile,deg_enh_profile)
            if leg_maps is None:
                raise RuntimeError ("Pullback failed: %r is not a degeneration of %r")\
                    % (deg_enh_profile,self._enh_profile)
            psi_list = []
            aut_factor = QQ(1) / QQ(len(leg_maps))
            for leg_map in leg_maps:
                new_leg_dict = {leg_map[l]:e for l, e in self._leg_dict.items()}
                psi_list.append((aut_factor,self._X.additive_generator(deg_enh_profile,new_leg_dict)))
            return ELGTautClass(self._X,psi_list)

    def evaluate(self,quiet=False,warnings_only=False,admcycles_output=False):
        """
        Evaluate self (cap with the fundamental class of self._X).

        Note that this gives 0 if self is not a top-degree class.

        Evaluation works by taking the product of the evaluation of each level
        (i.e. evaluating, for each level, the psi monomial on this level) and
        multiplying this with the stack factor.

        The psi monomials on the levels are evaluated using admcycles (after 
        removing residue conditions).
        
        Args:
            quiet (bool, optional): No output. Defaults to False.
            warnings_only (bool, optional): Output warnings. Defaults to False.
            admcycles_output (bool, optional): Output admcycles debugging info 
                (used when evaluating levels). Defaults to False.
        
        Raises:
            RuntimeError: raised if there are inconsistencies with the psi
            degrees on the levels.
        
        Returns:
            QQ: integral of self on X.
        """
        if self.degree < self._X.dim():
            if not quiet or warnings_only:
                print("Warning: %r is not of top degree: %r (instead of %r)" % (self,self.degree,self._X.dim()))
            return 0
        level_list = []
        for l in range(self.codim + 1):
            if self.degree_on_level(l) < self.level_dim(l):
                raise RuntimeError("%r is of top degree, but not on level %r" % (self,l))
            L = self.level(l)
            # The psi classes on this level should be expressed in terms of the legs
            # of the smooth_LG of L:
            EG = L.smooth_LG
            try:
                # Careful: the legs of the smooth_LG are numbered 1,...,n
                # The psi classes are still numbered inside the whole graph
                # The conversion runs through the embedding of the LevelStratum
                # and back through the embedding of smooth_LG (dmp_inv)
                psis_on_level = {EG.dmp_inv[L.leg_dict[leg]] : self.leg_dict[leg] 
                            for leg in self.inv_level_dict[l]}
            except KeyError:
                # no psis on this level
                psis_on_level = {}
            value = L.evaluate(psis=psis_on_level,quiet=quiet,warnings_only=warnings_only,admcycles_output=admcycles_output)
            if value == 0:
                return 0
            level_list.append(value)
        # product over levels:
        prod = 1
        for p in level_list:
            prod *= p
        if not quiet:
            print("----------------------------------------------------")
            print("Contribution of Additive generator:")
            print(self)
            print("Product of level-wise integrals: %r" % prod)
            print("Stack factor: %r" % self.stack_factor)
            print("Total: %r" % (prod*self.stack_factor))
            print("----------------------------------------------------")
        return self.stack_factor * prod

#################################################################
#################################################################
#################################################################
#################################################################

class ELGTautClass (SageObject):
    """
    A Tautological class of a stratum X, i.e. a formal sum of of psi classes on
    EmbeddedLevelGraphs.

    This is encoded by a list of summands.

    Each summand corresponds to an AdditiveGenerator with coefficient.

    Thus an ELGTautClass is a list with entries tuples (coefficient, AdditiveGenerator).

    These can be added, multiplied and reduced (simplified).

    INPUT :

      * X : GeneralisedStratum that we are on
      * psi_list : list of tuples (coefficient, AdditiveGenerator) as
            described above.
      * reduce=True : call self.reduce() on initialisation
    """
    def __init__(self,X,psi_list,reduce=True):
        self._psi_list = psi_list
        self._X = X
        if reduce:
            self.reduce()

    @classmethod
    def from_hash_list(cls,X,hash_list):
        # This does not reduce!
        return cls(X,[(c, X.additive_generator_from_hash(h)) for c,h in hash_list], reduce=False)

    @property
    def psi_list(self):
        return self._psi_list

    def __repr__(self):
        return "ELGTautClass(X=%r,psi_list=%r)"\
             % (self._X,self._psi_list)
    def __str__(self):
        str = "Tautological class on %s\n" % self._X
        for coeff, psi in self._psi_list:
            str += "%s * %s + \n" % (coeff, psi)
        return str
    
    def __eq__(self,other):
        if isinstance(other, AdditiveGenerator):
            return self == other.as_taut()
        try:
            return self._psi_list == other._psi_list
        except AttributeError:
            return False
    
    def __add__(self,other):
        # for sum, we need to know how to add '0':
        if other == 0:
            return self
        try:
            if not self._X == other._X:
                return NotImplemented
            new_psis = self._psi_list + other._psi_list
            return ELGTautClass(self._X,new_psis)
        except AttributeError:
            return NotImplemented
    def __iadd__(self,other):
        return self.__add__(other)
    def __radd__(self,other):
        return self.__add__(other)

    def __neg__(self):
        return (-1)*self

    def __sub__(self,other):
        return self + (-1)*other

    def __mul__ (self, other):
        if 0 == other:
            return 0
        elif self._X.ONE == other:
            return self
        # convert AdditiveGenerators to Tautclasses:
        if isinstance(other, AdditiveGenerator):
            return self * other.as_taut()
        try:
            # check if other is a tautological class
            _other_psi_list = other._psi_list
        except AttributeError:
            # attempt scalar multiplication:
            new_psis = [(coeff * other, psi) for coeff, psi in self._psi_list]
            return ELGTautClass(self._X,new_psis,reduce=False)
        if not self._X == other._X:
            return NotImplemented
        else:
            return self._X.intersection(self,other)
    def __rmul__(self,other):
        return self.__mul__(other)
    def __pow__(self,exponent):
        if exponent == 0:
            return self._X.ONE
        # TODO: quick check for going over top degree?
        prod = self
        for _ in range(1,exponent):
            prod = self * prod
        return prod

    @cached_method
    def is_equidimensional(self):
        """
        Determine if all summands of self have the same degree.

        Note that the empty empty tautological class (ZERO) gives True.
        
        Returns:
            bool: True if all AdditiveGenerators in self.psi_list are of same degree,
                False otherwise.
        """
        if self.psi_list:
            first_deg = self.psi_list[0][1].degree
            return all(AG.degree == first_deg for _c, AG in self.psi_list)
        return True

    def reduce(self):
        """
        Reduce self.psi_list by combining summands with the same AdditiveGenerator
        and removing those with coefficient 0 or that die for dimension reasons.
        """
        # we use the hash of the AdditiveGenerators to group:
        hash_dict = Counter()
        for c, AG in self._psi_list:
            hash_dict[AG] += c
        self._psi_list = [(c, AG) for AG, c in hash_dict.items() if c != 0 and AG.dim_check()]

    # To evaluate, we go through the AdditiveGenerators and
    # take the (weighted) sum of the AdditiveGenerators.
    def evaluate(self,quiet=True,warnings_only=False,admcycles_output=False):
        """
        Evaluation of self, i.e. cap with fundamental class of X.

        This is the sum of the evaluation of the AdditiveGenerators in psi_list
        (weighted with their coefficients).

        Each AdditiveGenerator is (essentially) the product of its levels,
        each level is (essentially) evaluated by admcycles.
        
        Args:
            quiet (bool, optional): No output. Defaults to True.
            warnings_only (bool, optional): Only warnings output. Defaults to False.
            admcycles_output (bool, optional): admcycles debugging output. Defaults to False.
        
        Returns:
            QQ: integral of self on X
        
        EXAMPLES ::

            sage: from admcycles.diffstrata import *
            sage: X=GeneralisedStratum([Signature((0,0))])
            sage: assert (X.xi^2).evaluate() == 0

            sage: X=GeneralisedStratum([Signature((1,1,1,1,-6))])
            sage: assert set([(X.cnb(((i,),0),((i,),0))).evaluate() for i in range(len(X.bics))]) == {-2, -1}
        """
        if warnings_only:
            quiet = True
        DS_list = []
        for c, AG in self.psi_list:
            value = AG.evaluate(quiet=quiet,warnings_only=warnings_only,admcycles_output=admcycles_output)
            DS_list.append(c * value)
        if not quiet:
            print("----------------------------------------------------")
            print("In summary: We sum")
            for i, summand in enumerate(DS_list):
                print("Contribution %r from AdditiveGenerator" % summand)
                print(self.psi_list[i][1])
                print("(With coefficient %r)" % self.psi_list[i][0])
            print("To obtain a total of %r" % sum(DS_list))
            print("----------------------------------------------------")
        return sum(DS_list)
    
    def extract(self,i):
        """
        Return the i-th component of self.
        
        Args:
            i (int): index of self._psi_list
        
        Returns:
            ELGTautClass: coefficient * AdditiveGenerator at position i of self.
        """
        return ELGTautClass(self._X,[self._psi_list[i]],reduce=False)

    @cached_method
    def degree(self, d):
        """
        The degree d part of self.
        
        Args:
            d (int): degree
        
        Returns:
            ELGTautClass: degree d part of self
        """
        new_psis = []
        for c, AG in self.psi_list:
            if AG.degree == d:
                new_psis.append((c, AG))
        return ELGTautClass(self._X, new_psis, reduce=False)
    
    @cached_method
    def list_by_degree(self):
        """
        A list of length X.dim with the degree d part as item d
        
        Returns:
            list: list of ELGTautClasses with entry i of degree i.
        """
        deg_psi_list = [[] for _ in range(self._X.dim() + 1)]
        for c, AG in self.psi_list:
            deg_psi_list[AG.degree].append((c, AG))
        return [ELGTautClass(self._X, piece, reduce=False) for piece in deg_psi_list]

#################################################################
#################################################################
#################################################################
#################################################################

#################################################################
#################################################################
### Auxillary functions:
#################################################################
#################################################################

def unite_embedded_graphs(gen_LGs):
    """
    Create a (disconnected) EmbeddedLevelGraph from a tuple of tuples that generate EmbeddedLevelGraphs.

    (The name is slightly misleading, but of course it does not make sense to actually unite two complete
    EmbeddedLevelGraphs, as the checks would (and do!) throw errors otherwise! Therefore, this essentially
    takes the data of a LevelGraph embedded into each connected componenent of a GeneralisedStratum and
    returns an EmbeddedLevelGraph on the product.)

    This should be used on (products) of BICs in generalised strata.
    
    Args:
        gen_LGs (tuple): tuple of tuples that generate EmbeddedLevelGraphs.
            More precisely, each tuple is of the form:
                * X (GeneralisedStratum): Enveloping stratum (should be the same for all tuples!)
                * LG (LevelGraph): Underlying LevelGraph
                * dmp (dict): (partial) dictionary of marked points
                * dlevels (dict): (partial) dictionary of levels
    
    Returns:
        EmbeddedLevelGraph: The (disconnected) LevelGraph obtained from the input with
            the legs renumbered (continuously, starting with 1), and the levels numbered
            according to the embedding. 
    """
    newgenera = []
    newlevels = []
    newlegs = []
    newpoleorders = {}
    newedges = []
    newdmp = {}
    newdlevels = {}
    max_leg_number = 0
    oldX = gen_LGs[0][0]  # for check that all belong to the same stratum:
    for emb_g in gen_LGs:
        # Unpack tuple:
        X, LG, dmp, dlevels = emb_g
        if X != oldX:
            raise RuntimeError("Can't unite graphs on different Strata! %r" % gen_LGs)
        # the genera are just appended
        newgenera += LG.genera
        # same for the levels, but while we're at it, we might just as well
        # replace them by their embedding (then newdlevels will be trivial)
        # and these should be consistens for all graphs in the tuple.
        # Thus, newdlevels will be the identity.
        newlevels += [dlevels[l] for l in LG.levels]
        # the legs will have to be renumbered
        leg_dict = {}  # old number -> new number
        legs = 0
        for i, l in enumerate(flatten(LG.legs)):
            newlegnumber = max_leg_number + i + 1
            leg_dict[l] = newlegnumber
            # while we're at it, we add the pole orders:
            newpoleorders[newlegnumber] = LG.poleorders[l]
            # For the dictionary of marked points (for the embedding), we
            # must distinguish if this is a marked point or a half-edge.
            # Marked points are simply the ones for which we have a key
            # in dmp :-)
            try:
                newdmp[newlegnumber] = dmp[l]
            except KeyError:
                pass
            legs += 1
        max_leg_number += legs
        # append (nested) list of legs:
        newlegs += [[leg_dict[l] for l in comp] for comp in LG.legs]
        # finally, the edges are renumbered accordingly:
        newedges += [(leg_dict[e[0]], leg_dict[e[1]]) for e in LG.edges]
    # the levels are already numbered according to the embedding dict
    newdlevels = {l:l for l in newlevels}
    newLG = admcycles.diffstrata.levelgraph.LevelGraph(
        newgenera, newlegs, newedges, newpoleorders, newlevels
    )
    return EmbeddedLevelGraph(X, newLG, newdmp, newdlevels)

def sort_with_dict(l):
    """
    Sort a list and provide a dictionary relating old and new indices.

    If x had index i in l, then x has index sorted_dict[i] in the sorted l.
    
    Args:
        l (list): List to be sorted.
    
    Returns:
        tuple: A tuple consisting of:
            list: The sorted list l.
            dict: A dictionary old index -> new index.
    """
    sorted_list = []
    sorted_dict = {}
    for i,(j,v) in enumerate(sorted(enumerate(l),key=lambda w:w[1])):
        sorted_list.append(v)
        sorted_dict[j] = i
    return sorted_list, sorted_dict

def get_squished_level(deg_ep,ep):
    """
    Get the (relative) level number of the level squished in ep.

    This is the index of the corresponding BIC in the profile.
    
    Args:
        deg_ep (tuple): enhanced profile
        ep (tuple): enhanced profile
    
    Raises:
        RuntimeError: raised if deg_ep is not a degeneration of ep
    
    Returns:
        int: relative level number
    """
    deg_p = deg_ep[0]
    p = set(ep[0])
    for i, b in enumerate(deg_p):
        if not b in p:
            break
    else:
        raise RuntimeError("%r is not a degeneration of %r!" % (deg_ep, p))
    return i

def _graph_word(n):
    if n == 1:
        return "graph"
    else:
        return "graphs"

#################################################################
#################################################################
### Auxillary functions for caching:
#################################################################
#################################################################

def hash_AG(leg_dict, enh_profile):
    """
    The hash of an AdditiveGenerator, built from the psis and the enhanced profile.

    The hash-tuple is (leg-tuple,profile,index), where profile is
    changed to a tuple and leg-tuple is a nested tuple consisting of
    tuples (leg,exponent) (or None).

    Args:
        leg_dict (dict): dictioary for psi powers (leg -> exponent)
        enh_profile (tuple): enhanced profile
    
    Returns:
        tuple: nested tuple
    """
    if leg_dict is None:
        leg_hash = ()
    else:
        leg_hash = tuple(sorted(leg_dict.items()))
    return (leg_hash,tuple(enh_profile[0]),enh_profile[1])

def adm_key(sig, psis):
    """
    The hash of a psi monomial on a connected stratum without residue conditions.

    This is used for caching the values computed using admcycles (using 
    GeneralisedStratum.adm_evaluate)

    The signature is sorted, the psis are renumbered accordingly and also
    sorted (with the aim of computing as few duplicates as possible).
    
    Args:
        sig (tuple): signature tuple
        psis (dict): psi dictionary
    
    Returns:
        tuple: nested tuple
    """
    sorted_psis = {}
    sorted_sig  = []
    psi_by_order = defaultdict(list)
    # sort signature and relabel psis accordingly:
    # NOTE: Psis are labelled 'mathematically', i.e. 1,...,len(sig)
    for new_i, (old_i, order) in enumerate(sorted(enumerate(sig), key=lambda k: k[1])):
        psi_new_i = new_i + 1
        psi_old_i = old_i + 1
        sorted_sig.append(order)
        if psi_old_i in psis:
            assert not (psi_new_i in sorted_psis)
            psi_exp = psis[psi_old_i]
            sorted_psis[psi_new_i] = psi_exp
            psi_by_order[order].append(psi_exp)
    # sort psis for points of same order:
    ordered_sorted_psis = {}
    i = 0
    assert len(sig) == len(sorted_sig)
    while i < len(sig):
        order = sorted_sig[i]
        for j, psi_exp in enumerate(sorted(psi_by_order[order])):
            assert sorted_sig[i+j] == order
            ordered_sorted_psis[i+j+1] = psi_exp
        while i < len(sig) and sorted_sig[i] == order:
            i += 1
    return (tuple(sorted_sig), tuple(sorted(ordered_sorted_psis.items())))

def import_adm_evals(filename):
    """
    Import a dictionary of the form adm_key : value into the cache.

    Before and after the import, the cache is synched with FILENAME.
    
    Args:
        filename (String): filename
    """
    cache = load_adm_evals()
    cache.update(sage.misc.persist.load(filename))
    sage.misc.persist.save(cache, FILENAME)

def import_top_xis(filename):
    """
    Import a dictionary of the form LevelStratum.dict_key : value into the cache.

    Before and after the import, the cache is synched with XI_FILENAME.
    
    Args:
        filename (String): filename
    """
    cache = load_xis()
    cache.update(sage.misc.persist.load(filename))
    sage.misc.persist.save(cache, XI_FILENAME)

def load_adm_evals():
    """
    The cache dictionary for the admcycles evaluations (via GeneralisedStratum.adm_evaluate)

    If non-existent, the dictionary is attempted to be read from FILENAME.

    The cache dictionary is of the form:

    adm_key -> GeneralisedStratum.adm_evaluate(adm_key)  (a rational number)
    
    Returns:
        dict: cache dictionary
    """
    global ADM_EVALS
    if not ADM_EVALS:
        # read from file (if existent)
        try:
            ADM_EVALS = sage.misc.persist.load(FILENAME)
        except IOError:
            return {}
    return ADM_EVALS

def load_xis():
    """
    The cache dictionary for the top xi powers (evaluated)

    If non-existent, the dictionary is attempted to be read from XI_FILENAME.

    The cache dictionary is of the form:

    L.dict_key -> (L.xi)^L.dim().evaluate()  (a rational number)

    for a LevelStratum L.
    
    Returns:
        dict: cache dictionary
    """
    global TOP_XIS
    if not TOP_XIS:
        # read from file (if existent)
        try:
            TOP_XIS = sage.misc.persist.load(XI_FILENAME)
        except IOError:
            return {}
    return TOP_XIS

def list_top_xis(xi_dict=None):
    """
    A generator for decyphering LevelStratum.dict_key

    By default, the xi cache is used (via load_xis), alternatively a different
    cache dictionary may be specified (see load_xis).
    
    Args:
        xi_dict (dict, optional): cache dictionary. Defaults to None.
    
    Yields:
        tuple: signature list, residue conditions, top xi evaluation
    """
    if xi_dict is None:
        xi_dict = load_xis()
    for key in sorted(xi_dict):
        sig_list, rcs = key
        yield (sig_list, rcs, xi_dict[key])

def print_top_xis(xi_dict=None):
    """
    The top xi powers in the cache are printed in human-readable form.

    Alternatively, any valid xi cache dictionary may be specified (see load_xis
    for details on the format).

    The dimensions of the table might have to be adapted to console size and
    complexity of the involved strata.
    
    Args:
        xi_dict (dict, optional): xi cache dictionary. Defaults to None.
    """
    if xi_dict is None:
        xi_dict = load_xis()
    LEFT = 40
    MIDDLE = 45
    RIGHT = 13
    print('{:<{width}}'.format('Stratum', width=LEFT) + '|' + 
        '{:<{width}}'.format(' Residue Conditions', width=MIDDLE) + '|' +
        '{:<{width}}'.format(' xi^dim', width=RIGHT))
    print('-'*(LEFT+MIDDLE+RIGHT))
    for sig_list, res_conds, xi in list_top_xis(xi_dict):
        if len(sig_list) == 1:
            sig = sig_list[0]
        else:
            sig = list(sig_list)
        if not res_conds:
            rcs = tuple()
        else:
            if len(res_conds) == 1:
                rcs = list(res_conds[0])
            else:
                rcs = [list(c) for c in res_conds]
        print('{:<{width}}'.format(str(sig), width=LEFT) + '| ' + 
            '{:<{width}}'.format(str(rcs), width=MIDDLE-1) + '| ' +
            '{:<{width}}'.format(str(xi), width=RIGHT-1))

def print_adm_evals(adm_dict=None):
    """
    The cached evaluations are printed in human-readable form.

    Alternatively, any valid adm cache dictionary may be specified (see load_adm_evals
    for details on the format).

    The dimensions of the table might have to be adapted to console size and
    complexity of the involved strata.
    
    Args:
        adm_dict (dict, optional): evaluations cache dictionary. Defaults to None.
    """
    if adm_dict is None:
        adm_dict = load_adm_evals()
    LEFT = 40
    MIDDLE = 45
    RIGHT = 13
    print('{:<{width}}'.format('Stratum', width=LEFT) + '|' + 
        '{:<{width}}'.format(' Psis', width=MIDDLE) + '|' +
        '{:<{width}}'.format(' eval', width=RIGHT))
    print('-'*(LEFT+MIDDLE+RIGHT))
    for key in sorted(adm_dict, key=lambda k: k[1]):  # sort by stratum
        sig, psis = key
        value = adm_dict[key]
        dpsis = dict(psis)
        print('{:<{width}}'.format(str(sig), width=LEFT) + '| ' + 
            '{:<{width}}'.format(str(dpsis), width=MIDDLE-1) + '| ' +
            '{:<{width}}'.format(str(value), width=RIGHT-1))

def jsonify_dict(d):
    json_dict = {}
    for k, v in d.items():
        json_dict[str(k)] = v
    return json_dict

def unjsonify_dict(json_dict):
    restored_dict = {}
    for k, v in json_dict.items():
        restored_dict[literal_eval(k)] = v
    return restored_dict