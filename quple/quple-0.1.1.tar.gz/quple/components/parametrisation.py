from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)    

import re
import sympy
import numpy as np

class UnresolvedParameters():
    def __init__(self, params: Union[str, List[str], List[sympy.Symbol], None]=None):
        self._params = {}
        if params:
            self.append(params)
    
    @property
    def params(self) -> Dict:
        return self._params
    
    def remove_array(self, symbol:str):
        expr = '{}\[\d+\]'.format(symbol)
        matched = [ param for param in self._params if re.match(expr, param)]
        for param in matched:
            self._params.pop(param, None)
    
    def __getitem__(self, key):
        return self._params[key]
    
    def __len__(self):
        return len(self._params)
    
    def get_array(self, symbol:str, indices: Sequence[int]) -> np.ndarray:
        array = [self._params['{}[{}]'.format(symbol, index)] for index in indices]
        return np.asarray(array)
    
    def append_array(self, symbol:str, length:int):
        expanded_symbols = ['{}[{}]'.format(symbol, i) for i in range(length)]
        self.append(expanded_symbols)
        
    def keys(self):
        return self._params.keys()
    
    def values(self):
        return self._params.values()
    
    def append(self, params: Union[str, List[str], sympy.Symbol, List[sympy.Symbol]] ):
        if isinstance(params, list):
            if all(isinstance(param, str) for param in params):
                self._params.update(UnresolvedParameters._create_params(params))
            elif all(isinstance(param, sympy.Symbol) for param in params):
                self._params.update({param.name: param for param in params})
            else:
                raise ValueError('inconsistent list of parameters passed: {}'.format(params))
        elif isinstance(params, str):
            self.append([params])
        elif isinstance(params, sympy.Symbol):
            self._params[params.name] = params
        else:
            raise TypeError('unsupported parameter type : {}'.format(type(params)))
    
    
    @staticmethod
    def _create_params(params:List[str]) -> Dict:
        return {param: sympy.Symbol(param) for param in params}
        