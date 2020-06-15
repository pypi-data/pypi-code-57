"""Python version compatibility helper."""

def iterkeys(d): return d.iterkeys() if hasattr(d, "iterkeys") else d.keys()
def itervalues(d): return d.itervalues() if hasattr(d, "itervalues") else d.values()
def iteritems(d): return d.iteritems() if hasattr(d, "iteritems") else d.items()


def listkeys(d): return d.keys() if hasattr(d, "iterkeys") else list(d.keys())
def listvalues(d): return d.values() if hasattr(d, "itervalues") else list(d.values())
def listitems(d): return d.items() if hasattr(d, "iteritems") else list(d.items())
