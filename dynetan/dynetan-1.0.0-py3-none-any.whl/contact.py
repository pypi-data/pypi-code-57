#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: melomcr
"""

import numpy as np

from MDAnalysis.analysis            import distances            as mdadist 

from numba import jit

import cython

@jit('i8(i4, i8, i4)', nopython=True)
def getLinIndexNumba(src, trgt, n):
    
    # based on https://stackoverflow.com/questions/27086195/linear-index-upper-triangular-matrix
    k = (n*(n-1)/2) - (n-src)*((n-src)-1)/2 + trgt - src - 1.0
    return k

@jit('void(i8, i8, f8[:], i8[:], i8[:], i8[:], f8[:])', nopython=True)
def atmToNodeDist(numNodes, nAtoms, tmpDists, atomToNode, nodeGroupIndicesNP, nodeGroupIndicesNPAux, nodeDists):
    
    maxVal = np.finfo(np.float64).max
    
    # Initialize with maximum possible value of a float64
    tmpDistsAtms = np.full( nAtoms, maxVal, dtype=np.float64 )
    
    # We iterate untill we have only one node left
    for i in range(numNodes - 1):
        
        # Initializes the array for this node.
        tmpDistsAtms.fill(maxVal)
        
        # index of first atom in node "i"
        nodeAtmIndx = nodeGroupIndicesNPAux[i]
        # index of first atom in node "i+1"
        nodeAtmIndxNext = nodeGroupIndicesNPAux[i+1]
        
        # Gets first atom in next node
        nextIfirst = nodeGroupIndicesNP[nodeAtmIndxNext]
        
        # Per node:  Iterate over atoms from node i
        for nodeI_k in nodeGroupIndicesNP[nodeAtmIndx:nodeAtmIndxNext]:
            
            # Go from 2D indices to 1D (n*(n-1)/2) indices:
            j1 = getLinIndexNumba(nodeI_k, nextIfirst, nAtoms)
            jend = j1 + (nAtoms - nextIfirst)
            
            # Gets the shortest distance between atoms in different nodes
            tmpDistsAtms[nextIfirst:] = np.where(tmpDists[j1: jend] < tmpDistsAtms[nextIfirst:], 
                     tmpDists[j1: jend], 
                     tmpDistsAtms[nextIfirst:])
            
        for pairNode in range(i+1, numNodes):
            np.where(atomToNode == pairNode)
            
            # Access the shortests distances between atoms from "pairNode" and the current node "i"
            minDist = np.min(tmpDistsAtms[ np.where(atomToNode == pairNode) ])
            
            # Go from 2D node indices to 1D (numNodes*(numNodes-1)/2) indices:
            ijLI = getLinIndexNumba(i, pairNode, numNodes)
            
            nodeDists[ijLI] = minDist
    
# High memory usage (nAtoms*(nAtoms-1)/2), calcs all atom distances at once.
# We use self_distance_array and iterate over the trajectory.
# https://www.mdanalysis.org/mdanalysis/documentation_pages/analysis/distances.html
def calcDistances(selection, numNodes, nAtoms, atomToNode, 
                       nodeGroupIndicesNP, nodeGroupIndicesNPAux, nodeDists, backend="serial" ):
    
    tmpDists = np.zeros( int(nAtoms*(nAtoms-1)/2), dtype=np.float64 )
    
    # serial vs OpenMP
    mdadist.self_distance_array(selection.positions, result=tmpDists, backend=backend)
    
    # Translate atoms distances in minimum node distance.
    atmToNodeDist(numNodes, nAtoms, tmpDists, atomToNode, nodeGroupIndicesNP, nodeGroupIndicesNPAux, nodeDists)

@cython.cfunc
@cython.returns(cython.int)
@cython.locals(src=cython.int, trgt=cython.int, n=cython.int)
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def getLinIndexC(src, trgt, n):
    
    # based on https://stackoverflow.com/questions/27086195/linear-index-upper-triangular-matrix
    k = (n*(n-1)/2) - (n-src)*((n-src)-1)/2 + trgt - src - 1.0
    return int(k)
    
@cython.cfunc
@cython.returns(cython.void)
@cython.locals(numNodes=cython.int, nAtoms=cython.int, cutoffDist=cython.float,
               tmpDists="np.ndarray[np.float_t, ndim=1]",
               tmpDistsAtms="np.ndarray[np.float_t, ndim=1]",
               contactMat="np.ndarray[np.int_t, ndim=2]",
               atomToNode="np.ndarray[np.int_t, ndim=1]",
               nodeGroupIndicesNP="np.ndarray[np.int_t, ndim=1]",
               nodeGroupIndicesNPAux="np.ndarray[np.int_t, ndim=1]")
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def calcContactC(numNodes, nAtoms, cutoffDist, 
                 tmpDists, 
                 tmpDistsAtms, 
                 contactMat,
                 atomToNode,
                 nodeGroupIndicesNP,
                 nodeGroupIndicesNPAux):
    
    #cdef int nextIfirst, j1, jend, i, nodeI_k, nodeAtmIndx, nodeAtmIndxNext
    nextIfirst = cython.declare(cython.int)
    
    # Cython types are evaluated as for cdef declarations
    j1: cython.int
    jend: cython.int
    i: cython.int
    nodeI_k: cython.int
    nodeAtmIndx: cython.int
    nodeAtmIndxNext: cython.int
    
    
    # We iterate untill we have only one node left
    for i in range(numNodes - 1):
        
        # Initializes the array for this node.
        tmpDistsAtms.fill(cutoffDist*2)
        
        # index of first atom in node "i"
        nodeAtmIndx = nodeGroupIndicesNPAux[i]
        # index of first atom in node "i+1"
        nodeAtmIndxNext = nodeGroupIndicesNPAux[i+1]
        
        # Gets first atom in next node
        nextIfirst = nodeGroupIndicesNP[nodeAtmIndxNext]
        
        # Per node:  Iterate over atoms from node i
        for nodeI_k in nodeGroupIndicesNP[nodeAtmIndx:nodeAtmIndxNext]:
            
            # Go from 2D indices to 1D (n*(n-1)/2) indices:
            j1 = getLinIndexC(nodeI_k, nextIfirst, nAtoms)
            jend = j1 + (nAtoms - nextIfirst)
            
            # Gets the shortest distance between atoms in different nodes
            tmpDistsAtms[nextIfirst:] = np.where(tmpDists[j1: jend] < tmpDistsAtms[nextIfirst:], 
                     tmpDists[j1: jend], 
                     tmpDistsAtms[nextIfirst:])

        # Gets a list of nodes for which at least one atom was closer than the
        #   cutoff diatance in this frame.
#         contactingNodes = np.unique( atomToNode[ np.where(tmpDistsAtms < cutoffDist)[0] ] )
        
        # Adds one to the contact to indicate that this frame had a contact.
        contactMat[i, np.unique( atomToNode[ np.where(tmpDistsAtms < cutoffDist)[0] ] )] += 1

# High memory usage (nAtoms*(nAtoms-1)/2), calcs all atom distances at once.
@cython.cfunc
@cython.returns(cython.void)
@cython.locals(numNodes=cython.int, nAtoms=cython.int, cutoffDist=cython.float,
               tmpDists="np.ndarray[np.float_t, ndim=1]",
               tmpDistsAtms="np.ndarray[np.float_t, ndim=1]",
               contactMat="np.ndarray[np.int_t, ndim=2]",
               atomToNode="np.ndarray[np.int_t, ndim=1]",
               nodeGroupIndicesNP="np.ndarray[np.int_t, ndim=1]",
               nodeGroupIndicesNPAux="np.ndarray[np.int_t, ndim=1]")
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def getContactsC(selection, numNodes, 
                        nAtoms, 
                        cutoffDist, 
                        tmpDists, 
                        tmpDistsAtms, 
                        contactMat,
                        atomToNode,
                        nodeGroupIndicesNP,
                        nodeGroupIndicesNPAux):
    
    # serial vs OpenMP
    mdadist.self_distance_array(selection.positions, result=tmpDists, backend='openmp')
    
    calcContactC(numNodes, nAtoms, cutoffDist, tmpDists, tmpDistsAtms, 
                 contactMat, atomToNode, nodeGroupIndicesNP, nodeGroupIndicesNPAux)


