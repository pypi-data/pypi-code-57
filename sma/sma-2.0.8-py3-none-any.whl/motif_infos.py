#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sma
import inspect, sys
import itertools

class MotifInfo:
    """
    Parent class of all MotifInfo classes. Subclasses contain information about
    motifs, their classificators and counters. The following properties are provided:
        
    :var signature: signature of the motifs
    :var classes: list of names of all motif classes
    :var classes_type: type of the class names, e.g. ``str`` or ``int``
    :var classificator: subclass of :py:class:`sma.MotifClassificator` for 
          classifying motifs
    :var counter: counting function with signature
        
          ``counter(G, *levels, **kwargs)``
    :var sparse_counter: counting function for sparse graphs with signature
        
          ``sparse_counter(G, *levels, **kwargs)``
    :var expectations: function for computing motif expectations in a
          Erdős-Rényi model
        
          ``expectations(G, *levels, **kwargs)``
    :var variances: function for computing motif variances in a Erdős-Rényi model
        
          ``variances(G, *levels, **kwargs)``
    :var projections: dict containing information about closed/open pairs of motifs,
        i.e. which motif classes belong together when non considering dyads on a 
        specific level of the motif. The dict is indexed by abstract levels (indexes
        of levels in ``signature``). Every entry is a list of tuples of motif class
        names. Each tuple contains first the open and secondly the closed motif.
        See :py:class:`sma.Motif3Info` as an example.
    
    If a certain feature is not implemented, the corresponding value is set to ``None``.
    """
    signature      = []
    classes        = []
    classes_type   = None
    classificator  = None
    counter        = None
    sparse_counter = None
    expectations   = None
    variances      = None
    projections    = {}

class Motif3Info(MotifInfo):
    signature      = [1, 2]
    classes        = sma.MOTIF3_NAMES
    classes_type   = str
    classificator  = sma.ThreeMotifClassificator
    counter        = sma.count3Motifs
    sparse_counter = sma.count3MotifsSparse
    expectations   = sma.expected3Motifs
    variances      = sma.var3Motifs
    projections    = {1: [('I.A', 'II.A'),
                          ('I.B', 'II.B'),
                          ('I.C', 'II.C')]}

class Motif4Info(MotifInfo):
    signature      = [2, 2]
    classes        = sma.MOTIF4_NAMES
    classes_type   = str
    classificator  = sma.FourMotifClassificator
    counter        = sma.count4Motifs
    sparse_counter = sma.count4MotifsSparse
    expectations   = sma.expected4Motifs
    variances      = sma.var4Motifs
    projections    = {0: [('I.A', 'I.B'),
                          ('I.C', 'I.D'),
                          ('II.A', 'II.B'),
                          ('II.C', 'II.D'),
                          ('III.A', 'III.B'),
                          ('III.C', 'III.D'),
                          ('IV.A', 'IV.B'),
                          ('IV.C', 'IV.D'),
                          ('V.A', 'V.B'),
                          ('V.C', 'V.D'),
                          ('VII.A', 'VI.A'),
                          ('VII.B', 'VI.B'),
                          ('VII.C', 'VI.C'),
                          ('VII.D', 'VI.D')],
                      1: [('I.A', 'I.C'),
                          ('II.A', 'II.C'),
                          ('III.A', 'III.C'),
                          ('IV.A', 'IV.C'),
                          ('V.A', 'V.C'),
                          ('I.B', 'I.D'),
                          ('II.B', 'II.D'),
                          ('III.B', 'III.D'),
                          ('IV.B', 'IV.D'),
                          ('V.B', 'V.D'),
                          ('VI.A', 'VI.B'),
                          ('VI.C', 'VI.D'),
                          ('VII.A', 'VII.B'),
                          ('VII.C', 'VII.D')]}

class Motif111Info(MotifInfo):
    signature      = [1, 1, 1]
    classes        = [0, 1, 2, 3, 4, 5, 6, 7]
    classes_type   = int
    classificator  = sma.Multi111MotifClassificator
    counter        = None
    sparse_counter = None
    expectations   = None
    variances      = None

class Motif121Info(MotifInfo):
    signature      = [1, 2, 1]
    classes        = [-1, 1, 2, 3, 4]
    classes_type   = int
    classificator  = sma.Multi121MotifClassificator
    counter        = None
    sparse_counter = sma.count121MotifsSparse
    expectations   = sma.expected121Motifs
    variances      = None

class Motif221Info(MotifInfo):
    signature      = [2, 2, 1]
    classes        = ['Unclassified'] + list(map(lambda x : '%s.%d' % x, 
                     itertools.product(sma.MOTIF4_NAMES, [0,1,2,3])))
    classes_type   = str
    classificator  = sma.Multi221MotifClassificator
    counter        = None
    sparse_counter = sma.count221MotifsSparse
    expectations   = sma.expected221Motifs
    variances      = None

class Motif222Info(MotifInfo):
    signature      = [2, 2, 2]
    classes        = [-1, 1, 2, 3, 4]
    classes_type   = int
    classificator  = sma.Multi222MotifClassificator
    counter        = None
    sparse_counter = sma.count222MotifsSparse
    expectations   = sma.expected222Motifs
    variances      = None

class Motif2Info(MotifInfo):
    signature      = [2]
    classes        = [0, 1]
    classes_type   = int
    classificator  = sma.TwoMotifClassificator
    counter        = None
    sparse_counter = None
    expectations   = None
    variances      = None

class Motif11Info(MotifInfo):
    signature      = [1, 1]
    classes        = [0, 1]
    classes_type   = int
    classificator  = sma.TwoMotifClassificator
    counter        = None
    sparse_counter = None
    expectations   = None
    variances      = None
    
class Motif3pInfo(MotifInfo):
    signature      = [3]
    classes        = [0, 1, 2, 3]
    classes_type   = int
    classificator  = sma.ThreePMotifClassificator
    counter        = None
    sparse_counter = None
    expectations   = None
    variances      = None

class Motif1Info(MotifInfo):
    signature      = [1]
    classes        = [1]
    classes_type   = int
    classificator  = sma.OneMotifClassificator
    counter        = None
    sparse_counter = None
    expectations   = None
    variances      = None

def _infoObjects():
    return filter(lambda info: issubclass(info[1], MotifInfo) and info[1] != MotifInfo,
                  inspect.getmembers(sys.modules[__name__], inspect.isclass))
    
def motifInfo(signature):
    """
    Returns a subclass of :py:class:`sma.MotifInfo` correponding to the given
    signature. The order of the signature is irrelevant.
    
    :param signature: the signature
    :returns: subclass of :py:class:`sma.MotifInfo`
    :raises NotImplementedError: if no subclass of :py:class:`sma.MotifInfo` is
        available for the given signature
    """
    signature = sorted(signature)
    for name, obj in _infoObjects():
        if signature == sorted(obj.signature):
            return obj
    raise NotImplementedError('motifs with signature %s not implemented' % str(signature))

def supportedSignatures() -> iter:
    """
    Returns an iterator yielding all supported signatures.
    
    .. code :: Python
        
        print(list(sma.supportedSignatures()))
        
    
    :returns: iterator yielding all supported signatures.
    """
    return map(lambda x : x[1].signature, _infoObjects())
