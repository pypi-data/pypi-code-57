#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:11:21 2019

@author: arrigoni
"""
import unittest

import numpy as np
from itertools import permutations

from spinney.structures.wigner_seitz import WignerSeitzCell

np.random.seed(12)

# cube
cube = {'no faces' : 6, 'no vertices' : 8, 'no edges' : 12, 
        'vertices coord' : [(1, 1, 1)] + list(set(permutations([1, 1, -1]))) + 
                           list(set(permutations([1, -1, -1]))) + 
                           [(-1, -1, -1)]
                        }

# rhombic dodecahedron
rhombic_dodecahedron = {'no faces' : 12, 'no vertices' : 14, 'no edges' : 24,
                        'vertices coord' : cube['vertices coord'] + 
                        list(set(permutations([2, 0, 0]))) + 
                        list(set(permutations([-2, 0, 0])))
                        }
# truncated octahedron
truncated_octahedron = {'no faces' : 14, 'no vertices' : 24, 'no edges' : 36,
                        'vertices coord' : 
                        list(set(permutations([0, 1, 2]))) + 
                        list(set(permutations([0, -1, 2]))) + 
                        list(set(permutations([0, 1, -2]))) +
                        list(set(permutations([0, -1, -2])))
                        }

print('Testing: ', WignerSeitzCell.__name__)

class WSTestCase(unittest.TestCase):

    def setUp(self):
        self.sc_cell = np.eye(3)
        self.fcc_cell = np.array([[0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0]])
        self.bcc_cell = np.array([[-0.5, 0.5, 0.5],
                                  [0.5, -0.5, 0.5],
                                  [0.5, 0.5, -0.5]])
    
    def make_testWS(self, cell, ws_dict):
        ws = WignerSeitzCell(cell)
        vertices = ws.cell_vertices
        faces = ws.face_vertices
        self.assertEqual(len(vertices), ws_dict['no vertices'])
        self.assertEqual(len(faces), ws_dict['no faces'])
        vals = np.array(ws_dict['vertices coord'])
        non_zero = vals[vals != 0]
        min_v = np.min(np.abs(non_zero))
        vals2 = np.array(ws.cell_vertices)
        non_zero = vals2[vals2 != 0]
        min_v2 = np.min(np.abs(non_zero))
        c_factor = min_v/min_v2
        vals2 *= c_factor
        for v in vals:
            found = False
            for v2 in vals2:
                if np.allclose(v, v2, 1e-12):
                    found = True
                    break
            self.assertTrue(found, "Vertices' coordinates do not match!") 
        # check that perpendicular vectors are actually perpendicular to
        # the faces
        for no_f, face in enumerate(ws.face_vertices):
            n = ws.points[ws.face_normals[no_f]]
            face_coords = ws.vertices[face]
            index = np.random.randint(0, len(face_coords))
            p0 = face_coords[index]
            other_coords = face_coords[(face_coords != p0).any(axis=1)]
            for point in other_coords:
                v = point - p0
                self.assertAlmostEqual(np.dot(v, n), 0, 9,
                                       msg="NOT PERPENDICULAR")  
                
    def testWSsc(self):
        self.make_testWS(self.sc_cell, cube)
       
    def testWSfcc(self):
        self.make_testWS(self.fcc_cell, rhombic_dodecahedron)
        
    def testWSbcc(self):
        self.make_testWS(self.bcc_cell, truncated_octahedron)
        
if __name__ == '__main__':
    unittest.main()
