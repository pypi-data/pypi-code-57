#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import sma

def countMultiMotifs(G : nx.Graph, 
                     *arities, 
                     roles = [], 
                     iterator = None, 
                     **kwargs):
    """
    Front-end function for counting multi-motifs. The default iterator is
    :py:class:`sma.MultiMotifs`. As classificator serves :py:class:`sma.MultiMotifClassificator`.
    All options of :py:meth:`sma.countMotifs` are available.
    
    Call :py:meth:`sma.supportedSignatures` for an overview of all supported 
    signatures.
    
    See also :py:meth:`sma.countMultiMotifsSparse`.
    
    :param G: the graph
    :param arities: arities for the motif source and the classificator
    :param roles: roles of the level, cf. :py:class:`sma.MultiMotifClassificator`.
    :param iterator: a custom iterator, default is :py:class:`sma.MultiMotifs`.
    :param kwargs: additional parameters for :py:meth:`sma.countMotifs`
    """
    signature = sma.multiSignature(arities)
    
    # speeding up 3 and 4 motifs
    if signature == [1,2]:
        positions = sma.matchPositions([1,2], arities, roles)
        if iterator is None:
            iterator = sma.iterate3Motifs(G, positions[0], positions[1])
        return sma.count3Motifs(G, iterator, **kwargs)
    elif signature == [2,2]:
        positions = sma.matchPositions([2,2], arities, roles)
        if iterator is None:
            iterator = sma.iterate4Motifs(G, positions[0], positions[1])
        return sma.count4Motifs(G, iterator, **kwargs)
    
    # now handle all other motifs
    motif_info = sma.motifInfo(signature)
    if iterator is None:
        iterator = sma.MultiMotifsNormalized(G, *arities, roles = roles, motif_info = motif_info)
    return sma.countMotifs(G, motif_info.classificator(G), iterator, **kwargs)
        

def countMultiMotifsSparse(G : nx.Graph,
                           *arities, 
                           roles = [],
                           **kwargs):
    """
    Front-end function for several counting functions for sparse networks. It supports
    the same parameters for defining the motifs (arities, roles) as other multi-level
    counting functions. Please check the documentations of the respective functions
    as some of them might return partial counts only. A full list of supported
    motif signatures can be accessed via :py:meth:`sma.supportedSignatures`.
    
    See also :py:meth:`sma.countMultiMotifs`.
    
    :param G: the SEN
    :param arities: arities of the motifs, cf. :py:class:`sma.MultiMotifClassificator`.
    :param roles: roles of the levels, cf. :py:class:`sma.MultiMotifClassificator`.
    :param kwargs: additional parameters for the counter functions, see above.
    """
    signature  = sma.multiSignature(arities)
    motif_info = sma.motifInfo(signature)
    positions  = sma.matchPositions(motif_info.signature, arities, roles)
    if motif_info.sparse_counter is None:
        raise NotImplementedError('sparse counting for signature %s is not implemented'\
                                  % str(motif_info.signature))
    return motif_info.sparse_counter(G, *positions, **kwargs)

