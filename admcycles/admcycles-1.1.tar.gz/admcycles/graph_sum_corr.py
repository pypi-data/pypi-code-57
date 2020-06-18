r"""
Double ramification cycle
"""

from __future__ import absolute_import, print_function
from six.moves import range
from admcycles.admcycles import Tautv_to_tautclass, Tautvb_to_tautclass, Tautvecttobasis, tautgens, psiclass, tautclass, prodtautclass, list_strata, fundclass, lambdaclass
from admcycles.stable_graph import StableGraph
import admcycles.DR as DR

import itertools
from copy import deepcopy, copy

from sage.combinat.subset import Subsets
from sage.combinat.integer_vector import IntegerVectors
from sage.arith.all import factorial
from sage.functions.other import floor, ceil
from sage.misc.misc_c import prod
from sage.rings.all import PolynomialRing, QQ, ZZ
from sage.modules.free_module_element import vector
from sage.rings.polynomial.polynomial_ring import polygen
from sage.rings.polynomial.multi_polynomial_element import MPolynomial
from sage.rings.power_series_ring import PowerSeriesRing

# S.<x0,x1>=PowerSeriesRing(QQ,'x0,x1',default_prec=14)
def graph_sum(g,n,decgraphs=None,globalfact=None, vertterm=None,legterm=None,edgeterm=None,maxdeg=None,deg=None,termsout=False):
    r"""Returns the (possibly mixed-degree) tautological class obtained by summing over graphs gamma, 
    inserting vertex-, leg- and edgeterms.

    INPUT:

    - ``decgraphs`` -- list or generator; entries of decgraphs are pairs (gamma,dec) of a StableGraph
      gamma and some additional combinatorial structure dec associated to gamma

    - ``globalfact`` -- function; globalfact(gamma,dec) gets handed the parameters gamma,dec as arguments and gives out a number that is multiplied with the corresponding term in the graph sum; default is 1
      
    - ``vertterm`` -- function; vertterm(gv,nv,maxdeg **kwargs) takes arguments local genus gv and number of legs nv
      and maxdeg gets handed the parameters gamma,dec,v as optional keyworded arguments and gives out a
      tautological class on Mbar_{gv,nv}; the class is assumed to be of degree at most maxdeg,
      if deg is given, the class is exactly of degree deg
      
    - ``legterm`` -- function; legterm(gv,nv,i,maxdeg, **kwargs) similar to vertterm, except input is 
      gv,nv,i,maxdeg where i is number of marking on Mbar_{gv,nv} associated to leg
      gamma, dec given as keyworded arguments
      
    - ``edgeterm`` -- function; edgeterm(maxdeg,**kwargs) takes keyworded arguments gamma,dec,e,maxdeg
      it gives a generating series s in x0,x1 such that the insertion at edge
      e=(h0,h1) is given by s(psi_h0, psi_h1)

    - ``termsout`` -- parameter; if termsout=False, return sum of all terms
      if termsout = 'coarse', return tuple of terms, one for each pair (gamma,dec)
      if termsout = 'fine', return tuple of terms, one for each pair (gamma,dec) and each distribution 
      of cohomological degrees to vertices and half-edges
    """
    if maxdeg == None:
        if deg == None:
            maxdeg = 3*g-3+n
        else:
            maxdeg = deg    
    if decgraphs == None:
        decgraphs = [(gr,None) for ednum in range(3*g-3+n+1) for gr in list_strata(g,n,ednum)]
    if globalfact == None:
        globalfact = lambda a,b : 1
    if vertterm == None:
        def vertterm(gv,nv,maxdeg, **kwargs):
            return fundclass(gv,nv)
    if legterm == None:
        def legterm(gv,nv,i,maxdeg, **kwargs):
            return fundclass(gv,nv)    
    if edgeterm == None:
        def edgeterm(maxdeg,**kwargs):
            S=PowerSeriesRing(QQ,'x0,x1',default_prec=maxdeg+1)
            return S.one()
    
                        
    termlist = []
    
    for (gamma,dec) in decgraphs:
        restdeg = maxdeg - len(gamma.edges)
        if restdeg < 0:
            continue
        
        gammadectermlist=[]
        
        numvert = gamma.numvert()
        gnvect=[(gamma.genera[i],len(gamma.legs[i])) for i in range(numvert)]
        dimvect=[3*g-3+n for (g,n) in gnvect]
        halfedges = gamma.halfedges()
        markings = gamma.list_markings()
        vertdic = {l:v for v in range(numvert) for l in gamma.legs[v]}
        indexdic = {l:j+1 for v in range(numvert) for j,l in enumerate(gamma.legs[v])}
        # ex_dimvect=[dimvect[vertdic[l]] for l in halfedges]  # list of dimensions of spaces adjacent to half-edges
        
        # Pre-compute all vertex-, leg- and edgeterms
        vterms = {v:vertterm(gnvect[v][0],gnvect[v][1],restdeg, gamma=gamma,dec=dec,v=v) for v in range(numvert)}
        lterms = {i:legterm(gnvect[vertdic[i]][0],gnvect[vertdic[i]][1],indexdic[i], restdeg, gamma=gamma,dec=dec) for i in markings}
        eterms = {e: edgeterm(restdeg,gamma=gamma,dec=dec,e=e) for e in gamma.edges}
        varlist = {(h0,h1): eterms[h0,h1].parent().gens() for h0,h1 in gamma.edges}
        eterms = {e:eterms[e].coefficients() for e in eterms}
        varx = {h0 : varlist[h0,h1][0] for h0,h1 in gamma.edges}
        varx.update({h1 : varlist[h0,h1][1] for h0,h1 in gamma.edges})
        
        if deg == None:
            rdlis = range(restdeg+1) # terms of all degrees up to restdeg must be computed
        else:
            rdlis = [deg - len(gamma.edges)]    
        for rdeg in rdlis:    
            # distribute the remaining degree rdeg to vertices
            for degdist in IntegerVectors(rdeg,numvert,outer=dimvect):
                # now for each vertex, split degree to vertex- and leg/half-edge terms
                vertchoices = [IntegerVectors(degdist[v],len(gamma.legs[v])+1) for v in range(numvert)]
                for choice in itertools.product(*vertchoices):
                    vdims = []
                    ldims = {}
                    for v in range(numvert):
                        vdims.append(choice[v][0])
                        ldims.update({l:choice[v][i+1] for i,l in enumerate(gamma.legs[v])})
                        
                    effvterms = [vterms[v].degree_part(vdims[v]) for v in vterms]
                    efflterms = {i: lterms[i].degree_part(ldims[i]) for i in lterms}
                    for i in efflterms:
                        effvterms[vertdic[i]]*=efflterms[i] # multiply contributions from legs to vertexterms
                    for h0,h1 in gamma.edges:
                        # TODO: optimization potential here by multiplying kppolys directly
                        effvterms[vertdic[h0]]*= eterms[(h0,h1)].get(varx[h0]**ldims[h0] * varx[h1]**ldims[h1],0)* (psiclass(indexdic[h0],*gnvect[vertdic[h0]]))**ldims[h0]
                        effvterms[vertdic[h1]]*= (psiclass(indexdic[h1],*gnvect[vertdic[h1]]))**ldims[h1]
                    for t in effvterms:
                        t.simplify()
                    #print(gamma)
                    #print(rdeg)
                    #print(degdist)
                    #print(choice)
                    #print(effvterms)
                    #print(eterms)
                    #print(indexdic)
                    #print('\n')
                    tempres=gamma.boundary_pushforward(effvterms)
                    tempres.simplify()
                    if(len(tempres.terms))>0:
                        tempres*=globalfact(gamma,dec)
                        gammadectermlist.append(tempres)
                    #print(termlist)
        if termsout=='coarse':
            termlist.append(sum(gammadectermlist))
        else:
            termlist+=gammadectermlist    
    if termsout:
        return termlist
    else:
        return sum(termlist)                
                        
