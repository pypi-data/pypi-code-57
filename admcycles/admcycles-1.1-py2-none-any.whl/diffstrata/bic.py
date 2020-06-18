from __future__ import print_function

import itertools

from sympy.utilities.iterables import partitions, permutations, multiset_partitions

# pylint does not know sage
from sage.graphs.graph import Graph # pylint: disable=import-error
from sage.graphs.generators.basic import CompleteBipartiteGraph # pylint: disable=import-error
# sage documentation says compositions are better than OrderedPartitions, no idea why....
from sage.combinat.composition import Compositions as sage_part # pylint: disable=import-error
from sage.combinat.partition import OrderedPartitions # pylint: disable=import-error
from sage.misc.cachefunc import cached_function # pylint: disable=import-error

from admcycles.stable_graph import StableGraph as stgraph
import admcycles.diffstrata.levelgraph
import admcycles.diffstrata.levelstratum
from admcycles.diffstrata.sig import Signature

############################################################
############################################################
#### Old BIC generation:
#### This was the first attempt at generating BICs 
#### (generating all stable graphs with admcycles and then
#### putting all possible bipartite structures etc on them).
#### It's nice for historic reasons but painfully slow!
#### Definitely use bic_alt below instead!!!
############################################################
############################################################

def SageGraph(gr):
    # converts stgraph gr in Sage graph
    legdic={i:vnum for vnum in range(len(gr.legs(copy=False))) for i in gr.legs(vnum,copy=False)}
    return Graph([(legdic[a], legdic[b]) for (a,b) in gr.edges(copy=False)],loops=True, multiedges=True)

def bics(g,orders):
    """
    Generate BICs for stratum with signature orders of genus g.

    DO NOT USE!!! USE bic_alt instead!!!
    
    Args:
        g (int): genus
        orders (tuple): signature tuple
    
    Returns:
        list: list of BICs
    """
    print('WARNING! This is not the normal BIC generation algorithm!')
    print("Only use if you know what you're doing!")
    n=len(orders)
    bound=g+n
    result=[] # list of levelgraphs
    orderdict={i+1:orders[i] for i in range(n)}
  
    for e in range(1,bound+1):
        # look at which stgraphs in Mbar_g,n with e edges are bipartite
        for gr in new_list_strata(g,n,e):
            check=SageGraph(gr).is_bipartite(True)
            if check[0]:
                # check[1] contains dictionary {vertices: 0 or 1}
                vert1=[v for v in check[1] if check[1][v]==0]
                vert2=[v for v in check[1] if check[1][v]==1]
                result+=bics_on_bipgr(gr,vert1,vert2,orderdict)
                result+=bics_on_bipgr(gr,vert2,vert1,orderdict)
    return result
    
def bics_on_bipgr(gr,vertup,vertdown,orderdict):
    # takes stable graph and partition of range(len(gr.genera)) into vertup, vertdown
    # creates list of possible pole orders at edges
    result=[]

    # removed from admcycles so reinserted here for legacy purposes:
    def dicunion(*dicts):
        return dict(itertools.chain.from_iterable(dct.items() for dct in dicts))
    
    numvert=len(gr.genera(copy=False))
    halfedges=gr.halfedges()
    halfedgeinvers={e0:e1 for (e0,e1) in gr.edges(copy=False)}
    halfedgeinvers.update({e1:e0 for (e0,e1) in gr.edges(copy=False)})
    
    levels=[0 for i in range(numvert)]
    for i in vertdown:
        levels[i]=-1
    
    helist=[[l for l in ll if l in halfedges] for ll in gr.legs(copy=False)] #list of half-edges of each vertex
    degs=[] # list (with len numvert) of orders that need to be provided by pole orders of half-edges (not legs)
    for v in range(numvert):
        degs.append(2*gr.genera(v)-2-sum([orderdict[l] for l in gr.list_markings(v)]))
        # if degs<0:
        #     return []
    
    weightparts=[]
    for v in vertup:
        vweightpart=[]
        for part in OrderedPartitions(degs[v]+len(helist[v]),len(helist[v])):
            # dictionary of weights from edges connected to vertex v
            vdic={helist[v][i]:part[i]-1 for i in range(len(helist[v]))}
            vdic.update({halfedgeinvers[helist[v][i]]:-part[i]-1 for i in range(len(helist[v]))})
            #print vdic
            vweightpart.append(vdic)
        weightparts+=[vweightpart]
        #print weightparts
    
    for parts in itertools.product(*weightparts):
        #print parts
        poleorders=dicunion(orderdict,*parts)
        CandGraph=admcycles.diffstrata.levelgraph.LevelGraph(gr.genera(copy=False),gr.legs(copy=False),gr.edges(copy=False),poleorders,levels,quiet=True)
        if CandGraph.is_legal(True) and CandGraph.checkadmissible(True):
            result.append(CandGraph)
    return result
    
