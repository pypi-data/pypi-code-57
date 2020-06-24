import re

_cap_words_re = re.compile(f"[A-Z]+[^A-Z]*")
def cap2snake(s):
    return "_".join((w.lower() for w in _cap_words_re.findall(s)))
