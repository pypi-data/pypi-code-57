from typing import List, Union, Optional, Callable, Sequence, Tuple

from quple import ParameterisedCircuit
from quple.circuit.templates.excitation_preserving_block import ExcitationPreservingBlock

class ExcitationPreserving(ParameterisedCircuit):
    '''Excitation preserving trial wavefunction

    '''    
    def __init__(self, n_qubit: int, copies: int=2, 
                 mode:str='iswap',
                 entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                 parameter_symbol:str='θ', name:str=None):
        
        supported_modes = ['iswap', 'fsim']
        if mode not in supported_modes:
            raise ValueError('Unsupported mode {}, choose one of {}'.format(mode, supported_modes))
        
        excitation_preserving_block = ExcitationPreservingBlock(mode)   
        super().__init__(n_qubit=n_qubit, copies=copies,
                         rotation_blocks='RZ',
                         entanglement_blocks=excitation_preserving_block,
                         entangle_strategy=entangle_strategy,
                         parameter_symbol=parameter_symbol,
                         final_rotation_layer=False, name=name)