def findIdealCounter(signature : list, 
                     motifs : list, 
                     assume_sparse : bool = True):
    """
    Determines an ideal counter for a family of motifs. This function checks whether
    the given motifs can be counted with countes for sparse networks 
    (if ``assume_sparse = True``) and returns in this case the counter supplemented
    with additional parameters for the counter.
    
    This function is a called by :py:meth:`sma.countMotifsAuto`.
    
    :param signature: (ordered) signature
    :param motifs: list of motif classes
    :param assume_sparse: whether the network is assumed to be sparse
    :returns: tuple consisting of
    
        - a counting function, e.g. :py:meth:`sma.countMultiMotifs` or 
          :py:meth:`sma.countMultiMotifsSparse`,
        - a dict with additional parameters for this counting function
    """
    if signature == [1,2] and assume_sparse:
        return sma.countMultiMotifsSparse, {}
    elif signature == [2,2]:
        if assume_sparse and (not('IV.A' in motifs) and 
                              not('IV.B' in motifs) and 
                              not('IV.C' in motifs) and 
                              not('IV.D' in motifs)):
            return sma.countMultiMotifsSparse, {}
    elif signature == [1,1,2]:
        if assume_sparse:
            for motif in motifs:
                if int(motif) != 3 and int(motif) != 4:
                    return sma.countMultiMotifsSparse, {}
            return sma.countMultiMotifsSparse, {'optimize_top_adjacent' : True}
    elif signature == [1,2,2]:
        if assume_sparse:
            dense = all(map(lambda m : m.endswith('.2') or m.endswith('.3'), motifs))
            if dense and all(map(lambda m : m.endswith('.3'), motifs)):
                return sma.countMultiMotifsSparse, {'optimize_top_adjacent' : True}
            return sma.countMultiMotifsSparse, {}
    elif signature == [2,2,2]:
        if assume_sparse:
            for motif in motifs:
                if int(motif) != 3 and int(motif) != 4:
                    return sma.countMultiMotifs, {}
            return sma.countMultiMotifsSparse, {}
    return sma.countMultiMotifs, {}

def countMotifsAuto(G : nx.Graph, 
                    *motifs, 
                    assume_sparse : bool = True,
                    **kwargs):
    """
    Front-end function for all counting functions in sma. This function determines
    automatically an ideal counter (sparse or dense) for a set of motifs. This 
    reduces overhead and leads to an optimization.
    
    .. code :: Python
        
        # let G by a SEN
        # count open and closed social and ecological triangles
        partial, total = sma.countMotifsAuto(G, "1,2[I.C]", "1,2[II.C]", "2,1[I.C]", "2,1[II.C]")
        print(partial)
        print(total)
    
    :param G: the SEN
    :param motifs: list of motif identifier, see documentation
    :param assume_sparse: whether the network shall be assumed to be sparse
    :param kwargs: more arguments for the counter
    :returns: tuple consisting of:
        
        - a dict with the motif identifiers as keys and the corresponding counts
          as values
        - a dict with all counts collected
    
    :raises TypeError: in case of unrecognizable motif identifiers
    """
    grouped_request = sma.groupMotifIdentifiers(*motifs)
    partial_results = {}
    total_results = {}
    
    # overwrite inadmissible parameters
    kwargs['array'] = False
    
    for cl in grouped_request.keys():
        arities, roles, _ = sma.parseMotifIdentifier(cl)
        signature = sma.multiSignature(arities)
        motif_info = sma.motifInfo(signature)
        counter, kw = sma.findIdealCounter(signature, grouped_request[cl], assume_sparse)
        counted = counter(G, *arities, roles = roles, **{**kwargs, **kw})
        total_results[cl] = counted
        # put partial result together
        for motif in grouped_request[cl]:
            # cast motif class to correct type
            key = motif_info.classes_type(motif)
            if key not in counted:
                raise TypeError("Unrecognizable motif class in identifier %s[%s]."\
                                % (cl, motif))
            partial_results["%s[%s]" % (cl, motif)] = counted[key]
    
    return partial_results, total_results

def exemplifyMotif(G : nx.Graph, identifier : str) -> tuple:
    """
    Returns an example for a motif with given identifier in a SEN.
    
    :param G: the SEN
    :param identifier: motif identifier string
    :returns: motif tuple in normalized form (ordered as in signature)
    :raises StopIteration: if the SEN does not contain such a motif
    """
    arities, roles, motif = sma.parseMotifIdentifier(identifier)
    signature = sma.multiSignature(arities)
    motif_info = sma.motifInfo(signature)
    source = sma.MultiMotifsNormalized(G, *arities, roles = roles, motif_info = motif_info)
    motif = motif_info.classes_type(motif)
    selector = sma.isClass(motif_info.classificator(G), motif)
    return next(source & selector)