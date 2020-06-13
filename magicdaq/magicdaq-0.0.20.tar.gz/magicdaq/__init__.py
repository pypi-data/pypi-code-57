##########################################################
#*** magicdaq module __init__.py file ***
##########################################################

# Add magicdaq module file path to Python search path
import os
import sys
path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, path)