############
#
# Useful functions and examples
#
############

###
# Example 1 : Conjectural graph sum for DR_g(1,-1)
###

# Generating functions for graphs

def DR11_tree_test(gr):
    i=gr.vertex(1)
    if not i == gr.vertex(2):
        return False
    else:
        return True
    
def DR11_trees(g):
    return [gr for n in range(1,g+1) for e in range(n) for gr in list_strata(0,2+n,e) if DR11_tree_test(gr)]

def DR11_graphs(g):
    result=[]
    for gr in DR11_trees(g):
        n=len(gr.list_markings())-2
        maxleg=max([max(j+[0]) for j in gr.legs])
        grlist=[]
        for gdist in IntegerVectors(g,n,min_part=1):
            genera=copy(gr.genera)+list(gdist)
            legs=copy(gr.legs)+[[j] for j in range(maxleg+1,maxleg+n+1)]
            edges=copy(gr.edges)+[(j-maxleg+2,j) for j in range(maxleg+1,maxleg+n+1)]
            grlist.append(StableGraph(genera,legs,edges))
        result+=[(gam,None) for gam in grlist]
    removedups(result,lambda a,b : a[0].is_isomorphic(b[0]))
    return result

def removedups(li, comp=None,inplace=True):
    if inplace:
        l=li
    else:
        l=deepcopy(li) # could be done more efficiently
    if comp == None:
        comp = lambda a,b : a == b
    n = len(l)
    currn = len(l)
    for i in range(n,-1,-1):
        if any(comp(l[i],l[j]) for j in range(i+1,currn)):
            l.pop(i)
            currn-=1
    return l      

# Global factor = 1/|Aut(Gamma)|

def divbyaut(gamma,dec):
    return QQ(1)/gamma.automorphism_number()

# Vertex- and edgeterms for DR11
def DR11_vterm(gv, nv, maxdeg,**kwargs):
    if gv==0:
        gamma = kwargs['gamma']
        v = kwargs['v']
        if not 1 in gamma.legs[v]:
            # we are in genus zero vertex not equal to base
            return -nv * fundclass(gv,nv)
        else:
            # we are at the base vertex
            return fundclass(gv,nv)
    else:
        return sum([(-1)**j * lambdaclass(j,gv,nv) for j in range(maxdeg+1)])
def DR11_eterm(maxdeg,**kwargs): # smarter: edterm(maxdeg=None,gamma=None,dec=None,e=None, *args, *kwds)
    S=PowerSeriesRing(QQ,'x0,x1',default_prec=maxdeg+1)
    x0,x1 = S.gens()
    return 1/(1-x0-x1+x0*x1)

# Final conjectural graph sum expressing DR_g(1,-1)
def DR11_sum(g,deg=None,**kwds):
    if deg == None:
        deg = g
    return graph_sum(g,2,decgraphs=DR11_graphs(g),globalfact=divbyaut,vertterm=DR11_vterm,edgeterm=DR11_eterm,deg=deg,**kwds)                  
