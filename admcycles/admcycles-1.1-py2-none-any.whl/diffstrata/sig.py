from sage.rings.integer_ring import ZZ # pylint: disable=import-error

class Signature(object):
    """
    A signature of a stratum.
    
    Attributes:
        sig (tuple): signature tuple
        g (int): genus
        n (int): total number of points
        p (int): number of poles
        z (int): number of zeroes
        poles (tuple): tuple of pole orders
        zeroes (tuple): tuple of zero orders
        pole_ind (tuple): tuple of indices of poles
        zero_ind (tuple): tuple of indices of zeroes
    
    EXAMPLES ::

        sage: from admcycles.diffstrata.sig import Signature
        sage: sig=Signature((2,1,-1,0))
        sage: sig.g
        2
        sage: sig.n
        4
        sage: sig.poles
        (-1,)
        sage: sig.zeroes
        (2, 1)
        sage: sig.pole_ind
        (2,)
        sage: sig.zero_ind
        (0, 1)
        sage: sig.p
        1
        sage: sig.z
        2
    """
    def __init__(self,sig):
        """
        Initialise signature
        
        Args:
            sig (tuple): signature tuple of integers adding up to 2g-2
        """
        self.sig = sig
        sum_sig = sum(sig)
        if sum_sig % 2 != 0:
            raise ValueError("Error! Illegal signature: Genus not an integer")
        self.g = int(sum_sig/2) + 1
        self.n = len(sig)
        self.poles = tuple(p for p in sig if p < 0)
        self.zeroes = tuple(z for z in sig if z > 0)
        self.marked_points = tuple(k for k in sig if k == 0)
        self.p = len(self.poles)
        self.z = len(self.zeroes)
        self.pole_ind = tuple(i for i,p in enumerate(sig) if p < 0)
        self.zero_ind = tuple(i for i,z in enumerate(sig) if z > 0)

    def __repr__(self):
        return "Signature(%r)" % (self.sig,)
    def __hash__(self):
        return hash(self.sig)
    def __eq__(self,other):
        try:
            return self.sig == other.sig
        except AttributeError:
            return False
