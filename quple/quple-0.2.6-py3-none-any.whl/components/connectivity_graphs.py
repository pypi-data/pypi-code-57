from typing import List, Tuple
import itertools
    
def nearest_neighbor(n:int, m:int=2) -> List[Tuple[int]]:
    return [tuple(range(i, i+m)) for i in range(n - m + 1)]    

def cyclic(n:int, m:int=2) -> List[Tuple[int]]:
    return nearest_neighbor(n,m) + [tuple(range(n - m + 1, n)) + (0,)]

def fully_connected(n:int, m:int=2) -> List[Tuple[int]]:
    return list(itertools.combinations(list(range(n)), m))

def all_to_all(n:int, m:int=2) -> List[Tuple[int]]:
    return list(itertools.permutations(list(range(n)), m))

def star(n:int, m:int=2) -> List[Tuple[int]]:
    if m != 2:
        raise ValueError('the connectiviy graphs of the "star" method'
                         ' requires 2 qubits in an interaction unit'
                        ' but {} is given'.format(m))
    return [(0, i+1) for i in range(n - m + 1)]


connectivity_graph = {
    'nearest_neighbor': nearest_neighbor,
    'linear': nearest_neighbor,
    'cyclic': cyclic,
    'circular': cyclic,
    'full': fully_connected,
    'fully_connected': fully_connected,
    'all_to_all': all_to_all,
    'star': star
}