def new_list_strata(g,n,r):
    return [lis[0] for lis in admcycles.admcycles.degeneration_graph(int(g),n,r)[0][r] ]

############################################################
############################################################

############################################################
############################################################
#### New BIC generation. This is currently used.
############################################################
############################################################

@cached_function
def bic_alt_noiso(sig):
    """
    Construct all non-horizontal divisors in the stratum sig.

    More precisely, each BIC is LevelGraph with two levels numbered 0, -1
    and marked points 1,...,n where the i-th point corresponds to the element
    i-1 of the signature.

    Note that this is the method called by GeneralisedStratum.gen_bic.
    
    Args:
        sig (Signature): Signature of the stratum.
    
    Returns:
        list: list of 2-level non-horizontal LevelGraphs.
 
    EXAMPLES ::

        sage: from admcycles.diffstrata import *
        sage: assert comp_list(bic_alt(Signature((1,1))),\
        [LevelGraph([1, 0],[[3, 4], [1, 2, 5, 6]],[(3, 5), (4, 6)],{1: 1, 2: 1, 3: 0, 4: 0, 5: -2, 6: -2},[0, -1],True),\
        LevelGraph([1, 1, 0],[[4], [3], [1, 2, 5, 6]],[(3, 5), (4, 6)],{1: 1, 2: 1, 3: 0, 4: 0, 5: -2, 6: -2},[0, 0, -1],True),\
        LevelGraph([1, 1],[[3], [1, 2, 4]],[(3, 4)],{1: 1, 2: 1, 3: 0, 4: -2},[0, -1],True),\
        LevelGraph([2, 0],[[3], [1, 2, 4]],[(3, 4)],{1: 1, 2: 1, 3: 2, 4: -4},[0, -1],True)])

        sage: assert comp_list(bic_alt(Signature((2,))),\
        [LevelGraph([1, 1],[[2], [1, 3]],[(2, 3)],{1: 2, 2: 0, 3: -2},[0, -1],True),\
        LevelGraph([1, 0],[[2, 3], [1, 4, 5]],[(2, 4), (3, 5)],{1: 2, 2: 0, 3: 0, 4: -2, 5: -2},[0, -1],True)])

        sage: assert comp_list(bic_alt(Signature((4,))),\
        [LevelGraph([1, 1, 0],[[2, 4], [3], [1, 5, 6, 7]],[(2, 5), (3, 6), (4, 7)],{1: 4, 2: 0, 3: 0, 4: 0, 5: -2, 6: -2, 7: -2},[0, 0, -1],True),\
        LevelGraph([1, 1, 1],[[3], [2], [1, 4, 5]],[(2, 4), (3, 5)],{1: 4, 2: 0, 3: 0, 4: -2, 5: -2},[0, 0, -1],True),\
        LevelGraph([2, 0],[[2, 3], [1, 4, 5]],[(2, 4), (3, 5)],{1: 4, 2: 2, 3: 0, 4: -4, 5: -2},[0, -1],True),\
        LevelGraph([2, 0],[[2, 3], [1, 4, 5]],[(2, 4), (3, 5)],{1: 4, 2: 1, 3: 1, 4: -3, 5: -3},[0, -1],True),\
        LevelGraph([1, 0],[[2, 3, 4], [1, 5, 6, 7]],[(2, 5), (3, 6), (4, 7)],{1: 4, 2: 0, 3: 0, 4: 0, 5: -2, 6: -2, 7: -2},[0, -1],True),\
        LevelGraph([1, 2],[[2], [1, 3]],[(2, 3)],{1: 4, 2: 0, 3: -2},[0, -1],True),\
        LevelGraph([2, 1],[[2], [1, 3]],[(2, 3)],{1: 4, 2: 2, 3: -4},[0, -1],True),\
        LevelGraph([1, 1],[[2, 3], [1, 4, 5]],[(2, 4), (3, 5)],{1: 4, 2: 0, 3: 0, 4: -2, 5: -2},[0, -1],True)])

        sage: len(bic_alt(Signature((1,1,1,1)))) # long time (2 seconds)
        102

        sage: len(bic_alt(Signature((2,2,0,-2))))
        61

        sage: len(bic_alt((2,2,0,-2)))
        61
    """
    if isinstance(sig, tuple):
        sig = Signature(sig)
    zeros = [i+1 for i,a in enumerate(sig.sig) if a > 0] # for keeping track of the numbered half-edges, we remember the index
    z = sig.z
    poles = [i+1 for i,a in enumerate(sig.sig) if a < 0]
    p = sig.p
    marked_points = [i+1 for i,a in enumerate(sig.sig) if a == 0]
    mp = len(marked_points)
    g = sig.g
    orders = {i+1 : ord for i,ord in enumerate(sig.sig)}

    n = sig.n

    # As every g=0 top component needs at least one pole, the bottom max depends on this:
    if p > 0:
        g_bot_max = g
        g_top_min = 0
        pole_ind = [0,1]
    else:
        g_bot_max = g - 1
        g_top_min = 1
        pole_ind = [0] # poles don't need to be distributed...
    
    found = []

    for bot_comp_len in range(1,z+mp+1):
        # every component on bottom level needs at least one zero or two marked points 
        # (in case it's genus 0 and has only one edge with a double pole going up...)
        # Therefore, we split the zeros into top and bottom and distribute these:
        for parts in itertools.chain(multiset_partitions(zeros,2), iter([[zeros,[]]])):
            for i in [0,1]:
                if mp > 0 or len(parts[i]) >= bot_comp_len:
                    bottom_zeros = parts[i]
                    top_zeros = parts[1-i]
                else:
                    continue
                # if there are no marked points, every component needs a zero
                # otherwise we are more flexible (this could be improved, but is good enoug for now)
                if mp == 0:
                    bot_zero_gen = _distribute_fully(bottom_zeros,bot_comp_len)
                else:
                    bot_zero_gen = _distribute_points(bottom_zeros,bot_comp_len)
                for distr_bot_zeros in bot_zero_gen:
                    # partition genus into top, bottom and graph:
                    for total_g_bot in range(g_bot_max+1):
                        for total_g_top in range(g_top_min, g - total_g_bot + 1):
                            total_g_graph = g - total_g_bot - total_g_top
                            # partition bottom genus into components
                            for distr_bot_g in _distribute_part_ordered(total_g_bot,bot_comp_len):
                                # first test:
                                # orders on each component must add up to 2g-2, from now on only poles get
                                # added and we need at least one edge going up (adding at least a pole of order 2)
                                # So if sum(zeros) < 2g, we're screwed
                                if not all(sum(orders[bz] for bz in distr_bot_zeros[c]) 
                                            >= 2*distr_bot_g[c] for c in range(bot_comp_len)):
                                    continue
                                # start distributing poles, first between top and bottom:
                                for pole_parts in itertools.chain(multiset_partitions(poles,2), iter([[poles,[]]])):
                                    for ip in pole_ind: # no poles => nothing to distribute
                                        bottom_poles = pole_parts[ip]
                                        top_poles = pole_parts[1-ip]
                                        # poles on top necessary for g=0 components
                                        if total_g_top == 0 and len(top_poles) == 0:
                                            continue
                                        # poles are optional (i.e. not every vertex needs a pole)
                                        for distr_bot_poles in _distribute_points(bottom_poles,bot_comp_len):
                                            # we save the "space" left to distribute among poles from half-edges:
                                            spaces_bot = [(-sum(orders[tz] for tz in distr_bot_zeros[c]) 
                                                        - sum(orders[tp] for tp in distr_bot_poles[c]) 
                                                                + 2*distr_bot_g[c] - 2) for c in range(bot_comp_len)]
                                            # retest: each space must be at least -2
                                            if not all(s <= -2 for s in spaces_bot):
                                                continue
                                            # iterate over top components
                                            for top_comp_len in range(1,total_g_top+len(top_poles)+1):
                                                # now we know all vertices and the genus distribution, we know the number of edges:
                                                num_of_edges = top_comp_len + bot_comp_len + total_g_graph - 1
                                                # "global" condition on bottom: 
                                                # for each edge there will be at least another pole of order 2
                                                if (sum(sum(orders[bz] for bz in distr_bot_zeros[c]) 
                                                        + sum(orders[bp] for bp in distr_bot_poles[c]) 
                                                            for c in range(bot_comp_len))
                                                        - 2*num_of_edges < 2*total_g_bot - 2*bot_comp_len):
                                                    continue
                                                # distribute genus and poles
                                                for distr_top_g in _distribute_part_ordered(total_g_top,top_comp_len):
                                                    for distr_top_poles in _distribute_points(top_poles,top_comp_len):
                                                        # test: if orders add up to more than 2g-2 this won't work
                                                        # (effectively this should only concern g=0 components here...)
                                                        if not all(sum(orders[tp] for tp in distr_top_poles[c]) 
                                                                            <= 2*distr_top_g[c] - 2
                                                                                    for c in range(top_comp_len)):
                                                            continue
                                                        # distribute remaining zeros optionally
                                                        for distr_top_zeros in _distribute_points(top_zeros,top_comp_len):
                                                            # again, we record the spaces:
                                                            spaces_top = [-sum(orders[tp] for tp in distr_top_poles[c]) 
                                                                          - sum(orders[tz] for tz in distr_top_zeros[c])
                                                                                 + 2*distr_top_g[c] - 2
                                                                                        for c in range(top_comp_len)] # yapf: disable
                                                            # retest:
                                                            if not all(s >= 0 for s in spaces_top):
                                                                continue
                                                            # We distribute the edges together with their prongs/poleorders
                                                            # before we check for connectednes
                                                            # We start on bottom level, because there each half-edge
                                                            # comes with a mandatory pole:
                                                            for half_edges_bot, orders_he in _place_legs_on_bot(spaces_bot, num_of_edges, n+num_of_edges):
                                                                # note for the numbering of half-edges:
                                                                # * the HE on bot are numbered n+num_of_edges+1,...,n+2*num_of_edges
                                                                # * the HE on top are numbered the same for now, i.e. edges are (l,l) ,
                                                                #   (and will be renumbered n+1,...,n+num_of_edges in a moment)
                                                                for half_edges_top in _place_legs_on_top(spaces_top,orders_he):
                                                                    # check if graph is connected!
                                                                    # We create the associated sage graph
                                                                    # this doesn't have multiple edges, but we only
                                                                    # care about connectedness
                                                                    # For this, we build a dictionary {leg: comp bottom}
                                                                    edge_dict = {}
                                                                    for j, c in enumerate(half_edges_bot):
                                                                        for l in c:
                                                                            # note that the vertices of G will be numbered
                                                                            # 0,...,top_comp_len+bot_comp_len-1
                                                                            # so the bot components are numbered by their index
                                                                            # offset by top_comp_len
                                                                            edge_dict[l] = j + top_comp_len
                                                                            # add in the orders for top edges (note the offset)
                                                                            orders_he[l-num_of_edges] = -2 - orders_he[l]
                                                                    G = Graph([(j,edge_dict[l]) for j,c in enumerate(half_edges_top)
                                                                                                        for l in c], multiedges=False)
                                                                    if not G.is_connected():
                                                                        continue
                                                                    genera = distr_top_g+distr_bot_g
                                                                    # Distribute order 0 marked points
                                                                    for distr_mp in _distribute_points(marked_points,len(genera)):
                                                                        # combine nested lists of legs:
                                                                        legs = ([distr_top_zeros[c] + distr_top_poles[c]
                                                                                    + distr_mp[c]
                                                                                    # renumber top HE
                                                                                    + [l-num_of_edges for l in half_edges_top[c]]
                                                                                    for c in range(top_comp_len)] # top component
                                                                                + [distr_bot_zeros[c] + distr_bot_poles[c]
                                                                                    + distr_mp[c+top_comp_len] # offset
                                                                                    + half_edges_bot[c]
                                                                                    for c in range(bot_comp_len)] # bot component
                                                                            ) # yapf: disable
                                                                        # check stability:
                                                                        if any(len(ls) < 3 for c,ls in enumerate(legs) 
                                                                                                if genera[c] == 0):
                                                                            continue
                                                                        lg_data = (genera, legs, 
                                                                            [(l,l+num_of_edges) for l in range(n+1,n+num_of_edges+1)],
                                                                            _merge_dicts(orders,orders_he), # orders as dict
                                                                            [0]*top_comp_len + [-1]*bot_comp_len, # levels
                                                                            # True # quiet
                                                                        )
                                                                        LG = admcycles.diffstrata.levelgraph.LevelGraph(*lg_data)
                                                                        if LG.checkadmissible(quiet=True):
                                                                            if LG.is_legal(quiet=True):
                                                                                found.append(LG)
                                                                        else:
                                                                            # this should not happen!
                                                                            print("Not admissible(!): ", LG)
    found = list(set(found)) # remove duplicates
    return found

