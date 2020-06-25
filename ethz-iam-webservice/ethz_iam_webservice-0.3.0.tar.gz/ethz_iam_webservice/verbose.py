# display messages when in a interactive context (IPython or Jupyter)

VERBOSE = False

try:
    get_ipython()
except Exception:
    VERBOSE = False
else:
    VERBOSE = True

