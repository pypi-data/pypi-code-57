# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 11:05:42 2018

@author: arrigoni

From Energies and compositions, find the convex hull and the compounds on it.
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial

class BinaryConvexHull(scipy.spatial.ConvexHull):
    """ Manage the convex hull of a binary system
    Usual procedure:
    
    - Query a database and get the formation energies per atom of all 
      compounds of interests. Energies are assumed to be in eV/atom.
      Energies per atom are usually present in each database, if the 
      formation energies per atom are not available, they have to be 
      calculated.
      E.g. for the Mn-O system, all the compounds containing Mn and O.
      The tuple (x_molar_fractions, form_energies_per_atom) 
      is used to find the convex hull of the system. 
      x is the compound in the binary system which is used for the molar 
      fraction (e.g. O or Mn in Mn-O system).
      len(x_molar_fractions) = len(form_energies_per_atom) = number of 
      compounds in the binary system.
      
      If one is interested to filter out the species on the convex hull,
      one should add the array:
          *identifiers*
      which contains the unique identifiers for the compounds
      in the system, generally as employed in the database of choice.
      
    - The module can calculate the convex hull and keep a list of candidates
      compounds. These are compounds on the convex hull, or with a formation
      energy at a given distance from the hull or added by the user.
      The use of identifiers allows to extract more information from these
      compounds from a database.
      
      Parameters
      ----------
      points : 2D array 
              contains the points to be used for calculating the convex hull.
              It must have shape (number_compounds, 2)
              each rows of the array contains the coordinates of a point:
                   (x_molar_fractions, formation_energies_per_atom)
                   
      identifiers : 1D array
               Contain the identifiers for each compound used in *points*
               Useful in order to filters the compounds according to their 
               energy.
               
      Attributes
      ----------
      vertices : 1D array
          the indices of the compounds forming the convex hull
          
      simplices : 2D array of shape (len(vertices), 2)
          the indices of the the points forming the simplical facets of the 
          convex hull
    
      candidates : 1D array
          the indices of the candidate compounds, this is a superset of 
          *self.vertices* which might contains other compounds of interest
          which are not on the hull.
          
      compound_identifiers : 1D array
          a sequence of identifiers corresponding to the input *identifiers*
          
      candidates_identifiers : 1D array
          the sequence of identifiers corresponding to *self.candidates*. It
          is a subset of *self.compound_identifiers*     
      
    """
    def __init__(self, points, identifiers=None):
        if not (identifiers is None):            
            self.compound_identifiers = list(identifiers)
            if len(self.compound_identifiers) != len(points):
                raise CompoundsLenghtsDoNotMatch('The number of points does ' 
                                                 'not match the number of '
                                                 'identifiers')                
        else:           
            self.compound_identifiers = list(range(len(points)))
           
        scipy.spatial.ConvexHull.__init__(self, points,
                                          incremental=None,
                                          qhull_options=None)
        
        # remove from vertices the compounds with energy > 0
        self._remove_outer_vertices()
        # indexes of the compounds we want to keep
        self.candidates = list(self.vertices)
        # identifiers of the candidates
        self.candidates_identifiers = [self.compound_identifiers[cand] 
                                       for cand in self.candidates]
    
    # the scipy.spatial.ConvexHull has no setter for self.vertices;
    # we thus redefine the attribute
    @property
    def vertices(self):
        return self._vertices
    @vertices.setter
    def vertices(self, value):
        self._vertices = value
        
    def _remove_outer_vertices(self):
        """ Remove the vertices corresponding to compounds with energy larger
        than zero.
        """      
        form_energies = self.points[:, 1]
        
        self._vertices = self._vertices[form_energies[self._vertices] <= 0]
        
        n = len(self._vertices)
        self.simplices = np.zeros((n, self.simplices.shape[-1]), dtype='int32')
        
        for i in range(n):
            self.simplices[i] = [self.vertices[i], self.vertices[(i + 1) % n]]
    
    def add_candidate(self, candidate_index, print_warning=True):
        """ Manually adds one candidate from the initial dataset used for 
            *points*.
        
        Parameters
        ----------
        candidate_index : int
            the index in *points* corresponding to the candidate.
            
        print_warning : bool
            if True, a message will be printed when one tries to add a 
            candidate already present in *self.candidates*.
            When this happens, the candidate is not added to the list.
        """
        candidate_identifier = self.compound_identifiers[candidate_index]
        if not ((candidate_index in self.candidates) 
            or (candidate_identifier in self.candidates_identifiers)):
            self.candidates.append(candidate_index)
            self.candidates_identifiers.append(candidate_identifier)
        else:
            if print_warning:
                print('''Candidate {} of index {} is already present in the
                         \rcandidates list.'''.format(candidate_identifier,
                                                      candidate_index))
            
    def add_candidates_within_tolerance(self, tolerance=0.026):
        """ Extends the array of candidates by considering the compounds whose
        energy per atom is larger than at most *tolerance* from the convex hull
        for that given composition.
        
        Parameters
        ----------
        tolerance : float
            the tolerance value in eV/atom. The default value corresponds to 
            the thermal energy at room temperature
        """
        energies_compounds = self.points[:, 1]
        for index in range(len(self.compound_identifiers)):
            # for each compound, calculate its distance from the simplex
            # lying below it
            if not (index in self.candidates):
                x,y = self.points[index]
                for simplex in self.simplices: 
                    x1, y1 = self.points[simplex[0]]
                    x2, y2 = self.points[simplex[1]]
                    if abs(1 - abs(x1 - x2)) < 1e-9: # skip horizontal simplex
                        continue
                    if x1 < x2:
                        xi = x1
                        xf = x2
                        yi = y1
                        yf = y2
                    else:
                        xi = x2
                        yi = y2
                        xf = x1
                        yf = y1
                    if xi <= x < xf:
                        break
                # equation of the simplex (a line for a binary hull)
                # y = yi + m(x - xi)
                m = (yf - yi)/(xf - xi)
                r = lambda x: yi + m*(x - xi)
                if np.abs(energies_compounds[index] - r(x)) <= tolerance:
                    self.add_candidate(index, print_warning=False)
      
    def _reorder_simplices(self):
        """ Reorder the simplices, for plotting purposes.
        They are reordered so that the simplex joining the points at the end
        points of the hull is the first element.
        """ 
        self._simplices_backup = self.simplices.copy()
        # indexes end points            
        a_index = np.argmin(self.points[:, 0])
        b_index = np.argmax(self.points[:, 0])
        pair1 = [a_index, b_index]
        pair2 = [b_index, a_index]
        for i, row in enumerate(self.simplices):
            if (row == pair1).all() or (row == pair2).all():
                break
        self.simplices[[0, i]] = self.simplices[[i, 0]]
        
    def plot_hull(self, title='', molar_fraction_symbol='x', save_name=None):
        ''' Plots the convex hull of the binary system.
        
        title : string
                the plot's title
                
        molar_fraction_symbol : string
                the element label for the molar fraction axis
                
        save_name : string
                where to save the plot, if None, the plot will not be
                saved
        '''        
        plt.figure(figsize=(10,8))
        plt.title(title, {'fontsize':26})
        plt.xlim(0,1)
        plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                   labels=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
               fontsize=22)
        plt.yticks(fontsize=22)
        plt.xlabel('at % ' + molar_fraction_symbol, fontsize=26)
        plt.ylabel(r'$\Delta_fE$ (eV/atom)', fontsize=26)
        
        # all initial data
        plt.scatter(self.points[:, 0], self.points[:, 1], color='blue',
                    alpha=0.5)
        
        # the compounds on the hull
        plt.scatter(self.points[self.vertices, 0], 
                    self.points[self.vertices, 1], color='red',
                    s=60)

        # candidates
        if len(self.candidates) != len(self.vertices):
            plt.scatter(self.points[self.candidates, 0],
                        self.points[self.candidates, 1],
                        color = 'red', s=60, label='Candidates')
            plt.legend(loc='best', fontsize=24)
            
        # hull lines
        self._reorder_simplices()
        for simplex in self.simplices[1:]:
            plt.plot(self.points[simplex,0], self.points[simplex, 1],
                     color='black', linewidth=2)
        plt.tight_layout()   
        if save_name:            
            plt.savefig(save_name + '.pdf', format='pdf', tight_layout=True)
            
        self.simplices = self._simplices_backup


class CompoundsLenghtsDoNotMatch(Exception):
    ''' Raise this exception when the length of the arrays containing 
    information about the compounds is not what expected
    '''