def bic_alt(sig):
    """
    The BICs of the stratum sig up to isomorphism of LevelGraphs.

    This should not be used directly, use a GeneralisedStratum or Stratum
    instead to obtain EmbeddedLevelGraphs and the correct isomorphism classes.
    
    Args:
        sig (tuple): signature tuple
    
    Returns:
        list: list of LevelGraphs.
    """
    return isom_rep(bic_alt_noiso(sig)) # remove duplicates up to iso

def _merge_dicts(x,y):
    z = x.copy()
    z.update(y)
    return z

def _place_legs_on_bot(space,num_of_points,start):
    ## iterator distributing n legs with pole orders on (bottom) components according to space (each pole order is at least -2)
    ## here space is a list of 2g-2-stuff we already placed on each bottom component
    ## return a pair (pointlist,orderdict) where
    ## * pointlist is a nested list of points (numbered start+1,...,n)
    ## * orderdict is a dictionary leg number : order
    legal_splits = []
    distr = [] # list to hold the current distribution
    def split(n):
        ## distribute n points onto space and add to distr
        # note that space and distr are accessed from back to front...
        if n==0:
            # done
            # correct signs and reverse order
            legal_splits.append([[-a for a in c] for c in reversed(distr)])
            return
        else:
            if not space: # check if empty
                return
            current = space.pop()
            remaining_comp = len(space)
            # there is a sign issue here: partitions are of positive integers, our pole orders are negative
            # each leg has pole order at least 2, so we only list these partitions
            # moreover, we may place at most n-remaining_comp points on this component
            possibilities = sage_part(-current,min_part=2,max_length=n-remaining_comp).list()
            if possibilities: # check if non-empty
                for possibility in possibilities:
                    distr.append(possibility)
                    # recursion
                    split(n-len(possibility))
                    # undo damage
                    distr.pop()
            space.append(current)
    # generate splits:
    split(num_of_points)
    # we now convert the generated lists (of pole orders) into the format: nested list of numbered legs
    # Note: 
    # * the legs are numbered starting from start+1 to start+num_of_points+1
    # * the orders are saved in the list of dictionaries edge_orders_bot
    for dist in legal_splits:
        order_dic = {} 
        p = start + 1
        for c in range(len(dist)):
            for a in range(len(dist[c])):
                order_dic[p] = dist[c][a]
                dist[c][a] = p
                p += 1
        yield (dist, order_dic)

