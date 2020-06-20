from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)    

import re
import sympy as sp
import numpy as np

class ParameterTable():
    def __init__(self, params: Union[str, List[str], List[sp.Symbol]]=None):
        self._params = {}
        if params:
            self.append(params)
    
    @property
    def params(self) -> Dict:
        return self._params
    
    def count_params(self) -> int:
        count = 0
        for name in self._params:
            if isinstance(self._params[name], np.ndarray):
                count += self._params[name].shape[0]
            else:
                count += 1
        return count
    
    def count_symbols(self) -> int:
        return len(self._params)
    
    def pop(self, symbol:str):
        self._params.pop(symbol, None)
    
    def __getitem__(self, key):
        return self._params[key]
    
    def __len__(self):
        return len(self._params)
    
    
    def append_array(self, symbol:str, size:int):
        self._params[symbol] = sp.symarray(symbol, size)
        
    def keys(self):
        return self._params.keys()
    
    def values(self):
        return self._params.values()
    
    def append(self, params: Union[str, List[str], sp.Symbol, List[sp.Symbol]] ):
        if isinstance(params, list):
            if all(isinstance(param, str) for param in params):
                self._params.update(UnresolvedParameters._create_param_key_values(params))
            elif all(isinstance(param, sp.Symbol) for param in params):
                self._params.update({param.name: param for param in params})
            else:
                raise ValueError('inconsistent list of parameters passed: {}'.format(params))
        elif isinstance(params, str):
            self.append([params])
        elif isinstance(params, sp.Symbol):
            self._params.update({params.name: params})
        else:
            raise TypeError('unsupported parameter type : {}'.format(type(params)))
    
    @staticmethod
    def _create_param_key_values(params:List[str]) -> Dict:
        return {param: sp.Symbol(param) for param in params}
    
    
        