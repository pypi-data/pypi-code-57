#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:35:47 2019

@author: arrigoni
"""
import numpy as np
from scipy.spatial import Voronoi

class WignerSeitzCell(Voronoi):
    """ Object describing the crystal Wigner-Seitz cell.
    
    Parameters
    ----------
    cell : 2D array
        the Cartesian components of the cell parameters. One row for one cell
        parameter
    
    furthest_site : bool
        see **scipy.statial.Voronoi**
    
    incremental : bool
        see **scipy.statial.Voronoi**
        
    qhull_options : str
        see **scipy.statial.Voronoi**
        
    Attributes
    ----------
    cell : 2D array
        the input cell
        
    cell_vertices : 2D numpy array
        each row holds the Cartesian coordinates of one of the Wigner-Seitz 
        cell vertices
      
    cell_vertices_indexes : 2D numpy array
        indices of the Wigner-Seitz vertices forming the Wigner-Seitz diagram.
        The indices correspond to the points in *self.vertices*
    
    center_index : int
        the index of the lattice point, wrt *self.points* corresponding to the
        center of the Wigner-Seitz cell
    
    face_vertices : list of lists
        for each face forming the Wigner-Seitz diagram, one row contans the 
        indices of the vertices, wrt *self.vertices*, forming that face
    
    face_normals : list
        for each face described in *self.face_vertices*, one element of 
        *face_normal* is an integer representing the index of the lattice point
        in *self.points*, such that the vector joining the origin and this
        point is normal to this face
    
    face_distances : list
        for each face described in *self.face_vertices*, an element of 
        *face_distances* is the minimum distance of a lattice point 
        from that face
    """
    def __init__(self, cell, furthest_site=False, incremental=False, 
                 qhull_options=None):
        if not (type(cell) is np.ndarray):
            cell = np.array(cell)
        if cell.shape != (3, 3):
            raise ValueError('Implemented only for 3D cells!')
        self._cell = cell 
        aa, bb, cc = np.meshgrid(np.arange(-1,2), np.arange(-1,2),
                                 np.arange(-1,2))
        self._scaled_positions = np.vstack((aa.ravel(),
                                            bb.ravel(), cc.ravel())).T
        Voronoi.__init__(self, np.dot(self._scaled_positions, self._cell),
                         furthest_site, incremental, qhull_options)
        self._ws_initialization()
        
    def _ws_initialization(self):
        self._find_cell_vertices()
        self._get_center_index()
        self._get_face_normals()
        self._get_face_vertices()
        self._get_face_distances()
        
    @property
    def cell(self):
        return self._cell
    
    def _find_cell_vertices(self):
        """ Return the Cartesian coordinates of the 
        vertices of the Wigner-Seitz cell
        """
        # there should be only one finite Voronoi region with the point we have
        # chosen
        points_indexes = []
        count = 0
        for region in self.regions:
            if region:
                if -1 in region:
                    continue
                else:
                    count += 1
                    points_indexes.append(region)
        if count != 1:
            raise RuntimeError("Error in cell vertices.")
        self._cell_vertices = self.vertices[points_indexes[0]]
        self._cell_vertices_indexes = points_indexes[0]
        
    @property
    def cell_vertices(self):
        """ The cartesian coordinates of the vertices forming the
        Wigner-Seitz cell
        """
        return self._cell_vertices
    
    @property
    def cell_vertices_indexes(self):
        """ The indexes of the vertices of the Wigner-Seitz cell
        """
        return self._cell_vertices_indexes    
        
    @property
    def center_index(self):
        """ Return the index on the lattice point (0,0,0)
        """
        return self._center_index
    
    @property
    def face_vertices(self):
        """ For each face of the Wigner-Seitz cell, returns the indices of the
        cell vertices forming the face. """
        return self._face_vertices
    
    @property
    def face_normals(self):
        """ For each face of the Wigner-Seitz cell, return the index of the
        point defining the bisecting vector perpendicular to that face.
        (vector origin is always at the index *self.center_index*, 
        corresponding to (0,0,0)).
        Such vector bisect
        """
        return self._face_normals
    
    @property
    def face_distances(self):
        """ Return the distance of each face of the Wigner-Seitz cell from
        a lattice point
        """        
        return self._face_distances
        
    def _get_center_index(self):
        self._center_index = np.where((self.points == (0,0,0)).all(1))[0][0]
    
    def _get_face_vertices(self):
        ridges = []
        for ridge in self.ridge_vertices:
            if set(ridge).issubset(self.cell_vertices_indexes):
                ridges.append(ridge)
        self._face_vertices = ridges   
        
    def _get_face_normals(self):
        normals = []
        for ridge in self.ridge_points:
            if self.center_index in ridge:
                mask = ridge != self.center_index
                index = ridge[mask][0]
                normals.append(index)
        self._face_normals = normals
         
    def _get_face_distances(self):
        distances = []
        for normal_index in self.face_normals:            
            distances.append(np.linalg.norm(self.points[normal_index])/2)
        self._face_distances = distances
                
    def is_in_cell(self, point):
        """ Given a point in the coordinates given by *self.cell*,
        it returns True if the point belongs to the Wigner-Seitz cell.
        
        Parameters
        ----------
        point : array
            scaled coordinates of a test point.
        
        Returns
        -------
        in_cell : bool
        """
        point = np.dot(point, self.cell)
        dist_0 = np.linalg.norm(point)
        # points on the bisecting line for each face
        nnn_points = self.points[self.face_normals]
        vectors = nnn_points-point
        vectors_norms = np.linalg.norm(vectors, axis=1)
        in_cell = (dist_0 <= vectors_norms).all()
        return in_cell
        