def _place_legs_on_top(space,orders_bot):
    ## iterator distributing n legs with zero orders (determined by their friends on the bottom component)
    ## onto the top components according to space
    ## here space is a list of 2g_comp-2-stuff we already placed on each top component
    ## return a pointlist (numbered according to keys of orders_bot for now...)
    legal_splits = []
    distr = [[] for _ in space] # list to hold current distribution
    # we sort the points by order, as the ones with the highest order are the hardest to place
    # note that this is actually reverse sorted, as the top order is -2-bottom order, but this 
    # is good, as we want to manipulate the list from the end
    ordered_keys = [k for k,v in reversed(sorted(orders_bot.items(), key=lambda o: o[1]))]
    def splits(keys):
        # distribute the points (keys) onto spaces
        if not keys:
            # done if we hit all components and all spaces are 0
            if all(distr) and all(s == 0 for s in space):
                legal_splits.append([[a for a in c] for c in distr])
            return
        else:
            # check if there are enough points left
            remaining_comp = len([hit for hit in distr if not hit]) # components that don't have a point yet
            if remaining_comp > len(keys):
                return
            current = keys.pop()
            current_order = -2 - orders_bot[current]
            # try to place current on all components
            for i in range(len(space)):
                if space[i] >= current_order:
                    space[i] -= current_order
                    distr[i].append(current)
                    splits(keys) # recursion
                    # undo changes:
                    space[i] += current_order
                    distr[i].pop()
            keys.append(current)
    # generate splits:
    splits(ordered_keys)
    return legal_splits

