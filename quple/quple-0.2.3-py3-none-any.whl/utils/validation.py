from typing import Union

def bounded_below(value:Union[float, int], bound:Union[float, int], label:str='') -> None:
    if value < bound:
        raise ValueError('Value out of bound. ({} < {})'.format(label, bound))

def bounded_above(value:Union[float, int], bound:Union[float, int], label:str='') -> None:
    if value > bound:
        raise ValueError('Value out of bound. ({} > {})'.format(label, bound))
        
def bounded_between(value:Union[float, int], lower:Union[float, int], upper:Union[float, int], label:str='') -> None:
    if not ( lower < value < upper):
        raise ValueError('Value out of bound. ( {} < {} < {})'.format(lower, label, upper))
        