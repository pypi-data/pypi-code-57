#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: melomcr
"""

import numpy as np
import cython

# For generalized correlations
from numba import jit

##################################################
##################################################

## Auxiliary functions for calculation of correlation coefficients.

@cython.cfunc
@cython.returns(cython.void)
@cython.locals(numNodes=cython.int, numDims=cython.int, traj="np.ndarray[np.float_t, ndim=3]")
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def standVarsC(traj, numNodes, numDims):
    
    # Standardize variables
    for atm in range(numNodes):
        for dim in range(numDims):
            # Noromalize each dimension.
            traj[atm, dim, :] = (traj[atm, dim, :] - traj[atm, dim, :].mean())/ traj[atm, dim, :].std()

            # Offset all data by minimum normalilzed value.
            traj[atm, dim, :] -= traj[atm, dim, :].min()

@cython.cfunc
@cython.returns(cython.void)
@cython.locals(traj="np.ndarray[np.float_t, ndim=3]",
               beg=cython.int, 
               end=cython.int, 
               numNodes=cython.int, 
               numDims=cython.int)
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def prepMIc(universe, traj, beg, end, numNodes, numDims):
    '''
    Transfer tranjectory to NumPy array in *new format*: variable-dimension-step (atom-x/y/z-frame).
    Standardize each dimension of each atom.
    '''
    
    # Copy trajectory
    for frameIndx, ts in enumerate(universe.trajectory[beg:end]):
    
        for atmIndx in range(numNodes):
            for dim in range(numDims):
                traj[atmIndx, dim, frameIndx] = ts.positions[atmIndx,dim]
    
    standVarsC(traj, numNodes, numDims)
 
#
# This takes ~4.52 ms ± 43.1 µs for 250 frames
#
@jit('f8(f8[:,:,:], i4, i8, i4, f8[:], f8[:])', nopython=True)
def calcMIRnumba2var(traj, numFrames, numDims, kNeighb, psi, phi):
    """
    Calculate the mutual information estimate based on Kraskov et. al. (2004) Physical Review E.
    This function uses the rectangle method, and is hardcoded for 2 variables.
    """
    dxy = 0
    
    diffX = np.zeros(numFrames, dtype=np.float64)
    diffY = np.zeros(numFrames, dtype=np.float64)
    tmpDiff = np.zeros(numFrames, dtype=np.float64)
    sortIndx = np.zeros(numFrames, dtype=np.int64)
    
    for step in range(numFrames):
        diffX.fill(0)
        diffY.fill(0)
        tmpDiff.fill(0)
        sortIndx.fill(0)

        for d in range(numDims):
            
            tmpDiff = np.abs( traj[0,d,:] - traj[0,d,step] )
            
            diffX = np.where( diffX > tmpDiff, diffX, tmpDiff )
            
            tmpDiff = np.abs( traj[1,d,:] - traj[1,d,step] )
            
            diffY = np.where( diffY > tmpDiff, diffY, tmpDiff )
        
        # Create an array with indices of sorted distance arrays
        sortIndx = np.argsort( np.where(diffX > diffY, diffX, diffY))
        
        epsx = 0
        epsy = 0
        
        # Get the maximum diatance in each dimention, for each variable,
        #  among k nearest neighbors.
        # We add one to the count to include the k-th neighbour, as the first index
        #  in the list it the frame itself.
        for kindx in range(1, kNeighb+1):
            
            for d in range(numDims):
                # For variable "i"
                dist = np.abs( traj[0,d,step] - traj[0, d, sortIndx[kindx]] )
                
                if epsx < dist :
                    epsx = dist

                # For variable "j"
                dist = np.abs( traj[1,d,step] - traj[1, d, sortIndx[kindx]] )
                
                if epsy < dist :
                    epsy = dist
        
        # Count the number of frames in which the point is within "eps-" distance from
        #   the position in frame "step". Subtract one so not to count the frame itself.
        nx = len(np.nonzero( diffX <= epsx )[0]) -1
        ny = len(np.nonzero( diffY <= epsy )[0]) -1
        
        dxy += psi[nx] + psi[ny];
    
    dxy /= numFrames
    
    # Mutual Information R
    return psi[numFrames] + phi[kNeighb] - dxy

def calcCorProc(traj, winLen, psi, phi, numDims, kNeighb, inQueue, outQueue):
    '''
    Calculates the generalized correlation in a Process for parallel execution.
    '''
    
    # While we still hape elements to process, get a new pair of nodes. 
    while not inQueue.empty():
        
        atmList = inQueue.get()
        
        # Calls the Numba-compiled function.
        corr = calcMIRnumba2var(traj[atmList, :, :], winLen, numDims, kNeighb, psi, phi)
        
        # Assures that the Mutual Information estimate is not lower than zero.
        corr = max(0, corr)
        
        # Determine generalized correlation coeff from the Mutual Information
        corr = np.sqrt(1-np.exp(-corr*(2.0/3)));
            
        #return (atmList, corr)
        outQueue.put( (atmList, corr) )