def _distribute_fully(points,n):
    ## iterator distributing list of points onto n components, where each component gets at least one point
    ## return a nested list of points
    # generate partitions into n subsets of permuted_points:
    for part in multiset_partitions(points, n):
        # we need to consider all permutations (multiset_partitions sorts!)
        for permuted_points in permutations(part):
            yield list(permuted_points) # permutations give tuples...

def _b_ary_gen(x,b,n):
    ## generator for reverse b-ary integers x of length n
    for _ in itertools.repeat(None,n):
        r = x % b
        x = (x-r)//b
        yield r

def _distribute_points(points,n):
    ## iterator distributing list of points onto n components (some might not receive any)
    ## return a nested list of points
    l = len(points)
    # n^l possibilities:
    for i in range(n**l):
        point_list = [[] for j in range(n)]
        # n-ary representation of i tells us where the points should go
        for pos,d in enumerate(_b_ary_gen(i,n,l)):
            point_list[d].append(points[pos])
        yield point_list

def _distribute_part_ordered(g,n):
    ## iterator of partitions (g_1,...,g_k) of g of length k <= n distributed onto n points
    ## return a list of length n (that sums to g)
    if n < g:
        maxi = n
    else:
        maxi = None
    for part_dict in partitions(g,m=maxi):
        # partitions are dictionaries {g_i : multiplicity}
        part = []
        for k in part_dict.keys():
            part += [k]*part_dict[k]
        # fill up with zeros:
        part += (n-len(part))*[0]
        yield part
        # we do not have to permute if everything else is permuted....
        # for perm_part in set(permutations(part)):
        #     yield perm_part

