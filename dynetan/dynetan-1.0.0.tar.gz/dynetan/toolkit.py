#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: melomcr
"""

# For trajectory analysis
import MDAnalysis as mda

def diagnostic():
    return mda.lib.distances.USED_OPENMP

## Progress Bar with time estimate
## Based on https://github.com/alexanderkuk/log-progress
def log_progress(sequence, every=None, size=None, name='Items', userProgress=None):
    
    from ipywidgets import IntProgress, HTML, HBox, Label
    from IPython.display import display
    from numpy import mean as npmean
    from collections import deque
    from math import floor
    from datetime import datetime
    from string import Template
    
    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = floor(float(size)*0.005)     # every 0.5%, minimum is 1
    else:
        assert every is not None, 'sequence is iterator, set every'
    
    # For elapsed time
    initTime = datetime.now()
    totTime = "?"
    labTempl = Template(" (~ $min total time (min) ; $ell minutes elapsed)")
    
    # If provided, we use the objects already created.
    # If not provided, we create from scratch.
    if userProgress is None or userProgress == []:
        
        progress = IntProgress(min=0, max=1, value=1)

        label = HTML()
        labelTime = Label("")

        box = HBox(children=[label, progress, labelTime])
        
        if userProgress == []:
            userProgress.append(box)
        display(box)
    else:
        box = userProgress[0]
    
    if is_iterator:
        #progress = IntProgress(min=0, max=1, value=1)
        box.children[1].min = 0
        box.children[1].max = 1
        box.children[1].value = 1
        box.children[1].bar_style = 'info'
    else:
        #progress = IntProgress(min=0, max=size, value=0)
        box.children[1].min = 0
        box.children[1].max = size
        box.children[1].value = 0

        # For remaining time estimation
        deltas = deque()
        lastTime = None
        meandelta = 0
    
    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    box.children[0].value = '{name}: {index} / ?'.format(
                        name=name,
                        index=index
                    )
                else:
                    box.children[1].value = index
                    box.children[0].value = u'{name}: {index} / {size}'.format(
                        name=name,
                        index=index,
                        size=size
                    )
                
                    # Estimates remaining time with average delta per iteration
                    # Uses (at most) the last 30 iterations
                    if len(deltas) == 101:
                        deltas.popleft()
                    
                    if lastTime:
                        deltas.append( (datetime.now() - lastTime).total_seconds() )
                        meandelta = npmean(deltas)/60.0    # From seconds to minute
                        totTime = round(meandelta*size/float(every), 3)  # Mean iteration for all iterations
                    else:
                        totTime = "?"       # First iteration has no time
                    
                    lastTime = datetime.now()
                
                # All ellapsed time in minutes
                elapsed = round( (datetime.now() - initTime).total_seconds()/60.0, 3)

                box.children[2].value = labTempl.safe_substitute({"min":totTime,
                                                       "ell":elapsed})
                
            yield record
    except:
        box.children[1].bar_style = 'danger'
        raise
    else:
        box.children[1].bar_style = 'success'
        box.children[1].value = index
        box.children[0].value = "{name}: {index}".format(
            name=name,
            index=str(index or '?')
        )


def getNGLSelFromNode(nodeIndx, atomsel, atom=True):
    """
    Creates an atom selection (whole residue or single atom) for NGLView.
    We also need an atom-selection object.
    """
    node = atomsel.atoms[nodeIndx]
    if atom:
        return " and ".join([str(node.resid), node.resname, "." + node.name])
    else:
        return " and ".join([str(node.resid), node.resname])

def getNodeFromSel(selection, atomsel, atomToNode):
    """
    Gets the node index from an atom selection. 
    We also need an atom-selection object.
    """
    
    nodes = atomToNode[ atomsel.select_atoms(selection).ix_array ]
    
    # There may be atoms not assigned to nodes, in case a whole nucleotide was
    #   kept but only one of its nodes had contacts.
    return nodes[ nodes >= 0 ]

def getSelFromNode(i, atomsel, atom=False):
    """
    Gets the selection string from a node index: resname and resid and segid [and name]
    We also need an atom-selection object.
    """
    i = int(i)
    if i < 0:
        raise
    resName = atomsel.atoms[i].resname
    resID = str(atomsel.atoms[i].resid)
    segID = atomsel.atoms[i].segid
    atmName = atomsel.atoms[i].name
    
    if atom:
        return "resname " + resName + " and resid " + resID + " and segid " + segID + " and name " + atmName
    else:
        return "resname " + resName + " and resid " + resID + " and segid " + segID


def getPath(src, trg, nodesAtmSel, preds, win=0):
    """
    Returns a NumPy array with the list of nodes that connect src and trg.
    """

    import numpy as np

    src = int(src)
    trg = int(trg)

    if src == trg:
        return []

    if src not in preds[win].keys():
        return []

    if trg not in preds[win][src].keys():
        return []

    if getSelFromNode(src, nodesAtmSel) == getSelFromNode(trg, nodesAtmSel):
        return []

    path = [trg]

    while path[-1] != src:
        path.append(preds[win][src][path[-1]])

    return np.asarray(path)

# %%cython 

# cdef int getLinIndexC(int src, int trgt, int n):
    
#     # based on https://stackoverflow.com/questions/27086195/linear-index-upper-triangular-matrix
#     k = (n*(n-1)/2) - (n-src)*((n-src)-1)/2 + trgt - src - 1.0
#     return <int>k

def getLinIndexC( src, trgt, n):
    
    #based on https://stackoverflow.com/questions/27086195/linear-index-upper-triangular-matrix
    k = (n*(n-1)/2) - (n-src)*((n-src)-1)/2 + trgt - src - 1.0
    return int(k)

def getCartDist(src,trgt, numNodes, nodeDists, distype=0):
    '''
    Retreives the mean cartesian distance between nodes src and trgt.
    If provided, the "type" argument causes the function to return the 
    mean distance (type 0: default), SEM (type 1), minimum distance (type 2), 
    or maximum distance (type 3).
    '''
    
    if src == trgt:
        return 0
    elif trgt < src:
        # We need to access the list with smaller index on row, larger on the column
        src, trgt = trgt, src
    
    k = getLinIndexC(src, trgt, numNodes)
    
    return nodeDists[distype, k]
    
