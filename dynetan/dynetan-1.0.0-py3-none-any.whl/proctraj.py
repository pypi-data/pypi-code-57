#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: melomcr
"""

from . import toolkit as tk
from . import gencor as gc
from . import contact as ct
from . import network as nw
from . import datastorage as ds

import numpy as np

import cython

import MDAnalysis as mda

import multiprocessing as mp

import networkx as nx

import community

from networkx                       import eigenvector_centrality_numpy as nxeigencentrality

from MDAnalysis.lib.NeighborSearch  import AtomNeighborSearch   as mdaANS
from MDAnalysis.coordinates.memory  import MemoryReader         as mdaMemRead
from MDAnalysis.analysis.base       import AnalysisFromFunction as mdaAFF
from MDAnalysis.analysis            import distances            as mdadist 
from MDAnalysis.analysis.distances  import between              as mdaB

from colorama import Fore
from operator       import itemgetter
from collections    import OrderedDict, defaultdict

import copy,os

##################################################
##################################################

class DNAproc:
    
    def __init__(self):
                
        self.dnaData = None 
        
        self.contactPersistence = 0
        self.cutoffDist = 0
        self.numSampledFrames = 0
        self.numWinds = 0
        
        # Number of neighbours for Generalized Correlation estimate
        self.kNeighb = 7
        
        self.h2oName            = None
        self.segIDs             = None
        self.customResNodes     = None
        self.usrNodeGroups      = None
        
        self.allResNamesSet     = None
        self.selResNamesSet     = None
        self.notSelResNamesSet  = None
        self.notSelSegidSet     = None
        
        self.workU          = None
        
        self.selRes         = None
        
        self.nodesAtmSel    = None
        self.atomToNode     = None
        self.resNodeGroups  = None
        
        self.numNodes       = None
        
        self.nodeGroupIndicesNP     = None
        self.nodeGroupIndicesNPAux  = None
        self.contactMatAll          = None
        self.corrMatAll             = None
        
        self.nodeDists              = None
        self.nxGraphs               = None
        self.distsAll               = None
        self.preds                  = None
        self.maxDist                = None
        self.maxDirectDist          = None
        self.btws                   = None
        self.nodesComm              = None
        
        self.interNodePairs         = None
        self.contactNodesInter      = None
        
    def setNumWinds(self, numWinds):
        self.numWinds = numWinds
    
    def setNumSampledFrames(self, numSampledFrames):
        self.numSampledFrames = numSampledFrames
    
    def setCutoffDist(self, cutoffDist):
        self.cutoffDist = cutoffDist
        
    def setContactPersistence(self, contactPersistence):
        self.contactPersistence = contactPersistence
        
    def seth2oName(self, h2oName):
        self.h2oName = h2oName
        
    def setSegIDs(self, segIDs):
        self.segIDs = segIDs
    
    def setCustomResNodes(self, customResNodes):
        self.customResNodes = customResNodes
    
    def setUsrNodeGroups(self, usrNodeGroups):
        self.usrNodeGroups = usrNodeGroups
    
    def getU(self):
        return self.workU 
    
    def saveData(self, fileNameRoot="dnaData"):
        
        self.dnaData = ds.DNAdata()
        
        self.dnaData.nodesIxArray   = self.nodesAtmSel.ix_array
        self.dnaData.numNodes       = self.numNodes
        self.dnaData.atomToNode     = self.atomToNode
        self.dnaData.contactMat     = self.contactMat
        
        self.dnaData.corrMatAll     = self.corrMatAll
        self.dnaData.nodeDists      = self.nodeDists
        
        self.dnaData.distsAll       = self.distsAll
        self.dnaData.preds          = self.preds
        self.dnaData.maxDist        = self.maxDist
        self.dnaData.maxDirectDist  = self.maxDirectDist
        self.dnaData.btws           = self.btws
        self.dnaData.nodesComm      = self.nodesComm
        self.dnaData.nxGraphs       = self.nxGraphs
        
        self.dnaData.interNodePairs    = self.interNodePairs
        self.dnaData.contactNodesInter = self.contactNodesInter
        
        self.dnaData.saveToFile(fileNameRoot)
        
    def saveReducedTraj(self, fileNameRoot="dnaData", stride=1):
        
        dcdVizFile = fileNameRoot + "_reducedTraj.dcd"
        
        with mda.Writer(dcdVizFile, self.workU.atoms.n_atoms) as W:
            for ts in tk.log_progress(self.workU.trajectory[::stride], 
                                      every=1, 
                                      size=int(len(self.workU.trajectory[::stride])),
                                name="Frames"):
                W.write(self.workU.atoms)
        
        pdbVizFile = fileNameRoot + "_reducedTraj.pdb"

        with mda.Writer(pdbVizFile, multiframe=False, bonds="conect", n_atoms=self.workU.atoms.n_atoms) as PDB:
            PDB.write(self.workU.atoms)
        
    def loadSystem(self, psfFile, dcdFiles):        
        self.workU = mda.Universe(psfFile,dcdFiles)

    def checkSystem(self):
        
        if not self.workU:
            print("ERROR! This function can only be called after loading a system. Check your universe!")
            return -1
        
        allResNamesSet = set()
        selResNamesSet = set()
        notSelResNamesSet = set()
        notSelSegidSet = set()
        
        print(Fore.BLUE + "Residue verification:\n" + Fore.RESET)

        # Loop over segments and checks residue names
        for segment in self.workU.segments:
            segid = segment.segid
            
            resNames = set([res.resname for res in segment.residues ])
            
            if segid in self.segIDs:
                print("---> SegID ",Fore.GREEN + segid, Fore.RESET +":", len(resNames),"unique residue types:")
                print(resNames)
                print()
                selResNamesSet.update(resNames)
            else:
                notSelSegidSet.add(segid)
                
            allResNamesSet.update(resNames)
            
        print("---> {0} total selected residue types:".format(len(selResNamesSet)))
        print(selResNamesSet) ; print()

        notSelResNamesSet = allResNamesSet - selResNamesSet

        print(("---> {0} " + Fore.RED + "not-selected" + Fore.RESET + \
            " residue types in other segments:").format(len(notSelResNamesSet)))
        print(notSelResNamesSet)  ; print()

        print("---> {0} total residue types:".format(len(allResNamesSet)))
        print(allResNamesSet)  ; print()

        self.selRes = self.workU.select_atoms("segid " + " ".join(self.segIDs))
        print("--->",len(self.selRes.residues),"total residues were selected for network analysis.") ; print()

        print(Fore.BLUE + "Segments verification:\n" + Fore.RESET)

        print(("---> {0} " + Fore.GREEN + "selected" + Fore.RESET + " segments:").format(len(self.segIDs)))
        print(self.segIDs)  ; print()

        print(("---> {0} " + Fore.RED + "not-selected" + Fore.RESET + " segments:").format(len(notSelSegidSet)))
        print(sorted(notSelSegidSet, key=str.lower))  ; print()
        
        self.allResNamesSet = allResNamesSet
        self.selResNamesSet = selResNamesSet
        self.notSelResNamesSet = notSelResNamesSet
        self.notSelSegidSet = notSelSegidSet
    
    def selectSystem(self, withSolvent=False):
        
        if withSolvent:
            # With Solvent
            checkSet = self.workU.select_atoms("(not (name H*, [123]H*)) and segid " + " ".join(self.notSelSegidSet) )
        else:
            # Without Solvent
            checkSet = self.workU.select_atoms("segid " + " ".join(self.notSelSegidSet) + \
                " and not resname " + " ".join(self.h2oName) + " and not (name H*, [123]H*)")
        
        numAutoFrames = self.numSampledFrames*self.numWinds

        stride = int(np.floor(len(self.workU.trajectory)/numAutoFrames))

        print("Checking {0} frames (striding {1})...".format(numAutoFrames, stride))

        searchSelRes = self.selRes.select_atoms("not name H*, [123]H*")

        # Keeps a set with all residues that were close to the interaction region in ALL
        #  sampled timesteps

        resIndexDict = defaultdict(int)
        for ts in tk.log_progress(self.workU.trajectory[:numAutoFrames*stride:stride], name="Frames",size=numAutoFrames):
            
            # Creates neighbor search object. We pass the atoms we want to check,
            #   and then search using the main selection.
            # This is expensive because it creates a KD-tree for every frame, 
            #   but the search for Neighbors is VERY fast.
            searchNeigh = mdaANS(checkSet)
            
            resNeigh = searchNeigh.search(searchSelRes, self.cutoffDist)
            
            for indx in resNeigh.residues.ix:
                resIndexDict[indx] += 1
            

        resIndxList = [ k for k,v in resIndexDict.items() if v > int(numAutoFrames*self.contactPersistence) ]

        checkSetMin = self.workU.residues[ np.asarray(resIndxList, dtype=int) ]

        print("{} solvent residues will be added to the system.".format(len(checkSetMin.resnames)))
        
        selStr = "segid " + " ".join(self.segIDs) 
        initialSel = self.workU.select_atoms(selStr)
        initialSel = initialSel.union(checkSetMin.atoms)
        initialSel = initialSel.select_atoms("not (name H*, [123]H*)")
        #initialSel
        
        print("The initial universe had {} atoms.".format( len(self.workU.atoms) ))
        
        # Merging a selection from the universe returns a new (and smaller) universe
        self.workU = mda.core.universe.Merge(initialSel)
        
        print("The final universe has {} atoms.".format( len(self.workU.atoms) ))
        
        # We now load the new universe to memory, with coordinates from the selected residues.
        
        print("Loading universe to memory...")

        self.workU.load_new(mdaAFF(lambda ag: ag.positions.copy(),
                                    initialSel).run().results, 
                    format=mdaMemRead)
        self.workU
        
    def prepareNetwork(self):
        
        from itertools import groupby
        from itertools import chain
        from operator import itemgetter

        # Dictionary associating residue type and node-atom to set of 
        #   atom names associated with that node.
        self.resNodeGroups = {}

        self.resNodeGroups.update(self.usrNodeGroups)

        for res in self.workU.select_atoms("not protein").residues:
            # Verifies if there are unkown residues
            if len(res.atoms) > 1 and res.resname not in self.customResNodes.keys():
                print((Fore.RED + "Unknown residue type" + Fore.RESET + " {0}, from segment {1}").format(
                    res.resname, res.segid))
            
            # For residues that are not proteic, and that have one atom (IONS)
            # Creates the "node group" and the atom name for the node.
            if len(res.atoms) == 1:
                self.resNodeGroups[res.resname] = {}
                self.resNodeGroups[res.resname][res.atoms.names[0]] = set(res.atoms.names)

                if res.resname not in self.customResNodes.keys():
                    self.customResNodes[res.resname] = [res.atoms[0].name]
            else:
                # If the residue is not an ION, check for Hydrogen atoms.
                
                # Adds hydrogen atomss to a groups of atoms in every residue.
                for atm in res.atoms:
                    # Assume it is a hydrogen and bind it to the group of the atom
                    # it is connected to.
                    if atm.name not in set.union(*self.resNodeGroups[res.resname].values()):
                        boundTo = atm.bonded_atoms[0].name
                        
                        for key, val in self.resNodeGroups[res.resname].items():
                            if boundTo in val:
                                self.resNodeGroups[res.resname][key].add(atm.name)
            
            
            kMissing = set(self.resNodeGroups[res.resname].keys()).difference(set(res.atoms.names))
            if kMissing:
                warningStr = (Fore.RED + "Warning!" + Fore.RESET + " residue {0} \
        segid {1} resid {2} does not contain all node atoms. Missing atoms: {3}").format(
                    res.resname, res.segid, res.resid, ' '.join(kMissing))
                print(warningStr)
                
        resNodeAtoms = self.customResNodes.copy()

        # Creates node groups for protein atoms.
        for res in self.workU.select_atoms("protein").residues:
            if res.resname not in resNodeAtoms.keys():
                resNodeAtoms[res.resname] = ["CA"]
                # Creates the group of atoms in the group represented by this node.
                self.resNodeGroups[res.resname] = {}
                self.resNodeGroups[res.resname]["CA"] = set(res.atoms.names)
            else:
                self.resNodeGroups[res.resname]["CA"].update(set(res.atoms.names))

        ## Create atom selection for atoms that represent nodes

        # Builds list of selection statements
        selStr = ["(protein and name CA)"]
        selStr += [ "(resname {0} and name {1})".format(k," ".join(v)) for k,v in self.customResNodes.items() ]
        # Combines all statements into one selection string
        selStr = " or ".join(selStr)

        self.nodesAtmSel = self.workU.select_atoms(selStr)

        self.numNodes = self.nodesAtmSel.n_atoms
        
        print("Preparing nodes...")
        
        #self.atomToNode = np.full(shape=initialSel.n_atoms, fill_value=-1, dtype=int)
        self.atomToNode = np.full(shape=len(self.workU.atoms), fill_value=-1, dtype=int)
        
        # Creates an array relating atoms to nodes.
        for indx, node in enumerate(tk.log_progress(self.nodesAtmSel.atoms, name="Nodes")):
            
            # Loops over all atoms in the residue related to the node
            for atm in node.residue.atoms:
                
                # Checks if the atom name is listed for the node
                if atm.name in self.resNodeGroups[node.resname][node.name]:
                    self.atomToNode[atm.ix] = indx
                
        # Verification: checks if there are any "-1" left. If so, that atom was not assigned a node.
        loneAtms = np.where( self.atomToNode < 0 )[0]
        if len(loneAtms) > 0:
            print( loneAtms )
        
        # Determine groups of atoms that define each node.
        # We need all this because the topology in the PSF may 
        #   list atoms in an order that separates atoms from the same node.
        #   Even though atoms in the same *residue* are contiguous,
        #   atoms in our arbitrary node groups need not be contiguous.
        # Since amino acids have just one node, they will have just one range
        #   but nucleotides and other residues may be different.

        nodeGroupRanges = {}

        nodeGroupIndices = []

        for x in np.unique(self.atomToNode):
            data = np.where(self.atomToNode == x)[0]
            
            ranges =[]
            for k,g in groupby(enumerate(data),lambda x:x[0]-x[1]):
                # Creates an iterable from the group object.
                group = (map(itemgetter(1),g))
                # Creates a list using the itterable
                group = list(map(int,group))
                # Appends to the list of ranges the first and last items in each range.
                ranges.append((group[0],group[-1]))
            
            nodeGroupRanges[x] = ranges
            
            # Transforms the ranges into lists
            tmp = [ [x for x in range(rang[0],rang[1]+1)] for rang in nodeGroupRanges[x]]
            # Combine lists into one list
            nodeGroupIndices.append( list(chain.from_iterable(tmp)) )
            
        nodeGroupIndices = np.asarray(nodeGroupIndices, dtype=object)

        self.nodeGroupIndicesNP = np.asarray(list(chain.from_iterable(nodeGroupIndices)), dtype=int)
        
        self.nodeGroupIndicesNPAux = np.zeros(self.numNodes, dtype=int)

        for indx, atmGrp in enumerate(nodeGroupIndices[1:], start=1):
            self.nodeGroupIndicesNPAux[indx] = len(nodeGroupIndices[indx -1]) + self.nodeGroupIndicesNPAux[indx -1]
        
        print("Nodes are ready for network analysis.")
        
        return None
        
    def alignTraj(self, inMemory=True):
        from MDAnalysis.analysis import align as mdaAlign
        
        # Set the first frame as reference for alignment
        self.workU.trajectory[0]

        alignment = mdaAlign.AlignTraj(self.workU, self.workU, 
                                       select="segid " + " ".join(self.segIDs) + " and not (name H*, [123]H*)",
                                       verbose=True, 
                                       in_memory=True, 
                                       weights="mass" )
        alignment.run()
        

    def _contactTraj(self, contactMat, beg = 0, end = -1, stride = 1):
        
        # Prealocates initial contact matrix
    #     cdef np.ndarray contactMat = np.zeros([self.numNodes, self.numNodes], dtype=int)
        
        # Creates atom selection for distance calculation
        selectionAtms = self.workU.select_atoms("all")
        
        nAtoms = selectionAtms.n_atoms
        
        # Array to receive all-to-all distances, at every step
        tmpDists = np.zeros( int(nAtoms*(nAtoms-1)/2), dtype=float )
        
        # Array to get minimum distances per node
        tmpDistsAtms = np.full( nAtoms, self.cutoffDist*2, dtype=float )
        
        if end < 0:
            end = self.workU.trajectory.n_frames
        
        for ts in self.workU.trajectory[beg:end:stride]:
            
            # Calculates distances to determine contact matrix
            ct.getContactsC(selectionAtms, self.numNodes, nAtoms, self.cutoffDist, tmpDists, tmpDistsAtms, 
                        contactMat, self.atomToNode, 
                        self.nodeGroupIndicesNP, self.nodeGroupIndicesNPAux)

    def findContacts(self, stride=1):
        numFrames = self.workU.trajectory.n_frames

        # Allocate contact matrix(ces)
        self.contactMatAll = np.zeros([self.numWinds, self.numNodes, self.numNodes], dtype=np.int)
        
        # Set number of frames per window.
        winLen = int(np.floor(self.workU.trajectory.n_frames/self.numWinds))

        # Set number of frames that defines a contact
        contactCutoff = (winLen/stride)*self.contactPersistence

        for winIndx in tk.log_progress(range(self.numWinds),every=1, size=self.numWinds, name="Window"):
            beg = winIndx*winLen
            end = (winIndx+1)*winLen
            
            ## RUNs calculation
            self._contactTraj( self.contactMatAll[winIndx, :, :], beg, end, stride)

            self.contactMatAll[winIndx, :, :] = np.where(self.contactMatAll[winIndx, :, :] > contactCutoff, 1, 0)

            for i in range(self.numNodes):
                for j in range(i+1, self.numNodes):
                    self.contactMatAll[winIndx, j,i] = self.contactMatAll[winIndx, i,j]
        
        # Update unified contact matrix for all windows
        self._genContactMatrix()
        
        self.checkContactMat()
    
    def _genContactMatrix(self):
        # Allocate a unified contact matrix for all windows.
        self.contactMat = np.zeros([self.numNodes, self.numNodes], dtype=np.int)
        
        # Join all data for all windows on the same unified contact matrix.
        for winIndx in range(self.numWinds):
            self.contactMat = np.add(self.contactMat, self.contactMatAll[winIndx, :, :])
        
        # Creates binary mask with pairs of nodes in contact
        self.contactMat = np.where(self.contactMat > 0, 1, 0)
    
    def checkContactMat(self, verbose=True):
        
        # Sanity Checks that the contact matrix is symmetric
        if not np.allclose(self.contactMat, self.contactMat.T, atol=0.1):
            print("ERROR: the contact matrix is not symmetric.")
        
        # Checks if there is any node that does not make contacts to ANY other node.
        noContactNodes = np.asarray(np.where( np.sum(self.contactMat, axis=1) == 0 )[0])
        if verbose: 
            print("We found {0} nodes with no contacts.".format(len(noContactNodes)))
        
        # Counts total number of contacts
        if verbose: 
            pairs = np.asarray(np.where(np.triu(self.contactMat) > 0)).T
            totalPairs = int(self.contactMat.shape[0]*(self.contactMat.shape[0]-1)/2)
            print("We found {0:n} contacting pairs out of {1:n} total pairs of nodes.".format(len(pairs), totalPairs))
            print("(That's {0}%, by the way)".format( round((len(pairs)/(totalPairs))*100,1) ))
        
    
    def filterContacts(self, notSameRes=True, notConsecutiveRes=False, removeIsolatedNodes=True):
        
        recycleBar = []
        
        for winIndx in tk.log_progress(range(self.numWinds), every=1, size=self.numWinds, name="Window"):
            
            self._filterContactsWindow(self.contactMatAll[winIndx, :, :], 
                                       nodeProgress=recycleBar,
                                       notSameRes=notSameRes, 
                                       notConsecutiveRes=notConsecutiveRes)
    
            #for winIndx in range(self.numWinds):
            print("Window:", winIndx)
            pairs = np.asarray(np.where(np.triu(self.contactMatAll[winIndx, :, :]) > 0)).T
            totalPairs = int(self.contactMat.shape[0]*(self.contactMat.shape[0]-1)/2)
            print("We found {0:n} contacting pairs out of {1:n} total pairs of nodes.".format(len(pairs), totalPairs))
            print("(That's {0}%, by the way)".format( round((len(pairs)/(totalPairs))*100,3) ))
        
        if removeIsolatedNodes:
            
            print("\nRemoving isolated nodes...\n")
            
            # Update unified contact matrix for all windows
            self._genContactMatrix()
            
            # Gets indices for nodes with no contacts
            contactNodesArray = ~(np.sum(self.contactMat, axis=1) == 0)
            noContactNodesArray = (np.sum(self.contactMat, axis=1) == 0)
            
            # Atom selection for nodes with contact
            contactNodesSel = self.nodesAtmSel.atoms[ contactNodesArray ]
            noContactNodesSel = self.nodesAtmSel.atoms[ noContactNodesArray ]
            
            # Checks if there is any node that does not make contacts to ANY other node.
            print("We found {0} nodes with no contacts.".format(len(noContactNodesSel)))
            noContactNodesSel.names
            
            # Trims matrices
            self.contactMatAll = self.contactMatAll[:, ~(np.sum(self.contactMat, axis=1) == 0),  :]
            self.contactMatAll = self.contactMatAll[:, :,  ~(np.sum(self.contactMat, axis=0) == 0)]

            self.contactMat = self.contactMat[ ~(np.sum(self.contactMat, axis=1) == 0), :]
            self.contactMat = self.contactMat[:,  ~(np.sum(self.contactMat, axis=0) == 0)]
            
            print("\nIsolated nodes removed. We now have {} nodes in the system\n".format(self.contactMatAll[0].shape[0]) )
            print("Running new contact matrix sanity check...")
            
            self.checkContactMat()
            
            #########################
            # Update Universe and network data
            
            print("\nUpdating Universe to reflect new node selection...")
            
            # selStr = "(segid " + " ".join(segIDs) + ") or "
            selStr = " or ".join(["(segid {0} and resid {1})".format(res.segid, res.resid) for res in contactNodesSel.residues])
            
            allSel = self.workU.select_atoms( selStr )
            
            # Merging a selection from the universe returns a new (and smaller) universe
            self.workU = mda.core.universe.Merge(allSel)
            
            # We now create a new universe with coordinates from the selected residues
            self.workU.load_new(mdaAFF(lambda ag: ag.positions.copy(),
                              allSel).run().results, format=mdaMemRead)
            
            # Regenerate selection of atoms that represent nodes.
            # We use the atom selection structure from the previous universe (that still had nodes with
            #   no contacts) to create selection strings and apply them to the new, smaller universe.
            #   This guarantees we have the correct index for all atoms that represent nodes in the new universe.
            selStr = " or ".join([ "(" + tk.getSelFromNode(indx, contactNodesSel, atom=True) + ")" for indx in range(contactNodesSel.n_atoms)])
            
            self.nodesAtmSel = self.workU.select_atoms(selStr)

            self.numNodes = self.nodesAtmSel.n_atoms
            
            # Creates an array relating all atoms in the system to nodes.
            self.atomToNode = np.full(shape=allSel.n_atoms, fill_value=-1, dtype=int)
            
            print("Updating atom-to-node mapping...")
            
            for indx, node in enumerate(tk.log_progress(self.nodesAtmSel.atoms, name="Node")):
                
                # Loops over all atoms in the residue related to the node
                for atm in node.residue.atoms:
                    
                    # Checks if the atom name is listed for the node
                    if atm.name in self.resNodeGroups[node.resname][node.name]:
                        self.atomToNode[atm.ix] = indx
                    
            # Verification: checks if there are any "-1" left. If so, that atom was not assigned a node.
            loneAtms = np.where( self.atomToNode < 0 )[0]
            if len(loneAtms) > 0:
                print("\nERROR: atom assignment incomplete!")
                print("The following atoms were not assigned a node:")
                print( loneAtms )
            
            #########################
            
    
    def _filterContactsWindow(self, mat, nodeProgress = [], notSameRes=True, notConsecutiveRes=False):
        
        """
        Filter contacts in a contact matrix.
        
        This function receives a contact matrix and guarantees that there will be no
        self-contacts (a results of some contact detection algorithms).
        Optionally, it can also erase contacts between nodes in the same residue (notSameRes) 
        and between nodes in consecutive residues (notConsecutiveRes).
        """
        
        # Cycles over all nodes in the system. There may be several nodes per residue.
        for node in tk.log_progress(self.nodesAtmSel.atoms, name="Node", userProgress=nodeProgress):

            # Get current node index
            nodeIndx = self.atomToNode[node.ix]
            # Get current node residue
            res = node.residue

            # No contact between the same node (main diagonal) 
            mat[nodeIndx, nodeIndx] = 0

            ## No contact between nodes in same residue
            if notSameRes:
                # Get all node atom(s) in current residue
                resSelection = self.workU.select_atoms(
                    "(segid {0} and resid {1})".format(res.segid, res.resid) \
                    + " and name " + " ".join(self.resNodeGroups[res.resname].keys())
                )
                # Get their node indices
                nodeIndxs = self.atomToNode[resSelection.atoms.ix_array]
                # No correlation between nodes in the same residue.
                # Also zeroes self-correlation.
                for i,j in [(i,j) for i in nodeIndxs for j in nodeIndxs]:
                    mat[i,j] = 0

            # Keeps node from making direct contact to previous residue in chain
            if notConsecutiveRes and (res.resindex -1 >= 0):
                prevRes = self.workU.residues[ res.resindex -1 ]

                if prevRes.segid == res.segid:

                    # Select previous residue in the chain
                    prevResSel = self.workU.select_atoms(
                        "(segid {0} and resid {1})".format(res.segid, prevRes.resid)
                    )
                    # Select the node atom(s) from previous residue
                    prevResSel = prevResSel.select_atoms("name " + \
                                                        " ".join(self.resNodeGroups[prevRes.resname].keys()))

                    # Checks that it is not an ION
                    if prevRes.atoms.n_atoms > 1:
                        # Get the actual node(s) indice(s) from the previous residue
                        nodeIndxs = self.atomToNode[prevResSel.atoms.ix_array]

                        # Zeroes all correlation between nodes in consecutive residues
                        for trgtIndx in nodeIndxs:
                            mat[nodeIndx, trgtIndx] = 0
                            mat[trgtIndx, nodeIndx] = 0

            # Keeps node from making direct contact to following residue in chain
            # (same as above)
            if notConsecutiveRes and (res.resindex +1 < self.workU.residues.n_residues):
                folRes = self.workU.residues[ res.resindex +1 ]

                if folRes.segid == res.segid:

                    folResSel = self.workU.select_atoms(
                        "(segid {0} and resid {1})".format(res.segid, folRes.resid)
                    )
                    folResSel = folResSel.select_atoms("name " + \
                                                    " ".join(self.resNodeGroups[folRes.resname].keys()))

                    if folRes.atoms.n_atoms > 1:
                        nodeIndxs = self.atomToNode[folResSel.atoms.ix_array]

                        for trgtIndx in nodeIndxs:
                            mat[nodeIndx, trgtIndx] = 0
                            mat[trgtIndx, nodeIndx] = 0
    
    def calcCor(self, ncores=1):
        
        if ncores <= 0:
            print("ERROR: number of cores must be at least 1.")
            return 1
        
        # For 3D atom position data
        numDims = 3
        
        print("Calculating correlations...\n")
        
        winLen = int(np.floor(self.workU.trajectory.n_frames/self.numWinds))
        print("Using window length of {} simulation steps.".format(winLen))

        # Allocate the space for all correlations matrices (for all windows).
        self.corrMatAll = np.zeros([self.numWinds, self.numNodes, self.numNodes], dtype=np.float64)
        
        # Stores all data in a dimension-by-frame format.
        traj = np.ndarray( [self.numNodes, numDims, winLen], dtype=np.float64 )
        #traj.nbytes
        
        # Pre-calculate psi values for all frames. (allocation and initialization step)
        psi = np.zeros([winLen+1], dtype=np.float)
        psi[1] = -0.57721566490153

        # Pre-calculate psi values for all frames. (actual calculation step)
        for indx in range(winLen):
            if indx > 0:
                psi[indx + 1] = psi[indx] + 1/(indx)

        # Pre calculates "psi[k] - 1/k" 
        phi = np.ndarray( self.kNeighb+1, dtype=np.float64 )
        for tmpindx in range(1, self.kNeighb+1):
            phi[tmpindx] = psi[tmpindx] - 1/tmpindx
        
        recycleBar = []
        
        if ncores == 1:
            
            print("- > Using single-core implementation.")
            
            for winIndx in tk.log_progress(range(self.numWinds),every=1, size=self.numWinds, name="Window"):
                beg = int(winIndx*winLen)
                end = int((winIndx+1)*winLen)
                
                pairList = np.asarray(np.where(np.triu(self.contactMatAll[winIndx, :, :]) > 0)).T
                
                # Resets the trajectory NP array for the current window.
                traj.fill(0)
                
                # Prepares data for fast calculation of the current window.
                gc.prepMIc(self.workU, traj, beg, end, self.numNodes, numDims)
                
                # Iterates over all pairs of nodes that are in contact.
                for atmList in tk.log_progress(pairList, name="Contact Pair", userProgress=recycleBar ):
                    
                    # Calls the Numba-compiled function.
                    corr = gc.calcMIRnumba2var(traj[atmList, :, :], winLen, numDims, self.kNeighb, psi, phi)
                    
                    # Assures that the Mutual Information estimate is not lower than zero.
                    corr = max(0, corr)
                    
                    # Determine generalized correlation coeff from the Mutual Information
                    if corr:
                        corr = np.sqrt(1-np.exp(-2.0/numDims*corr));
                    
                    self.corrMatAll[winIndx, atmList[0], atmList[1]] = corr
                    self.corrMatAll[winIndx, atmList[1], atmList[0]] = corr
                    
        else:
            
            print("- > Using multi-core implementation with {} threads.".format(ncores))
            
            for winIndx in tk.log_progress(range(self.numWinds),every=1, size=self.numWinds, name="Window"):
                beg = int(winIndx*winLen)
                end = int((winIndx+1)*winLen)
                
                #pairList = np.asarray(np.where(np.triu(contactMatAll[winIndx, :, :]) > 0)).T
                pairList = []
                
                # Build pair list avoiding overlapping nodes (which would require reading the same
                #   trajectory).
                for diag in range(1, self.numNodes):
                    contI = 0
                    contJ = diag
                    while contJ < self.numNodes:
                        if self.contactMatAll[winIndx, contI, contJ]:
                            pairList.append( [contI, contJ] )
                        contI += 1
                        contJ += 1
                
                pairList = np.asarray(pairList)
                
                # Resets the trajectory NP array for the current window.
                traj.fill(0)
                
                # Prepares trajectory data for fast calculation of the current window.
                gc.prepMIc(self.workU, traj, beg, end, self.numNodes, numDims)
                
                # Create queues that feed processes with node pairs, and gather results.
                data_queue = mp.Queue()
                results_queue = mp.Queue()
                for atmList in pairList:
                    data_queue.put(atmList)
                
                # Creates processes.
                procs = []
                for _ in range(ncores):
                    proc = mp.Process(target=gc.calcCorProc, 
                               args=(traj, winLen, psi, phi, numDims, self.kNeighb, data_queue, results_queue)) 
                    proc.start()
                    procs.append(proc)
                
                # Gathers all resuls.
                for _ in tk.log_progress(range(len(pairList)), name="Contact Pair", userProgress=recycleBar ):
                    
                    ## Waits until the next result is available, then puts it in the matrix.
                    result = results_queue.get()
                    
                    self.corrMatAll[winIndx, result[0][0], result[0][1]] = result[1]
                    self.corrMatAll[winIndx, result[0][1], result[0][0]] = result[1]
                    
                # Joins processes.
                for proc in procs:
                    proc.join()
                
        # Sanity Check: Checks that the correlation and contact matrix is symmetric
        for win in range(self.numWinds):
            if not np.allclose(self.corrMatAll[win, :, :], self.corrMatAll[win, :, :].T, atol=0.1):
                print("ERROR: Correlation matrix for window {0} is NOT symmetric!!".format(win))
                
    def calcCartesian(self, backend="serial"):
        
        ## numFramesDists is used in the calculation of statistics!
        numFramesDists = self.numSampledFrames*self.numWinds
        # numFramesDists = self.numWinds

        selectionAtms = self.workU.select_atoms("all")
        nAtoms = selectionAtms.n_atoms

        nodeDistsTmp = np.zeros( int(self.numNodes*(self.numNodes-1)/2), dtype=np.float64 )

        self.nodeDists = np.zeros( [4, int(self.numNodes*(self.numNodes-1)/2)], dtype=np.float64 )

        print("Sampling a total of {0} frames from {1} windows ({2} per window)...".format(numFramesDists, 
                                                                                        self.numWinds, 
                                                                                        self.numSampledFrames))

        steps = int(np.floor(len(self.workU.trajectory)/numFramesDists))
        maxFrame = numFramesDists*steps

        # Mean distance
        for indx, ts in enumerate(tk.log_progress(self.workU.trajectory[0:maxFrame:steps], 
                                            size=numFramesDists, name="MEAN: Timesteps")):
            
            ct.calcDistances(selectionAtms, self.numNodes, selectionAtms.n_atoms, self.atomToNode, 
                            self.nodeGroupIndicesNP, self.nodeGroupIndicesNPAux, nodeDistsTmp, backend)
            
            # Mean
            self.nodeDists[0, :] += nodeDistsTmp

        self.nodeDists[0, :] /= numFramesDists

        # Initializes the min and max distances with the means.
        self.nodeDists[2, :] = self.nodeDists[0, :]
        self.nodeDists[3, :] = self.nodeDists[0, :]

        ## Standard Error of the Mean
        for indx, ts in enumerate(tk.log_progress(self.workU.trajectory[0:maxFrame:steps], 
                                            size=numFramesDists, name="SEM/MIN/MAX: Timesteps")):
            # serial vs OpenMP
            mdadist.self_distance_array(self.nodesAtmSel.positions, result=nodeDistsTmp, backend=backend)
            
            # Accumulates the squared difference
            self.nodeDists[1, :] += np.square( self.nodeDists[0, :] - nodeDistsTmp )
            
            # Checks for the minimum
            self.nodeDists[2, :] = np.where( nodeDistsTmp < self.nodeDists[2, :], nodeDistsTmp, self.nodeDists[2, :])
            
            # Checks for the maximum
            self.nodeDists[3, :] = np.where( nodeDistsTmp > self.nodeDists[3, :], nodeDistsTmp, self.nodeDists[3, :])
            
        if numFramesDists > 1:
            # Sample standard deviation: SQRT of sum divided by N-1
            self.nodeDists[1, :] = np.sqrt(self.nodeDists[1, :] / (numFramesDists - 1) )
            # SEM:  STD / sqrt(N)
            self.nodeDists[1, :] = self.nodeDists[1, :]/np.sqrt(numFramesDists)

    def calcGraphInfo(self):
        '''
        For network analysis, we use a log transformation for network distance calculations.
        '''
        self.nxGraphs = []

        for win in range(self.numWinds):
            self.nxGraphs.append( nx.Graph(self.corrMatAll[win, :, :]) )
            
            # We substitute zeros for a non-zero value to avoid "zero division" warnings
            #   from the np.log transformation below.
            self.corrMatAll[ np.where( self.corrMatAll == 0) ] = 10**-11
            
            # Use log transformation for network distance calculations.
            tmpLogTransf = -1.0*np.log(self.corrMatAll[win,:,:])
            
            # Now we guarantee that the previous transformation does not 
            #   create "negative infitite" distances. We set those to zero.
            tmpLogTransf[ np.where( np.isinf(tmpLogTransf) ) ] = 0
            
            # Now we return to zero-correlation we had before.
            self.corrMatAll[ np.where( self.corrMatAll < 10**-10) ] = 0
            
            # Loop over all graph edges and set their distances.
            for pair in self.nxGraphs[win].edges.keys():
                self.nxGraphs[win].edges[(pair[0], pair[1])]["dist"] = tmpLogTransf[pair[0], pair[1]]
            
            # Sets the degree of each node.
            degree_dict = dict(self.nxGraphs[win].degree(self.nxGraphs[win].nodes()))
            nx.set_node_attributes(self.nxGraphs[win], degree_dict, 'degree')
            
    def getDegreeDict(self, window=0):
        return dict( self.nxGraphs[window].degree( self.nxGraphs[window].nodes() ) )
        
    def calcOptPaths(self, ncores=1):
        
        if ncores <= 0:
            print("ERROR: number of cores must be at least 1.")
            return 1
        
        # Sets the network distance array.
        self.distsAll = np.zeros([self.numWinds, self.numNodes, self.numNodes], dtype=np.float)
        
        self.preds = {}
        for i in range(self.numWinds):
            self.preds[i] = 0
        
        if ncores == 1:
            ## Serial Version
            
            for win in tk.log_progress(range(self.numWinds), name="Window"):
                
                ### IMPORTANT!
                # For the FW optimal path determination, we use the "distance" as weight, 
                #  that is, the log-transformation of the correlations. NOT the correlation itself.
                pathsPred, pathsDist = nxFWPD(self.nxGraphs[win], weight='dist')
                
                # Turns dictionary of distances into NumPy 2D array per window
                # Notice the nested list comprehensions.
                self.distsAll[win,:,:] = np.array([[pathsDist[i][j] for i in sorted(pathsDist[j])] for j in sorted(pathsDist)])
                
                # Combines predecessor dictionaries from all windows
                self.preds[win] = copy.deepcopy(pathsPred)
            
        else:
            
            inQueue = mp.Queue()
            outQueue = mp.Queue()

            for win in range(self.numWinds):
                inQueue.put(win)

            # Creates processes.
            procs = []
            for _ in range(ncores):
                procs.append( mp.Process(target=nw.calcOptPathPar, args=(self.nxGraphs, inQueue, outQueue)) )
                procs[-1].start()
                
            for win in tk.log_progress(range(self.numWinds), name="Window"):
                
                ## Waits until the next result is available, then stores it in the object.
                result = outQueue.get()
                
                win = result[0]
                self.distsAll[win,:,:] = np.copy(result[1])
                self.preds[win] = copy.deepcopy(result[2])

            # Joins processes.
            for proc in procs:
                proc.join()
            
        # Get maximum network distance
        self.maxDist = np.max(self.distsAll[self.distsAll != np.inf])

        # Set -1 as distance of nodes with no connecting path (instead of np.inf)
        self.distsAll[ np.where( np.isinf(self.distsAll) ) ] = -1
        
        # Maximum network distance between directly connected nodes (path length == 2)
        # We check connection with the correlation matrix because at times, two nodes may be
        # in contact (physical proximity) but may not have any correlation.
        self.maxDirectDist = max([ self.distsAll[ win, self.corrMatAll[win, :, :] > 0  ].max() for win in range(self.numWinds) ])
        
    def getPath(self, nodeI, nodeJ):
        
        return nx.reconstruct_path(nodeI, nodeJ, self.preds)
        
    def calcBetween(self, ncores=1):
        
        if ncores <= 0:
            print("ERROR: number of cores must be at least 1.")
            return 1
        
        self.btws = {}
        
        if ncores == 1:
            ## Serial Version
            # Single core version
            for win in tk.log_progress(range(self.numWinds), every=1, size=self.numWinds, name="Window"):
                # Calc all betweeness in entire system.
                ### IMPORTANT!
                # For the betweeness, we only care about the number of shortests paths 
                #   passing through a given edge, so no weight are considered.
                self.btws[win] = nxbetweenness(self.nxGraphs[win], weight=None)
                
                # Creates an ordered dict of pairs with betweenness higher than zero.
                self.btws[win] = {k:self.btws[win][k] for k in self.btws[win].keys() if self.btws[win][k] > 0}
                self.btws[win] = OrderedDict(sorted(self.btws[win].items(), key=lambda t: t[1], reverse=True))
        else:
            
            inQueue = mp.Queue()
            outQueue = mp.Queue()

            for win in range(self.numWinds):
                inQueue.put(win)

            # Creates processes.
            procs = []
            for _ in range(ncores):
                procs.append( mp.Process(target=nw.calcBetweenPar, args=(self.nxGraphs, inQueue, outQueue)) )
                procs[-1].start()
                
            for win in tk.log_progress(range(self.numWinds), name="Window"):
                
                ## Waits until the next result is available, then stores it in the object.
                result = outQueue.get()
                
                win = result[0]
                self.btws[win] = copy.deepcopy(result[1])

            # Joins processes.
            for proc in procs:
                proc.join()
        
    def calcEigenCentral(self):
        for win in range(self.numWinds):
            # Calc all node centrality values in the system.
            cent = nxeigencentrality(self.nxGraphs[win], weight='weight')
            nx.set_node_attributes(self.nxGraphs[win], cent, 'eigenvector')

    def calcCommunities(self):
        
        self.nodesComm = {}
        
        for win in range(self.numWinds):
            
            self.nodesComm[win] = {}
            
            communities = community.best_partition(self.nxGraphs[win])

            communitiesLabels = np.unique( np.asarray( list(communities.values()), dtype=int ) )
            
            self.nodesComm[win]["commLabels"] = copy.deepcopy( communitiesLabels )
            
            nx.set_node_attributes(self.nxGraphs[win], communities, 'modularity')
            
            self.nodesComm[win]["commNodes"] = {}
            
            for comm in communitiesLabels:
                # First get a list of just the nodes in that class
                nodesInClass = [n for n in self.nxGraphs[win].nodes() if self.nxGraphs[win].nodes[n]['modularity'] == comm]

                # Then create a dictionary of the eigenvector centralities of those nodes
                nodesInClassEigenVs = {n:self.nxGraphs[win].nodes[n]['eigenvector'] for n in nodesInClass}

                # Then sort that dictionary
                nodesInClassEigenVsOrd = sorted(nodesInClassEigenVs.items(), 
                                                key=itemgetter(1), 
                                                reverse=True)
                nodesInClassEigenVsOrdList = [x[0] for x in nodesInClassEigenVsOrd]
                
                self.nodesComm[win]["commNodes"][comm] = copy.deepcopy( nodesInClassEigenVsOrdList )
            
            # Orders communities based on size.
            communitiesOrdSize = list( sorted(self.nodesComm[win]["commNodes"].keys(),
                                            key=lambda k: len(self.nodesComm[win]["commNodes"][k]),
                                            reverse=True) )
            
            self.nodesComm[win]["commOrderSize"] = copy.deepcopy( communitiesOrdSize )
            
            # Orders communities based on highest eigenvector centrality of all its nodes.
            communitiesOrdEigen = list( sorted(self.nodesComm[win]["commNodes"].keys(), 
                                            key=lambda k: self.nxGraphs[win].nodes[self.nodesComm[win]["commNodes"][k][0]]['eigenvector'], 
                                            reverse=True) )
            
            self.nodesComm[win]["commOrderEigenCentr"] = copy.deepcopy( communitiesOrdEigen )
    
    def interfaceAnalysis(self, selAstr, selBstr, betweenDist = 15, samples = 10):
        
        # Select the necessary stride so that we get *samples*.
        stride = int(np.floor(len(self.workU.trajectory)/samples))
        
        selPtn = self.workU.select_atoms(selAstr)
        selNcl = self.workU.select_atoms(selBstr)

        contactNodes = set()

        # Find selection of atoms that are within "betweenDist" from both selections.
        # Get selection of nodes represented by the atoms by sampling several frames.
        for ts in tk.log_progress(self.workU.trajectory[:samples*stride:stride], every=1, 
                            name="Samples",size=samples):
            
            contactSel = mdaB(self.workU.select_atoms("all"), selPtn, selNcl, betweenDist )    
            contactNodes.update(np.unique( self.atomToNode[ contactSel.atoms.ix_array ] ))
        
        # Makes it into a list for better processing
        contactNodesL = np.asarray(list(contactNodes))
        
        # Sanity check.
        # Verifies possible references from atoms that had no nodes.
        if len(contactNodesL[ contactNodesL < 0 ]):
            print("ERROR! There are {} atoms not represented by nodes! Verify your universe and atom selection.".format(len(contactNodesL[ contactNodesL < 0 ])))
        
        # These are all nodes in both selections.
        numContactNodesL = len(contactNodes)
        
        #print("{0} nodes found in the interface.".format(numContactNodesL))

        # Filter pairs of nodes that have contacts
        contactNodePairs = []
        for i in range(numContactNodesL):
            for j in range(i,numContactNodesL):
                nodeI = contactNodesL[i]
                nodeJ = contactNodesL[j]
                if max([ self.corrMatAll[win, nodeI, nodeJ] for win in range(self.numWinds) ]) > 0:
                    contactNodePairs.append( (nodeI, nodeJ) )

        # These are all pairs of nodes that make direct connections. These pairs WILL INCLUDE
        #    pairs where both nodes are on the same side of the interface.
        contactNodePairs = np.asarray( contactNodePairs, dtype=np.int )
        
        #print("{0} contacting node pairs found in the interface.".format(len(contactNodePairs)))

        def inInterface(nodesAtmSel, i, j):
            segID1 = nodesAtmSel.atoms[i].segid
            segID2 = nodesAtmSel.atoms[j].segid
            
            if (segID1 != segID2) and ((segID1 in self.segIDs) or (segID2 in self.segIDs)):
                return True
            else:
                return False
        
        # These are pairs where the nodes are NOT on the same selection, that is, pairs that connect
        #   the two atom selections.
        self.interNodePairs = [ (i,j) for i,j in contactNodePairs if inInterface(self.nodesAtmSel, i, j) ]
        self.interNodePairs = np.asarray( self.interNodePairs, dtype=np.int )
        print("{0} pairs of nodes connecting the two selections.".format(len(self.interNodePairs)))

        self.contactNodesInter = np.unique(self.interNodePairs)
        print("{0} unique nodes in interface node pairs.".format(len(self.contactNodesInter)))
        
        
        
        
        
        
        
        
