# -*- coding: utf-8 -*-

import numpy

NODE_TYPE_SOC = 1
NODE_TYPE_ECO = 0 

EDGE_TYPE_SOC_SOC = 2
EDGE_TYPE_ECO_SOC = 1
EDGE_TYPE_ECO_ECO = 0

MOTIF4_NAMES = ['I.A', 'I.B', 'I.C', 'I.D', 'II.A', 'II.B', 'II.C', 'II.D', 
                'III.A', 'III.B', 'III.C', 'III.D', 'IV.A', 'IV.B', 'IV.C', 'IV.D', 
                'V.A', 'V.B', 'V.C', 'V.D', 'VI.A', 'VI.B', 'VI.C', 'VI.D', 
                'VII.A', 'VII.B', 'VII.C', 'VII.D']
MOTIF3_NAMES = ['I.A', 'I.B', 'I.C', 'II.A', 'II.B', 'II.C']

COLORS_TYPES = {
                NODE_TYPE_ECO : 'green', 
                NODE_TYPE_SOC : 'red',
                2 : 'c', 
                3 : 'm', 
                4 : 'y', 
                5 : 'k', 
                6 : 'w'
                }

MULTI_DEFAULT_NAMES = ['Lake', 'Town', 'Issue', 'System', 'Entity', 'Item', 'Universe']

MOTIF3_EDGES = numpy.array([[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]])

MOTIF4_EDGES = numpy.array([[0,2,0],
                         [1,2,0],
                         [0,2,1],
                         [1,2,1],
                         [0,2,0],
                         [1,2,0],
                         [0,2,1],
                         [1,2,1],
                         [0,4,0],
                         [1,4,0],
                         [0,4,1],
                         [1,4,1],
                         [0,0,0],
                         [1,0,0],
                         [0,0,1],
                         [1,0,1],
                         [0,3,0],
                         [1,3,0],
                         [0,3,1],
                         [1,3,1],
                         [1,1,0],
                         [1,1,1],
                         [1,2,0],
                         [1,2,1],
                         [0,1,0],
                         [0,1,1],
                         [0,2,0],
                         [0,2,1]])

MOTIF4_SYMMETRIES = numpy.array([2, 2, 2, 2, 
                                 2, 2, 2, 2, 
                                 4, 4, 4, 4, 
                                 1, 1, 1, 1, # sparse motifs IV.A-IV.D
                                 3, 3, 3, 3, 
                                 1, 1, 2, 2, 
                                 1, 1, 2, 2])

MOTIF4_AUT = numpy.array([2, 2, 2, 2, 
                          2, 2, 2, 2, 
                          1, 1, 1, 1, 
                          1, 1, 1, 1, # sparse motifs IV.A-IV.D
                          4, 4, 4, 4, 
                          4, 4, 2, 2, 
                          4, 4, 2, 2])
MOTIF3_AUT = numpy.array([1, 2, 1, 1, 2, 1])

# models for random baselines
MODEL_ERDOS_RENYI     = 'erdos_renyi'
MODEL_ACTORS_CHOICE   = 'actors_choice'
MODEL_FIXED_DENSITIES = 'fixed_densities'

def binaryCodeToClass4Motifs(digits : int) -> str:
    """
    Classifies 4-motifs according to 
    Ö. Bodin, M. Tengö: Disentangling intangible social–ecological systems 
    Global Environmental Change 22 (2012) 430–439
    http://dx.doi.org/10.1016/j.gloenvcha.2012.01.005
    
    :param digits: binary code of the motif as described in the paper
    :returns: string code 'I.A' to 'VII.D'
    :raises ValueError: if the given digits are not in the required range
    """
    if digits == 0b000000:  return 'IV.A'
    if(digits == 0b000100 or
       digits == 0b010000 or
       digits == 0b000001 or
       digits == 0b000010): return 'VII.A'
    if digits == 0b001000:  return 'IV.C'
    if digits == 0b100000:  return 'IV.B'
    if(digits == 0b000101 or
       digits == 0b010010): return 'II.A'
    if(digits == 0b000110 or
       digits == 0b010001): return 'VII.C'
    if(digits == 0b010100 or
       digits == 0b000011): return 'I.A'
    if(digits == 0b001100 or
       digits == 0b011000 or
       digits == 0b001010 or
       digits == 0b001001): return 'VII.B'
    if(digits == 0b100100 or
       digits == 0b100001 or
       digits == 0b100010 or
       digits == 0b110000): return 'VI.A'
    if digits == 0b101000:  return 'IV.D'
    if(digits == 0b001101 or
       digits == 0b011010): return 'II.C'
    if(digits == 0b100101 or
       digits == 0b110010): return 'II.B'
    if(digits == 0b101100 or
       digits == 0b111000 or
       digits == 0b101001 or
       digits == 0b101010): return 'VI.B'
    if(digits == 0b001110 or
       digits == 0b011001): return 'VII.D'
    if(digits == 0b010110 or
       digits == 0b010011 or
       digits == 0b010101 or
       digits == 0b000111): return 'V.A'
    if(digits == 0b100110 or
       digits == 0b110001): return 'VI.C'
    if(digits == 0b011100 or
       digits == 0b001011): return 'I.C'
    if(digits == 0b110100 or
       digits == 0b100011): return 'I.B'
    if digits == 0b010111:  return 'III.A'
    if(digits == 0b101101 or
       digits == 0b111010): return 'II.D'
    if(digits == 0b011110 or
       digits == 0b011011 or
       digits == 0b011101 or
       digits == 0b001111): return 'V.C'
    if(digits == 0b101110 or
       digits == 0b111001): return 'VI.D'
    if(digits == 0b110110 or
       digits == 0b110011 or
       digits == 0b110101 or
       digits == 0b100111): return 'V.B'
    if(digits == 0b111100 or
       digits == 0b101011): return 'I.D'
    if digits == 0b011111:  return 'III.C'
    if digits == 0b110111:  return 'III.B'
    if(digits == 0b111110 or
       digits == 0b111101 or
       digits == 0b101111 or
       digits == 0b111011): return 'V.D'
    if digits == 0b111111:  return 'III.D'
    raise ValueError('cannot decode digits {0:b} for 4-motif'.format(digits))

def binaryCodeToClass3Motifs(digits : int) -> str:
    """
    Classifies 3-motifs according to the following scheme: A 3-motif consists of either
    one social and two ecological nodes or one ecological and two social nodes. Thus, 
    one node can be considered distinct from the two other nodes. Let's call this node
    a and the other two nodes b1 and b2. The following classes occur (listing undirected edges):
        
    class I: without edge (b1,b2):
        - I.A: no edges,
        - I.B: either (a,b1) or (a,b2),
        - I.C: both (a,b1) and (a,b2).
    class II: with edge (b1,b2):
        - II.A: (b1,b2),
        - II.B: (b1,b2) and either (a,b1) or (a,b2),
        - II.C: (b1,b2) and both (a,b1) and (a,b2).
    
    :param digits: binary code of the motif as described above
    :returns: string code 'I.A' to 'VII.D'
    :raises ValueError: if the given digits are not in the required range
    """ 
    digits1 = digits // 4
    digits2 = digits % 4
    
    cl1 = ''
    if digits1 == 0:
        cl1 = 'I'
    elif digits1 == 1:
        cl1 = 'II'
    else:
        raise ValueError('cannot decode digits {0:b} for 3-motif'.format(digits))
    
    cl2 = ''
    if digits2 == 0b00:
        cl2 = 'A'
    elif digits2 == 0b11:
        cl2 = 'C'
    else:
        cl2 = 'B'
    return cl1 + '.' + cl2