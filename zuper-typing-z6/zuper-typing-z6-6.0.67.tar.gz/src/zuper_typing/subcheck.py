from dataclasses import dataclass, field, is_dataclass
from datetime import datetime
from decimal import Decimal
from numbers import Number
from typing import Any, cast, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Type

import numpy as np

from zuper_commons.text import indent
from zuper_commons.types import ZNotImplementedError, ZValueError
from . import logger
from .aliases import TypeLike
from .annotations_tricks import (
    get_ForwardRef_arg,
    get_Iterable_arg,
    get_NewType_arg,
    get_Optional_arg,
    get_Sequence_arg,
    get_tuple_types,
    get_Type_arg,
    get_TypeVar_name,
    get_Union_args,
    is_Any,
    is_Callable,
    is_ClassVar,
    is_ForwardRef,
    is_Iterable,
    is_List,
    is_Optional,
    is_Sequence,
    is_TupleLike,
    is_Type,
    is_TypeVar,
    is_Union,
    make_Tuple,
)
from .constants import ANNOTATIONS_ATT
from .literal import get_Literal_args, is_Literal, make_Literal
from .my_dict import (
    get_DictLike_args,
    get_ListLike_arg,
    get_SetLike_arg,
    is_DictLike,
    is_ListLike,
    is_SetLike,
)
from .my_intersection import get_Intersection_args, is_Intersection
from .type_algebra import Matches
from .uninhabited import is_Uninhabited

__all__ = ["can_be_used_as2", "value_liskov", "CanBeUsed"]


@dataclass
class CanBeUsed:
    result: bool
    why: str
    M: Matches
    matches: Optional[Dict[str, type]] = None

    reasons: "Dict[str, CanBeUsed]" = field(default_factory=dict)

    def __post_init__(self):
        assert isinstance(self.M, Matches), self
        self.matches = self.M.get_matches()

    def __bool__(self):
        return self.result


verbose = True

can_be_used_cache = {}