def isom_rep(L):
    """
    Return a list of representatives of isomorphism classes of L.

    TODO: optimise!
    """
    dist_list = []
    for g in L:
        if all(not g.is_isomorphic(h) for h in dist_list):
            dist_list.append(g)
    return dist_list

def comp_list(L,H):
    r"""
    Compare two lists of LevelGraphs (up to isomorphism).

    Returns a tuple: (list L without H, list H without L)
    """
    return ([g for g in L if not any(g.is_isomorphic(h) for h in H)],
            [g for g in H if not any(g.is_isomorphic(h) for h in L)])

def test_bic_algs(sig_list=None):
    """
    Compare output of bics and bic_alt.

    EXAMPLES ::

        sage: from admcycles.diffstrata import *
        sage: test_bic_algs()  # long time (45 seconds)  # skip, not really needed + long # doctest: +SKIP
        (1, 1): ([], [])
        (1, 1, 0, 0, -2): ([], [])
        (2, 0, -2): ([], [])
        (1, 0, 0, 1): ([], [])
        (1, -2, 2, 1): ([], [])
        (2, 2): ([], [])

        sage: test_bic_algs([(0,0),(2,1,1)])  # long time (50 seconds)  # doctest: +SKIP
        (0, 0): ([], [])
        (2, 1, 1): ([], [])

        sage: test_bic_algs([(1,0,-1),(2,),(4,),(1,-1)])
        WARNING! This is not the normal BIC generation algorithm!
        Only use if you know what you're doing!
        (1, 0, -1): ([], [])
        WARNING! This is not the normal BIC generation algorithm!
        Only use if you know what you're doing!
        (2,): ([], [])
        WARNING! This is not the normal BIC generation algorithm!
        Only use if you know what you're doing!
        (4,): ([], [])
        WARNING! This is not the normal BIC generation algorithm!
        Only use if you know what you're doing!
        (1, -1): ([], [])
    """
    if sig_list == None:
        sig_list = [(1,1),(1,1,0,0,-2),(2,0,-2),(1,0,0,1),(1,-2,2,1),(2,2)]
    for sig in sig_list:
        Sig = Signature(sig)
        print("%r: %r" % (Sig.sig, comp_list(bics(Sig.g,Sig.sig),bic_alt(Sig)))) 