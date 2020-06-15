import pickle
import random as r
import os

data_path = os.path.join(os.path.dirname(__file__), 'data', 'stanzas')
stanzas = pickle.load(open(data_path, "rb"))

def all(numbered=False):
    """
    Get all included stanzas.

    Takes optional argument numbered.

    Returns a dict if numbered=True, else returns a list.
    """
    return dict(zip(range(1, 165 + 1), stanzas)) if numbered else stanzas

def find_by_number(n):
    """
    Get a stanza by number (not zero-based).

    Takes natural number n.

    Returns a stanza or None if n is out of range.
    """
    return all(True)[n] if 1 <= n <= 165 else None

def random():
    """
    Get a random stanza.

    Returns a random stanza.
    """
    return r.choice(all())

def range_by_number(a, b):
    """
    Get a range of stanzas (not zero-based).

    Takes two natural numbers a and b.

    Returns a list of all stanzas within the range of a and b inclusive (may be empty).
    """
    results = []
    for n in range(a, b + 1):
        results.append(find_by_number(n))
    return results