def can_be_used_as2(
    T1: TypeLike,
    T2: TypeLike,
    matches: Optional[Matches] = None,
    assumptions0: Tuple[Tuple[Any, Any], ...] = (),
) -> CanBeUsed:
    if matches is None:
        matches = Matches()
    from .get_patches_ import is_placeholder

    if is_placeholder(T1) or is_placeholder(T2):
        msg = "cannot compare classes with 'Placeholder' in the name (reserved internally)."
        raise ZValueError(msg, T1=T1, T2=T2)
    if is_Any(T2):
        return CanBeUsed(True, "Any", matches)
    if is_Any(T1):
        return CanBeUsed(True, "Any", matches)

    if is_Uninhabited(T1):
        return CanBeUsed(True, "Empty", matches)

    assert isinstance(matches, Matches), matches
    if (T1, T2) in assumptions0:
        return CanBeUsed(True, "By assumption", matches)

    if (T1 is T2) or (T1 == T2):
        return CanBeUsed(True, "equal", matches)

    if is_Any(T1) or is_Any(T2):
        return CanBeUsed(True, "Any ignores everything", matches)
    if T2 is object:
        return CanBeUsed(True, "object is the top", matches)
    # cop out for the easy cases
    assumptions = assumptions0 + ((T1, T2),)

    if is_Literal(T1):
        v1 = get_Literal_args(T1)
        if is_Literal(T2):
            v2 = get_Literal_args(T2)
            included = all(any(x1 == x2 for x2 in v2) for x1 in v1)
            if included:
                return CanBeUsed(True, "included", matches)
            else:
                return CanBeUsed(False, "not included", matches)
        else:
            t1 = type(v1[0])
            return can_be_used_as2(t1, T2, matches, assumptions)

            # logger.info(f'can_be_used_as\n {T1} {T2}\n {assumptions0}')
    if is_Literal(T2):
        return CanBeUsed(False, "T1 not literal", matches)

    if T1 is type(None):
        if is_Optional(T2):
            return CanBeUsed(True, "", matches)
        elif T2 is type(None):
            return CanBeUsed(True, "", matches)
        else:
            msg = f"Needs type(None), got {T2}"
            return CanBeUsed(False, msg, matches)

    if is_Union(T1):
        if is_Union(T2):
            if get_Union_args(T1) == get_Union_args(T2):
                return CanBeUsed(True, "same", matches)
        # can_be_used(Union[A,B], C)
        # == can_be_used(A,C) and can_be_used(B,C)

        for t in get_Union_args(T1):
            can = can_be_used_as2(t, T2, matches, assumptions)
            # logger.info(f'can_be_used_as t = {t} {T2}')
            if not can.result:
                msg = f"Cannot match {t}"
                return CanBeUsed(False, msg, matches)

        return CanBeUsed(True, "", matches)

    if is_Union(T2):
        reasons = []
        for t in get_Union_args(T2):
            can = can_be_used_as2(T1, t, matches, assumptions)
            if can.result:
                return CanBeUsed(True, f"union match with {t} ", can.M)
            reasons.append(f"- {t}: {can.why}")

        msg = f"Cannot use {T1} as any of {T2}:\n" + "\n".join(reasons)
        return CanBeUsed(False, msg, matches)

    if is_TypeVar(T2):
        n2 = get_TypeVar_name(T2)
        if is_TypeVar(T1):
            n1 = get_TypeVar_name(T1)
            if n1 == n2:
                # TODO: intersection of bounds
                return CanBeUsed(True, "", matches)
            else:
                matches = matches.must_be_subtype_of(n1, T2)
                # raise ZNotImplementedError(T1=T1,T2=T2)

        matches = matches.must_be_supertype_of(n2, T1)
        return CanBeUsed(True, "", matches)
        #
        # if T2.__name__ not in matches:
        #     matches = dict(matches)
        #     matches[T2.__name__] = T1
        #     return CanBeUsed(True, "", matches)
        # else:
        #     prev = matches[T2.__name__]
        #     if prev == T1:
        #         return CanBeUsed(True, "", matches)
        #     else:
        #         raise NotImplementedError((T1, T2, matches))
    if is_Intersection(T1):
        if is_Intersection(T2):
            if get_Intersection_args(T1) == get_Intersection_args(T2):
                return CanBeUsed(True, "same", matches)

        # Int[a, b] <= Int[C, D]
        # = Int[a, b] <= C  Int[a, b] <= D
        for t2 in get_Intersection_args(T2):
            can = can_be_used_as2(T1, t2, matches, assumptions)
            # logger.info(f'can_be_used_as t = {t} {T2}')
            if not can.result:
                msg = f"Cannot match {t2}"
                return CanBeUsed(False, msg, matches)

        return CanBeUsed(True, "", matches)

    if is_Intersection(T2):
        # a <= Int[C, D]
        # = a <= C  and a <= D

        reasons = []
        for t2 in get_Intersection_args(T2):
            can = can_be_used_as2(T1, t2, matches, assumptions)
            if not can.result:
                return CanBeUsed(False, f"no match  {T1} {t2} ", can.M)

        msg = f"Cannot use {T1} as any of {T2}:\n" + "\n".join(reasons)
        return CanBeUsed(False, msg, matches)

    if is_TypeVar(T1):
        n1 = get_TypeVar_name(T1)
        matches = matches.must_be_subtype_of(n1, T2)
        return CanBeUsed(True, "Any", matches)
        # TODO: not implemented

    if is_Optional(T1):
        t1 = get_Optional_arg(T1)

        if is_Optional(T2):
            t2 = get_Optional_arg(T2)
            return can_be_used_as2(t1, t2, matches, assumptions)

        if T2 is type(None):
            return CanBeUsed(True, "", matches)

        return can_be_used_as2(t1, T2, matches, assumptions)

    if is_Optional(T2):
        t2 = get_Optional_arg(T2)
        if is_Optional(T1):
            t1 = get_Optional_arg(T1)
            return can_be_used_as2(t1, t2, matches, assumptions)

        return can_be_used_as2(T1, t2, matches, assumptions)

    # ---- concrete

    trivial = (int, str, bool, Decimal, datetime, float, Number)

    if T1 in trivial:
        if T2 not in trivial:
            return CanBeUsed(False, "A trivial cannot be a subclass of non-trivial", matches)

    if T2 in trivial:
        if T1 in trivial + (np.float32, np.float64):
            return CanBeUsed(issubclass(T1, T2), "trivial subclass", matches)
            # raise ZNotImplementedError(T1=T1, T2=T2)

        return CanBeUsed(False, f"Not a trivial type (T1={T1}, T2={T2})", matches)
    if is_DictLike(T2):

        if not is_DictLike(T1):
            msg = f"Expecting a dictionary, got {T1}"
            return CanBeUsed(False, msg, matches)
        else:
            T1 = cast(Type[Dict], T1)
            T2 = cast(Type[Dict], T2)
            K1, V1 = get_DictLike_args(T1)
            K2, V2 = get_DictLike_args(T2)

            rk = can_be_used_as2(K1, K2, matches, assumptions)
            if not rk:
                return CanBeUsed(False, f"keys {K1} {K2}: {rk}", matches)

            rv = can_be_used_as2(V1, V2, rk.M, assumptions)
            if not rv:
                return CanBeUsed(False, f"values {V1} {V2}: {rv}", matches)

            return CanBeUsed(True, f"ok: {rk} {rv}", rv.M)
    else:
        if is_DictLike(T1):
            msg = "A Dict needs a dictionary"
            return CanBeUsed(False, msg, matches)

    assert not is_Union(T2)

    if is_dataclass(T1):
        if not is_dataclass(T2):
            msg = "Second is not dataclass "
            return CanBeUsed(False, msg, matches)
    from .zeneric2 import StructuralTyping

    if isinstance(T2, StructuralTyping):
        if not isinstance(T1, StructuralTyping):
            msg = "Not structural typing"
            return CanBeUsed(False, msg, matches)

    if is_dataclass(T2):
        if not is_dataclass(T1):
            if verbose:
                msg = (
                    f"Expecting dataclass to match to {T2}, got something that is not a "
                    f"dataclass: {T1}"
                )
                msg += f"  union: {is_Union(T1)}"
            else:
                msg = "not dataclass"
            return CanBeUsed(False, msg, matches)
        # h1 = get_type_hints(T1)
        # h2 = get_type_hints(T2)

        key = (T1.__module__, T1.__qualname__, T2.__module__, T2.__qualname__)
        if key in can_be_used_cache:
            return can_be_used_cache[key]

        h1 = getattr(T1, ANNOTATIONS_ATT, {})
        h2 = getattr(T2, ANNOTATIONS_ATT, {})

        for k, v2 in h2.items():
            if not k in h1:
                if verbose:
                    msg = (
                        f'Type {T2}\n  requires field "{k}" \n  of type {v2} \n  but {T1} does '
                        f""
                        f"not have it. "
                    )
                else:
                    msg = k
                res = CanBeUsed(False, msg, matches)
                can_be_used_cache[key] = res
                return res

            v1 = h1[k]

            # XXX
            if is_ClassVar(v1):
                continue

            can = can_be_used_as2(v1, v2, matches, assumptions)
            if not can.result:
                if verbose:
                    msg = (
                        f'Type {T2}\n  requires field "{k}"\n  of type\n       {v2} \n  but'
                        + f" {T1}\n  has annotated it as\n       {v1}\n  which cannot be used. "
                    )
                    msg += "\n\n" + f"assumption: {assumptions}"
                    msg += "\n\n" + indent(can.why, "> ")
                else:
                    msg = ""
                res = CanBeUsed(False, msg, matches)
                can_be_used_cache[key] = res
                return res

        res = CanBeUsed(True, "dataclass", matches)
        can_be_used_cache[key] = res
        return res
    #
    # if T1 is int:
    #
    #     if isinstance(T2, type) and issubclass(T1, T2):
    #         return CanBeUsed(True, "", matches)
    #
    #     if T2 is int:
    #         return CanBeUsed(True, "", matches)
    #     else:
    #         msg = "Need int"
    #         return CanBeUsed(False, msg, matches)
    #
    # if T1 is str:
    #     if isinstance(T2, type) and issubclass(T1, T2):
    #         return CanBeUsed(True, "", matches)
    #
    #     assert T2 is not str
    #     msg = "A string can only be used a string"
    #     return CanBeUsed(False, msg, matches)

    if is_TupleLike(T1):
        assert not is_Union(T2)
        if not is_TupleLike(T2):
            msg = "A tuple can only be used as a tuple"
            return CanBeUsed(False, msg, matches)
        else:

            T1 = cast(Type[Tuple], T1)
            T2 = cast(Type[Tuple], T2)

            for t1, t2 in zip(get_tuple_types(T1), get_tuple_types(T2)):
                can = can_be_used_as2(t1, t2, matches, assumptions)
                if not can.result:
                    return CanBeUsed(False, f"{t1} {T2}", matches)
                matches = can.M
            return CanBeUsed(True, "", matches)

    if is_TupleLike(T2):
        assert not is_TupleLike(T1)
        return CanBeUsed(False, f"Not a tuple type T1={T1} T2={T2}", matches)

    if is_Any(T1):
        assert not is_Union(T2)
        if not is_Any(T2):
            msg = "Any is the top"
            return CanBeUsed(False, msg, matches)

    if is_ListLike(T2):
        if not is_ListLike(T1):
            msg = "A List can only be used as a List"
            return CanBeUsed(False, msg, matches)

        T1 = cast(Type[List], T1)
        T2 = cast(Type[List], T2)
        t1 = get_ListLike_arg(T1)
        t2 = get_ListLike_arg(T2)
        # print(f'matching List with {t1} {t2}')
        can = can_be_used_as2(t1, t2, matches, assumptions)

        if not can.result:
            return CanBeUsed(False, f"{t1} {T2}", matches)

        return CanBeUsed(True, "", can.M)

    if is_Callable(T2):
        if not is_Callable(T1):
            return CanBeUsed(False, "not callable", matches)

        raise ZNotImplementedError(T1=T1, T2=T2)

    if is_ForwardRef(T1):
        n1 = get_ForwardRef_arg(T1)
        if is_ForwardRef(T2):
            n2 = get_ForwardRef_arg(T2)
            if n1 == n2:
                return CanBeUsed(True, "", matches)
            else:
                return CanBeUsed(False, "different name", matches)
        else:
            return CanBeUsed(False, "not fw ref", matches)
    if is_ForwardRef(T2):
        n2 = get_ForwardRef_arg(T2)
        if hasattr(T1, "__name__"):
            if T1.__name__ == n2:
                return CanBeUsed(True, "", matches)
            else:
                return CanBeUsed(False, "different name", matches)

    if is_Iterable(T2):

        T2 = cast(Type[Iterable], T2)
        t2 = get_Iterable_arg(T2)

        if is_Iterable(T1):
            T1 = cast(Type[Iterable], T1)
            t1 = get_Iterable_arg(T1)
            return can_be_used_as2(t1, t2, matches)

        if is_SetLike(T1):
            T1 = cast(Type[Set], T1)
            t1 = get_SetLike_arg(T1)
            return can_be_used_as2(t1, t2, matches)

        if is_ListLike(T1):
            T1 = cast(Type[List], T1)
            t1 = get_ListLike_arg(T1)
            return can_be_used_as2(t1, t2, matches)

        if is_DictLike(T1):
            T1 = cast(Type[Dict], T1)
            K, V = get_DictLike_args(T1)
            t1 = Tuple[K, V]
            return can_be_used_as2(t1, t2, matches)

        return CanBeUsed(False, "expect iterable", matches)

    if is_SetLike(T2):
        if not is_SetLike(T1):
            msg = "A Set can only be used as a Set"
            return CanBeUsed(False, msg, matches)

        T1 = cast(Type[Set], T1)
        T2 = cast(Type[Set], T2)
        t1 = get_SetLike_arg(T1)
        t2 = get_SetLike_arg(T2)
        # print(f'matching List with {t1} {t2}')
        can = can_be_used_as2(t1, t2, matches, assumptions)

        if not can.result:
            return CanBeUsed(False, f"Set argument fails", matches, reasons={"set_arg": can})

        return CanBeUsed(True, "", can.M)

    if is_Sequence(T1):
        T1 = cast(Type[Sequence], T1)
        t1 = get_Sequence_arg(T1)

        if is_ListLike(T2):
            T2 = cast(Type[List], T2)
            t2 = get_ListLike_arg(T2)
            can = can_be_used_as2(t1, t2, matches, assumptions)

            if not can.result:
                return CanBeUsed(False, f"{t1} {T2}", matches)

            return CanBeUsed(True, "", can.M)

        msg = f"Needs a Sequence[{t1}], got {T2}"
        return CanBeUsed(False, msg, matches)

    if isinstance(T1, type) and isinstance(T2, type):
        # NOTE: this didn't work with Number for whatever reason
        # NOTE: issubclass(A, B) == type(T2).__subclasscheck__(T2, T1)
        # a0 = type.__subclasscheck__(T2, T1)
        # b0 = type.__subclasscheck__(T1, T2)
        logger.info(T1=T1, T2=T2)

        a = issubclass(T1, T2)
        # assert a0 == a and b0 == b, (T1, T2, a0, b0, a, b)
        if a:
            return CanBeUsed(True, f"type.__subclasscheck__ {T1} {T2}", matches)
        else:
            msg = f"Type {T1} is not a subclass of {T2} "
            # msg += f"; viceversa : {b}"
            return CanBeUsed(False, msg, matches)

    if is_List(T1):
        msg = f"Needs a List, got {T2}"
        return CanBeUsed(False, msg, matches)

    if T2 is type(None):
        msg = f"Needs type(None), got {T1}"
        return CanBeUsed(False, msg, matches)

    from .annotations_tricks import is_NewType

    if is_NewType(T1):
        n1 = get_NewType_arg(T1)
        if is_NewType(T2):
            n2 = get_NewType_arg(T2)
            return can_be_used_as2(n1, n2, matches, assumptions)
            # if n1 == n2:
            #     return CanBeUsed(True, "", matches)
            # else:
            #     raise ZNotImplementedError(T1=T1, T2=T2)
        else:
            return can_be_used_as2(n1, T2, matches, assumptions)
            raise ZNotImplementedError(T1=T1, T2=T2)

    if is_Type(T1):
        if not is_Type(T2):
            return CanBeUsed(False, f"Not a Type[X], T1={T1}, T2={T2}", matches)
        sc1 = get_Type_arg(T1)
        sc2 = get_Type_arg(T2)
        return can_be_used_as2(sc1, sc2, matches, assumptions)

    # msg = f"{T1} ? {T2}"  # pragma: no cover
    raise ZNotImplementedError(T1=T1, T2=T2)


def value_liskov(a: object, T: TypeLike):
    if is_Literal(T):
        return a in get_Literal_args(T)  # XXX
    S = ztype(a)
    return can_be_used_as2(S, T)


def ztype(a: object) -> type:
    if type(a) is tuple:
        a = cast(tuple, a)
        ts = tuple(make_Literal(_) for _ in a)
        return make_Tuple(*ts)
    # todo: substitute tuple, list, dict with estimated
    return type(a)
