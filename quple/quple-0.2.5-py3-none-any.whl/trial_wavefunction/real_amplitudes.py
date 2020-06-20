from typing import List, Union, Optional, Callable, Sequence, Tuple

from quple import ParameterisedCircuit

class RealAmplitudes(ParameterisedCircuit):
    '''RealAmplitudes trial wavefunction

    '''    
    def __init__(self, n_qubit: int, copies: int=2, 
                 entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                 parameter_symbol:str='θ', name:str=None):
        super().__init__(n_qubit=n_qubit, copies=copies,
                         rotation_blocks='RY',
                         entanglement_blocks='CX',
                         entangle_strategy=entangle_strategy,
                         parameter_symbol=parameter_symbol,
                         final_rotation_layer=True, name=name)