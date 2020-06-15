from typing import List, Optional, Tuple
from titlecase import titlecase as _titlecase
from slugify import slugify as _slugify
from copy import copy


def canonical(s: str) -> str:
    return s.lower()


def camel(s: str, delims=" _-", capitalize_first=False) -> str:
    ops = [(uppercase_after, d) for d in delims]
    ops.append((replace_all, delims, ""))
    if capitalize_first:
        ops.append((capitalize1,))
    return process(s, ops)


def pascal(s: str) -> str:
    return camel(s, capitalize_first=True)


def constant(s: str) -> str:
    ops = [(str.upper,), (replace_all, " -", "_")]
    return process(s, ops)


def title(s: str) -> str:
    ops = [(replace_all, "-_", " "), (_titlecase,)]
    return process(s, ops)


def titlecase(s: str) -> str:
    return title(s)


def pythonic(s: str) -> str:
    ixs = find_uppercase(s)
    ops = [(precede_uppercase, "_"), (str.lower,), (replace_all, "- ", "_")]
    return process(s, ops)


def snake(s: str) -> str:
    return pythonic(s)


def kebab(s: str) -> str:
    ixs = find_uppercase(s)
    ops = [(precede_uppercase, "-"), (str.lower,), (replace_all, "_ ", "-")]
    return process(s, ops)


def slug(s: str) -> str:
    return _slugify(s)


def slugify(s: str) -> str:
    return slug(s)


def process(s: str, steps: List[Tuple]) -> str:
    out = s
    for step in steps:
        func = step[0]
        params = step[1:]
        out = func(out, *params)
    return out


def replace_all(s: str, old: str, new: str) -> str:
    for c in old:
        s = s.replace(c, new)
    return s


def capitalize1(s: str):
    if len(s) == 0:
        return s
    elif len(s) == 1:
        return s.upper()
    return s[0].upper() + s[1:]


def uppercase_after(s: str, p: str, keep_delim=True):
    out = []
    found = False
    for c in s:
        if found:
            out.append(c.upper())
            found = False
        elif c == p:
            found = True
            if keep_delim:
                out.append(c)
        else:
            out.append(c)
    return "".join(out)


def precede_uppercase(s: str, p: str) -> str:
    ixs = find_uppercase(s)
    tokens = split_on(s, ixs)
    return p.join(tokens)


def find_uppercase(s: str) -> List[Optional[int]]:
    ixs: List[Optional[int]] = []
    for i, c in enumerate(s):
        if c.isupper():
            ixs.append(i)
    return ixs


def split_on(
    s: str, ixs: List[Optional[int]], keep_start=True, keep_end=True
) -> List[str]:
    cp = copy(ixs)
    if keep_start and cp[0] != 0:
        cp.insert(0, 0)
    if keep_end:
        cp.insert(len(cp), None)
    return [s[cp[i] : cp[i + 1]] for i in range(len(cp) - 1)]
